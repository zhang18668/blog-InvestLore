// 股市操练笔记 · 注册 Service Worker（PWA 离线能力）
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('Service Worker 注册成功，作用域：', registration.scope);
      })
      .catch((err) => {
        console.warn('Service Worker 注册失败：', err);
      });
  });
}
