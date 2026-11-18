/* Runs before paint. Storage may be unavailable for file:// or private windows. */
(function () {
  var mode;
  try { mode = localStorage.getItem("best-offline-theme"); } catch (error) {}
  if (mode !== "dark" && mode !== "light") {
    mode = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  document.documentElement.setAttribute("data-theme", mode);
}());
