(() => {
  'use strict';

  const header = document.getElementById('site-header');
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');

  /* Mobile navigation ---------------------------------------------------- */
  const setMenu = (open) => {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  };

  if (toggle && nav) {
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', (event) => {
      if (!header.contains(event.target)) setMenu(false);
    });
  }

  /* Header border once the page has scrolled ----------------------------- */
  const onScroll = () => header && header.classList.toggle('is-scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* Highlight the nav link for the section in view (homepage only) ------- */
  const links = Array.from(document.querySelectorAll('.primary-nav a[data-section]'));
  const sections = links
    .map((link) => document.getElementById(link.dataset.section))
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    const visible = new Map();
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => visible.set(entry.target.id, entry.isIntersecting ? entry.intersectionRatio : 0));
      let current = null;
      let best = 0;
      visible.forEach((ratio, id) => { if (ratio > best) { best = ratio; current = id; } });
      links.forEach((link) => {
        if (link.dataset.section === current) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-30% 0px -50% 0px', threshold: [0, 0.25, 0.5, 1] });
    sections.forEach((section) => observer.observe(section));
  }

  /* Copy email address --------------------------------------------------- */
  const copyButton = document.querySelector('[data-copy]');
  const status = document.querySelector('.copy-status');
  if (copyButton && status) {
    copyButton.addEventListener('click', async () => {
      const value = copyButton.dataset.copy;
      try {
        await navigator.clipboard.writeText(value);
        status.textContent = 'Email address copied.';
      } catch (err) {
        status.textContent = 'Copy failed. Select the address above and copy it manually.';
      }
      window.setTimeout(() => { status.textContent = ''; }, 3500);
    });
  }

  /* Hide project images that fail to load -------------------------------- */
  document.querySelectorAll('.shot img').forEach((img) => {
    const hide = () => { const figure = img.closest('figure'); if (figure) figure.hidden = true; };
    if (img.complete && img.naturalWidth === 0) hide();
    img.addEventListener('error', hide);
  });

  /* ======================================================================
     Motion layer
     ====================================================================== */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Scroll reveal -------------------------------------------------------- */
  const revealEls = Array.from(document.querySelectorAll('[data-reveal]'));
  if (revealEls.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealEls.forEach((el) => el.classList.add('is-in'));
    } else {
      const revealer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) { entry.target.classList.add('is-in'); revealer.unobserve(entry.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
      revealEls.forEach((el) => revealer.observe(el));
    }
  }

  /* Cursor glow and project spotlight (fine pointers only) --------------- */
  const pointer = { x: window.innerWidth / 2, y: window.innerHeight / 2, active: false };
  if (finePointer && !reduceMotion) {
    const glow = document.querySelector('.cursor-glow');
    let glowX = pointer.x, glowY = pointer.y, glowRaf = 0;
    const moveGlow = () => {
      glowX += (pointer.x - glowX) * 0.14;
      glowY += (pointer.y - glowY) * 0.14;
      glow.style.transform = 'translate3d(' + glowX.toFixed(1) + 'px,' + glowY.toFixed(1) + 'px,0)';
      glowRaf = (Math.abs(pointer.x - glowX) + Math.abs(pointer.y - glowY) > 0.5) ? requestAnimationFrame(moveGlow) : 0;
    };
    window.addEventListener('pointermove', (event) => {
      pointer.x = event.clientX; pointer.y = event.clientY; pointer.active = true;
      if (glow) { glow.classList.add('is-on'); if (!glowRaf) glowRaf = requestAnimationFrame(moveGlow); }
    }, { passive: true });
    document.addEventListener('pointerleave', () => { pointer.active = false; if (glow) glow.classList.remove('is-on'); });

    document.querySelectorAll('.project').forEach((row) => {
      row.addEventListener('pointermove', (event) => {
        const box = row.getBoundingClientRect();
        row.style.setProperty('--mx', (event.clientX - box.left) + 'px');
        row.style.setProperty('--my', (event.clientY - box.top) + 'px');
      }, { passive: true });
    });
  } else {
    window.addEventListener('pointermove', (event) => { pointer.x = event.clientX; pointer.y = event.clientY; pointer.active = true; }, { passive: true });
  }

  /* Project page: highlight the current heading in "On this page" -------- */
  const tocLinks = Array.from(document.querySelectorAll('.toc a'));
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const targets = tocLinks.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const seen = new Map();
    const tocObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => seen.set(entry.target.id, entry.isIntersecting));
      const current = targets.find((el) => seen.get(el.id));
      tocLinks.forEach((a) => {
        if (current && a.getAttribute('href') === '#' + current.id) a.setAttribute('aria-current', 'true');
        else a.removeAttribute('aria-current');
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    targets.forEach((el) => tocObserver.observe(el));
  }

  /* Canvas background: pipeline lanes ------------------------------------
     Thin lanes drift past at different depths (scroll parallax). Small
     packets travel along them like builds moving through a pipeline.
     Scrolling speeds the packets up; the pointer pulls nearby packets
     toward it and lights up the lane. No libraries. */
  const canvas = document.getElementById('bg-canvas');
  const ctx = canvas && canvas.getContext ? canvas.getContext('2d') : null;
  if (ctx) {
    const AMBER = '255,180,84';
    const SLATE = '157,176,192';
    let W = 0, H = 0, dpr = 1, lanes = [];
    let scrollY = window.scrollY, scrollVel = 0, lastScrollY = scrollY;
    let running = false, raf = 0, last = 0;

    const rand = (a, b) => a + Math.random() * (b - a);

    const build = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = window.innerWidth; H = window.innerHeight;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = W < 700 ? 7 : W < 1100 ? 10 : 14;
      lanes = Array.from({ length: count }, (_, i) => {
        const depth = rand(0.06, 0.42);
        const packets = Array.from({ length: Math.round(rand(1, 3)) }, () => ({
          x: rand(0, W), len: rand(18, 64), speed: rand(18, 60), warm: Math.random() < 0.38, lift: 0,
        }));
        return { base: (i + rand(0.1, 0.9)) / count * (H * 1.5), depth, packets, glow: 0 };
      });
    };

    const laneY = (lane) => {
      const span = H * 1.5;
      let y = (lane.base - scrollY * lane.depth) % span;
      if (y < 0) y += span;
      return y - H * 0.25;
    };

    const draw = (dt) => {
      ctx.clearRect(0, 0, W, H);
      const boost = 1 + Math.min(Math.abs(scrollVel) * 0.04, 5);
      const R = 190;

      lanes.forEach((lane) => {
        const y = laneY(lane);
        if (y < -40 || y > H + 40) return;

        const near = pointer.active ? Math.max(0, 1 - Math.abs(pointer.y - y) / R) : 0;
        lane.glow += (near - lane.glow) * Math.min(1, dt * 6);

        ctx.beginPath();
        ctx.moveTo(0, y); ctx.lineTo(W, y);
        ctx.strokeStyle = 'rgba(' + SLATE + ',' + (0.045 + lane.glow * 0.10).toFixed(3) + ')';
        ctx.lineWidth = 1;
        ctx.stroke();

        lane.packets.forEach((p) => {
          p.x += p.speed * boost * dt * (0.5 + lane.depth * 2);
          if (p.x - p.len > W) { p.x = -rand(20, 200); p.warm = Math.random() < 0.38; }

          let py = y;
          let alpha = p.warm ? 0.5 : 0.22;
          if (pointer.active) {
            const dx = pointer.x - p.x, dy = pointer.y - y;
            const dist = Math.hypot(dx, dy);
            if (dist < R) {
              const f = 1 - dist / R;
              p.lift += (dy * f * 0.35 - p.lift) * Math.min(1, dt * 8);
              alpha = Math.min(0.95, alpha + f * 0.5);
            } else p.lift += (0 - p.lift) * Math.min(1, dt * 5);
          } else p.lift += (0 - p.lift) * Math.min(1, dt * 5);
          py += p.lift;

          const rgb = (p.warm || alpha > 0.6) ? AMBER : SLATE;
          const grad = ctx.createLinearGradient(p.x - p.len, 0, p.x, 0);
          grad.addColorStop(0, 'rgba(' + rgb + ',0)');
          grad.addColorStop(1, 'rgba(' + rgb + ',' + alpha.toFixed(3) + ')');
          ctx.strokeStyle = grad; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(p.x - p.len, py); ctx.lineTo(p.x, py); ctx.stroke();
          ctx.fillStyle = 'rgba(' + rgb + ',' + Math.min(1, alpha + 0.2).toFixed(3) + ')';
          ctx.fillRect(p.x - 1.5, py - 2.5, 4, 5);
        });
      });
    };

    const frame = (now) => {
      const dt = Math.min((now - last) / 1000 || 0.016, 0.05);
      last = now;
      scrollY = window.scrollY;
      scrollVel += ((scrollY - lastScrollY) / Math.max(dt, 0.001) - scrollVel) * Math.min(1, dt * 8);
      lastScrollY = scrollY;
      draw(dt);
      raf = running ? requestAnimationFrame(frame) : 0;
    };

    const start = () => { if (running || reduceMotion) return; running = true; last = performance.now(); raf = requestAnimationFrame(frame); };
    const stop = () => { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; };

    build();
    if (reduceMotion) {
      /* One still frame, redrawn when the size or scroll position changes. */
      lanes.forEach((lane) => lane.packets.forEach((p) => { p.speed = 0; }));
      draw(0);
      window.addEventListener('scroll', () => { scrollY = window.scrollY; draw(0); }, { passive: true });
      window.addEventListener('resize', () => { build(); lanes.forEach((l) => l.packets.forEach((p) => { p.speed = 0; })); draw(0); });
    } else {
      start();
      let resizeTimer = 0;
      window.addEventListener('resize', () => { clearTimeout(resizeTimer); resizeTimer = setTimeout(build, 150); });
      document.addEventListener('visibilitychange', () => { document.hidden ? stop() : start(); });
    }
  }
})();


/* Prefer lighter hero video on small screens / Save-Data */
(function () {
  const video = document.querySelector('.hero-video');
  if (!video) return;
  const saveData = navigator.connection && navigator.connection.saveData;
  const slow = navigator.connection && /2g|slow-2g/.test(navigator.connection.effectiveType || '');
  const mobile = window.matchMedia('(max-width: 767px)').matches;
  if (saveData || slow || mobile) {
    const light = video.querySelector('source[src*="720"]');
    if (light) {
      video.src = light.getAttribute('src');
      video.load();
      video.play().catch(function () {});
    }
  }
})();
