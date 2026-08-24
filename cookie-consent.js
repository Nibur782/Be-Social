/**
 * Cookie consent + Google Consent Mode v2 - dawidrubin.pl
 * Banner UI. Domyslne stany zgod ustawia inline stub w <head> (przed GTM).
 * Polskie znaki zapisane jako \uXXXX - dziala niezaleznie od naglowka charset serwera.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'drConsent';
  var POLICY_URL = '/polityka-prywatnosci';

  // Polskie znaki
  var a_ = '\u0105', c_ = '\u0107', e_ = '\u0119', l_ = '\u0142',
      n_ = '\u0144', o_ = '\u00f3', s_ = '\u015b', z_ = '\u017c', zx = '\u017a';

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function saveConsent(analytics, ads) {
    var data = { analytics: !!analytics, ads: !!ads, ts: new Date().toISOString(), v: 1 };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) {}
    applyConsent(data);
    return data;
  }

  function applyConsent(c) {
    if (typeof window.gtag !== 'function') {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
    }
    window.gtag('consent', 'update', {
      ad_storage: c.ads ? 'granted' : 'denied',
      ad_user_data: c.ads ? 'granted' : 'denied',
      ad_personalization: c.ads ? 'granted' : 'denied',
      analytics_storage: c.analytics ? 'granted' : 'denied'
    });
    window.gtag('set', 'ads_data_redaction', !c.ads);
    window.dataLayer.push({
      event: 'consent_update',
      consent_analytics: c.analytics ? 'granted' : 'denied',
      consent_ads: c.ads ? 'granted' : 'denied'
    });
  }

  // ---------- UI ----------

  var BANNER_HTML =
    '<div id="dr-cookie-banner" role="dialog" aria-modal="false" aria-labelledby="dr-cc-title" ' +
    'class="fixed bottom-0 left-0 right-0 z-[9999] p-4 sm:p-6" style="display:none">' +
      '<div class="max-w-5xl mx-auto bg-slate-900 text-white rounded-2xl shadow-2xl border border-white/10 p-5 sm:p-6">' +
        '<div class="flex flex-col lg:flex-row lg:items-center gap-5">' +
          '<div class="flex-1">' +
            '<h2 id="dr-cc-title" class="text-base font-bold mb-1.5">Ta strona u' + z_ + 'ywa plik' + o_ + 'w cookie</h2>' +
            '<p class="text-sm text-slate-300 leading-relaxed">' +
              'Niezb' + e_ + 'dne pliki cookie s' + a_ + ' wymagane do dzia' + l_ + 'ania strony. ' +
              'Analityczne i marketingowe uruchamiam dopiero za Twoj' + a_ + ' zgod' + a_ + ' - ' +
              'pomagaj' + a_ + ' mi zrozumie' + c_ + ' ruch i mierzy' + c_ + ' skuteczno' + s_ + c_ + ' kampanii. ' +
              '<a href="' + POLICY_URL + '" class="text-blue-300 hover:text-blue-200 underline underline-offset-2">Polityka prywatno' + s_ + 'ci</a>' +
            '</p>' +
          '</div>' +
          '<div class="flex flex-col sm:flex-row gap-2 lg:flex-shrink-0">' +
            '<button type="button" data-dr-cc="settings" class="px-5 py-2.5 rounded-full text-sm font-semibold border border-white/25 hover:bg-white/10 transition-colors order-3 sm:order-1">Ustawienia</button>' +
            '<button type="button" data-dr-cc="reject" class="px-5 py-2.5 rounded-full text-sm font-semibold border border-white/25 hover:bg-white/10 transition-colors order-2">Tylko niezb' + e_ + 'dne</button>' +
            '<button type="button" data-dr-cc="accept" class="px-5 py-2.5 rounded-full text-sm font-bold bg-blue-600 hover:bg-blue-700 transition-colors order-1 sm:order-3">Akceptuj' + e_ + ' wszystkie</button>' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>';

  var MODAL_HTML =
    '<div id="dr-cookie-modal" role="dialog" aria-modal="true" aria-labelledby="dr-cm-title" ' +
    'class="fixed inset-0 z-[10000] items-center justify-center p-4" style="display:none">' +
      '<div data-dr-cc="backdrop" class="absolute inset-0 bg-slate-900/70 backdrop-blur-sm"></div>' +
      '<div class="relative bg-white rounded-3xl shadow-2xl max-w-lg w-full max-h-[85vh] overflow-y-auto">' +
        '<div class="p-6 sm:p-8">' +
          '<h2 id="dr-cm-title" class="text-2xl font-bold mb-2 text-slate-900">Ustawienia prywatno' + s_ + 'ci</h2>' +
          '<p class="text-sm text-slate-600 mb-6 leading-relaxed">Zdecyduj, kt' + o_ + 're pliki cookie mog' + e_ + ' u' + z_ + 'ywa' + c_ + '. Zgod' + e_ + ' mo' + z_ + 'esz zmieni' + c_ + ' w ka' + z_ + 'dej chwili.</p>' +

          '<div class="space-y-3 mb-6">' +
            '<div class="border border-gray-200 rounded-2xl p-4 bg-slate-50">' +
              '<div class="flex items-start justify-between gap-4">' +
                '<div>' +
                  '<div class="font-bold text-slate-900 text-sm">Niezb' + e_ + 'dne</div>' +
                  '<p class="text-xs text-slate-600 mt-1 leading-relaxed">Podstawowe dzia' + l_ + 'anie strony, bezpiecze' + n_ + 'stwo, zapami' + e_ + 'tanie Twojego wyboru cookie. Zawsze aktywne.</p>' +
                '</div>' +
                '<span class="text-xs font-bold text-slate-500 bg-gray-200 px-3 py-1 rounded-full flex-shrink-0 mt-0.5">Zawsze</span>' +
              '</div>' +
            '</div>' +

            '<label class="block border border-gray-200 rounded-2xl p-4 cursor-pointer hover:border-blue-300 transition-colors">' +
              '<div class="flex items-start justify-between gap-4">' +
                '<div>' +
                  '<div class="font-bold text-slate-900 text-sm">Analityczne</div>' +
                  '<p class="text-xs text-slate-600 mt-1 leading-relaxed">Google Analytics 4 - liczba odwiedzin, ' + zx + 'r' + o_ + 'd' + l_ + 'a ruchu, popularne podstrony. Dane zagregowane, bez identyfikacji osoby.</p>' +
                '</div>' +
                '<input type="checkbox" id="dr-cc-analytics" class="mt-1 w-5 h-5 accent-blue-600 flex-shrink-0 cursor-pointer">' +
              '</div>' +
            '</label>' +

            '<label class="block border border-gray-200 rounded-2xl p-4 cursor-pointer hover:border-blue-300 transition-colors">' +
              '<div class="flex items-start justify-between gap-4">' +
                '<div>' +
                  '<div class="font-bold text-slate-900 text-sm">Marketingowe</div>' +
                  '<p class="text-xs text-slate-600 mt-1 leading-relaxed">Google Ads i Meta Ads - mierzenie skuteczno' + s_ + 'ci reklam i dopasowanie przekazu. Bez zgody reklamy nadal si' + e_ + ' wy' + s_ + 'wietlaj' + a_ + ', ale s' + a_ + ' mniej trafne.</p>' +
                '</div>' +
                '<input type="checkbox" id="dr-cc-ads" class="mt-1 w-5 h-5 accent-blue-600 flex-shrink-0 cursor-pointer">' +
              '</div>' +
            '</label>' +
          '</div>' +

          '<div class="flex flex-col sm:flex-row gap-2">' +
            '<button type="button" data-dr-cc="save" class="flex-1 px-5 py-3 rounded-full text-sm font-bold bg-blue-600 hover:bg-blue-700 text-white transition-colors">Zapisz wyb' + o_ + 'r</button>' +
            '<button type="button" data-dr-cc="accept" class="flex-1 px-5 py-3 rounded-full text-sm font-semibold border border-gray-300 hover:bg-gray-50 text-slate-800 transition-colors">Akceptuj' + e_ + ' wszystkie</button>' +
          '</div>' +
          '<p class="text-xs text-slate-400 mt-4 text-center">' +
            '<a href="' + POLICY_URL + '" class="hover:text-slate-600 underline underline-offset-2">Pe' + l_ + 'na polityka prywatno' + s_ + 'ci i cookie</a>' +
          '</p>' +
        '</div>' +
      '</div>' +
    '</div>';

  var bannerEl, modalEl;

  function showBanner() { if (bannerEl) bannerEl.style.display = 'block'; }
  function hideBanner() { if (bannerEl) bannerEl.style.display = 'none'; }

  function openModal() {
    var c = readConsent();
    document.getElementById('dr-cc-analytics').checked = c ? !!c.analytics : false;
    document.getElementById('dr-cc-ads').checked = c ? !!c.ads : false;
    modalEl.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modalEl.style.display = 'none';
    document.body.style.overflow = '';
  }

  function handleAction(action) {
    if (action === 'accept') {
      saveConsent(true, true); closeModal(); hideBanner();
    } else if (action === 'reject') {
      saveConsent(false, false); hideBanner();
    } else if (action === 'settings') {
      openModal();
    } else if (action === 'save') {
      saveConsent(
        document.getElementById('dr-cc-analytics').checked,
        document.getElementById('dr-cc-ads').checked
      );
      closeModal(); hideBanner();
    } else if (action === 'backdrop') {
      closeModal();
    }
  }

  function init() {
    var wrap = document.createElement('div');
    wrap.innerHTML = BANNER_HTML + MODAL_HTML;
    while (wrap.firstChild) document.body.appendChild(wrap.firstChild);

    bannerEl = document.getElementById('dr-cookie-banner');
    modalEl = document.getElementById('dr-cookie-modal');

    document.addEventListener('click', function (e) {
      var trigger = e.target.closest ? e.target.closest('[data-dr-cc]') : null;
      if (trigger) { handleAction(trigger.getAttribute('data-dr-cc')); return; }
      // Link "Ustawienia cookie" w stopce / na stronie polityki
      var opener = e.target.closest ? e.target.closest('[data-cookie-settings]') : null;
      if (opener) { e.preventDefault(); openModal(); }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalEl.style.display === 'flex') closeModal();
    });

    // Banner tylko gdy brak zapisanego wyboru
    if (!readConsent()) showBanner();
  }

  // Publiczne API - ponowne otwarcie ustawien
  window.drCookieSettings = function () { openModal(); };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
