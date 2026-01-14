self.addEventListener('install', (e) => {
    console.log('[Service Worker] Install');
});

self.addEventListener('fetch', (e) => {
    // Ici, on pourrait ajouter une gestion du cache pour le mode hors-ligne
    e.respondWith(fetch(e.request));
});