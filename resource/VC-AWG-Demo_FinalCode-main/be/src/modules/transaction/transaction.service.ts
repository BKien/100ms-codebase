import {
  Injectable,
  InternalServerErrorException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository, InjectDataSource } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Transaction, TransactionType, TransactionStatus } from './transaction.entity';
import { Account } from '../account/account.entity';
import { Category } from '../category/category.entity';
import { CreateTransactionDto } from './dto/create-transaction.dto';

@Injectable()
export class TransactionService {
  constructor(
    @InjectRepository(Transaction)
    private transactionRepository: Repository<Transaction>,
    @InjectRepository(Account)
    private accountRepository: Repository<Account>,
    @InjectRepository(Category)
    private categoryRepository: Repository<Category>,
    @InjectDataSource()
    private dataSource: DataSource,
  ) {}

  /**
   * Get the user's transaction list with pagination and filtering by type
   * @param userId - User ID
   * @param type - Transaction type: "All" | "Revenue" | "Expense"
   * @param limit - Number of records per page (default 10)
   * @param offset - Starting offset (default 0)
   * @returns Transaction list with total and hasMore
   */
  async findAllByUserId(
    userId: number,
    type: string,
    limit: number = 10,
    offset: number = 0,
  ) {
    try {
      // Validate type parameter
      if (type !== 'All' && type !== 'Revenue' && type !== 'Expense') {
        throw new BadRequestException('Invalid type parameter');
      }

      // Get the user's account_id list
      const accounts = await this.accountRepository.find({
        where: { userId },
        select: ['accountId'],
      });

      if (accounts.length === 0) {
        return {
          data: [],
          total: 0,
          hasMore: false,
        };
      }

      const accountIds = accounts.map((acc) => acc.accountId);

      // Build the query builder
      const queryBuilder = this.transactionRepository
        .createQueryBuilder('transaction')
        .where('transaction.accountId IN (:...accountIds)', { accountIds });

      // Add a filter condition by type if it is not "All"
      if (type === 'Revenue') {
        queryBuilder.andWhere('transaction.type = :type', {
          type: TransactionType.REVENUE,
        });
      } else if (type === 'Expense') {
        queryBuilder.andWhere('transaction.type = :type', {
          type: TransactionType.EXPENSE,
        });
      }

      // Count total records (before pagination)
      const total = await queryBuilder.getCount();

      // Apply pagination and sorting
      const transactions = await queryBuilder
        .orderBy('transaction.transactionDate', 'DESC')
        .skip(offset)
        .take(limit)
        .getMany();

      // Map data to return the correct format (snake_case to match frontend types)
      const data = transactions.map((transaction) => ({
        transaction_id: transaction.transactionId,
        account_id: transaction.accountId,
        transaction_date: transaction.transactionDate,
        type: transaction.type,
        item_description: transaction.itemDescription,
        shop_name: transaction.shopName || null,
        amount: Number(transaction.amount),
        payment_method: transaction.paymentMethod || null,
        status: transaction.status,
      }));

      // Calculate hasMore
      const hasMore = offset + transactions.length < total;

      return {
        data,
        total,
        hasMore,
      };
    } catch (error) {
      // If it is a BadRequestException, rethrow it
      if (error instanceof BadRequestException) {
        throw error;
      }
      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'A system error occurred while retrieving the transaction list. Please try again later.',
      );
    }
  }

  /**
   * Create a new transaction for the user
   * @param userId - User ID (from JWT)
   * @param createTransactionDto - DTO containing transaction information
   * @returns The newly created transaction
   */
  async create(userId: number, createTransactionDto: CreateTransactionDto) {
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      // 1. Check data validity
      if (!createTransactionDto.itemDescription || createTransactionDto.itemDescription.trim() === '') {
        throw new BadRequestException('Invalid or missing transaction data');
      }

      if (!createTransactionDto.amount || createTransactionDto.amount <= 0) {
        throw new BadRequestException('Invalid or missing transaction data');
      }

      if (
        createTransactionDto.type !== TransactionType.REVENUE &&
        createTransactionDto.type !== TransactionType.EXPENSE
      ) {
        throw new BadRequestException('Invalid or missing transaction data');
      }

      // 2. Check category_id if present
      if (createTransactionDto.category_id) {
        const category = await queryRunner.manager.findOne(Category, {
          where: { categoryId: createTransactionDto.category_id },
        });

        if (!category) {
          throw new BadRequestException('Invalid or missing transaction data');
        }
      }

      // 3. Check whether accountId belongs to the current user_id
      const account = await queryRunner.manager.findOne(Account, {
        where: {
          accountId: createTransactionDto.accountId,
          userId: userId,
        },
      });

      if (!account) {
        throw new BadRequestException('Invalid or missing transaction data');
      }

      // 4. Check the balance for Expense
      if (createTransactionDto.type === TransactionType.EXPENSE) {
        const currentBalance = Number(account.balance);
        if (currentBalance < createTransactionDto.amount) {
          throw new BadRequestException('Invalid or missing transaction data');
        }
      }

      // 5. Create a new transaction
      const newTransaction = new Transaction();
      newTransaction.accountId = createTransactionDto.accountId;
      newTransaction.transactionDate = new Date(createTransactionDto.transactionDate);
      newTransaction.type = createTransactionDto.type;
      newTransaction.itemDescription = createTransactionDto.itemDescription;
      newTransaction.categoryId = createTransactionDto.category_id || null;
      newTransaction.shopName = createTransactionDto.shopName || null;
      newTransaction.amount = createTransactionDto.amount;
      newTransaction.paymentMethod = createTransactionDto.paymentMethod || null;
      newTransaction.status = createTransactionDto.status || TransactionStatus.COMPLETE;

      const savedTransaction = await queryRunner.manager.save(Transaction, newTransaction);

      // 6. Update the balance in Accounts
      if (createTransactionDto.type === TransactionType.EXPENSE) {
        account.balance = Number(account.balance) - createTransactionDto.amount;
      } else if (createTransactionDto.type === TransactionType.REVENUE) {
        account.balance = Number(account.balance) + createTransactionDto.amount;
      }

      await queryRunner.manager.save(Account, account);

      // 7. Commit transaction
      await queryRunner.commitTransaction();

      // 8. Return the response in the required format
      return {
        message: 'Transaction created successfully',
        data: {
          transactionId: savedTransaction.transactionId,
          accountId: savedTransaction.accountId,
          transactionDate: savedTransaction.transactionDate,
          type: savedTransaction.type,
          itemDescription: savedTransaction.itemDescription,
          shopName: savedTransaction.shopName,
          amount: Number(savedTransaction.amount),
          paymentMethod: savedTransaction.paymentMethod,
          status: savedTransaction.status,
          receiptId: savedTransaction.receiptId,
          createdAt: new Date(),
          category_id: savedTransaction.categoryId,
        },
      };
    } catch (error) {
      // Roll back the transaction if an error occurs
      await queryRunner.rollbackTransaction();

      // If it is a BadRequestException, rethrow it
      if (error instanceof BadRequestException) {
        throw error;
      }

      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'A system error occurred while creating the transaction. Please try again later.',
      );
    } finally {
      // Release the query runner
      await queryRunner.release();
    }
  }
}

