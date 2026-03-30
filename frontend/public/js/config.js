(function bootstrapClientConfig() {
  const runtimeConfig = window.__APP_RUNTIME_CONFIG__ || {};
  const protocol = window.location.protocol || "http:";
  const hostname = window.location.hostname || "127.0.0.1";

  const normalizeBaseURL = (value) => (value.endsWith("/") ? value : `${value}/`);

  window.baseURL = normalizeBaseURL(
    runtimeConfig.baseURL || `${protocol}//${hostname}:8000`
  );
  window.AIURL = runtimeConfig.aiURL || `${protocol}//${hostname}:6006`;
  globalThis.AIURL = window.AIURL;
})();
