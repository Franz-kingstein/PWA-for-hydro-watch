self.addEventListener('install', function(event) {
    event.waitUntil(
      caches.open('hydro-watch-cache').then(function(cache) {
        return cache.addAll([
          '/',
          '/static/styles.css',
          '/static/icons/icon-192x192.png',
          '/static/icons/icon-512x512.png',
          // add other assets that you want to cache
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      })
    );
  });
  