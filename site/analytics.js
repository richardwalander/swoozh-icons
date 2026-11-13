// Analytics without cookies: GA4 with Consent Mode v2 denied by default (cookieless pings only),
// Microsoft Clarity when an id is set (cookies are switched off in the Clarity project settings).
(function () {
  var GA = 'G-ZBYBV1JXX4', CLARITY = '';
  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;
  gtag('consent', 'default', { ad_storage: 'denied', analytics_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
  gtag('js', new Date());
  gtag('config', GA);
  var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA; document.head.appendChild(s);
  if (CLARITY) {
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY);
  }
  window.track = function (name, params) { try { gtag('event', name, params || {}); if (window.clarity) clarity('event', name); } catch (e) {} };
})();
