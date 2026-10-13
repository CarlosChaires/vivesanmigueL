const CACHE_NAME = 'vivesanmiguel-cache-v1';
const urlsToCache = [
  './index.html',
  './eventos.html',
  './gastronomia.html',
  './hospedaje.html',
  './sitiosdeinteres.html',
  './mapa.html',
  './blog.html',
  './manifest.json'
];

// Instalación del Service Worker y almacenamiento de archivos clave
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// Activación y limpieza de cachés antiguos
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interceptación de peticiones para servir contenido offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Si está en caché, lo devuelve; si no, intenta buscarlo en la red
        return response || fetch(event.request);
      })
  );
});
