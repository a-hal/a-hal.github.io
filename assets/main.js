/* Alain Halbouny, personal site.
   - The lamp: pull its cord (or click it) to switch light and dark.
     After Pin UI's Lamp Switch; the swing is one damped spring.
   - The bar: one indicator glides to the section you are in, a thin line
     shows how far down you are, and every section is a tap away.
   - Copy the email with one click (an icon swap after Fluid Functionalism).
   - The material recovery illustration: decisions land on the rows,
     then the total rolls like an odometer, after Bencho's rolling counter.
   - Sounds: Bencho's synthesised "tick", only ever for your own pull. */
(function () {
  "use strict";
  var root = document.documentElement;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── one spring, in frames (from Bencho's lab/spring) ─────────── */
  function springOf(tune) { return { k: 0.08 + (tune / 100) * 0.16, d: 0.62 + (tune / 100) * 0.2 }; }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  /* ── sound (Bencho sounds, Web Audio, no files) ───────────────── */
  var ctx = null;
  var SOUNDS = {
    tick: [{ hz: 196, to: 130, ms: 150, gain: 0.07, wave: "sine", cut: 900 }],
    latch: [{ hz: 256, ms: 90, gain: 0.04, wave: "square", cut: 2400, atk: 10 }]
  };
  function play(name) {
    try {
      ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
      if (ctx.state === "suspended") ctx.resume();
      var when = ctx.currentTime + 0.005;
      SOUNDS[name].forEach(function (n) {
        var t0 = when + (n.at || 0) / 1000, t1 = t0 + n.ms / 1000;
        var o = ctx.createOscillator();
        o.type = n.wave || "sine";
        o.frequency.setValueAtTime(n.hz, t0);
        if (n.to) o.frequency.exponentialRampToValueAtTime(n.to, t1);
        var g = ctx.createGain();
        var atk = Math.min((n.atk || 4) / 1000, (n.ms / 1000) * 0.6);
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.exponentialRampToValueAtTime(n.gain || 0.05, t0 + atk);
        g.gain.exponentialRampToValueAtTime(0.0001, t1);
        var tail = o;
        if (n.cut) { var f = ctx.createBiquadFilter(); f.type = "lowpass"; f.frequency.value = n.cut; o.connect(f); tail = f; }
        tail.connect(g).connect(ctx.destination);
        o.start(t0); o.stop(t1 + 0.02);
      });
    } catch (e) {}
  }

  /* ── theme ────────────────────────────────────────────────────── */
  function theme() {
    return root.getAttribute("data-theme") ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function flip() {
    var next = theme() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("theme", next); } catch (e) {}
    var lamp = document.getElementById("lamp");
    if (lamp) lamp.setAttribute("aria-pressed", next === "light" ? "true" : "false");
  }

  /* ── the lamp ─────────────────────────────────────────────────── */
  (function lamp() {
    var btn = document.getElementById("lamp");
    if (!btn) return;
    var swing = btn.querySelector(".swing"), hang = btn.querySelector(".hang"), cord = btn.querySelector(".cord");
    var REST = 34, DETENT = 20, MAX = 40;
    var y = 0, vy = 0, a = 0, va = 0, raf = 0, dragging = false, crossed = false;
    var start = null, moved = 0;
    btn.setAttribute("aria-pressed", theme() === "light" ? "true" : "false");

    function paint() {
      cord.setAttribute("y2", String(REST + y));
      hang.setAttribute("transform", "translate(0 " + y.toFixed(2) + ")");
      /* rotate in SVG's own coordinates, around the hook at (22, 0): same in every browser */
      swing.setAttribute("transform", "rotate(" + a.toFixed(2) + " 22 0)");
    }
    function run() {
      if (raf) return;
      /* with Reduce Motion on, the cord still follows the hand but settles back
         without overshoot, and nothing swings on its own */
      var prev = 0, sy = springOf(still ? 0 : 55), sa = springOf(70);
      function frame(t) {
        var dt = prev ? clamp((t - prev) / 16.67, 0, 2.5) : 1; prev = t;
        var busy = false;
        if (!dragging) {
          vy += (0 - y) * sy.k * dt; vy *= Math.pow(sy.d, dt); y += vy * dt;
          if (Math.abs(y) < 0.05 && Math.abs(vy) < 0.05) { y = 0; vy = 0; } else busy = true;
        }
        va += (0 - a) * sa.k * 0.35 * dt; va *= Math.pow(0.93, dt); a += va * dt;
        if (Math.abs(a) < 0.05 && Math.abs(va) < 0.05) { a = 0; va = 0; } else busy = true;
        paint();
        raf = busy || dragging ? requestAnimationFrame(frame) : 0;
      }
      raf = requestAnimationFrame(frame);
    }

    btn.addEventListener("pointerdown", function (e) {
      if (e.button !== 0) return;
      start = { x: e.clientX, y: e.clientY, a: a }; moved = 0; crossed = false; dragging = true;
      try { btn.setPointerCapture(e.pointerId); } catch (err) {}
      run();
    });
    btn.addEventListener("pointermove", function (e) {
      if (!dragging || !start) return;
      var dx = e.clientX - start.x, dy = Math.max(0, e.clientY - start.y);
      moved = Math.max(moved, Math.hypot(dx, dy));
      /* rubber band past the end of the cord */
      y = dy < MAX ? dy : MAX + (dy - MAX) * 0.2;
      a = still ? 0 : clamp(-dx * 0.5, -28, 28);
      if (!crossed && y > DETENT) { crossed = true; play("latch"); }
      if (crossed && y < DETENT - 6) crossed = false;
    });
    function release(e) {
      if (!dragging) return;
      dragging = false;
      var pulled = crossed;
      var clicked = moved < 5;
      if (pulled || clicked) { flip(); play("tick"); }
      if (clicked && !still) { vy = 7; va = (Math.random() > 0.5 ? 1 : -1) * 2.2; }
      if (!clicked && !still) { va += clamp(-a * 0.1, -4, 4); }
      start = null;
      run();
      if (e && e.pointerId !== undefined) { try { btn.releasePointerCapture(e.pointerId); } catch (err) {} }
    }
    btn.addEventListener("pointerup", release);
    btn.addEventListener("pointercancel", release);
    btn.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault(); flip(); play("tick");
        if (!still) { vy = 7; va = 2; run(); }
      }
    });
    btn.addEventListener("click", function (e) { e.preventDefault(); });
  })();

  /* ── blocks arrive once, as they first come into view ─────────── */
  (function reveal() {
    var blocks = document.querySelectorAll(".chapter .wrap > *");
    if (!("IntersectionObserver" in window)) { blocks.forEach(function (b) { b.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      var n = 0;
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.style.transitionDelay = (n++ * 60) + "ms";
        en.target.classList.add("in");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.05 });
    blocks.forEach(function (b) { io.observe(b); });
  })();

  /* ── the bar: where you are, and how far down ─────────────────── */
  (function bar() {
    var links = Array.prototype.slice.call(document.querySelectorAll(".track a[data-spy]"));
    var track = document.querySelector(".track"), pill = document.querySelector(".pill");
    var fill = document.querySelector(".progress span");
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("data-spy")); });
    var current = null, ticking = false;

    function place(a) {
      if (!a) { pill.classList.remove("on"); return; }
      pill.style.width = a.offsetWidth + "px";
      pill.style.transform = "translateX(" + a.offsetLeft + "px)";
      pill.classList.add("on");
    }
    function setActive(a) {
      if (a === current) return;
      if (current) current.classList.remove("on");
      if (a) a.classList.add("on");
      /* first appearance fades in where it lands instead of sliding over */
      if (!current && a) { pill.style.transition = "opacity 160ms ease"; place(a); void pill.offsetWidth; pill.style.transition = ""; }
      else place(a);
      current = a;
      /* on a phone, keep the active section in view in the strip */
      if (a && track.scrollWidth > track.clientWidth) {
        var left = a.offsetLeft - (track.clientWidth - a.offsetWidth) / 2;
        track.scrollTo({ left: left, behavior: still ? "auto" : "smooth" });
      }
    }
    function update() {
      ticking = false;
      var y = window.scrollY, vh = window.innerHeight, max = document.documentElement.scrollHeight - vh;
      if (fill) fill.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
      /* the section whose top has passed a line a third of the way down the screen */
      var line = vh * 0.33, active = null;
      targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top <= line) active = links[i]; });
      if (max - y < 4) active = links[links.length - 1];
      setActive(active);
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () { if (current) place(current); onScroll(); });
    links.forEach(function (a) {
      a.addEventListener("click", function () { setActive(a); });
    });
    update();
  })();

  /* ── copy the email: two glyphs in one cell, crossfading ──────── */
  document.querySelectorAll(".copy").forEach(function (btn) {
    var label = btn.querySelector(".copy-label"), live = btn.querySelector(".sr"), orig = label.textContent, t = 0;
    btn.addEventListener("click", function () {
      var email = btn.getAttribute("data-email");
      function done() {
        btn.classList.add("done"); label.textContent = btn.getAttribute("data-copied"); live.textContent = btn.getAttribute("data-copied");
        clearTimeout(t); t = setTimeout(function () { btn.classList.remove("done"); label.textContent = orig; live.textContent = ""; }, 1800);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(email).then(done, function () { window.location.href = "mailto:" + email; });
      else window.location.href = "mailto:" + email;
    });
  });

  /* ── the illustration plays when it scrolls into view ─────────── */
  document.querySelectorAll(".stage").forEach(function (stage) {
    if (!("IntersectionObserver" in window)) { playStage(stage); return; }
    var io = new IntersectionObserver(function (en) {
      if (en[0].isIntersecting) { io.disconnect(); setTimeout(function () { playStage(stage); }, still ? 0 : 200); }
    }, { threshold: 0.5 });
    io.observe(stage);
  });

  /* ── the illustration: decisions land, then the total rolls ───── */
  function playStage(stage) {
    if (stage.classList.contains("played")) return;
    stage.classList.add("played");
    var strips = Array.prototype.slice.call(stage.querySelectorAll(".dg > span"));
    var cell = strips[0].firstElementChild.offsetHeight;
    /* targets in turns: ones spin a full turn to 0, tens carry to 1 */
    var cols = strips.map(function (el) {
      return { el: el, pos: 0, vel: 0, target: 0, due: 0, next: Number(el.getAttribute("data-to")) };
    });
    var t0 = performance.now() + 620;
    /* last digit first, a column apart */
    cols.slice().reverse().forEach(function (c, i) { c.due = t0 + i * 90; });
    function paint() {
      cols.forEach(function (c) {
        var m = ((c.pos % 10) + 10) % 10;
        var smear = Math.min(3, Math.abs(c.vel) * 2.4);
        c.el.style.transform = "translateY(" + (-m * cell).toFixed(2) + "px)";
        c.el.style.filter = smear > 0.15 ? "blur(" + smear.toFixed(2) + "px)" : "";
      });
    }
    if (still) { cols.forEach(function (c) { c.pos = c.next; c.vel = 0; }); paint(); return; }
    var prev = 0, s = springOf(30);
    function frame(t) {
      var dt = prev ? clamp((t - prev) / 16.67, 0, 2.5) : 1; prev = t;
      var now = performance.now(), busy = false;
      cols.forEach(function (c) {
        if (c.due && c.due <= now) { c.target = c.next; c.due = 0; }
        if (c.due) busy = true;
        c.vel += (c.target - c.pos) * s.k * 0.5 * dt;
        c.vel *= Math.pow(s.d, dt);
        c.pos += c.vel * dt;
        if (Math.abs(c.target - c.pos) < 0.004 && Math.abs(c.vel) < 0.004) { c.pos = c.target; c.vel = 0; }
        else busy = true;
      });
      paint();
      if (busy) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
})();
