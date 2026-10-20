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
