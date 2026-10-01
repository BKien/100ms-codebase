import {
  Injectable,
  InternalServerErrorException,
  NotFoundException,
  ForbiddenException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository, InjectDataSource } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Goal, GoalType } from './goal.entity';
import { Transaction, TransactionType } from '../transaction/transaction.entity';
import { Account } from '../account/account.entity';
import { Category } from '../category/category.entity';
import { UpdateGoalDto } from './dto/update-goal.dto';
import { CreateGoalDto } from './dto/create-goal.dto';

@Injectable()
export class GoalService {
  constructor(
    @InjectRepository(Goal)
    private goalRepository: Repository<Goal>,
    @InjectRepository(Account)
    private accountRepository: Repository<Account>,
    @InjectRepository(Transaction)
    private transactionRepository: Repository<Transaction>,
    @InjectRepository(Category)
    private categoryRepository: Repository<Category>,
    @InjectDataSource()
    private dataSource: DataSource,
  ) {}

  /**
   * Get the user's savings goal and spending goals
   * @param userId - User ID (from JWT)
   * @returns Goal data including savingGoal and expenseGoals
   */
  async getGoals(userId: number) {
    try {
      // 1. Get the savings goal (Saving)
      const savingGoal = await this.goalRepository.findOne({
        where: {
          userId,
          goalType: GoalType.SAVING,
        },
        relations: ['category'],
      });

      // 2. Get the current month (start and end of the month)
      const now = new Date();
      const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);

      // 3. Get spending goals (Expense_Limit) whose periods include the current month
      const allExpenseGoals = await this.goalRepository.find({
        where: {
          userId,
          goalType: GoalType.EXPENSE_LIMIT,
        },
        relations: ['category'],
      });

      // Filter goals with start_date <= the end of the current month and end_date >= the start of the current month
      const expenseGoals = allExpenseGoals.filter((goal) => {
        const goalStartDate = goal.startDate instanceof Date 
          ? goal.startDate 
          : new Date(goal.startDate);
        const goalEndDate = goal.endDate instanceof Date 
          ? goal.endDate 
          : new Date(goal.endDate);
        
        // Goals are active in the current month if:
        // start_date <= endOfMonth AND end_date >= startOfMonth
        return goalStartDate <= endOfMonth && goalEndDate >= startOfMonth;
      });

      // 4. Calculate target_achieved for savingGoal if available
      let targetAchieved = 0;
      if (savingGoal) {
        // Get the user's account_id list
        const accounts = await this.accountRepository.find({
          where: { userId },
          select: ['accountId'],
        });

        if (accounts.length > 0) {
          const accountIds = accounts.map((acc) => acc.accountId);

          // Calculate total income (Revenue) for the current month
          const revenueResult = await this.transactionRepository
            .createQueryBuilder('transaction')
            .select('COALESCE(SUM(transaction.amount), 0)', 'total')
            .where('transaction.accountId IN (:...accountIds)', { accountIds })
            .andWhere('transaction.type = :type', { type: TransactionType.REVENUE })
            .andWhere('transaction.transactionDate >= :startDate', { startDate: startOfMonth })
            .andWhere('transaction.transactionDate <= :endDate', { endDate: endOfMonth })
            .getRawOne();

          const totalRevenue = parseFloat(revenueResult?.total || '0') || 0;

          // Calculate total expenses (Expense) for the current month
          const expenseResult = await this.transactionRepository
            .createQueryBuilder('transaction')
            .select('COALESCE(SUM(transaction.amount), 0)', 'total')
            .where('transaction.accountId IN (:...accountIds)', { accountIds })
            .andWhere('transaction.type = :type', { type: TransactionType.EXPENSE })
            .andWhere('transaction.transactionDate >= :startDate', { startDate: startOfMonth })
            .andWhere('transaction.transactionDate <= :endDate', { endDate: endOfMonth })
            .getRawOne();

          const totalExpense = parseFloat(expenseResult?.total || '0') || 0;

          // Calculate target_achieved = Total Income - Total Expenses
          targetAchieved = totalRevenue - totalExpense;
        }
      }

      // 5. Get the user's account_id list to calculate expenses by category
      const accounts = await this.accountRepository.find({
        where: { userId },
        select: ['accountId'],
      });

      const accountIds = accounts.length > 0 ? accounts.map((acc) => acc.accountId) : [];

      // 6. Format the response for savingGoal
      const savingGoalResponse = savingGoal
        ? {
            goal_id: savingGoal.goalId,
            goal_type: savingGoal.goalType,
            target_amount: Number(savingGoal.targetAmount),
            target_achieved: targetAchieved,
            start_date: savingGoal.startDate instanceof Date
              ? savingGoal.startDate.toISOString().split('T')[0]
              : String(savingGoal.startDate).split('T')[0],
            end_date: savingGoal.endDate instanceof Date
              ? savingGoal.endDate.toISOString().split('T')[0]
              : String(savingGoal.endDate).split('T')[0],
          }
        : null;

      // 7. Format the response for expenseGoals and calculate the amount spent in the current month
      const expenseGoalsResponse = await Promise.all(
        expenseGoals.map(async (goal) => {
          let currentExpense = 0;

          // Calculate the amount spent in the current month for this category
          if (accountIds.length > 0 && goal.categoryId) {
            const expenseResult = await this.transactionRepository
              .createQueryBuilder('transaction')
              .select('COALESCE(SUM(transaction.amount), 0)', 'total')
              .where('transaction.accountId IN (:...accountIds)', { accountIds })
              .andWhere('transaction.type = :type', { type: TransactionType.EXPENSE })
              .andWhere('transaction.categoryId = :categoryId', { categoryId: goal.categoryId })
              .andWhere('transaction.transactionDate >= :startDate', { startDate: startOfMonth })
              .andWhere('transaction.transactionDate <= :endDate', { endDate: endOfMonth })
              .getRawOne();

            currentExpense = parseFloat(expenseResult?.total || '0') || 0;
          }

          return {
            goal_id: goal.goalId,
            category: goal.category?.categoryName || 'Unknown',
            target_amount: Number(goal.targetAmount),
            current_expense: currentExpense,
          };
        }),
      );

      return {
        savingGoal: savingGoalResponse,
        expenseGoals: expenseGoalsResponse,
      };
    } catch (error) {
      // Handle errors and throw InternalServerErrorException
      throw new InternalServerErrorException(
        'A system error occurred while loading goals, please try again later.',
      );
    }
  }

  /**
   * Create a new goal
   * @param userId - User ID (from JWT)
   * @param createGoalDto - DTO containing goal information
   * @returns The newly created goal
   */
  async createGoal(userId: number, createGoalDto: CreateGoalDto) {
    try {
      // 1. Validation: target_amount must be greater than 0
      if (!createGoalDto.target_amount || createGoalDto.target_amount <= 0) {
        throw new BadRequestException('target_amount must be greater than 0.');
      }

      // 2. Validation: end_date must be after start_date
      const startDate = new Date(createGoalDto.start_date);
      const endDate = new Date(createGoalDto.end_date);

      if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
        throw new BadRequestException('start_date and end_date must be in a valid date format.');
      }

      if (endDate <= startDate) {
        throw new BadRequestException('end_date must be after start_date.');
      }

      // 3. Validation: If goal_type is Expense_Limit, category_id must not be null and must be a valid category
      if (createGoalDto.goal_type === GoalType.EXPENSE_LIMIT) {
        if (!createGoalDto.category_id) {
          throw new BadRequestException('category_id must not be empty when goal_type is Expense_Limit.');
        }

        // Check whether the category exists
        const category = await this.categoryRepository.findOne({
          where: { categoryId: createGoalDto.category_id },
        });

        if (!category) {
          throw new BadRequestException('Invalid category_id. The category does not exist.');
        }
      }

      // 4. Create a new record in the Goals table
      const newGoal = this.goalRepository.create({
        userId,
        goalType: createGoalDto.goal_type,
        categoryId: createGoalDto.goal_type === GoalType.EXPENSE_LIMIT ? createGoalDto.category_id : null,
        startDate,
        endDate,
        targetAmount: createGoalDto.target_amount,
      });

      // 5. Save the record to the database
      const savedGoal = await this.goalRepository.save(newGoal);

      return savedGoal;
    } catch (error) {
      // If it is already a BadRequestException, rethrow it
      if (error instanceof BadRequestException) {
        throw error;
      }

      // If an error occurs while saving to the database, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'Unable to create the goal at this time. Please try again later.',
      );
    }
  }

  /**
   * Update the goal's target_amount
   * @param goalId - ID of the goal to update
   * @param userId - User ID (from JWT)
   * @param updateGoalDto - DTO containing the new target_amount
   * @returns The updated goal
   */
  async updateGoal(goalId: number, userId: number, updateGoalDto: UpdateGoalDto) {
    try {
      // 1. Find the goal in the database by goalId
      const goal = await this.goalRepository.findOne({
        where: { goalId },
      });

      // 2. If not found, throw NotFoundException
      if (!goal) {
        throw new NotFoundException('The goal does not exist.');
      }

      // 3. Verify ownership: Compare goal.userId with userId from the token
      if (goal.userId !== userId) {
        throw new ForbiddenException('You do not have permission to edit this goal.');
      }

      // 4. Business validation has been performed by class-validator in the DTO
      // (target_amount must be a positive number > 0)

      // 5. Update the goal's target_amount field in the database
      goal.targetAmount = updateGoalDto.target_amount;
      const updatedGoal = await this.goalRepository.save(goal);

      // 6. Return the updated goal
      return updatedGoal;
    } catch (error) {
      // If it is already an HttpException (NotFoundException, ForbiddenException), rethrow it
      if (error instanceof NotFoundException || error instanceof ForbiddenException) {
        throw error;
      }

      // If an error occurs while updating the database, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'Unable to save changes at this time. Please try again later.',
      );
    }
  }
}

