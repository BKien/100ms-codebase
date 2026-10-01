import {
  Injectable,
  InternalServerErrorException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Transaction, TransactionType } from '../transaction/transaction.entity';
import { Account } from '../account/account.entity';
import { SavingsSummaryResponse, MonthlySavings } from './dto/savings-summary-response.dto';

@Injectable()
export class SavingsService {
  constructor(
    @InjectRepository(Transaction)
    private transactionRepository: Repository<Transaction>,
    @InjectRepository(Account)
    private accountRepository: Repository<Account>,
  ) {}

  /**
   * Calculate total monthly net savings for a specific year
   * @param userId - User ID
   * @param year - Year to calculate
   * @returns Array of 12 months with net savings amounts
   */
  async getSavingsSummary(userId: number, year: number): Promise<SavingsSummaryResponse> {
    try {
      // 1. Get the user's account_id list
      const accounts = await this.accountRepository.find({
        where: { userId },
        select: ['accountId'],
      });

      if (accounts.length === 0) {
        // If there are no accounts, return an array of 12 months with values of 0
        const emptyYear = this.generateEmptyYear();
        return {
          user_id: userId,
          year,
          summary: {
            this_year: emptyYear,
            last_year: emptyYear,
          },
        };
      }

      const accountIds = accounts.map((acc) => acc.accountId);

      // 2. Calculate for the current year (this_year)
      const thisYear = await this.calculateYearlySavings(accountIds, year);

      // 3. Calculate for the previous year (last_year)
      const lastYear = await this.calculateYearlySavings(accountIds, year - 1);

      return {
        user_id: userId,
        year,
        summary: {
          this_year: thisYear,
          last_year: lastYear,
        },
      };
    } catch (error) {
      throw new InternalServerErrorException(
        'An internal server error occurred while processing the savings summary.',
      );
    }
  }

  /**
   * Calculate net savings for each month in a year
   * @param accountIds - Array of account_id values
   * @param year - Year to calculate
   * @returns Array of 12 months with net savings amounts
   */
  private async calculateYearlySavings(
    accountIds: number[],
    year: number,
  ): Promise<MonthlySavings[]> {
    // Create a result array for 12 months
    const monthlySavings: MonthlySavings[] = [];

    for (let month = 1; month <= 12; month++) {
      // Create the time interval for that month
      // month - 1 because Date months start at 0 (0 = January, 11 = December)
      const startDate = new Date(year, month - 1, 1);
      // month (without -1) creates the first day of the next month, then setting day = 0 moves back to the last day of the previous month
      const endDate = new Date(year, month, 0, 23, 59, 59, 999);

      // Query Revenue (Income) for the month
      const revenueResult = await this.transactionRepository
        .createQueryBuilder('transaction')
        .select('COALESCE(SUM(transaction.amount), 0)', 'total')
        .where('transaction.accountId IN (:...accountIds)', { accountIds })
        .andWhere('transaction.type = :type', { type: TransactionType.REVENUE })
        .andWhere('transaction.transactionDate >= :startDate', { startDate })
        .andWhere('transaction.transactionDate <= :endDate', { endDate })
        .getRawOne();

      const totalRevenue = parseFloat(revenueResult?.total || '0');

      // Query Expense (Expenses) for the month
      const expenseResult = await this.transactionRepository
        .createQueryBuilder('transaction')
        .select('COALESCE(SUM(transaction.amount), 0)', 'total')
        .where('transaction.accountId IN (:...accountIds)', { accountIds })
        .andWhere('transaction.type = :type', { type: TransactionType.EXPENSE })
        .andWhere('transaction.transactionDate >= :startDate', { startDate })
        .andWhere('transaction.transactionDate <= :endDate', { endDate })
        .getRawOne();

      const totalExpense = parseFloat(expenseResult?.total || '0');

      // Calculate net savings = Income - Expenses
      const netSavings = totalRevenue - totalExpense;

      // Format the month with 2 digits (01, 02, ..., 12)
      const monthString = month.toString().padStart(2, '0');

      monthlySavings.push({
        month: monthString,
        amount: Math.round(netSavings * 100) / 100, // Round to 2 decimal places
      });
    }

    return monthlySavings;
  }

  /**
   * Create an array of 12 months with values of 0
   * @returns Array of 12 months with amount = 0
   */
  private generateEmptyYear(): MonthlySavings[] {
    return Array.from({ length: 12 }, (_, index) => ({
      month: (index + 1).toString().padStart(2, '0'),
      amount: 0,
    }));
  }
}

