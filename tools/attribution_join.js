#!/usr/bin/env node
/*
 * Which ad produced which paying customer.
 *
 * This is the only instrument that can ever produce a real cost per paying customer for
 * Quantica, and the reason is structural rather than a preference. The paywall sits days or
 * weeks of student time past the ad click, well outside Meta's 7-day-click attribution
 * window, so Ads Manager will report zero purchases even from a funnel that is working
 * perfectly. Do not judge a campaign on Ads Manager ROAS. Judge it on this file.
 *
 * Both halves of the join already exist and neither needed a deploy:
 *   functions/index.js:36  creates the Stripe customer with metadata: { uid }
 *   functions/index.js:49  stamps the subscription with metadata: { uid, plan }
 *   landing.html:52-64     captures first-touch UTMs into localStorage
 *   landing.html:3077      writes them to Firestore as users/{uid}.attr on account creation
 *
 * Runs entirely on your machine. It makes GET requests to Stripe and reads Firestore. It
 * writes nothing to either. No Cloud Functions are deployed and nothing goes near the live
 * webhook.
 *
 * USAGE
 *   export STRIPE_SECRET_KEY=sk_live_...            # or sk_test_ for a rehearsal
 *   export GOOGLE_APPLICATION_CREDENTIALS=/abs/path/to/serviceAccount.json
 *   node tools/attribution_join.js
 *   node tools/attribution_join.js --check          # validate wiring, touch no data
 *   node tools/attribution_join.js --out attribution.csv
 *
 * NEVER put the Stripe key in a file in this repo. functions/.env holds the live secret key
 * and is not to be read, copied or committed. Export it into your shell for the length of the
 * run and let it die with the shell.
 *
 * The service-account JSON must live OUTSIDE the repo, or if inside, note that .gitignore and
 * firebase.json now both carry *adminsdk*.json and serviceAccount*.json. Hosting publishes
 * from "." so an unignored key at repo root would be served on the open web.
 */

'use strict';

const https = require('https');
const fs = require('fs');
const path = require('path');

const ROOT = path.dirname(__dirname);

// ---------- args ----------
const argv = process.argv.slice(2);
const CHECK_ONLY = argv.includes('--check');
const outIdx = argv.indexOf('--out');
const OUT = outIdx >= 0 && argv[outIdx + 1] ? argv[outIdx + 1] : path.join(ROOT, 'attribution.csv');

// ---------- preflight ----------
function die(msg) {
  console.error('\n' + msg + '\n');
  process.exit(1);
}

const STRIPE_KEY = process.env.STRIPE_SECRET_KEY || '';
if (!STRIPE_KEY) {
  die(
    'STRIPE_SECRET_KEY is not set.\n' +
    '  export STRIPE_SECRET_KEY=sk_live_...\n' +
    'Read it from the Stripe dashboard. Do not copy it out of functions/.env.'
  );
}
if (!/^sk_(live|test)_/.test(STRIPE_KEY)) {
  die('STRIPE_SECRET_KEY does not look like a Stripe secret key (expected sk_live_ or sk_test_).');
}
if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
  die(
    'GOOGLE_APPLICATION_CREDENTIALS is not set.\n' +
    '  export GOOGLE_APPLICATION_CREDENTIALS=/abs/path/to/serviceAccount.json\n' +
    'Firebase console, Project settings, Service accounts, Generate new private key.\n' +
    'functions/index.js calls admin.initializeApp() with ambient credentials, which works\n' +
    'inside Cloud Functions and not on a laptop, so the key is how this script authenticates.'
  );
}
if (!fs.existsSync(process.env.GOOGLE_APPLICATION_CREDENTIALS)) {
  die('GOOGLE_APPLICATION_CREDENTIALS points at a file that does not exist:\n  ' +
      process.env.GOOGLE_APPLICATION_CREDENTIALS);
}

