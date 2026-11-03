<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pi Secure Vault Bridge</title>
  <style>
    :root { --primary: #1a73e8; --success: #34a853; --dark: #202124; --bg: #f8f9fa; }
    body { font-family: system-ui, -apple-system, sans-serif; background: var(--bg); margin: 0; padding: 24px; display: flex; justify-content: center; }
    .card { background: #fff; padding: 24px; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); max-width: 520px; width: 100%; border: 1px solid #e0e0e0; }
    h2 { margin: 0 0 8px 0; color: var(--dark); font-size: 20px; }
    .meta { font-size: 12px; color: #5f6368; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
    .badge { background: #e8f0fe; color: var(--primary); padding: 3px 8px; border-radius: 4px; font-family: monospace; font-weight: 600; }
    .section { padding: 14px 0; border-top: 1px solid #eee; }
    label { font-weight: 600; display: block; margin-bottom: 6px; font-size: 13px; color: #3c4043; }
    input[type="text"], input[type="file"] { width: 100%; padding: 9px 10px; box-sizing: border-box; border: 1px solid #dadce0; border-radius: 6px; margin-bottom: 10px; font-size: 14px; }
    button { background: var(--primary); color: #fff; border: none; padding: 9px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13px; transition: opacity 0.15s; }
    button.success { background: var(--success); }
    button.dark { background: var(--dark); }
    button:disabled { opacity: 0.5; cursor: not-allowed; }
    #status { margin-top: 16px; font-size: 13px; word-break: break-all; background: #f1f3f4; padding: 12px; border-radius: 6px; border-left: 4px solid var(--primary); line-height: 1.5; }
    code { background: #e8eaed; padding: 2px 5px; border-radius: 4px; font-size: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <h2>Pi Secure Vault Bridge</h2>
    <div class="meta">
      <span>Session Client ID: <span class="badge" id="clientIdDisplay"></span></span>
      <button class="dark" id="statusBtn" onclick="checkPiStatus()">Check Pi Tunnel</button>
    </div>

    <div class="section">
      <label>Test Text Relay (/encrypt):</label>
      <input type="text" id="inputText" placeholder="Enter message to reverse on Pi..." />
      <button onclick="runTextTest()">Send Text to Pi</button>
    </div>

    <div class="section">
      <label>Upload File to Pi (Saved as filename.ext.hash.clientid):</label>
      <input type="file" id="fileInput" />
      <button id="uploadBtn" onclick="uploadFile()">Upload &amp; Get Hash Receipt</button>
    </div>

    <div class="section">
      <label>Retrieve File by Hash Receipt:</label>
      <input type="text" id="hashInput" placeholder="Paste 64-character SHA-256 hash..." />
      <button class="success" id="downloadBtn" onclick="downloadFile()">Download File from Pi</button>
    </div>

    <div id="status">Status: Ready</div>
  </div>

  <script>
    const BASE_URL = window.location.origin.includes("onrender.com") || window.location.origin.includes("ts.net") || window.location.origin.includes("localhost")
      ? window.location.origin
      : "https://inf-data-h6g0.onrender.com";

    const statusDiv = document.getElementById("status");

    let clientId = sessionStorage.getItem("pi_client_id");
    if (!clientId) {
      clientId = "user_" + Math.random().toString(36).substring(2, 9);
      sessionStorage.setItem("pi_client_id", clientId);
    }
    document.getElementById("clientIdDisplay").innerText = clientId;

    async function safeJsonParse(res) {
      const contentType = res.headers.get("content-type") || "";
      if (!contentType.includes("application/json")) {
        const text = await res.text();
        throw new Error(`Expected JSON but received ${contentType || "HTML/Text"} (HTTP ${res.status}). Check that /api/status is active.`);
      }
      return await res.json();
    }

    async function checkPiStatus() {
      statusDiv.innerText = "Checking connection to Pi through Render proxy...";
      try {
        const res = await fetch(`${BASE_URL}/api/status`, {
          headers: { "Accept": "application/json" }
        });
        const data = await safeJsonParse(res);
        statusDiv.innerHTML = `<b>Connected!</b><br>Node: <code>${data.service}</code><br>Files Stored: <code>${data.files_stored}</code>`;
      } catch (err) {
        statusDiv.innerText = "Connection failed: " + err.message;
      }
    }

    async function runTextTest() {
      const text = document.getElementById("inputText").value.trim();
      if (!text) { statusDiv.innerText = "Enter text first."; return; }
      statusDiv.innerText = "Routing text to Pi...";
      try {
        const res = await fetch(`${BASE_URL}/encrypt`, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify({ text })
        });
        const data = await safeJsonParse(res);
        statusDiv.innerHTML = `<b>Response from Pi:</b> <code>${data.ciphertext}</code>`;
      } catch (err) {
        statusDiv.innerText = "Text relay error: " + err.message;
      }
    }

    async function uploadFile() {
      const fileInput = document.getElementById("fileInput");
      if (!fileInput.files.length) { statusDiv.innerText = "Please select a file first."; return; }

      const file = fileInput.files[0];
      const fileSizeMB = file.size / (1024 * 1024);
      let tierNotice = "Free Tier (<= 2MB)";
      if (fileSizeMB > 2) {
        const extraCost = (Math.ceil((fileSizeMB - 2) / 10) * 0.0001).toFixed(4);
        tierNotice = `Over 2MB (${fileSizeMB.toFixed(2)} MB) — Est. fee: $${extraCost}`;
      }

      const formData = new FormData();
      formData.append("file", file);
      formData.append("client_id", clientId);

      statusDiv.innerText = `Uploading ${file.name} (${tierNotice}) to local Pi...`;
      try {
        const res = await fetch(`${BASE_URL}/upload-file`, { method: "POST", body: formData });
        const data = await safeJsonParse(res);
        if (!res.ok) throw new Error(data.detail || "Upload failed");
        statusDiv.innerHTML = `<b>Saved on Pi as:</b><br><code>${data.saved_as}</code><br><br><b>Hash Receipt (Copy to retrieve):</b><br><code>${data.hash}</code>`;
        document.getElementById("hashInput").value = data.hash;
      } catch (err) {
        statusDiv.innerText = "Upload error: " + err.message;
      }
    }

    async function downloadFile() {
      const hash = document.getElementById("hashInput").value.trim();
      if (!hash) { statusDiv.innerText = "Please enter a hash receipt first."; return; }

      statusDiv.innerText = "Fetching file from Pi by hash...";
      try {
        const res = await fetch(`${BASE_URL}/get-file/${encodeURIComponent(hash)}`);
        if (!res.ok) {
          const errText = await res.text();
          throw new Error(`File not found on local node (HTTP ${res.status}): ${errText}`);
        }

        let filename = "retrieved_file";
        const disposition = res.headers.get("content-disposition");
        if (disposition && disposition.includes("filename=")) {
          filename = disposition.split("filename=")[1].replace(/["']/g, "").trim();
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        statusDiv.innerHTML = `<b>Success!</b> Rebuilt and downloaded: <code>${filename}</code>`;
      } catch (err) {
        statusDiv.innerText = "Retrieval error: " + err.message;
      }
    }
  </script>
</body>
</html>
