import { request } from "./client";

export function askQuestion(question, topK = 5) {
  return request("/query/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k: topK }),
  });
}
