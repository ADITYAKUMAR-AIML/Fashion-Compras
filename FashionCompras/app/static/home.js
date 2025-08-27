
(function(){
  const LOG = (msg) => { try { console.log("[DL] " + msg); } catch(e){} };

  function tryDownload(contentStr, filename){
    const blob = new Blob([contentStr], { type: 'text/plain' });
    // method 1: object URL
    try {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      LOG("Downloaded via object URL");
      return true;
    } catch (err) { LOG("object URL failed: " + err); }

    // method 2: data URL
    try {
      const reader = new FileReader();
      reader.onload = function() {
        try {
          const a2 = document.createElement('a');
          a2.style.display = 'none';
          a2.href = reader.result;
          a2.download = filename;
          document.body.appendChild(a2);
          a2.click();
          a2.remove();
          LOG("Downloaded via data URL");
        } catch(e2){
          LOG("data URL click failed: " + e2);
        }
      };
      reader.onerror = function(e){ LOG("FileReader error: " + e); };
      reader.readAsDataURL(blob);
      return true;
    } catch (err) { LOG("data URL method failed: " + err); }

    // msSave fallback
    try {
      if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveOrOpenBlob(blob, filename);
        LOG("Downloaded via msSaveOrOpenBlob");
        return true;
      }
    } catch (err) { LOG("msSave fallback failed: " + err); }

    return false;
  }

  function attachHandler() {
    const el = document.getElementById('downloadLink');
    if (!el) {
      LOG("Element with id 'downloadLink' not found");
      return false;
    }

    // remove previous listeners (defensive)
    el.replaceWith(el.cloneNode(true));
    const fresh = document.getElementById('downloadLink');

    fresh.addEventListener('click', function(e){
      e.preventDefault(); e.stopImmediatePropagation(); e.stopPropagation();
      LOG("downloadLink clicked");

      // if inside a form with submit button, also ensure form doesn't submit
      const parentForm = fresh.closest('form');
      if (parentForm) {
        parentForm.addEventListener('submit', function(subE){
          subE.preventDefault();
          subE.stopImmediatePropagation();
        }, { once: true, capture: true });
      }

      const content = `PRIVACY POLICY\n\nLast Updated: ${new Date().toLocaleString()}\n\nThis is a generated privacy policy for download.`;
      const ok = tryDownload(content, "PrivacyPolicy.txt");
      if (!ok) {
        alert("Download failed — check console for details.");
      }
    }, { capture: true });

    LOG("Download handler attached to #downloadLink");
    return true;
  }

  // Try attach now. If element not present, retry a few times (handles SPA / late-loaded DOM)
  if (!attachHandler()) {
    let attempts = 0;
    const interval = setInterval(() => {
      attempts++;
      if (attachHandler() || attempts > 10) {
        clearInterval(interval);
      }
    }, 300); // retry for ~3s
  }

  // Also log any top-level JS errors (helps identify earlier exceptions)
  window.addEventListener('error', function(ev){
    LOG("Top-level error: " + (ev && ev.message ? ev.message : ev));
  });
})();

