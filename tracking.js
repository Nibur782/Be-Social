/**
 * Tracking zdarzen - dawidrubin.pl
 * Wszystko leci do dataLayer (GTM -> GA4).
 *
 * GLOWNE KONWERSJE:
 *   select_offer  - klikniecie CTA jednej z trzech ofert
 *   generate_lead - wyslanie briefu (audyt / projekt)  [w brief-*.html]
 *   book_meeting_start - interakcja z kalendarzem rezerwacji
 *
 * ZDARZENIE DODATKOWE:
 *   download_pdf  - pobranie darmowej checklisty  [w audyt-paid-media.html]
 */
(function () {
  'use strict';

  window.dataLayer = window.dataLayer || [];

  function push(payload) {
    window.dataLayer.push(payload);
  }

  // ---------- 1. select_offer ----------
  // Wymaga atrybutow: data-track-offer="audyt|projekt|staly_partner"
  //                   data-offer-price="1200"  (opcjonalnie)
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-track-offer]') : null;
    if (!el) return;

    push({
      event: 'select_offer',
      offer_name: el.getAttribute('data-track-offer'),
      offer_price_from: el.getAttribute('data-offer-price') || undefined,
      offer_location: el.getAttribute('data-offer-location') || 'cennik',
      link_url: el.getAttribute('href') || undefined
    });
  }, true);

  // ---------- 2. download_pdf (bezposrednie linki do PDF) ----------
  // Formularz PDF wysyla wlasne zdarzenie; tu lapiemy klikniecia w gotowy plik.
  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href$=".pdf"]') : null;
    if (!a) return;
    if (a.hasAttribute('data-no-track')) return;

    var href = a.getAttribute('href') || '';
    push({
      event: 'download_pdf',
      file_name: href.split('/').pop(),
      file_extension: 'pdf',
      link_text: (a.textContent || '').trim().slice(0, 80),
      download_source: 'direct_link'
    });
  }, true);

  // ---------- 3. book_meeting_start (kalendarz Google, cross-origin) ----------
  // Kalendarz jest w iframe z innej domeny - nie da sie odczytac faktu rezerwacji.
  // Wykrywamy wejscie w interakcje: kliniecie w obszar iframe zabiera focus oknu.
  (function trackCalendar() {
    var frames = document.querySelectorAll('iframe[src*="calendar.google.com"]');
    if (!frames.length) return;

    var hovering = false;
    var alreadySent = false;

    Array.prototype.forEach.call(frames, function (f) {
      var target = f.parentElement || f;
      target.addEventListener('mouseenter', function () { hovering = true; });
      target.addEventListener('mouseleave', function () { hovering = false; });
    });

    window.addEventListener('blur', function () {
      if (alreadySent || !hovering) return;
      var ae = document.activeElement;
      if (!ae || ae.tagName !== 'IFRAME') return;
      if ((ae.src || '').indexOf('calendar.google.com') === -1) return;

      alreadySent = true;
      push({
        event: 'book_meeting_start',
        meeting_type: 'sesja_wstepna_15min',
        meeting_source: window.location.pathname
      });
    });

    // Klikniecie w zapasowy link "Otworz w nowej karcie"
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href*="calendar.google.com"]') : null;
      if (!a) return;
      push({
        event: 'book_meeting_start',
        meeting_type: 'sesja_wstepna_15min',
        meeting_source: window.location.pathname + ' (nowa karta)'
      });
    }, true);
  })();

})();
