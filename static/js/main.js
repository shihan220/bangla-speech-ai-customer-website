/* ===========================================
   ASYNC CLONE — main.js
=========================================== */

/* ── Pricing center-zoom slider ─────────────────────────── */
(function initPricingSlider() {
  const outer  = document.querySelector('.pricing-slider-outer');
  const track  = document.getElementById('pricingTrack');
  if (!track || !outer) return;

  const slides  = Array.from(track.querySelectorAll('.pricing-slide'));
  const dotEls  = Array.from(document.querySelectorAll('.pricing-dot'));
  const prevBtn = document.getElementById('pricingPrev');
  const nextBtn = document.getElementById('pricingNext');
  const total   = slides.length;
  if (!total) return;

  const CARD_W = 320, GAP = 24, STEP = CARD_W + GAP;
  let current = Math.floor((total - 1) / 2);

  function update(animate) {
    if (!animate) track.style.transition = 'none';
    const cx = outer.offsetWidth / 2 - CARD_W / 2;
    track.style.transform = `translateX(${cx - current * STEP}px)`;
    slides.forEach((s, i) => s.classList.toggle('is-center', i === current));
    dotEls.forEach((d, i) => d.classList.toggle('active', i === current));
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === total - 1;
    if (!animate) requestAnimationFrame(() => { track.style.transition = ''; });
  }

  prevBtn?.addEventListener('click', () => { if (current > 0)          { current--; update(true); } });
  nextBtn?.addEventListener('click', () => { if (current < total - 1)  { current++; update(true); } });
  dotEls.forEach((d, i) => d.addEventListener('click', () => { current = i; update(true); }));

  let tx = 0;
  outer.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
  outer.addEventListener('touchend',   e => {
    const dx = tx - e.changedTouches[0].clientX;
    if (Math.abs(dx) > 44) {
      if (dx > 0 && current < total - 1) current++;
      else if (dx < 0 && current > 0)    current--;
      update(true);
    }
  });

  update(false);
  window.addEventListener('resize', () => update(false));
})();