// firebase-admin is not a root dependency. functions/ already has it, so borrow it rather
// than installing a second 50MB copy. Falls back to a root install if you would rather have one.
let admin;
try {
  admin = require(path.join(ROOT, 'functions', 'node_modules', 'firebase-admin'));
} catch (e) {
  try {
    admin = require('firebase-admin');
  } catch (e2) {
    die(
      'Could not load firebase-admin. Either\n' +
      '  cd functions && npm install\n' +
      'or install a root copy with\n' +
      '  npm install --no-save firebase-admin'
    );
  }
}

// ---------- stripe, read only ----------
function stripeGet(pathname) {
  return new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: 'api.stripe.com',
        path: pathname,
        method: 'GET',                       // this script never writes to Stripe
        headers: {
          Authorization: 'Bearer ' + STRIPE_KEY,
          'Stripe-Version': '2024-06-20',
        },
      },
      (res) => {
        let body = '';
        res.on('data', (c) => (body += c));
        res.on('end', () => {
          let json;
          try { json = JSON.parse(body); } catch (e) { return reject(new Error('Stripe sent non-JSON: ' + body.slice(0, 200))); }
          if (res.statusCode >= 400) {
            return reject(new Error('Stripe ' + res.statusCode + ': ' + ((json.error && json.error.message) || body.slice(0, 200))));
          }
          resolve(json);
        });
      }
    );
    req.on('error', reject);
    req.end();
  });
}

async function allSubscriptions() {
  const out = [];
  let startingAfter = null;
  for (;;) {
    const qs = ['limit=100', 'status=all', 'expand[]=data.customer'];
    if (startingAfter) qs.push('starting_after=' + startingAfter);
    const page = await stripeGet('/v1/subscriptions?' + qs.join('&'));
    out.push(...page.data);
    if (!page.has_more || !page.data.length) break;
    startingAfter = page.data[page.data.length - 1].id;
  }
  return out;
}

// ---------- csv ----------
const COLUMNS = [
  'uid', 'email', 'plan', 'status', 'amount', 'currency', 'purchased_at',
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
  'referrer', 'landing', 'first_touch', 'days_first_touch_to_purchase',
];

