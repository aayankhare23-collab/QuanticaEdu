const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");
const admin = require("firebase-admin");
const stripe = require("stripe");

admin.initializeApp();
const db = admin.firestore();

const STRIPE_SECRET = process.env.STRIPE_SECRET;
const STRIPE_WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET;
const PRICE_ID = process.env.STRIPE_PRICE_ID;              // monthly
const PRICE_ID_YEARLY = process.env.STRIPE_PRICE_ID_YEARLY; // yearly, optional

// Map a plan name from the client to a Stripe price. Never trust a price id sent by the
// browser; the client picks a PLAN and the server decides what that costs.
function priceFor(plan) {
  if (plan === "yearly") {
    if (!PRICE_ID_YEARLY) throw new HttpsError("failed-precondition", "Yearly plan is not configured.");
    return PRICE_ID_YEARLY;
  }
  return PRICE_ID;
}
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

  const plan = (request.data && request.data.plan) === "yearly" ? "yearly" : "monthly";

  const session = await stripeClient.checkout.sessions.create({
    customer: customerId,
    mode: "subscription",
    line_items: [{ price: priceFor(plan), quantity: 1 }],
    success_url: `${APP_URL}?payment=success`,
    cancel_url: `${APP_URL}?payment=cancelled`,
    subscription_data: { metadata: { uid, plan } },
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

  // Stripe does not guarantee delivery order, and this bit us with real money on the first
  // live-card test (2026-08-20). The subscription.updated event (status active, 5:37:17)
  // was DELIVERED at 5:37:22 and wrote paid; then the older subscription.created event
  // (payload snapshot: incomplete, from 5:37:15) arrived after it and overwrote paid back
  // to inactive. A paying customer, locked, with every delivery showing a green 200.
  //
  // The guard orders by event.created, when the event OCCURRED, not when it arrived. A
  // transaction drops any event strictly older than the one already applied. Equal
  // timestamps let the later delivery win, which is harmless: same-second events describe
  // the same state transition.
  async function writeSubscription(uid, fields) {
    const ref = db.collection("users").doc(uid).collection("state").doc("subscription");
    await db.runTransaction(async (t) => {
      const snap = await t.get(ref);
      const prev = snap.exists ? snap.data() : null;
      if (prev && typeof prev.eventTs === "number" && event.created < prev.eventTs) {
        console.log(`Skipping stale ${event.type} (event ${event.created} < applied ${prev.eventTs})`);
        return;
      }
      t.set(ref, Object.assign({}, fields, {
        eventTs: event.created,
        updatedAt: admin.firestore.FieldValue.serverTimestamp(),
      }));
    });
  }

  if (event.type === "customer.subscription.created" || event.type === "customer.subscription.updated") {
    const uid = await getUid(sub);
    if (!uid) { res.json({ received: true }); return; }
    const isActive = sub.status === "active" || sub.status === "trialing";
    await writeSubscription(uid, {
      type: isActive ? "paid" : "inactive",
      status: sub.status,
      stripeSubId: sub.id,
    });
  }

  if (event.type === "customer.subscription.deleted") {
    const uid = await getUid(sub);
    if (!uid) { res.json({ received: true }); return; }
    await writeSubscription(uid, {
      type: "inactive",
      status: "cancelled",
      stripeSubId: sub.id,
    });
  }

  res.json({ received: true });
});
