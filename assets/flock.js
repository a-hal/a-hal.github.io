/* The flock: a small boids simulation that lives at the foot of the page.
   Light mode draws birds in ink; pull the lamp and they become fireflies.
   Move to steer them away, hold to call them in, click to scatter them.
   Plain canvas 2D, no libraries; it sleeps when it is off screen. */
(function () {
  "use strict";
  var canvas = document.getElementById("flock");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  var root = document.documentElement;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var W = 0, H = 0, DPR = 1, birds = [], running = false, visible = false, raf = 0;
  var pointer = { x: -1e4, y: -1e4, inside: false, down: false, downAt: 0 };
  var night = false, ink = "#18201c", glow = "#f3dc9a", sprite = null;
  var counter = document.getElementById("flock-count");

  function isDark() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "dark";
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function readTheme() {
    night = isDark();
    var cs = getComputedStyle(root);
    ink = cs.getPropertyValue("--ink").trim() || ink;
    glow = "#e9c46a";
    sprite = makeSprite(glow);
  }
  /* a soft dot, drawn once and stamped, so a hundred fireflies stay cheap */
  function makeSprite(color) {
    var s = document.createElement("canvas"), r = 16;
    s.width = s.height = r * 2 * DPR;
    var g = s.getContext("2d"), c = r * DPR;
    var grad = g.createRadialGradient(c, c, 0, c, c, c);
    grad.addColorStop(0, color);
    grad.addColorStop(0.18, color);
    grad.addColorStop(0.45, hexA(color, 0.25));
    grad.addColorStop(1, hexA(color, 0));
    g.fillStyle = grad;
    g.fillRect(0, 0, s.width, s.height);
    return s;
  }
  function hexA(hex, a) {
    var n = parseInt(hex.replace("#", ""), 16);
    return "rgba(" + (n >> 16 & 255) + "," + (n >> 8 & 255) + "," + (n & 255) + "," + a + ")";
  }

  function resize() {
    var r = canvas.getBoundingClientRect();
    DPR = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    var want = Math.round(clamp(W * H / 4200, 40, 140));
    while (birds.length < want) birds.push(spawn());
    birds.length = want;
    if (counter) counter.textContent = String(want);
    sprite = makeSprite(glow);
  }
  function spawn() {
    var a = Math.random() * Math.PI * 2, sp = 1 + Math.random();
    return { x: Math.random() * W, y: Math.random() * H, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp,
             phase: Math.random() * Math.PI * 2, flap: 0.18 + Math.random() * 0.08, size: 0.8 + Math.random() * 0.5 };
  }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  /* ── the rules ────────────────────────────────────────────────── */
  function step(dt) {
    var n = birds.length, i, j, b, o;
    var SEE = night ? 40 : 46, SEP = night ? 18 : 14;
    var maxV = night ? 1.1 : 2.6, minV = night ? 0.25 : 1.1;
    var held = pointer.down && performance.now() - pointer.downAt > 120;
    for (i = 0; i < n; i++) {
      b = birds[i];
      var ax = 0, ay = 0, cx = 0, cy = 0, sx = 0, sy = 0, cnt = 0;
      for (j = 0; j < n; j++) {
        if (i === j) continue;
        o = birds[j];
        var dx = o.x - b.x, dy = o.y - b.y, d2 = dx * dx + dy * dy;
        if (d2 > SEE * SEE) continue;
        cnt++;
        ax += o.vx; ay += o.vy; cx += o.x; cy += o.y;
        if (d2 < SEP * SEP && d2 > 0.01) { var d = Math.sqrt(d2); sx -= dx / d; sy -= dy / d; }
      }
      var fx = 0, fy = 0;
      if (cnt) {
        /* alignment, cohesion, separation; fireflies mostly ignore each other */
        var al = night ? 0.004 : 0.05, co = night ? 0.0004 : 0.0028, se = night ? 0.03 : 0.09;
        fx += (ax / cnt - b.vx) * al + (cx / cnt - b.x) * co + sx * se;
        fy += (ay / cnt - b.vy) * al + (cy / cnt - b.y) * co + sy * se;
      }
      if (night) { /* a firefly wanders */
        b.phase += 0.02 * dt;
        fx += Math.cos(b.phase * 1.3 + i) * 0.03; fy += Math.sin(b.phase * 0.9 + i * 2) * 0.03;
      }
      /* the hand: held, it calls them in; otherwise they keep their distance */
      if (pointer.inside || pointer.down) {
        var px = pointer.x - b.x, py = pointer.y - b.y, pd = Math.sqrt(px * px + py * py) || 1;
        if (held) {
          var pull = night ? 0.05 : 0.09;
          fx += (px / pd) * pull; fy += (py / pd) * pull;
          /* orbit rather than pile up */
          fx += (-py / pd) * pull * 0.6; fy += (px / pd) * pull * 0.6;
        } else if (pd < 90) {
          var push = (1 - pd / 90) * (night ? 0.25 : 0.5);
          fx -= (px / pd) * push; fy -= (py / pd) * push;
        }
      }
      /* soft walls: turn before the edge instead of bouncing off it */
      var m = 30, turn = 0.12;
      if (b.x < m) fx += turn * (1 - b.x / m); else if (b.x > W - m) fx -= turn * (1 - (W - b.x) / m);
      if (b.y < m) fy += turn * (1 - b.y / m); else if (b.y > H - m) fy -= turn * (1 - (H - b.y) / m);

      b.vx += fx * dt; b.vy += fy * dt;
      var v = Math.sqrt(b.vx * b.vx + b.vy * b.vy) || 1;
      var lim = held ? maxV * 1.5 : maxV;
      if (v > lim) { b.vx *= lim / v; b.vy *= lim / v; }
      else if (v < minV) { b.vx *= minV / v; b.vy *= minV / v; }
      b.x += b.vx * dt; b.y += b.vy * dt;
      b.x = clamp(b.x, -20, W + 20); b.y = clamp(b.y, -20, H + 20);
      b.phase += b.flap * dt * (0.6 + v * 0.25);
    }
  }

  function scatter(x, y) {
    for (var i = 0; i < birds.length; i++) {
      var b = birds[i], dx = b.x - x, dy = b.y - y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      if (d < 220) { var k = (1 - d / 220) * (night ? 3 : 7); b.vx += (dx / d) * k; b.vy += (dy / d) * k; }
    }
  }

  /* ── drawing ──────────────────────────────────────────────────── */
  function draw() {
    ctx.clearRect(0, 0, W, H);
    var i, b;
    if (night) {
      var s = 32;
      ctx.globalCompositeOperation = "lighter";
      for (i = 0; i < birds.length; i++) {
        b = birds[i];
        var flick = 0.35 + 0.65 * Math.pow(0.5 + 0.5 * Math.sin(b.phase * 1.7 + i), 3);
        ctx.globalAlpha = flick;
        var sz = s * b.size * (0.7 + flick * 0.3);
        ctx.drawImage(sprite, b.x - sz / 2, b.y - sz / 2, sz, sz);
      }
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
    } else {
      ctx.fillStyle = ink;
      for (i = 0; i < birds.length; i++) {
        b = birds[i];
        var ang = Math.atan2(b.vy, b.vx), wing = Math.sin(b.phase) * 0.9;
        var L = 5.5 * b.size, S = 4.2 * b.size;
        ctx.save();
        ctx.translate(b.x, b.y); ctx.rotate(ang);
        /* a bird is two strokes from the body, beating in turn */
        ctx.beginPath();
        ctx.moveTo(L * 0.5, 0);
        ctx.quadraticCurveTo(-L * 0.2, -S * (0.4 + wing * 0.6), -L, -S * (0.6 + wing));
        ctx.quadraticCurveTo(-L * 0.35, -S * 0.15, -L * 0.25, 0);
        ctx.quadraticCurveTo(-L * 0.35, S * 0.15, -L, S * (0.6 + wing));
        ctx.quadraticCurveTo(-L * 0.2, S * (0.4 + wing * 0.6), L * 0.5, 0);
        ctx.globalAlpha = 0.82;
        ctx.fill();
        ctx.restore();
      }
      ctx.globalAlpha = 1;
    }
  }

  function loop(t) {
    raf = 0;
    if (!running) return;
    var dt = loop.prev ? clamp((t - loop.prev) / 16.67, 0.2, 2.5) : 1;
    loop.prev = t;
    step(dt); draw();
    raf = requestAnimationFrame(loop);
  }
  function start() {
    if (running || still) return;
    running = true; loop.prev = 0; raf = requestAnimationFrame(loop);
  }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
  function wake() { if (visible && !document.hidden) start(); else stop(); }

  /* Reduce Motion: a still flock; it moves only while your hand is on it. */
  function nudge(ms) {
    if (!still) return;
    running = true; loop.prev = 0;
    if (!raf) raf = requestAnimationFrame(loop);
    clearTimeout(nudge.t); nudge.t = setTimeout(function () { running = false; }, ms);
  }

  /* ── input ────────────────────────────────────────────────────── */
  function local(e) { var r = canvas.getBoundingClientRect(); pointer.x = e.clientX - r.left; pointer.y = e.clientY - r.top; }
  canvas.addEventListener("pointermove", function (e) { local(e); pointer.inside = true; if (still && pointer.down) nudge(400); });
  canvas.addEventListener("pointerleave", function () { pointer.inside = false; pointer.down = false; });
  canvas.addEventListener("pointerdown", function (e) {
    local(e); pointer.down = true; pointer.downAt = performance.now(); pointer.inside = true;
    try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
    nudge(1500);
  });
  function up(e) {
    if (!pointer.down) return;
    local(e);
    if (performance.now() - pointer.downAt < 220) scatter(pointer.x, pointer.y);
    pointer.down = false;
    if (e.pointerType !== "mouse") pointer.inside = false;
    nudge(1500);
  }
  canvas.addEventListener("pointerup", up);
  canvas.addEventListener("pointercancel", function () { pointer.down = false; pointer.inside = false; });

  /* the lamp flips the theme: birds become fireflies and back */
  new MutationObserver(function () { readTheme(); if (!running) draw(); })
    .observe(root, { attributes: true, attributeFilter: ["data-theme"] });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () { readTheme(); if (!running) draw(); });

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (en) { visible = en[0].isIntersecting; wake(); }, { rootMargin: "100px" }).observe(canvas);
  } else { visible = true; }
  document.addEventListener("visibilitychange", wake);
  var rz = 0;
  window.addEventListener("resize", function () { clearTimeout(rz); rz = setTimeout(function () { resize(); if (!running) draw(); }, 120); });

  readTheme(); resize();
  for (var k = 0; k < 90; k++) step(1); /* open on a flock that has already found its shape */
  draw(); wake();
})();
