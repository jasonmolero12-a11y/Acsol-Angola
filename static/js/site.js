// ── SECTION NAVIGATION ──────────────────────
  function showSection(id) {
    document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
    document.getElementById('section-' + id).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Update nav active state
    document.querySelectorAll('.nav-link-custom').forEach(l => l.classList.remove('active'));
    const navLinks = {
      home: 0, about: 1, projects: 2, news: 3,
      gallery: 4, videos: 5, divisions: 6, volunteer: 7, partners: 8, faq: 9, contact: 10
    };
    const links = document.querySelectorAll('.nav-link-custom');
    if (navLinks[id] !== undefined) links[navLinks[id]].classList.add('active');

    // Close mobile menu
    const navCollapse = document.getElementById('navMenu');
    if (navCollapse.classList.contains('show')) {
      new bootstrap.Collapse(navCollapse).hide();
    }
  }

  // ── NAVBAR SCROLL ────────────────────────────
  window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 60) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');

    const btn = document.getElementById('back-to-top');
    if (window.scrollY > 400) btn.classList.add('visible');
    else btn.classList.remove('visible');
  });

  // ── COUNTER ANIMATION ────────────────────────
  function animateCounters() {
    document.querySelectorAll('.counter').forEach(counter => {
      const target = parseInt(counter.getAttribute('data-target'));
      const duration = 2000;
      const step = target / (duration / 16);
      let current = 0;
      const timer = setInterval(() => {
        current += step;
        if (current >= target) { counter.textContent = target.toLocaleString('pt-PT'); clearInterval(timer); }
        else counter.textContent = Math.floor(current).toLocaleString('pt-PT');
      }, 16);
    });
  }
  const statsObs = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { animateCounters(); statsObs.disconnect(); } });
  }, { threshold: 0.3 });
  const statsSection = document.getElementById('stats-section');
  if (statsSection) statsObs.observe(statsSection);

  // ── PROJECT FILTER ───────────────────────────
  function filterProjects(cat, btn) {
    document.querySelectorAll('#section-projects .filter-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.project-item').forEach(item => {
      if (cat === 'todos' || item.getAttribute('data-cat') === cat) {
        item.style.display = '';
        item.style.animation = 'fadeIn 0.4s ease';
      } else {
        item.style.display = 'none';
      }
    });
  }

  function filterGalleryPhotos(cat, btn) {
    document.querySelectorAll('#section-gallery .filter-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('#section-gallery .gallery-photo-item').forEach(item => {
      item.style.display = cat === 'todos' || item.getAttribute('data-gallery-cat') === cat ? '' : 'none';
    });
  }

  // ── LIGHTBOX ─────────────────────────────────
  function openLightbox(src) {
    const lb = document.getElementById('lightbox');
    document.getElementById('lightbox-img').src = src;
    lb.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('open');
    document.body.style.overflow = '';
  }
  document.getElementById('lightbox').addEventListener('click', function(e) {
    if (e.target === this) closeLightbox();
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });

  // ── FORMS ────────────────────────────────────
  async function submitAjaxForm(form, successMessage) {
    const data = new FormData(form);
    const response = await fetch(form.action, {
      method: 'POST',
      body: data,
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    let result = {};
    try {
      result = await response.json();
    } catch (error) {
      result = {};
    }
    if (!response.ok || result.ok === false) {
      throw new Error(result.message || 'Erro ao enviar formulario');
    }
    const toastMessage = result.reference ? `${result.message || successMessage} Referencia: ${result.reference}` : (result.message || successMessage);
    showToast(toastMessage, 'success');
    if (form.classList.contains('donation-form') && result.instructions) {
      const box = document.getElementById('donation-instructions');
      box.hidden = false;
      box.textContent = `Referencia: ${result.reference || 'ACSOL-DOA'}\n\n${result.instructions}`;
    }
    form.reset();
  }

  document.querySelectorAll('form.ajax-form').forEach(form => {
    form.addEventListener('submit', async event => {
      event.preventDefault();
      try {
        await submitAjaxForm(form, 'Pedido enviado com sucesso.');
      } catch (error) {
        showToast(error.message || 'Por favor, verifique os dados e tente novamente.', 'error');
      }
    });
  });

  async function loadDonationInstructions(select) {
    const box = document.getElementById('donation-instructions');
    if (!box || !select.dataset.instructionsUrl) return;
    try {
      const url = `${select.dataset.instructionsUrl}?tipo=${encodeURIComponent(select.value)}`;
      const response = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
      if (!response.ok) throw new Error('Erro ao carregar instrucoes');
      const result = await response.json();
      box.hidden = false;
      if (result.available === false) {
        box.classList.add('is-unavailable');
      } else {
        box.classList.remove('is-unavailable');
      }
      box.textContent = result.instructions || 'As instrucoes deste tipo de doacao serao enviadas pela equipa da ACSOL.';
    } catch (error) {
      box.hidden = false;
      box.textContent = 'Nao foi possivel carregar as instrucoes agora. A equipa enviara os dados de pagamento apos o registo.';
    }
  }

  const donationTypeSelect = document.querySelector('.donation-form select[name="tipo"]');
  if (donationTypeSelect) {
    donationTypeSelect.addEventListener('change', () => loadDonationInstructions(donationTypeSelect));
    loadDonationInstructions(donationTypeSelect);
  }

  function subscribeNewsletter() {
    const input = document.querySelector('footer input[type="email"]');
    if (input.value && input.value.includes('@')) {
      const data = new FormData();
      data.append('email', input.value);
      data.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
      fetch('/newsletter/', {
        method: 'POST',
        body: data,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      }).then(response => {
        if (!response.ok) throw new Error('Erro ao subscrever');
        showToast('Subscrito com sucesso. Bem-vindo à nossa newsletter.', 'success');
        input.value = '';
      }).catch(() => showToast('Por favor, introduza um email valido.', 'error'));
    } else {
      showToast('Por favor, introduza um email valido.', 'error');
    }
  }

  // ── COPY IBAN ────────────────────────────────
  function copyIBAN(el) {
    const text = el.textContent.trim();
    navigator.clipboard.writeText(text).then(() => {
      showToast('📋 Copiado para a área de transferência!', 'success');
    });
  }

  // ── DONATION AMOUNTS ─────────────────────────
  function setAmount(btn, val) {
    document.getElementById('donation-amount').value = val;
    document.querySelectorAll('#section-donations .filter-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
  }

  // ── CHATBOT ─────────────────────────────────
  function toggleChatbot() {
    const panel = document.getElementById('chatbot-panel');
    panel.hidden = !panel.hidden;
  }

  function addChatbotMessage(text, type) {
    const messages = document.getElementById('chatbot-messages');
    const item = document.createElement('div');
    item.className = `chatbot-message ${type}`;
    item.textContent = text;
    messages.appendChild(item);
    messages.scrollTop = messages.scrollHeight;
    return item;
  }

  const chatbotForm = document.getElementById('chatbot-form');
  let chatbotVoiceEnabled = true;
  const chatbotVoiceToggle = document.getElementById('chatbot-voice-toggle');
  const chatbotVoiceStop = document.getElementById('chatbot-voice-stop');
  if (chatbotVoiceToggle) {
    chatbotVoiceToggle.addEventListener('click', () => {
      chatbotVoiceEnabled = !chatbotVoiceEnabled;
      chatbotVoiceToggle.classList.toggle('chatbot-voice-on', chatbotVoiceEnabled);
      chatbotVoiceToggle.innerHTML = chatbotVoiceEnabled ? '<i class="bi bi-volume-up"></i>' : '<i class="bi bi-volume-mute"></i>';
    });
  }
  if (chatbotVoiceStop) {
    chatbotVoiceStop.addEventListener('click', () => {
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    });
  }

  function cleanChatbotText(text) {
    return String(text || '')
      .replace(/[`*_#~>|{}\[\]\\]/g, '')
      .replace(/[•●▪▫]/g, '-')
      .replace(/[^\S\r\n]{2,}/g, ' ')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  function speakChatbotAnswer(text, lang) {
    if (!chatbotVoiceEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang || 'pt-PT';
    utterance.rate = 0.96;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  if (chatbotForm) {
    chatbotForm.addEventListener('submit', async event => {
      event.preventDefault();
      const input = chatbotForm.querySelector('input[name="message"]');
      const text = input.value.trim();
      if (!text) return;
      addChatbotMessage(text, 'user');
      input.value = '';
      const waiting = addChatbotMessage('A responder...', 'bot');
      try {
        const data = new FormData(chatbotForm);
        data.set('message', text);
        const response = await fetch(chatbotForm.action, {
          method: 'POST',
          body: data,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (!response.ok) throw new Error('Erro no chatbot');
        const result = await response.json();
        const answer = cleanChatbotText(result.answer || 'Nao consegui responder agora.');
        waiting.textContent = answer;
        if (result.voice !== false) speakChatbotAnswer(answer, result.voice_lang);
      } catch (error) {
        waiting.textContent = 'Nao consegui responder agora. Tente novamente mais tarde.';
      }
    });
  }

  // ── TOAST ────────────────────────────────────
  function showToast(msg, type) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast-custom';
    toast.style.background = type === 'success' ? '#065f46' : type === 'error' ? '#991b1b' : '#1A3E6F';
    toast.innerHTML = msg;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(60px)'; toast.style.transition = 'all 0.4s'; setTimeout(() => toast.remove(), 400); }, 4000);
  }

  // ── INIT ─────────────────────────────────────
  // Make navbar always visible on page load
  document.getElementById('navbar').classList.add('scrolled');
  setTimeout(() => {
    if (window.scrollY < 60) document.getElementById('navbar').classList.remove('scrolled');
  }, 100);
