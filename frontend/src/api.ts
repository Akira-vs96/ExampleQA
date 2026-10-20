import type { DebugExample, DebugResult, Lab8Case, Lab8RunResult } from "./types";

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

export function getLab8Case(): Promise<Lab8Case> {
  return request<Lab8Case>("/lab8/case");
}

export function checkLab8QualityGate(): Promise<Lab8RunResult> {
  return request<Lab8RunResult>("/lab8/quality-gate", { method: "POST" });
}
