export type DebugExample = {
  id: string;
  title: string;
  error_type: string;
  difficulty: string;
  summary: string;
  buggy_code: string;
  fixed_code: string;
  breakpoint_line: number;
  variables: Record<string, string>;
  buggy_result: string;
  fixed_result: string;
  tests: { name: string; result: string }[];
  report: Record<string, string>;
};

export type DebugResult = {
  example_id: string;
  breakpoint_line: number;
  message: string;
  variables: Record<string, string>;
  buggy_result: string;
  fixed_result: string;
  next_action: string;
};

export type Lab8Diagnostic = {
  code: string;
  count: number;
  description: string;
  severity: string;
};

export type Lab8Case = {
  id: string;
  title: string;
  summary: string;
  source_files: string[];
  fixed_files: string[];
  buggy_code: string;
  fixed_code: string;
  standards: string[];
  tools: { name: string; version: string; purpose: string }[];
  warnings: Lab8Diagnostic[];
  errors: Lab8Diagnostic[];
  code_smells: string[];
  duplicate_evidence: string;
  complexity: { stage: string; block: string; max_cc: string; average: string }[];
  security_issues: Lab8Diagnostic[];
  checklist: string[];
  deficiencies: {
    id: number;
    problem: string;
    severity: string;
    detection: string;
    fix: string;
  }[];
  metrics: { metric: string; before: string; after: string; change: string }[];
  quality_gate: { condition: string; threshold: string; result: string; status: string }[];
  tasks: { id: number; title: string; evidence: string; status: string }[];
  conclusion: string;
};

export type Lab8RunResult = {
  message: string;
  ruff_issues: number;
  pylint_messages: number;
  pylint_score: string;
  security_issues: number;
  duplicate_blocks: number;
  max_complexity: number;
  tests: string;
  quality_gate: string;
};
