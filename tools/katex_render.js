// Batch KaTeX renderer for the SEO page generator.
//
// The lesson pages used to ship raw LaTeX and let a deferred CDN script render it in the
// browser. Googlebot's first pass therefore saw \(\dfrac{2\cdot 7}{3\cdot 5}\) instead of a
// formula, and one of those raw strings ended up ranking as a query in Search Console.
// gen_seo_pages.py now renders every expression here at build time instead.
//
// stdin  JSON  [[tex, displayMode], ...]
// stdout JSON  [{"ok":true,"html":"..."} | {"ok":false,"err":"..."}, ...]
//
// The <annotation encoding="application/x-tex"> element KaTeX embeds carries the TeX source
// back into the markup, which is the exact debris we are removing, so it is stripped. The
// MathML that screen readers and Google actually read is left untouched.

const katex = require('katex');

const ANNOTATION = /<annotation encoding="application\/x-tex">[\s\S]*?<\/annotation>/g;

let raw = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (c) => { raw += c; });
process.stdin.on('end', () => {
  let items;
  try {
    items = JSON.parse(raw);
  } catch (e) {
    process.stderr.write('katex_render: bad JSON on stdin: ' + e.message + '\n');
    process.exit(1);
  }
  const out = items.map(([tex, display]) => {
    try {
      const html = katex.renderToString(tex, {
        displayMode: !!display,
        throwOnError: true,
        strict: false,
        output: 'htmlAndMathml',
      });
      return { ok: true, html: html.replace(ANNOTATION, '') };
    } catch (e) {
      return { ok: false, err: String(e.message || e) };
    }
  });
  process.stdout.write(JSON.stringify(out));
});
