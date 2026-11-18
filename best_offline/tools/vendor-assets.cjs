/* Maintainer-only. Offline builds consume the resulting theme files directly. */
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const esbuild = require("esbuild");
const root = path.resolve(__dirname, "..");
const theme = path.join(root, "theme");
function mkdir(dir) { fs.mkdirSync(dir, {recursive: true}); }
function copy(from, to) {
  mkdir(path.dirname(to));
  fs.copyFileSync(from, to);
}
function copyTree(from, to) {
  mkdir(to);
  fs.readdirSync(from, {withFileTypes: true}).forEach(function (entry) {
    const source = path.join(from, entry.name), target = path.join(to, entry.name);
    if (entry.isDirectory()) { copyTree(source, target); } else { copy(source, target); }
  });
}
async function main() {
  mkdir(path.join(theme, "js"));
  await esbuild.build({
    entryPoints: [require.resolve("highlight.js")],
    outfile: path.join(theme, "js", "highlight.min.js"),
    bundle: true, minify: true, format: "iife", globalName: "hljs",
    target: ["firefox78", "chrome80"], legalComments: "eof"
  });
  copy(require.resolve("lunr/lunr.min.js"), path.join(theme, "js", "lunr.min.js"));
  const math = path.dirname(require.resolve("mathjax/package.json"));
  copyTree(path.join(math, "es5"), path.join(theme, "js", "mathjax"));
  let css = "/* Bundled Highlight.js themes, scoped for instant light/dark switching. */\n";
  ["vs", "vs2015"].forEach(function (name, i) {
    const source = fs.readFileSync(require.resolve("highlight.js/styles/" + name + ".css"), "utf8");
    copy(require.resolve("highlight.js/styles/" + name + ".css"), path.join(theme, "css", name + ".css"));
    css += source.replace(/\/\*[\s\S]*?\*\//g, "").replace(/(^|})(\s*)([^{}]+)\{/g, function (all, brace, space, selectors) {
      return brace + space + selectors.replace(/\/\*[\s\S]*?\*\//g, "").split(",").map(function (selector) {
        return '[data-theme="' + (i ? "dark" : "light") + '"] ' + selector.trim();
      }).join(",\n") + "{";
    }) + "\n";
  });
  css += "[data-theme] pre code.hljs{padding:0;background:transparent;overflow:visible;}\n";
  css += "@media print { .hljs, .hljs * { color: #111 !important; background: transparent !important; } }\n";
  fs.writeFileSync(path.join(theme, "css", "highlight.css"), css);
  let fonts = "/* Local font data is embedded to avoid file:// font-origin restrictions. */\n";
  [
    ["inter", "Inter", 400], ["inter", "Inter", 600], ["inter", "Inter", 700],
    ["jetbrains-mono", "JetBrains Mono", 400]
  ].forEach(function (font) {
    const filename = font[0] + "-latin-" + font[2] + "-normal.woff2";
    const file = require.resolve("@fontsource/" + font[0] + "/files/" + filename);
    copy(file, path.join(theme, "fonts", filename));
    fonts += '@font-face{font-family:"' + font[1] + '";font-style:normal;font-weight:' + font[2] +
      ';font-display:swap;src:url(data:font/woff2;base64,' + fs.readFileSync(file).toString("base64") + ') format("woff2");}\n';
  });
  fs.writeFileSync(path.join(theme, "css", "fonts.css"), fonts);
  const packages = [
    ["highlight.js", "LICENSE"], ["lunr", "LICENSE"], ["mathjax", "LICENSE"],
    ["@fontsource/inter", "LICENSE"], ["@fontsource/jetbrains-mono", "LICENSE"]
  ];
  const manifest = {packages: [], files: {}};
  packages.forEach(function (item) {
    const folder = path.join(root, "node_modules", item[0]);
    const meta = JSON.parse(fs.readFileSync(path.join(folder, "package.json"), "utf8"));
    manifest.packages.push({name: item[0], version: meta.version, license: meta.license, source: "https://registry.npmjs.org/" + item[0]});
    copy(path.join(folder, item[1]), path.join(theme, "licenses", item[0].replace(/[@/]/g, "_") + ".txt"));
  });
  fs.writeFileSync(path.join(theme, "js", "highlight-languages.json"), JSON.stringify(require("highlight.js").listLanguages().sort(), null, 2) + "\n");
  function hashTree(folder) {
    fs.readdirSync(folder, {withFileTypes: true}).forEach(function (entry) {
      const file = path.join(folder, entry.name);
      if (entry.isDirectory()) { hashTree(file); }
      else { manifest.files[path.relative(theme, file).replace(/\\/g, "/")] = crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex"); }
    });
  }
  ["js/mathjax", "fonts", "licenses"].forEach(function (folder) { hashTree(path.join(theme, folder)); });
  ["js/highlight.min.js", "js/highlight-languages.json", "js/lunr.min.js", "css/highlight.css", "css/vs.css", "css/vs2015.css", "css/fonts.css"].forEach(function (file) {
    manifest.files[file] = crypto.createHash("sha256").update(fs.readFileSync(path.join(theme, file))).digest("hex");
  });
  fs.writeFileSync(path.join(theme, "vendor-manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log("Vendored " + Object.keys(manifest.files).length + " assets; Highlight.js " + require("highlight.js").listLanguages().length + " languages.");
}
main().catch(function (error) { console.error(error); process.exit(1); });
