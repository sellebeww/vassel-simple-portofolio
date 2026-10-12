(() => {
  'use strict';

  const stage = document.querySelector('#stage');
  const menu = document.querySelector('.menu-toggle');
  const panel = document.querySelector('#menu-panel');
  const navigation = document.querySelector('#navigation');
  const sections = [...document.querySelectorAll('main > section')];
  const links = [...document.querySelectorAll('.side-nav a, .outer-nav a')];
  const previous = document.querySelector('#previous-section');
  const next = document.querySelector('#next-section');
  let activeIndex = 0;
  let lastNavigation = 0;
  document.body.classList.add('app-ready');
  menu.hidden = false;
  document.querySelector('.section-controls').hidden = false;
  sections.forEach(section => section.tabIndex = -1);

  function closeMenu(restoreFocus = true) {
    panel.hidden = true;
    stage.inert = false;
    document.body.classList.remove('menu-open');
    menu.setAttribute('aria-expanded', 'false');
    if (restoreFocus) menu.focus();
  }

  function showSection(target, { focus = false, history = false } = {}) {
    const section = target?.matches('main > section') ? target : target?.closest('main > section');
    const index = sections.indexOf(section);
    if (index < 0) return;
    activeIndex = index;
    sections.forEach(item => { item.hidden = item !== section; });
    const hash = '#' + section.id;
    links.forEach(link => {
      if (link.hash === hash) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    previous.disabled = index === 0;
    next.disabled = index === sections.length - 1;
    const title = navigation.querySelector(`[href="${hash}"]`).textContent;
    document.querySelector('#section-position').textContent = `${String(index + 1).padStart(2, '0')} / ${String(sections.length).padStart(2, '0')} — ${title}`;
    document.querySelector('.header-cta').hidden = section.id === 'home';
    document.title = `${title} — Vassel Goleyu`;
    if (history && location.hash !== '#' + target.id) window.history.pushState(null, '', '#' + target.id);
    setPressure(0);
    if (target === section) section.scrollTop = 0;
    else scrollToTarget(section, target);
    if (focus) section.focus({ preventScroll: true });
    if (target.id === 'chat') focusChat(target);
    lastNavigation = performance.now();
  }

  // Scroll a nested target (e.g. the Chat form) inside its section's own scroll container.
  function scrollToTarget(section, target) {
    const offset = target.getBoundingClientRect().top - section.getBoundingClientRect().top + section.scrollTop;
    section.scrollTop = Math.max(0, offset - 20);
  }

  function focusChat(chat) {
    const field = chat.querySelector('#name');
    chat.classList.remove('chat-highlight');
    void chat.offsetWidth;
    chat.classList.add('chat-highlight');
    // Wait for the chapter animation to finish so focus never fights the scroll position.
    setTimeout(() => {
      if (sections[activeIndex].contains(chat)) {
        field.focus({ preventScroll: true });
        scrollToTarget(sections[activeIndex], chat);
      }
    }, 380);
  }

  // Extra "pressure" needed at a section's edge before moving on, so a stray scroll never changes chapter.
  const pressureBar = document.querySelector('.pressure');
  let pressureTimer;
  function setPressure(value) {
    pressureBar.style.setProperty('--p', Math.min(1, value));
    pressureBar.classList.toggle('on', value > 0);
    clearTimeout(pressureTimer);
    if (value > 0) pressureTimer = setTimeout(() => setPressure(0), 900);
  }

  function followHash() {
    const id = location.hash.slice(1);
    const target = document.getElementById(id) || sections[0];
    if (!panel.hidden) closeMenu(false);
    showSection(target.closest('main > section') ? target : sections[0]);
  }
  function step(direction) {
    const section = sections[activeIndex + direction];
    if (section) {
      showSection(section, { history: true, focus: true });
      if (direction < 0) section.scrollTop = section.scrollHeight;
    }
  }
  previous.addEventListener('click', () => step(-1));
  next.addEventListener('click', () => step(1));
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href^="#"]');
    if (!anchor || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = document.getElementById(anchor.hash.slice(1));
    if (!target) return;
    if (target.id === 'main') {
      event.preventDefault();
      sections[activeIndex].focus();
      return;
    }
    if (!target.closest('main > section')) return;
    event.preventDefault();
    if (!panel.hidden) closeMenu(false);
    showSection(target, { focus: true, history: true });
  });
  menu.addEventListener('click', () => {
    panel.hidden = false;
    stage.inert = true;
    document.body.classList.add('menu-open');
    menu.setAttribute('aria-expanded', 'true');
    (navigation.querySelector('[aria-current]') || navigation.querySelector('a')).focus();
  });
  document.querySelector('.menu-close').addEventListener('click', () => closeMenu());
  document.querySelector('.menu-backdrop').addEventListener('click', () => closeMenu());
  const isInteractive = target => target.closest('input, textarea, select, button, a, summary, [contenteditable="true"], dialog');
  const atBoundary = (section, direction) => direction > 0
    ? section.scrollTop + section.clientHeight >= section.scrollHeight - 2
    : section.scrollTop <= 2;
  let keyArmed = 0;
  let keyTimer;
  document.addEventListener('keydown', event => {
    if (!panel.hidden) {
      if (event.key === 'Escape') { event.preventDefault(); closeMenu(); }
      if (event.key === 'Tab') {
        const focusable = [...panel.querySelectorAll('button, a')];
        const first = focusable[0], last = focusable.at(-1);
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
      return;
    }
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || isInteractive(event.target)) return;
    const direction = ['ArrowDown', 'ArrowRight', 'PageDown'].includes(event.key) ? 1 : ['ArrowUp', 'ArrowLeft', 'PageUp'].includes(event.key) ? -1 : 0;
    if (!direction) return;
    const section = sections[activeIndex];
    if (!['ArrowRight', 'ArrowLeft'].includes(event.key) && !atBoundary(section, direction)) return;
    event.preventDefault();
    if (event.repeat || performance.now() - lastNavigation < 500) return;
    // Arrow left/right jump directly; at a section's edge, up/down/page keys need a second press.
    if (['ArrowRight', 'ArrowLeft'].includes(event.key)) { step(direction); return; }
    if (keyArmed === direction) { keyArmed = 0; step(direction); return; }
    keyArmed = direction;
    setPressure(0.5);
    clearTimeout(keyTimer);
    keyTimer = setTimeout(() => { keyArmed = 0; }, 1500);
  });
  const WHEEL_PRESSURE = 480;
  let wheelPressure = 0;
  let wheelDirection = 0;
  let wheelTime = 0;
  let settling = false;
  document.addEventListener('wheel', event => {
    if (!panel.hidden || document.querySelector('dialog[open]') || event.ctrlKey || event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (Math.abs(event.deltaX) >= Math.abs(event.deltaY)) return;
    const section = sections[activeIndex];
    const delta = event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? section.clientHeight : 1);
    const direction = Math.sign(delta);
    const now = performance.now();
    event.preventDefault();
    if (now - lastNavigation < 400) { wheelTime = now; return; }
    // A pause between wheel events means a new gesture; momentum from the previous one is over.
    if (now - wheelTime > 140) settling = false;
    if (direction !== wheelDirection || now - wheelTime > 600) wheelPressure = 0;
    wheelDirection = direction;
    wheelTime = now;
    if (!atBoundary(section, direction)) {
      section.scrollTop += delta;
      wheelPressure = 0;
      setPressure(0);
      // Reaching the edge mid-gesture never counts; the user has to keep scrolling in a fresh push.
      settling = atBoundary(section, direction);
      return;
    }
    if (settling) return;
    wheelPressure += Math.abs(delta);
    setPressure(wheelPressure / WHEEL_PRESSURE);
    if (wheelPressure >= WHEEL_PRESSURE) {
      wheelPressure = 0;
      step(direction);
    }
  }, { passive: false });
  let touchStart;
  stage.addEventListener('touchstart', event => {
    const section = sections[activeIndex];
    touchStart = event.touches.length === 1 && !event.target.closest('input, textarea, select, [contenteditable="true"], dialog')
      ? { x: event.touches[0].clientX, y: event.touches[0].clientY, section: activeIndex,
        top: atBoundary(section, -1), bottom: atBoundary(section, 1) } : null;
  }, { passive: true });
  stage.addEventListener('touchend', event => {
    if (!touchStart || !panel.hidden) return;
    const deltaX = event.changedTouches[0].clientX - touchStart.x;
    const deltaY = event.changedTouches[0].clientY - touchStart.y;
    const direction = deltaY < 0 ? 1 : -1;
    // The swipe must begin at the edge, so scrolling to the end never flows straight into the next chapter.
    const startedAtEdge = direction > 0 ? touchStart.bottom : touchStart.top;
    if (touchStart.section === activeIndex && startedAtEdge && Math.abs(deltaY) > 110 && Math.abs(deltaY) > Math.abs(deltaX) * 1.5 && atBoundary(sections[activeIndex], direction) && performance.now() - lastNavigation > 400) step(direction);
    touchStart = null;
  }, { passive: true });
  stage.addEventListener('touchcancel', () => { touchStart = null; }, { passive: true });
  window.addEventListener('hashchange', followHash);
  window.addEventListener('popstate', followHash);
  followHash();

  const search = document.querySelector('#project-search');
  const cards = [...document.querySelectorAll('[data-project]')];
  document.querySelector('.project-search').hidden = false;
  function filterProjects() {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    cards.forEach((card) => {
      card.hidden = !terms.every((term) => card.dataset.search.includes(term));
      if (!card.hidden) visible += 1;
    });
    document.querySelector('#project-count').textContent = `${visible} of ${cards.length} repositories`;
    document.querySelector('#no-results').hidden = visible !== 0;
    document.querySelector('.archive-heading').hidden = !document.querySelector('.repo-card:not([hidden])');
  }
  search.addEventListener('input', filterProjects);
  filterProjects();

  const dialog = document.querySelector('#image-dialog');
  const dialogImage = dialog.querySelector('img');
  let imageOpener;
  document.querySelectorAll('[data-lightbox]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || typeof dialog.showModal !== 'function') return;
      event.preventDefault();
      imageOpener = anchor;
      dialogImage.src = anchor.href;
      dialogImage.alt = anchor.querySelector('img').alt;
      dialog.querySelector('p').textContent = dialogImage.alt;
      dialog.showModal();
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => imageOpener?.focus());

  const form = document.querySelector('#contact-form');
  form.querySelector('button').disabled = false;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const fields = new FormData(form);
    const name = fields.get('name').trim();
    const message = fields.get('message').trim();
    if (!name || !message) {
      document.querySelector('#contact-status').textContent = 'Please enter your name and a message.';
      return;
    }
    const subject = `Portfolio enquiry from ${name}`;
    const body = `Hi Vassel,\n\n${message}\n\nFrom: ${name}\nEmail: ${fields.get('email')}`;
    const recipient = document.querySelector('.contact-email').getAttribute('href');
    window.location.href = `${recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    document.querySelector('#contact-status').textContent = 'Email draft requested. If your email app did not open, use the email or WhatsApp link. Your message has not been sent by this website.';
  });
})();