(function () {
  'use strict';

  /* -----------------------------------------------
     0. ANNOUNCEMENT BAR — open contact modal
  ----------------------------------------------- */
  document.getElementById('announceContactBtn')?.addEventListener('click', function (e) {
    e.preventDefault();
    var overlay = document.getElementById('contactOverlay');
    if (overlay) {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  });

  /* -----------------------------------------------
     1. NAVBAR — scroll shadow
  ----------------------------------------------- */
  const header    = document.getElementById('header');
  const navWrapper = header ? header.querySelector('.nav-wrapper') : null;

  if (navWrapper) {
    const onScroll = () => {
      navWrapper.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* -----------------------------------------------
     2. HAMBURGER — open / close mobile menu
  ----------------------------------------------- */
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileMenu   = document.getElementById('mobileMenu');

  if (hamburgerBtn && mobileMenu) {
    hamburgerBtn.addEventListener('click', () => {
      const isOpen = hamburgerBtn.classList.toggle('open');
      mobileMenu.classList.toggle('open', isOpen);
      hamburgerBtn.setAttribute('aria-expanded', isOpen);
      mobileMenu.setAttribute('aria-hidden', !isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (
        hamburgerBtn.classList.contains('open') &&
        !hamburgerBtn.contains(e.target) &&
        !mobileMenu.contains(e.target)
      ) {
        closeMenu();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && hamburgerBtn.classList.contains('open')) {
        closeMenu();
      }
    });
  }

  function closeMenu() {
    if (!hamburgerBtn) return;
    hamburgerBtn.classList.remove('open');
    mobileMenu.classList.remove('open');
    hamburgerBtn.setAttribute('aria-expanded', false);
    mobileMenu.setAttribute('aria-hidden', true);
    document.body.style.overflow = '';
  }

  /* -----------------------------------------------
     3. MOBILE ACCORDION (nav sub-items)
  ----------------------------------------------- */
  const accordionBtns = document.querySelectorAll('.accordion-btn');

  accordionBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const content = btn.nextElementSibling;
      if (!content || !content.classList.contains('mobile-accordion')) return;

      const isOpen = btn.classList.contains('open');

      // Close all others
      accordionBtns.forEach((other) => {
        if (other !== btn) {
          other.classList.remove('open');
          const otherContent = other.nextElementSibling;
          if (otherContent) otherContent.classList.remove('open');
        }
      });

      btn.classList.toggle('open', !isOpen);
      content.classList.toggle('open', !isOpen);
    });
  });

  /* -----------------------------------------------
     4. DESKTOP DROPDOWN — keep open on hover
     (CSS handles :hover, JS handles focus/keyboard)
  ----------------------------------------------- */
  const navItems = document.querySelectorAll('.nav-item.has-dropdown');

  navItems.forEach((item) => {
    const trigger  = item.querySelector('.nav-link');
    const dropdown = item.querySelector('.dropdown');

    if (!trigger || !dropdown) return;

    // Keep accessible with keyboard tab
    trigger.addEventListener('focus', () => {
      item.classList.add('force-open');
    });

    item.addEventListener('focusout', (e) => {
      if (!item.contains(e.relatedTarget)) {
        item.classList.remove('force-open');
      }
    });
  });

  /* -----------------------------------------------
     5a. VOICE CARD WAVEFORMS — messenger-style
  ----------------------------------------------- */
  function seededRand(seed) {
    let s = seed;
    return function () {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }

  function drawVcWave(canvas, progress) {
    const dpr = window.devicePixelRatio || 1;
    if (!canvas.offsetWidth) return;
    if (canvas.width !== Math.round(canvas.offsetWidth * dpr)) {
      canvas.width  = Math.round(canvas.offsetWidth  * dpr);
      canvas.height = Math.round(canvas.offsetHeight * dpr);
    }
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = canvas.offsetWidth;
    const H = canvas.offsetHeight;
    const heights = canvas._vcHeights || [];
    const N = heights.length;
    if (!N) return;
    const gap   = 2.5;
    const barW  = (W - gap * (N - 1)) / N;
    const CY    = H / 2;
    const progX = progress * W;

    ctx.clearRect(0, 0, W, H);

    heights.forEach((h, i) => {
      const x  = i * (barW + gap);
      const bh = Math.max(3, h * H * 0.88);
      const y  = CY - bh / 2;
      const cx = x + barW / 2;
      const r  = Math.min(barW / 2, 2.5);

      ctx.fillStyle = cx <= progX ? '#F0A050' : 'rgba(255,255,255,0.18)';

      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.lineTo(x + barW - r, y);
      ctx.arcTo(x + barW, y,    x + barW, y + r,      r);
      ctx.lineTo(x + barW, y + bh - r);
      ctx.arcTo(x + barW, y + bh, x + barW - r, y + bh, r);
      ctx.lineTo(x + r,    y + bh);
      ctx.arcTo(x, y + bh, x, y + bh - r, r);
      ctx.lineTo(x, y + r);
      ctx.arcTo(x, y,      x + r, y,      r);
      ctx.closePath();
      ctx.fill();
    });
  }

  (function buildWaveforms() {
    document.querySelectorAll('.vc-waveform').forEach(canvas => {
      const seed = parseInt(canvas.dataset.seed, 10) || 42;
      const rand = seededRand(seed);
      const N    = 42;
      canvas._vcHeights = Array.from({ length: N }, (_, i) => {
        const env = 0.22 + 0.78 * Math.sin((i / N) * Math.PI);
        return Math.max(0.12, (0.25 + rand() * 0.75) * env);
      });
      /* defer draw until canvas has layout dimensions */
      requestAnimationFrame(() => drawVcWave(canvas, 0));
    });
  })();

  /* -----------------------------------------------
     5b. VOICE SECTION — tab switcher
  ----------------------------------------------- */
  document.querySelectorAll('.v-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.v-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  /* -----------------------------------------------
     5b2. MESSENGER-STYLE VOICE PLAYERS
  ----------------------------------------------- */
  /* -----------------------------------------------
     5a2. VOICE SECTION — background animation canvas
     Waves sit in the heading band (top ~28%) where
     they are actually visible — not behind the cards.
  ----------------------------------------------- */
  (function initVsBgAnimation() {
    const cvs = document.getElementById('vsBg');
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    let W = 0, H = 0;

    function resize() {
      W = cvs.parentElement.offsetWidth;
      H = cvs.parentElement.offsetHeight;
      cvs.width  = Math.round(W * dpr);
      cvs.height = Math.round(H * dpr);
    }
    /* defer first resize until layout is complete */
    requestAnimationFrame(resize);
    window.addEventListener('resize', resize);

    /*
     * Section layout (approx):
     *   0  – H*0.28  : heading + top padding  ← animation visible here
     *   H*0.28 – H*0.75 : card carousel        ← cards cover canvas here
     *   H*0.75 – H    : nav + bottom padding   ← animation visible here
     *
     * So waves are centred at H*0.18 (top) and H*0.85 (bottom).
     */
    const waves = [
      { yR: 0.16, speed: 0.22, freq: 0.0080, amp: 22, phase: 0.0,  r: 240, g: 150, b: 60  },
      { yR: 0.20, speed: 0.35, freq: 0.0110, amp: 16, phase: 2.0,  r: 232, g: 80,  b: 10  },
      { yR: 0.24, speed: 0.16, freq: 0.0055, amp: 28, phase: 3.8,  r: 255, g: 190, b: 70  },
      { yR: 0.84, speed: 0.28, freq: 0.0090, amp: 18, phase: 1.4,  r: 232, g: 80,  b: 10  },
      { yR: 0.88, speed: 0.18, freq: 0.0065, amp: 14, phase: 4.2,  r: 240, g: 150, b: 60  },
    ];

    const rings = [];
    let lastRingTs = 0;
    let t = 0;

    function frame(ts) {
      t += 0.016;
      if (!W || !H) { requestAnimationFrame(frame); return; }

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      /* top-left + top-right corner glow orbs — in heading area */
      const g1 = ctx.createRadialGradient(W * 0.15, H * 0.08, 0, W * 0.15, H * 0.08, W * 0.36);
      g1.addColorStop(0, 'rgba(232,80,10,0.18)');
      g1.addColorStop(1, 'rgba(232,80,10,0)');
      ctx.fillStyle = g1;
      ctx.fillRect(0, 0, W, H);

      const g2 = ctx.createRadialGradient(W * 0.85, H * 0.06, 0, W * 0.85, H * 0.06, W * 0.32);
      g2.addColorStop(0, 'rgba(240,150,60,0.14)');
      g2.addColorStop(1, 'rgba(240,150,60,0)');
      ctx.fillStyle = g2;
      ctx.fillRect(0, 0, W, H);

      /* wave lines — confined to top and bottom strips */
      waves.forEach((w, i) => {
        const breathe = 0.68 + 0.32 * Math.sin(t * 0.5 + i * 1.5);
        const alpha   = 0.22 * breathe;
        const amp     = w.amp * breathe;
        const cy      = H * w.yR;

        ctx.beginPath();
        for (let x = 0; x <= W; x += 3) {
          const y = cy
            + amp * Math.sin(x * w.freq + t * w.speed + w.phase)
            + amp * 0.4 * Math.sin(x * w.freq * 2.3 + t * w.speed * 1.7 + w.phase * 0.6);
          x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }

        ctx.strokeStyle = `rgba(${w.r},${w.g},${w.b},${alpha.toFixed(3)})`;
        ctx.lineWidth   = 1.6;
        ctx.shadowBlur  = 7;
        ctx.shadowColor = `rgba(${w.r},${w.g},${w.b},0.4)`;
        ctx.stroke();
        ctx.shadowBlur  = 0;
      });

      /* expanding arc rings from top-center — arcs through heading area */
      if (ts - lastRingTs > 2800) {
        rings.push({ born: ts });
        lastRingTs = ts;
      }
      const rcx = W * 0.5, rcy = H * 0.18;
      const maxR = W * 0.55;
      for (let i = rings.length - 1; i >= 0; i--) {
        const age = (ts - rings[i].born) / 3400;
        if (age >= 1) { rings.splice(i, 1); continue; }
        const r = maxR * age;
        const a = (1 - age) * 0.18;
        ctx.beginPath();
        ctx.arc(rcx, rcy, r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(240,150,60,${a.toFixed(3)})`;
        ctx.lineWidth   = 1.0;
        ctx.stroke();
      }

      requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
  })();

  (function initVoicePlayers() {
    const ICON_PLAY  = `<svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"/></svg>`;
    const ICON_PAUSE = `<svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>`;

    function fmt(s) {
      const t = Math.max(0, Math.floor(s));
      return `0:${t.toString().padStart(2, '0')}`;
    }

    let activeState = null;

    document.querySelectorAll('.vc-player').forEach(player => {
      const btn      = player.querySelector('.vc-play-btn');
      const canvas   = player.querySelector('.vc-waveform');
      const durEl    = player.querySelector('.vc-dur');
      const totalDur = parseFloat(player.dataset.duration) || 4;
      const audioSrc = player.dataset.audio || null;   /* real file URL from Django */

      btn.innerHTML     = ICON_PLAY;
      durEl.textContent = fmt(totalDur);

      /* ── Real audio object (only when file uploaded) ── */
      let audioEl = null;
      if (audioSrc) {
        audioEl = new Audio(audioSrc);
        audioEl.preload = 'metadata';
        /* update displayed duration once metadata loads */
        audioEl.addEventListener('loadedmetadata', () => {
          durEl.textContent = fmt(audioEl.duration);
        });
      }

      let playing = false;
      let rafId   = null;
      let lastTs  = null;
      let progress = 0;

      function stop(reset) {
        playing = false;
        cancelAnimationFrame(rafId);
        lastTs = null;
        btn.innerHTML = ICON_PLAY;
        if (audioEl) { audioEl.pause(); if (reset) audioEl.currentTime = 0; }
        if (reset) {
          progress = 0;
          durEl.textContent = audioEl ? fmt(audioEl.duration || totalDur) : fmt(totalDur);
          drawVcWave(canvas, 0);
        }
        if (activeState && activeState.player === player) activeState = null;
        player.closest('.vc-card')?.classList.remove('is-playing');
      }

      /* ── Animation loop ── */
      function tick(ts) {
        if (audioEl) {
          /* drive progress from real audio currentTime */
          const dur = audioEl.duration || totalDur;
          progress  = audioEl.currentTime / dur;
          durEl.textContent = fmt(audioEl.currentTime);
          if (audioEl.ended) { stop(true); return; }
        } else {
          /* simulated */
          if (!lastTs) lastTs = ts;
          progress += (ts - lastTs) / 1000 / totalDur;
          lastTs    = ts;
          durEl.textContent = fmt(progress * totalDur);
          if (progress >= 1) {
            progress = 1;
            drawVcWave(canvas, 1);
            setTimeout(() => stop(true), 320);
            return;
          }
        }

        drawVcWave(canvas, progress);
        rafId = requestAnimationFrame(tick);
      }

      btn.addEventListener('click', () => {
        if (playing) { stop(false); return; }

        /* pause any other active player */
        if (activeState && activeState.player !== player) activeState.stop(true);

        playing = true;
        lastTs  = null;
        btn.innerHTML = ICON_PAUSE;
        activeState   = { player, stop };
        player.closest('.vc-card')?.classList.add('is-playing');

        if (audioEl) {
          audioEl.play().catch(() => {});   /* real audio */
        }
        rafId = requestAnimationFrame(tick);
      });

      /* auto-reset when audio ends naturally */
      if (audioEl) audioEl.addEventListener('ended', () => stop(true));
    });
  })();

  /* -----------------------------------------------
     5c. VOICE CAROUSEL — prev / next + drag
  ----------------------------------------------- */
  (function initCarousel() {
    const track   = document.getElementById('vcTrack');
    const btnPrev = document.getElementById('vcPrev');
    const btnNext = document.getElementById('vcNext');
    if (!track) return;

    const SCROLL = 304; // card 290 + gap 14

    btnNext?.addEventListener('click', () => track.scrollBy({ left:  SCROLL, behavior: 'smooth' }));
    btnPrev?.addEventListener('click', () => track.scrollBy({ left: -SCROLL, behavior: 'smooth' }));

    /* drag to scroll */
    let isDown = false, startX = 0, scrollLeft = 0;
    track.addEventListener('mousedown', e => {
      isDown = true;
      startX = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });
    document.addEventListener('mouseup',   () => { isDown = false; });
    document.addEventListener('mousemove', e => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      track.scrollLeft = scrollLeft - (x - startX) * 1.2;
    });
  })();

  /* -----------------------------------------------
     4a. ORBIT BG — rotating concentric arcs
         used on white/light sections (HIW, FAQ)
  ----------------------------------------------- */
  (function initOrbitBg() {
    document.querySelectorAll('.orbit-bg').forEach(cvs => {
      const ctx = cvs.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      let W = 0, H = 0;

      function resize() {
        W = cvs.parentElement.offsetWidth;
        H = cvs.parentElement.offsetHeight;
        cvs.width  = Math.round(W * dpr);
        cvs.height = Math.round(H * dpr);
      }
      requestAnimationFrame(resize);
      window.addEventListener('resize', resize);

      /*
       * Center sits at (W/2, H*0.88) — near the bottom.
       * Radii: W*0.4 → W*1.6, so arcs cut beautifully
       * through the section from all sides.
       */
      const RINGS = [
        { rf: 0.40, speed:  0.00022, alpha: 0.13, lw: 1.2 },
        { rf: 0.60, speed: -0.00016, alpha: 0.11, lw: 1.1 },
        { rf: 0.82, speed:  0.00012, alpha: 0.10, lw: 1.0 },
        { rf: 1.06, speed: -0.00009, alpha: 0.09, lw: 1.0 },
        { rf: 1.32, speed:  0.00007, alpha: 0.07, lw: 0.9 },
        { rf: 1.62, speed: -0.00005, alpha: 0.06, lw: 0.8 },
      ];

      const angles = RINGS.map(() => Math.random() * Math.PI * 2);
      let last = null;

      function frame(ts) {
        const dt = last ? ts - last : 16;
        last = ts;
        if (!W || !H) { requestAnimationFrame(frame); return; }

        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, W, H);

        const cx = W * 0.5;
        const cy = H * 0.88;

        RINGS.forEach((ring, i) => {
          angles[i] += ring.speed * dt;
          const r = W * ring.rf;

          ctx.save();
          ctx.translate(cx, cy);
          ctx.rotate(angles[i]);
          ctx.beginPath();
          ctx.arc(0, 0, r, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(100,110,180,${ring.alpha})`;
          ctx.lineWidth   = ring.lw;
          ctx.stroke();
          ctx.restore();
        });

        requestAnimationFrame(frame);
      }

      requestAnimationFrame(frame);
    });
  })();

  /* -----------------------------------------------
     4b. PRICING — floating Bangla letters background
  ----------------------------------------------- */
  (function initPricingBg() {
    const cvs = document.getElementById('pricingBg');
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    let W = 0, H = 0;

    function resize() {
      W = cvs.parentElement.offsetWidth;
      H = cvs.parentElement.offsetHeight;
      cvs.width  = Math.round(W * dpr);
      cvs.height = Math.round(H * dpr);
    }
    requestAnimationFrame(resize);
    window.addEventListener('resize', resize);

    const LETTERS = [
      'অ','আ','ই','ঈ','উ','ঊ','এ','ঐ','ও','ঔ',
      'ক','খ','গ','ঘ','চ','ছ','জ','ঝ','ট','ঠ',
      'ড','ঢ','ত','থ','দ','ধ','ন','প','ফ','ব',
      'ভ','ম','য','র','ল','শ','ষ','স','হ','ড়',
      'ঢ়','য়','ং','ঃ','ঁ',
    ];

    const COUNT = 38;
    const glyphs = Array.from({ length: COUNT }, (_, i) => ({
      char:    LETTERS[i % LETTERS.length],
      cx:      Math.random(),            /* anchor x */
      cy:      Math.random(),            /* anchor y */
      size:    48 + Math.random() * 72,  /* 48–120 px */
      alpha:   0.07 + Math.random() * 0.11,
      rot:     (Math.random() - 0.5) * 0.25,
      floatR:  0.018 + Math.random() * 0.030, /* float radius */
      floatSx: 0.30  + Math.random() * 0.50,  /* x oscillation speed */
      floatSy: 0.22  + Math.random() * 0.40,  /* y oscillation speed */
      phaseX:  Math.random() * Math.PI * 2,
      phaseY:  Math.random() * Math.PI * 2,
      phaseA:  Math.random() * Math.PI * 2,
    }));

    let t = 0;

    function frame() {
      t += 0.016;
      if (!W || !H) { requestAnimationFrame(frame); return; }

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      glyphs.forEach(g => {
        /* float in place — sine-wave drift around anchor, no upward drift */
        const x = (g.cx + Math.sin(t * g.floatSx + g.phaseX) * g.floatR) * W;
        const y = (g.cy + Math.sin(t * g.floatSy + g.phaseY) * g.floatR * 0.6) * H;

        const twinkle = 0.65 + 0.35 * Math.sin(t * 0.9 + g.phaseA);
        const a = g.alpha * twinkle;

        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(g.rot);
        ctx.font = `${g.size}px "Noto Sans Bengali", serif`;
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle    = `rgba(240,160,80,${a.toFixed(3)})`;
        ctx.fillText(g.char, 0, 0);
        ctx.restore();
      });

      requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
  })();

  /* -----------------------------------------------
     5b0. USE CASES — background animation
  ----------------------------------------------- */
  (function initUcBgAnimation() {
    const cvs = document.getElementById('ucBg');
    if (!cvs) return;
    const ctx = cvs.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    let W = 0, H = 0;

    function resize() {
      W = cvs.parentElement.offsetWidth;
      H = cvs.parentElement.offsetHeight;
      cvs.width  = Math.round(W * dpr);
      cvs.height = Math.round(H * dpr);
    }
    requestAnimationFrame(resize);
    window.addEventListener('resize', resize);

    /* floating particles */
    const PARTICLE_COUNT = 55;
    const COLORS = [
      [240, 120,  60],   /* orange */
      [168,  85, 255],   /* purple */
      [ 56, 189, 248],   /* cyan   */
      [240, 160,  80],   /* amber  */
      [255, 100, 120],   /* pink   */
    ];

    const particles = Array.from({ length: PARTICLE_COUNT }, () => ({
      x:     Math.random(),
      y:     Math.random(),
      r:     1.2 + Math.random() * 2.4,
      speed: 0.00008 + Math.random() * 0.00014,
      drift: (Math.random() - 0.5) * 0.00006,
      color: COLORS[Math.floor(Math.random() * COLORS.length)],
      alpha: 0.18 + Math.random() * 0.30,
      phase: Math.random() * Math.PI * 2,
    }));

    let t = 0;

    function frame() {
      t += 0.016;
      if (!W || !H) { requestAnimationFrame(frame); return; }

      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      /* top aurora glow */
      const aurora = ctx.createLinearGradient(0, 0, 0, H * 0.45);
      aurora.addColorStop(0,   'rgba(120,60,200,0.12)');
      aurora.addColorStop(0.4, 'rgba(200,80,40,0.07)');
      aurora.addColorStop(1,   'rgba(0,0,0,0)');
      ctx.fillStyle = aurora;
      ctx.fillRect(0, 0, W, H);

      /* bottom glow */
      const bot = ctx.createLinearGradient(0, H * 0.7, 0, H);
      bot.addColorStop(0, 'rgba(0,0,0,0)');
      bot.addColorStop(1, 'rgba(56,40,120,0.10)');
      ctx.fillStyle = bot;
      ctx.fillRect(0, 0, W, H);

      /* particles */
      particles.forEach(p => {
        p.y -= p.speed;
        p.x += p.drift + Math.sin(t * 0.6 + p.phase) * 0.00008;
        if (p.y < -0.02) { p.y = 1.02; p.x = Math.random(); }

        const twinkle = 0.6 + 0.4 * Math.sin(t * 1.8 + p.phase);
        const a = p.alpha * twinkle;
        const [r, g, b] = p.color;

        ctx.beginPath();
        ctx.arc(p.x * W, p.y * H, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${r},${g},${b},${a.toFixed(3)})`;
        ctx.fill();

        /* soft glow around bigger particles */
        if (p.r > 2.5) {
          ctx.beginPath();
          ctx.arc(p.x * W, p.y * H, p.r * 3, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(${r},${g},${b},${(a * 0.12).toFixed(3)})`;
          ctx.fill();
        }
      });

      requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
  })();

  /* -----------------------------------------------
     5b. USE CASES CAROUSEL
  ----------------------------------------------- */
  (function initUcCarousel() {
    const track   = document.getElementById('ucTrack');
    const btnPrev = document.getElementById('ucPrev');
    const btnNext = document.getElementById('ucNext');
    if (!track) return;

    const SCROLL = 376; // card 360 + gap 16

    btnNext?.addEventListener('click', () => track.scrollBy({ left:  SCROLL, behavior: 'smooth' }));
    btnPrev?.addEventListener('click', () => track.scrollBy({ left: -SCROLL, behavior: 'smooth' }));

    let isDown = false, startX = 0, scrollLeft = 0;
    track.addEventListener('mousedown', e => {
      isDown = true;
      startX = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });
    document.addEventListener('mouseup',   () => { isDown = false; });
    document.addEventListener('mousemove', e => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      track.scrollLeft = scrollLeft - (x - startX) * 1.2;
    });
  })();

  /* -----------------------------------------------
     5. VOICE FILTER TABS (old grid filters)
  ----------------------------------------------- */
  const filterGroups = document.querySelectorAll('[data-filter-group]');
  const voiceCards   = document.querySelectorAll('#voicesGrid .voice-card');

  // Active filter state per group
  const activeFilters = { language: 'all', style: 'all', accent: 'all' };

  filterGroups.forEach((group) => {
    const groupName = group.dataset.filterGroup;
    const tabs      = group.querySelectorAll('.ftab');

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        // Update active UI
        tabs.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');

        // Update filter state
        activeFilters[groupName] = tab.dataset.val;

        // Apply filters
        applyVoiceFilters();
      });
    });
  });

  function applyVoiceFilters() {
    let visibleCount = 0;

    voiceCards.forEach((card) => {
      const lang   = card.dataset.language || '';
      const style  = card.dataset.style    || '';
      const accent = card.dataset.accent   || '';

      const langMatch   = activeFilters.language === 'all' || lang   === activeFilters.language;
      const styleMatch  = activeFilters.style    === 'all' || style  === activeFilters.style;
      const accentMatch = activeFilters.accent   === 'all' || accent === activeFilters.accent;

      const show = langMatch && styleMatch && accentMatch;
      card.classList.toggle('hidden', !show);
      if (show) visibleCount++;
    });

    // Show "no results" message if needed
    let noResults = document.getElementById('voiceNoResults');
    if (visibleCount === 0) {
      if (!noResults) {
        noResults = document.createElement('p');
        noResults.id = 'voiceNoResults';
        noResults.style.cssText = 'grid-column: 1/-1; text-align: center; padding: 40px; color: #9ca3af; font-size: 15px;';
        noResults.textContent = 'No voices match your filters. Try a different combination.';
        document.getElementById('voicesGrid').appendChild(noResults);
      }
    } else if (noResults) {
      noResults.remove();
    }
  }

  /* -----------------------------------------------
     6. PLAY BUTTON — visual toggle
  ----------------------------------------------- */
  const playBtns = document.querySelectorAll('.play-btn');

  playBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const isPlaying = btn.classList.contains('playing');

      // Stop all other playing buttons
      playBtns.forEach((b) => {
        b.classList.remove('playing');
        b.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
        b.setAttribute('aria-label', 'Play sample');
      });

      if (!isPlaying) {
        btn.classList.add('playing');
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>';
        btn.setAttribute('aria-label', 'Pause sample');

        // Auto stop after simulated playback
        setTimeout(() => {
          btn.classList.remove('playing');
          btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
          btn.setAttribute('aria-label', 'Play sample');
        }, 4000);
      }
    });
  });

  /* -----------------------------------------------
     7. FAQ ACCORDION
  ----------------------------------------------- */
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach((item) => {
    const btn = item.querySelector('.faq-q');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all
      faqItems.forEach((fi) => fi.classList.remove('open'));

      // Open clicked (if was closed)
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  /* -----------------------------------------------
     8. SMOOTH ANCHOR SCROLL
  ----------------------------------------------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const navHeight = header ? header.offsetHeight : 0;
        const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
        window.scrollTo({ top, behavior: 'smooth' });
        closeMenu();
      }
    });
  });

  /* -----------------------------------------------
     9. HERO SOUND WAVE — Music Equalizer
  ----------------------------------------------- */
  function initHeroWave() {
    const canvas = document.getElementById('heroWave');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let rafId = null, t0 = null;

    function resize() {
      const dpr = window.devicePixelRatio || 1;
      canvas.width  = canvas.offsetWidth  * dpr;
      canvas.height = canvas.offsetHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    /* ── colour palette stops (position 0→1 across width) ── */
    const STOPS = [
      { p: 0.00, r: 255, g:  43, b: 214 }, // magenta
      { p: 0.28, r: 143, g:  77, b: 255 }, // violet
      { p: 0.50, r:  93, g:  59, b: 255 }, // deep purple
      { p: 0.72, r:  46, g: 216, b: 255 }, // electric blue
      { p: 1.00, r: 125, g: 235, b: 255 }, // cyan
    ];

    function lerpColor(t) {
      let lo = STOPS[0], hi = STOPS[STOPS.length - 1];
      for (let i = 0; i < STOPS.length - 1; i++) {
        if (t >= STOPS[i].p && t <= STOPS[i+1].p) { lo = STOPS[i]; hi = STOPS[i+1]; break; }
      }
      const f = lo.p === hi.p ? 0 : (t - lo.p) / (hi.p - lo.p);
      return [
        Math.round(lo.r + (hi.r - lo.r) * f),
        Math.round(lo.g + (hi.g - lo.g) * f),
        Math.round(lo.b + (hi.b - lo.b) * f),
      ];
    }

    const N = 130; // number of bars

    /* ── per-bar random parameters for organic motion ── */
    const cfg = Array.from({ length: N }, (_, i) => {
      const xn = i / (N - 1);
      /* mountain envelope: taller in center, shorter at edges */
      const env = 0.08 + 0.30 * Math.sin(xn * Math.PI);
      return {
        env,
        f1: 0.55 + Math.random() * 1.8,
        f2: 1.20 + Math.random() * 2.5,
        f3: 0.30 + Math.random() * 1.2,
        p1: Math.random() * Math.PI * 2,
        p2: Math.random() * Math.PI * 2,
        p3: Math.random() * Math.PI * 2,
        /* occasional "beat spike" probability */
        spike: Math.random() < 0.18,
        spF:   1.8 + Math.random() * 2.4,
        spP:   Math.random() * Math.PI * 2,
      };
    });

    const SPD = 0.55; // speed multiplier — reduce for calmer motion

    /* ── bar height at time t ── */
    function barH(c, t, H) {
      const st = t * SPD;
      const dyn =
        0.50 * Math.abs(Math.sin(st * c.f1 + c.p1)) +
        0.32 * Math.abs(Math.sin(st * c.f2 + c.p2)) +
        0.18 * Math.abs(Math.sin(st * c.f3 + c.p3));
      /* occasional sharp spike */
      const spk = c.spike ? 0.18 * Math.pow(Math.max(0, Math.sin(st * c.spF + c.spP)), 6) : 0;
      return H * (c.env * dyn + spk);
    }

    function draw(ts) {
      if (!t0) t0 = ts;
      const t  = (ts - t0) * 0.001;
      const W  = canvas.offsetWidth;
      const H  = canvas.offsetHeight;
      ctx.clearRect(0, 0, W, H);

      const CY   = H * 0.52;         // slightly above true center
      const slot = W / N;
      const gap  = Math.max(1.5, slot * 0.22);
      const bw   = slot - gap;
      const r    = Math.min(bw / 2, 4); // rounded-cap radius

      /* global beat pulse */
      const beat = 0.80 + 0.20 * Math.abs(Math.sin(t * SPD * 2.1));

      /* ── draw bars ── */
      cfg.forEach((c, i) => {
        const xn = i / (N - 1);
        const x  = i * slot + gap * 0.5;
        const h  = barH(c, t, H) * beat;

        const [cr, cg, cb] = lerpColor(xn);
        const hex = `rgb(${cr},${cg},${cb})`;

        /* ── upper bar ── */
        const topY = CY - h;

        // fill gradient (transparent base → vivid tip)
        const ug = ctx.createLinearGradient(x, CY, x, topY);
        ug.addColorStop(0,   `rgba(${cr},${cg},${cb},0.08)`);
        ug.addColorStop(0.55,`rgba(${cr},${cg},${cb},0.55)`);
        ug.addColorStop(1,   `rgba(${cr},${cg},${cb},0.92)`);
        ctx.fillStyle = ug;

        // glow on tall bars
        const glowIntensity = Math.min(20, h / H * 60);
        ctx.shadowColor = hex;
        ctx.shadowBlur  = glowIntensity;

        // rounded-top rectangle
        ctx.beginPath();
        if (h > r * 2) {
          ctx.moveTo(x, CY);
          ctx.lineTo(x, topY + r);
          ctx.quadraticCurveTo(x, topY, x + r, topY);
          ctx.lineTo(x + bw - r, topY);
          ctx.quadraticCurveTo(x + bw, topY, x + bw, topY + r);
          ctx.lineTo(x + bw, CY);
        } else {
          ctx.rect(x, topY, bw, h);
        }
        ctx.closePath();
        ctx.fill();

        /* ── mirror reflection (below center, faded) ── */
        ctx.shadowBlur = 0;
        const rh = h * 0.45;
        const botY = CY + rh;
        const mg = ctx.createLinearGradient(x, CY, x, botY);
        mg.addColorStop(0,   `rgba(${cr},${cg},${cb},0.18)`);
        mg.addColorStop(1,   `rgba(${cr},${cg},${cb},0.00)`);
        ctx.fillStyle = mg;
        ctx.beginPath();
        ctx.rect(x, CY, bw, rh);
        ctx.fill();
      });

      ctx.shadowBlur = 0;

      /* ── thin luminous center line ── */
      const cl = ctx.createLinearGradient(0, 0, W, 0);
      STOPS.forEach(s => cl.addColorStop(s.p, `rgba(${s.r},${s.g},${s.b},0.55)`));
      ctx.shadowColor = '#7DEBFF';
      ctx.shadowBlur  = 10;
      ctx.beginPath();
      ctx.moveTo(0, CY); ctx.lineTo(W, CY);
      ctx.strokeStyle = cl;
      ctx.lineWidth   = 1;
      ctx.stroke();
      ctx.shadowBlur  = 0;

      rafId = requestAnimationFrame(draw);
    }

    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting) {
          if (!rafId) rafId = requestAnimationFrame(draw);
        } else {
          if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
        }
      }, { threshold: 0 });
      io.observe(canvas);
    } else {
      rafId = requestAnimationFrame(draw);
    }
  }

  initHeroWave();

  /* -----------------------------------------------
     10. INTERSECTION OBSERVER — fade in sections
  ----------------------------------------------- */
  const animTargets = document.querySelectorAll(
    '.feature-card, .usecase-card, .voice-card, .hiw-step, .faq-item, .stat-item'
  );

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );

    animTargets.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity 0.4s ease ${(i % 6) * 0.07}s, transform 0.4s ease ${(i % 6) * 0.07}s`;
      io.observe(el);
    });
  }

})();
