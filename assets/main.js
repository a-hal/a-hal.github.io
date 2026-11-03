// Theme toggle: follows the system setting until the visitor picks one.
(function () {
  var root = document.documentElement;
  var btn = document.getElementById("theme-toggle");
  if (!btn) return;

  function current() {
    var t = root.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  btn.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
  });
})();

// Remember the chosen language so the switch feels sticky.
document.querySelectorAll("[data-lang]").forEach(function (a) {
  a.addEventListener("click", function () {
    try { localStorage.setItem("lang", a.getAttribute("data-lang")); } catch (e) {}
  });
});