function csvCell(v) {
  if (v === undefined || v === null) return '';
  const s = String(v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

function daysBetween(isoDate, unixSeconds) {
  if (!isoDate || !unixSeconds) return '';
  const a = Date.parse(isoDate + 'T00:00:00Z');
  if (isNaN(a)) return '';
  // floor, not round. First touch is anchored at midnight and the purchase carries a real
  // time of day, so rounding turns 44 and a half days into 45.
  return Math.floor((unixSeconds * 1000 - a) / 86400000);
}

// ---------- main ----------
(async function main() {
  if (CHECK_ONLY) {
    console.log('Checking wiring, reading no data.');
    const acct = await stripeGet('/v1/account');
    console.log('  Stripe   ok, account ' + acct.id + (/^sk_test_/.test(STRIPE_KEY) ? ' (TEST mode)' : ' (LIVE mode)'));
    admin.initializeApp({ credential: admin.credential.applicationDefault() });
    const snap = await admin.firestore().collection('users').limit(1).get();
    console.log('  Firestore ok, users collection reachable, ' + snap.size + ' doc read');
    console.log('\nWiring is good. Run without --check to produce the CSV.');
    process.exit(0);
  }

  console.log('Reading Stripe subscriptions' + (/^sk_test_/.test(STRIPE_KEY) ? ' (TEST mode)' : ' (LIVE mode)') + ' ...');
  const subs = await allSubscriptions();
  console.log('  ' + subs.length + ' subscription(s)');

  if (!subs.length) {
    console.log(
      '\nNo subscriptions exist yet, so there is nothing to attribute. That is the expected\n' +
      'result until the first sale. The script is wired and will produce real rows the day\n' +
      'someone buys.'
    );
    fs.writeFileSync(OUT, COLUMNS.join(',') + '\n');
    console.log('Wrote an empty CSV with headers to ' + OUT);
    process.exit(0);
  }

  admin.initializeApp({ credential: admin.credential.applicationDefault() });
  const db = admin.firestore();

  const rows = [];
  let missingUid = 0, missingAttr = 0;

  for (const sub of subs) {
    const cust = sub.customer && typeof sub.customer === 'object' ? sub.customer : null;
    const uid =
      (sub.metadata && sub.metadata.uid) ||
      (cust && cust.metadata && cust.metadata.uid) ||
      '';
    if (!uid) { missingUid++; continue; }

    let attr = {};
    try {
      const doc = await db.collection('users').doc(uid).get();
      attr = (doc.exists && doc.data() && doc.data().attr) || {};
    } catch (e) {
      console.error('  could not read users/' + uid + ': ' + e.message);
    }
    if (!Object.keys(attr).length) missingAttr++;

    const item = sub.items && sub.items.data && sub.items.data[0];
    const price = item && item.price;

    rows.push({
      uid,
      email: (cust && cust.email) || '',
      plan: (sub.metadata && sub.metadata.plan) || (price && price.recurring && price.recurring.interval) || '',
      status: sub.status,
      amount: price && typeof price.unit_amount === 'number' ? (price.unit_amount / 100).toFixed(2) : '',
      currency: (price && price.currency) || '',
      purchased_at: new Date(sub.created * 1000).toISOString().slice(0, 10),
      utm_source: attr.utm_source, utm_medium: attr.utm_medium,
      utm_campaign: attr.utm_campaign, utm_content: attr.utm_content, utm_term: attr.utm_term,
      referrer: attr.referrer, landing: attr.landing, first_touch: attr.at,
      days_first_touch_to_purchase: daysBetween(attr.at, sub.created),
    });
  }

  fs.writeFileSync(
    OUT,
    COLUMNS.join(',') + '\n' + rows.map((r) => COLUMNS.map((c) => csvCell(r[c])).join(',')).join('\n') + '\n'
  );

  // ---------- what he actually wants to read ----------
  const byAd = {};
  for (const r of rows) {
    const k = r.utm_content || (r.utm_source ? r.utm_source + ' (no utm_content)' : 'unattributed');
    byAd[k] = byAd[k] || { n: 0, active: 0 };
    byAd[k].n++;
    if (r.status === 'active' || r.status === 'trialing') byAd[k].active++;
  }
  const lag = rows.map((r) => r.days_first_touch_to_purchase).filter((d) => d !== '' && !isNaN(d));

  console.log('\nPaying customers by ad (utm_content)');
  Object.keys(byAd).sort((a, b) => byAd[b].n - byAd[a].n).forEach((k) => {
    console.log('  ' + String(byAd[k].n).padStart(4) + '  ' + String(byAd[k].active).padStart(4) + ' active   ' + k);
  });

  if (lag.length) {
    lag.sort((a, b) => a - b);
    const median = lag[Math.floor(lag.length / 2)];
    const past7 = lag.filter((d) => d > 7).length;
    console.log('\nDays from first touch to purchase');
    console.log('  median ' + median + ', range ' + lag[0] + ' to ' + lag[lag.length - 1]);
    console.log('  ' + past7 + ' of ' + lag.length + ' fell outside Meta\'s 7-day click window,');
    console.log('  which is the number that says whether Ads Manager can be trusted here at all.');
  }

  if (missingUid) console.log('\n  ' + missingUid + ' subscription(s) carried no uid in metadata and were skipped.');
  if (missingAttr) {
    console.log('  ' + missingAttr + ' customer(s) had no stored attribution. Expected for anyone who');
    console.log('  arrived with no UTM, no fbclid and no cross-host referrer, or who first visited on');
    console.log('  another device. This undercounts paid, which is the safe direction, but say so');
    console.log('  when you quote the number.');
  }
  console.log('\nWrote ' + rows.length + ' row(s) to ' + OUT);
  console.log('That file contains customer emails. It is gitignored. Do not paste it anywhere.');
  process.exit(0);
})().catch((e) => {
  console.error('\nFailed: ' + e.message + '\n');
  process.exit(1);
});
