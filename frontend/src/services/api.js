const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5001").replace(/\/$/, "");

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });
  } catch {
    throw new Error("network");
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("invalid_response");
  }

  if (!response.ok || !data.success) {
    throw new Error(data?.error || "request_failed");
  }

  return data;
}

async function upload(path, file) {
  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, { method: "POST", body: formData });
  } catch {
    throw new Error("network");
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("invalid_response");
  }
  if (!response.ok || !data.success) throw new Error(data?.error || "request_failed");
  return data;
}

export const analyzeConversation = (text) =>
  request("/analyze", { method: "POST", body: JSON.stringify({ text }) });

export const assessRisk = (payload) =>
  request("/assess", { method: "POST", body: JSON.stringify(payload) });

export const analyzeImage = (file) => upload("/analyze/image", file);

export const analyzeAudio = (file) => upload("/analyze/audio", file);

export const getVaultCases = () => request("/vault");

export const getVaultCase = (id) => request(`/vault/${id}`);
