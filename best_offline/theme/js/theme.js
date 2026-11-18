/* Classic script, no modules/fetch/workers/service workers: works with file://. */
(function () {
  "use strict";
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");
  var label = document.getElementById("theme-label");
  function updateToggle() {
    var dark = root.getAttribute("data-theme") === "dark";
    label.textContent = dark ? "Light mode" : "Dark mode";
    toggle.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
    toggle.setAttribute("aria-pressed", String(dark));
  }
  toggle.addEventListener("click", function () {
    var mode = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", mode);
    try { localStorage.setItem("best-offline-theme", mode); } catch (error) {}
    updateToggle();
  });
  updateToggle();
  var preference = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  if (preference && preference.addListener) {
    preference.addListener(function (event) {
      var saved = null;
      try { saved = localStorage.getItem("best-offline-theme"); } catch (error) {}
      if (!saved) { root.setAttribute("data-theme", event.matches ? "dark" : "light"); updateToggle(); }
    });
  }
  var menu = document.getElementById("menu-toggle");
  function closeMenu() { document.body.classList.remove("nav-open"); menu.setAttribute("aria-expanded", "false"); }
  menu.addEventListener("click", function () {
    var open = document.body.classList.toggle("nav-open");
    menu.setAttribute("aria-expanded", String(open));
  });
  document.getElementById("nav-backdrop").addEventListener("click", closeMenu);

  // Highlight the complete source so tokens keep their context, then put the
  // author's links back at their original character offsets. Markdown fences
  // remain literal; only raw HTML pre.linked-code opts into this behavior.
  function highlightLinkedCode(code, language) {
    var links = [];
    code.querySelectorAll("a[href]").forEach(function (link) {
      var range = document.createRange();
      range.selectNodeContents(code);
      range.setEndBefore(link);
      var start = range.toString().length;
      if (link.textContent.length) {
        var anchor = document.createElement("a");
        anchor.setAttribute("href", link.getAttribute("href"));
        if (link.hasAttribute("title")) { anchor.setAttribute("title", link.getAttribute("title")); }
        links.push({start: start, end: start + link.textContent.length, node: anchor});
      }
    });
    var highlighted = document.createElement("code");
    highlighted.innerHTML = hljs.highlight(code.textContent, {language: language, ignoreIllegals: true}).value;
    var output = document.createDocumentFragment();
    var walker = document.createTreeWalker(highlighted, NodeFilter.SHOW_TEXT);
    var textNode, offset = 0, linkIndex = 0;
    while ((textNode = walker.nextNode())) {
      var local = 0;
      while (local < textNode.length) {
        while (linkIndex < links.length && links[linkIndex].end <= offset) { linkIndex++; }
        var link = links[linkIndex];
        var inside = link && offset >= link.start;
        var limit = link ? (inside ? link.end : link.start) : Infinity;
        var length = Math.min(textNode.length - local, limit - offset);
        var piece = document.createTextNode(textNode.data.slice(local, local + length));
        // Retain every syntax span surrounding this slice, including nested tokens.
        for (var parent = textNode.parentNode; parent !== highlighted; parent = parent.parentNode) {
          var span = parent.cloneNode(false);
          span.appendChild(piece);
          piece = span;
        }
        if (inside) {
          if (!link.node.parentNode) { output.appendChild(link.node); }
          link.node.appendChild(piece);
        } else { output.appendChild(piece); }
        local += length;
        offset += length;
      }
    }
    code.textContent = "";
    code.appendChild(output);
    code.classList.add("hljs");
  }

  document.querySelectorAll("pre > code").forEach(function (code) {
    var language = (code.className.match(/language-([\w+-]+)/) || [])[1];
    var pre = code.parentNode;
    if (window.hljs && language && hljs.getLanguage(language)) {
      if (pre.classList.contains("linked-code")) { highlightLinkedCode(code, language); }
      else { hljs.highlightElement(code); }
    }
    var bar = document.createElement("div");
    bar.className = "code-toolbar";
    var tag = document.createElement("span");
    tag.textContent = language || "text";
    bar.appendChild(tag);
    var copy = document.createElement("button");
    copy.type = "button";
    copy.textContent = "Copy";
    copy.setAttribute("aria-label", "Copy " + (language || "text") + " code");
    copy.addEventListener("click", function () {
      function done() { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy"; }, 1800); }
      function fallback() {
        var area = document.createElement("textarea");
        area.value = code.textContent;
        area.style.position = "fixed";
        area.style.opacity = "0";
        document.body.appendChild(area);
        area.select();
        var copied = false;
        try { copied = document.execCommand("copy"); } catch (error) {}
        area.remove();
        copy.focus();
        if (copied) { done(); } else { copy.textContent = "Select & copy"; }
      }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(code.textContent).then(done, fallback);
      } else { fallback(); }
    });
    bar.appendChild(copy);
    pre.parentNode.insertBefore(bar, pre);
    pre.classList.add("with-toolbar");
  });

  var dialog = document.getElementById("search-dialog");
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var status = document.getElementById("search-status");
  var entries = window.BEST_OFFLINE_SEARCH || [];
  var byId = {};
  var index = null;
  var lastFocus;
  var timer;
  var base = document.body.getAttribute("data-base-url") || ".";
  function normalizeTerms(value) {
    return value.replace(/\bc\+\+/gi, "cpp").replace(/\bc#/gi, "csharp");
  }
  function makeIndex() {
    if (index || !window.lunr) { return; }
    entries.forEach(function (entry) { byId[entry.id] = entry; });
    index = lunr(function () {
      this.ref("id");
      this.field("title", {boost: 8});
      this.field("page", {boost: 3});
      this.field("text");
      var builder = this;
      entries.forEach(function (entry) {
        builder.add({id: entry.id, title: normalizeTerms(entry.title),
          page: normalizeTerms(entry.page), text: normalizeTerms(entry.text)});
      });
    });
  }
  function openSearch() {
    lastFocus = document.activeElement;
    closeMenu();
    dialog.hidden = false;
    document.body.classList.add("search-active");
    input.focus();
    makeIndex();
    if (!entries.length || !index) { status.textContent = "Search data is missing. Rebuild with the best-offline plugin enabled."; }
  }
  function closeSearch() {
    dialog.hidden = true;
    document.body.classList.remove("search-active");
    if (lastFocus) { lastFocus.focus(); }
  }
  document.querySelectorAll(".search-open").forEach(function (button) { button.addEventListener("click", openSearch); });
  document.getElementById("search-close").addEventListener("click", closeSearch);
  dialog.addEventListener("click", function (event) { if (event.target === dialog) { closeSearch(); } });
  document.addEventListener("keydown", function (event) {
    var editing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) || document.activeElement.isContentEditable;
    if (event.key === "/" && !editing && dialog.hidden) { event.preventDefault(); openSearch(); }
    if (event.key === "Escape") { if (!dialog.hidden) { closeSearch(); } closeMenu(); }
    if (event.key === "Tab" && !dialog.hidden) {
      var focusable = dialog.querySelectorAll("button, input, a[href]");
      var first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
  });
  function search() {
    results.textContent = "";
    var query = input.value.trim().toLowerCase();
    if (!query) { status.textContent = "Type to search. Everything stays on this device."; return; }
    if (!index) { return; }
    var terms = lunr.tokenizer(normalizeTerms(query)).map(function (token) {
      return lunr.stopWordFilter(lunr.trimmer(token));
    }).filter(Boolean).map(function (token) { return token.toString(); });
    if (!terms.length) { status.textContent = "Try a more specific search term."; return; }
    var matches = index.query(function (q) {
      terms.forEach(function (term) {
        // Stem before adding the prefix wildcard; otherwise "equations*" misses "equat".
        index.pipeline.runString(term).forEach(function (stem) {
          q.term(stem, {usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING,
            presence: lunr.Query.presence.REQUIRED});
        });
      });
    });
    status.textContent = matches.length ? matches.length + " matching sections" : "No results. Try a shorter or different term.";
    matches.slice(0, 30).forEach(function (match) {
      var entry = byId[match.ref];
      var li = document.createElement("li"), link = document.createElement("a");
      link.href = base + "/" + entry.url;
      var title = document.createElement("strong");
      title.textContent = entry.title;
      var section = document.createElement("small");
      section.textContent = entry.page;
      var snippet = document.createElement("p");
      var position = entry.text.toLowerCase().indexOf(terms[0] || query);
      var start = Math.max(0, position - 55);
      snippet.textContent = (start ? "…" : "") + entry.text.slice(start, start + 190) + (entry.text.length > start + 190 ? "…" : "");
      link.appendChild(section); link.appendChild(title); link.appendChild(snippet);
      li.appendChild(link); results.appendChild(li);
    });
  }
  input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(search, 100); });
  input.addEventListener("keydown", function (event) {
    if (event.key === "ArrowDown") { var first = results.querySelector("a"); if (first) { event.preventDefault(); first.focus(); } }
    if (event.key === "Enter") { var hit = results.querySelector("a"); if (hit) { hit.click(); } }
  });
}());
