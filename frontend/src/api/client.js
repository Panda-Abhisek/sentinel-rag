const API_BASE = import.meta.env.VITE_API_URL || "/api";

export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail || `Request failed with status ${response.status}.`);
  }

  return response.json();
}
