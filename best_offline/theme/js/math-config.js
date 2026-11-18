/* Every loader path resolves inside the theme. SVG needs no browser font fetch. */
(function () {
  var script = document.getElementById("MathJax-script");
  var root = script.src.slice(0, script.src.lastIndexOf("/"));
  window.MathJax = {
    loader: {paths: {mathjax: root, a11y: root + "/a11y", sre: root + "/sre"}},
    tex: {
      inlineMath: [["\\(", "\\)"]],
      displayMath: [["\\[", "\\]"]],
      processEscapes: true,
      tags: "ams"
    },
    options: {
      ignoreHtmlClass: ".*|",
      processHtmlClass: "arithmatex",
      enableMenu: false
    },
    svg: {fontCache: "local"}
  };
}());
