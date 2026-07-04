(function () {
  function initLucide() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
  }

  function enhanceHeader() {
    const header = document.getElementById('header');
    if (!header || document.querySelector('.acsol-admin-search')) return;
    const sidebarToggle = document.createElement('button');
    sidebarToggle.type = 'button';
    sidebarToggle.className = 'acsol-sidebar-toggle';
    sidebarToggle.innerHTML = '<i data-lucide="panel-left-close"></i>';
    sidebarToggle.setAttribute('aria-label', 'Recolher menu');
    sidebarToggle.addEventListener('click', () => {
      document.body.classList.toggle('acsol-sidebar-collapsed');
      localStorage.setItem('acsolSidebarCollapsed', document.body.classList.contains('acsol-sidebar-collapsed') ? '1' : '0');
      setTimeout(initLucide, 0);
    });
    header.prepend(sidebarToggle);

    const search = document.createElement('div');
    search.className = 'acsol-admin-search';
    search.innerHTML = '<i data-lucide="search"></i><input type="search" placeholder="Pesquisar no painel..." aria-label="Pesquisar no painel"><kbd>Ctrl K</kbd>';
    const userTools = document.getElementById('user-tools');
    header.insertBefore(search, userTools || null);

    const themeButton = document.createElement('button');
    themeButton.type = 'button';
    themeButton.className = 'acsol-theme-toggle';
    themeButton.innerHTML = '<i data-lucide="moon"></i>';
    themeButton.setAttribute('aria-label', 'Alternar modo claro e escuro');
    themeButton.addEventListener('click', () => {
      const next = document.documentElement.dataset.acsolTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.acsolTheme = next;
      localStorage.setItem('acsolTheme', next);
      themeButton.innerHTML = next === 'dark' ? '<i data-lucide="sun"></i>' : '<i data-lucide="moon"></i>';
      setTimeout(initLucide, 0);
    });
    header.appendChild(themeButton);
  }

  function enhanceSidebar() {
    const sidebar = document.getElementById('nav-sidebar');
    if (!sidebar) return;
    const iconMap = [
      ['Utilizadores', 'users-round'],
      ['Grupos', 'shield-check'],
      ['Doacoes', 'gift'],
      ['Doacoes em especie', 'package-check'],
      ['Candidaturas', 'heart-handshake'],
      ['Projetos', 'folder-kanban'],
      ['Noticias', 'newspaper'],
      ['Galeria', 'images'],
      ['Equipa', 'badge-user'],
      ['Divisoes', 'map-pin'],
      ['Chatbot', 'bot'],
      ['Configuracao', 'settings'],
      ['Flyers', 'image'],
      ['FAQ', 'circle-help'],
      ['Parceiros', 'handshake'],
      ['Mensagens', 'mail'],
      ['Newsletter', 'send'],
      ['Historico', 'history'],
      ['Notificacoes', 'bell']
    ];

    sidebar.querySelectorAll('a').forEach(link => {
      if (link.querySelector('svg') || link.querySelector('i[data-lucide]')) return;
      const label = link.textContent.trim();
      const match = iconMap.find(([text]) => label.toLowerCase().includes(text.toLowerCase()));
      if (!match) return;
      const icon = document.createElement('i');
      icon.setAttribute('data-lucide', match[1]);
      icon.className = 'acsol-nav-icon';
      link.prepend(icon);
    });
  }

  function bindShortcut() {
    document.addEventListener('keydown', event => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
        const input = document.querySelector('.acsol-admin-search input') || document.getElementById('nav-filter') || document.querySelector('#toolbar input[type="text"]');
        if (input) {
          event.preventDefault();
          input.focus();
        }
      }
    });
  }

  function restorePreferences() {
    if (localStorage.getItem('acsolSidebarCollapsed') === '1') {
      document.body.classList.add('acsol-sidebar-collapsed');
    }
    const theme = localStorage.getItem('acsolTheme') || 'light';
    document.documentElement.dataset.acsolTheme = theme;
  }

  function renderChart() {
    const el = document.getElementById('acsol-admin-chart');
    if (!el || !window.ApexCharts || el.dataset.rendered) return;
    el.dataset.rendered = '1';
    const chart = new window.ApexCharts(el, {
      chart: { type: 'area', height: 180, toolbar: { show: false }, sparkline: { enabled: false }, fontFamily: 'Inter, sans-serif' },
      series: [{ name: 'Atividade', data: [18, 28, 24, 42, 36, 58, 52, 68, 74, 86, 78, 96] }],
      colors: ['#2563EB'],
      stroke: { curve: 'smooth', width: 3 },
      fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.26, opacityTo: 0.02, stops: [0, 95, 100] } },
      dataLabels: { enabled: false },
      grid: { borderColor: '#E2E8F0', strokeDashArray: 4 },
      xaxis: { categories: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], labels: { style: { colors: '#64748B' } } },
      yaxis: { labels: { style: { colors: '#64748B' } } },
      tooltip: { theme: 'light' }
    });
    chart.render();
  }

  document.addEventListener('DOMContentLoaded', () => {
    restorePreferences();
    enhanceHeader();
    enhanceSidebar();
    bindShortcut();
    renderChart();
    initLucide();
    setTimeout(initLucide, 250);
    setTimeout(renderChart, 350);
  });
})();
