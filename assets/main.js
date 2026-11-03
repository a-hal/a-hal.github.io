/* Alain Halbouny, personal site.
   - The lamp: pull its cord (or click it) to switch light and dark.
     After Pin UI's Lamp Switch; the swing is one damped spring.
   - Lists: one hover highlight per list that glides between rows,
     after Fluid Functionalism's fluid hover.
   - Rows open in place to show their details.
   - The material recovery illustration: decisions land on the rows,
     then the total rolls like an odometer, after Bencho's rolling counter.
   - Sounds: Bencho's synthesised "tick", only ever for your own pull. */
(function () {
  "use strict";
  var root = document.documentElement;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

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
    var svg = btn.querySelector("svg"), hang = btn.querySelector(".hang"), cord = btn.querySelector(".cord");
    var REST = 34, DETENT = 20, MAX = 40;
    var y = 0, vy = 0, a = 0, va = 0, raf = 0, dragging = false, crossed = false;
    var start = null, moved = 0;
    btn.setAttribute("aria-pressed", theme() === "light" ? "true" : "false");

    function paint() {
      cord.setAttribute("y2", String(REST + y));
      hang.setAttribute("transform", "translate(0 " + y.toFixed(2) + ")");
      svg.style.transform = "rotate(" + a.toFixed(2) + "deg)";
    }
    function run() {
      if (raf) return;
      var prev = 0, sy = springOf(55), sa = springOf(70);
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
      if (!still) run();
    });
    btn.addEventListener("pointermove", function (e) {
      if (!dragging || !start) return;
      var dx = e.clientX - start.x, dy = Math.max(0, e.clientY - start.y);
      moved = Math.max(moved, Math.hypot(dx, dy));
      if (still) return;
      /* rubber band past the end of the cord */
      y = dy < MAX ? dy : MAX + (dy - MAX) * 0.2;
      a = clamp(-dx * 0.5, -28, 28);
      if (!crossed && y > DETENT) { crossed = true; play("latch"); }
      if (crossed && y < DETENT - 6) crossed = false;
    });
    function release(e) {
      if (!dragging) return;
      dragging = false;
      var pulled = crossed || (still && moved > 12);
      var clicked = moved < 5;
      if (pulled || clicked) { flip(); play("tick"); }
      if (clicked && !still) { vy = 7; va = (Math.random() > 0.5 ? 1 : -1) * 2.2; }
      if (!clicked && !still) { va += clamp(-a * 0.1, -4, 4); }
      start = null;
      if (!still) run();
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

  /* ── fluid hover: one highlight per list ──────────────────────── */
  function fluidHover(list) {
    var hl = document.createElement("div");
    hl.className = "hl"; hl.setAttribute("aria-hidden", "true");
    list.insertBefore(hl, list.firstChild);
    var current = null;
    function place(el) {
      hl.style.width = el.offsetWidth + "px";
      hl.style.height = el.offsetHeight + "px";
      hl.style.transform = "translate(" + el.offsetLeft + "px," + el.offsetTop + "px)";
    }
    function light(li) {
      if (li === current) return;
      if (!current) {
        /* a fresh entry fades in where it lands instead of sliding over */
        hl.classList.add("snap"); place(li); void hl.offsetWidth; hl.classList.remove("snap");
      } else place(li);
      current = li; hl.classList.add("on");
    }
    function out() { current = null; hl.classList.remove("on"); }
    list.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      /* only the click target lights: the row's head, not its open details */
      var head = e.target.closest(".item-head");
      if (head && list.contains(head)) light(head); else out();
    });
    list.addEventListener("pointerleave", out);
    if ("ResizeObserver" in window) {
      new ResizeObserver(function () { if (current) place(current); }).observe(list);
    }
  }
  if (finePointer) document.querySelectorAll(".list").forEach(fluidHover);

  /* ── rows that open ───────────────────────────────────────────── */
  document.querySelectorAll(".item-head").forEach(function (head) {
    head.addEventListener("click", function () {
      var li = head.parentNode, open = !li.classList.contains("open");
      li.classList.toggle("open", open);
      head.setAttribute("aria-expanded", open ? "true" : "false");
      var stage = li.querySelector(".stage");
      if (open && stage) setTimeout(function () { playStage(stage); }, still ? 0 : 260);
    });
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
