import type { DebugExample, DebugResult } from "./types";

const API = import.meta.env.VITE_API_URL ?? "/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, options);
  if (!response.ok) {
    throw new Error(`Сервер сұрауды орындай алмады (${response.status}).`);
  }
  return response.json() as Promise<T>;
}

export function getLabExamples(): Promise<DebugExample[]> {
  return request<DebugExample[]>("/lab7/examples");
}

export function startDebug(example: DebugExample): Promise<DebugResult> {
  return request<DebugResult>("/lab7/debug/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      example_id: example.id,
      breakpoint_line: example.breakpoint_line,
    }),
  });
}
