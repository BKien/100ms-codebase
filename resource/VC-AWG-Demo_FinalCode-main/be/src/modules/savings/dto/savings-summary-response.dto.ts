export interface MonthlySavings {
  month: string;
  amount: number;
}

export interface SavingsSummaryResponse {
  user_id: number;
  year: number;
  summary: {
    this_year: MonthlySavings[];
    last_year: MonthlySavings[];
  };
}

