const API_URL = import.meta.env.VITE_API_URL;

async function request(path, options = {}) {
  let response;

  try {
    if (!API_URL) throw new Error("VITE_API_URL is not configured");
    if (path === "/analyze") {
      console.log("API URL:", API_URL);
      console.log("Analyze endpoint:", `${API_URL}/analyze`);
    }
    response = await fetch(`${API_URL}${path}`, {
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });
  } catch (error) {
    console.error("API request failed:", error);
    throw new Error(error.message || "network", { cause: error });
  }

  let data;
  try {
    data = await response.json();
  } catch (error) {
    console.error("API response parsing failed:", error);
    throw new Error("invalid_response", { cause: error });
  }

  if (!response.ok || !data.success) {
    console.error("API error response:", response.status, data);
    throw new Error(data?.error || "request_failed");
  }

  return data;
}

async function upload(path, file) {
  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    if (!API_URL) throw new Error("VITE_API_URL is not configured");
    response = await fetch(`${API_URL}${path}`, { method: "POST", body: formData });
  } catch (error) {
    console.error("API upload failed:", error);
    throw new Error(error.message || "network", { cause: error });
  }

  let data;
  try {
    data = await response.json();
  } catch (error) {
    console.error("API upload response parsing failed:", error);
    throw new Error("invalid_response", { cause: error });
  }
  if (!response.ok || !data.success) {
    console.error("API upload error response:", response.status, data);
    throw new Error(data?.error || "request_failed");
  }
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
