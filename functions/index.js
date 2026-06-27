const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");
const admin = require("firebase-admin");
const stripe = require("stripe");

admin.initializeApp();
const db = admin.firestore();

const STRIPE_SECRET = process.env.STRIPE_SECRET;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;
const PRICE_ID = process.env.STRIPE_PRICE_ID;
const APP_URL = process.env.APP_URL;

// Called by the frontend to create a Stripe Checkout session
exports.createCheckoutSession = onCall(async (request) => {
  if (!request.auth) throw new HttpsError("unauthenticated", "Must be signed in.");

  const uid = request.auth.uid;
  const email = request.auth.token.email;
  const stripeClient = stripe(STRIPE_SECRET);

  const userDoc = await db.collection("users").doc(uid).get();
  let customerId = userDoc.exists && userDoc.data().stripeCustomerId;

  if (!customerId) {
    const customer = await stripeClient.customers.create({ email, metadata: { uid } });
    customerId = customer.id;
    await db.collection("users").doc(uid).set({ stripeCustomerId: customerId }, { merge: true });
  }

  const session = await stripeClient.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    line_items: [{ price: PRICE_ID, quantity: 1 }],
    success_url: `${APP_URL}?payment=success`,
    cancel_url: `${APP_URL}?payment=cancelled`,
    subscription_data: { metadata: { uid } },
  });

  return { url: session.url };
});

// Called by Stripe after payment events
exports.stripeWebhook = onRequest(async (req, res) => {
  const stripeClient = stripe(STRIPE_SECRET);
  let event;

  try {
    event = stripeClient.webhooks.constructEvent(
      req.rawBody,
      req.headers["stripe-signature"],
      STRIPE_WEBHOOK_SECRET
    );
  } catch (err) {
    console.error("Webhook signature failed:", err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  const sub = event.data.object;

  async function getUid(subscription) {
    if (subscription.metadata && subscription.metadata.uid) return subscription.metadata.uid;
    const customer = await stripeClient.customers.retrieve(subscription.customer);
    return customer.metadata && customer.metadata.uid;
  }

  if (event.type === "customer.subscription.created" || event.type === "customer.subscription.updated") {
    const uid = await getUid(sub);
    if (!uid) { res.json({ received: true }); return; }
    const isActive = sub.status === "active" || sub.status === "trialing";
    await db.collection("users").doc(uid).collection("state").doc("subscription").set({
      type: isActive ? "paid" : "inactive",
      status: sub.status,
      stripeSubId: sub.id,
      updatedAt: admin.firestore.FieldValue.serverTimestamp(),
    });
  }

  if (event.type === "customer.subscription.deleted") {
    const uid = await getUid(sub);
    if (!uid) { res.json({ received: true }); return; }
    await db.collection("users").doc(uid).collection("state").doc("subscription").set({
      type: "inactive",
      status: "cancelled",
      stripeSubId: sub.id,
      updatedAt: admin.firestore.FieldValue.serverTimestamp(),
    });
  }

  res.json({ received: true });
});
