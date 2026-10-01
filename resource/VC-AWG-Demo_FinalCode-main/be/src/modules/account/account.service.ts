import { Injectable, InternalServerErrorException, ConflictException, NotFoundException, ForbiddenException, BadRequestException } from '@nestjs/common';
import { InjectRepository, InjectDataSource } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Account } from './account.entity';
import { Transaction, TransactionType } from '../transaction/transaction.entity';
import { CreateAccountDto } from './dto/create-account.dto';
import { UpdateAccountDto } from './dto/update-account.dto';

@Injectable()
export class AccountService {
  constructor(
    @InjectRepository(Account)
    private accountRepository: Repository<Account>,
    @InjectRepository(Transaction)
    private transactionRepository: Repository<Transaction>,
    @InjectDataSource()
    private dataSource: DataSource,
  ) {}

  /**
   * Get the user's accounts theo user_id
   * @param userId - User ID
   * @returns Account list
   */
  async findAllByUserId(userId: number) {
    try {
      const accounts = await this.accountRepository.find({
        where: { userId },
        select: [
          'accountId',
          'bankName',
          'accountType',
          'branchName',
          'accountNumberLast4',
          'balance',
        ],
        order: {
          accountId: 'ASC',
        },
      });

      // Map data to return the correct format
      return accounts.map((account) => ({
        id: account.accountId,
        bank_name: account.bankName,
        account_type: account.accountType,
        branch_name: account.branchName || null,
        account_number_last_4: account.accountNumberLast4,
        balance: Number(account.balance),
      }));
    } catch (error) {
      throw new InternalServerErrorException(
        'A system error occurred, please try again later.',
      );
    }
  }

  /**
   * Create a new account for the user
   * @param userId - User ID
   * @param createAccountDto - DTO containing account information
   * @returns The newly created account
   */
  async create(userId: number, createAccountDto: CreateAccountDto) {
    try {
      // Check whether the account number already exists for this user
      const existingAccount = await this.accountRepository.findOne({
        where: {
          userId,
          accountNumberFull: createAccountDto.account_number_full,
        },
      });

      if (existingAccount) {
        throw new ConflictException('This account already exists in your list.');
      }

      // Get the last 4 digits of the account number
      const accountNumberLast4 = createAccountDto.account_number_full.slice(-4);

      // Create a new account
      const newAccount = this.accountRepository.create({
        userId,
        bankName: createAccountDto.bank_name,
        accountType: createAccountDto.account_type,
        branchName: createAccountDto.branch_name || undefined,
        accountNumberFull: createAccountDto.account_number_full,
        accountNumberLast4,
        balance: createAccountDto.balance,
      });

      const savedAccount = await this.accountRepository.save(newAccount);

      // Return the correct response format
      return {
        id: savedAccount.accountId,
        user_id: savedAccount.userId,
        bank_name: savedAccount.bankName,
        account_type: savedAccount.accountType,
        branch_name: savedAccount.branchName || null,
        account_number_last_4: savedAccount.accountNumberLast4,
        balance: Number(savedAccount.balance),
      };
    } catch (error) {
      // If it is a ConflictException, rethrow it
      if (error instanceof ConflictException) {
        throw error;
      }
      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'Unable to add the account at this time. Please try again later.',
      );
    }
  }

  /**
   * Get account details with the 5 most recent transactions
   * @param accountId - Account ID
   * @param userId - User ID (from JWT)
   * @returns Account details with the list of recent transactions
   */
  async findOneWithTransactions(accountId: number, userId: number) {
    try {
      // 1. Find the account by accountId
      const account = await this.accountRepository.findOne({
        where: { accountId },
      });

      // 2. Validation 1: Check whether the account exists
      if (!account) {
        throw new NotFoundException('This account was not found.');
      }

      // 3. Validation 2: Check ownership
      if (account.userId !== userId) {
        throw new ForbiddenException('You do not have permission to view information about this account.');
      }

      // 4. Get the 5 most recent transactions of this account
      const recentTransactions = await this.transactionRepository.find({
        where: { accountId },
        order: { transactionDate: 'DESC' },
        take: 5,
      });

      // 5. Map data to return the correct format
      const accountData = {
        id: account.accountId,
        bank_name: account.bankName,
        account_type: account.accountType,
        branch_name: account.branchName || null,
        account_number_full: account.accountNumberFull,
        balance: Number(account.balance),
        recent_transactions: recentTransactions.map((transaction) => {
          // For Expense, amount will be negative
          const amount = Number(transaction.amount || 0)
          const finalAmount = transaction.type === TransactionType.EXPENSE ? -amount : amount
          
          // Handle dates safely - may be a Date object or a string depending on the database driver
          let formattedDate: string
          const transactionDate = transaction.transactionDate as Date | string
          if (transactionDate instanceof Date) {
            formattedDate = transactionDate.toISOString().split('T')[0]
          } else if (typeof transactionDate === 'string') {
            // If it is a string, get the date portion (YYYY-MM-DD)
            formattedDate = transactionDate.split('T')[0]
          } else {
            // Fallback: create a new Date object
            formattedDate = new Date(transactionDate as any).toISOString().split('T')[0]
          }
          
          return {
            date: formattedDate,
            amount: finalAmount,
            description: transaction.itemDescription || '',
            status: transaction.status || 'Pending',
            receipt_id: transaction.receiptId || null,
            type: transaction.type || TransactionType.EXPENSE,
          }
        }),
      };

      return accountData;
    } catch (error) {
      // If it is a NotFoundException or ForbiddenException, rethrow it
      if (error instanceof NotFoundException || error instanceof ForbiddenException) {
        throw error;
      }
      
      // Log errors for debugging (only in development)
      if (process.env.NODE_ENV !== 'production') {
        console.error('Error in findOneWithTransactions:', error);
      }
      
      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'A system error occurred while retrieving account details. Please try again later.',
      );
    }
  }

  /**
   * Update account information
   * @param accountId - ID of the account to update
   * @param userId - User ID (from JWT)
   * @param updateAccountDto - DTO containing update information
   * @returns The updated account
   */
  async update(accountId: number, userId: number, updateAccountDto: UpdateAccountDto) {
    try {
      // 1. Find the account by accountId
      const account = await this.accountRepository.findOne({
        where: { accountId },
      });

      // 2. Validation 1: Check whether the account exists
      if (!account) {
        throw new NotFoundException('This account was not found.');
      }

      // 3. Validation 2: Check ownership
      if (account.userId !== userId) {
        throw new ForbiddenException('You do not have permission to edit information about this account.');
      }

      // 4. Validation 3: Validate input data
      // Check that required fields are not empty
      if (!updateAccountDto.bank_name || updateAccountDto.bank_name.trim() === '') {
        throw new BadRequestException('Bank name must not be empty.');
      }

      if (!updateAccountDto.account_type) {
        throw new BadRequestException('Account type must not be empty.');
      }

      if (!updateAccountDto.account_number_full || updateAccountDto.account_number_full.trim() === '') {
        throw new BadRequestException('Full account number must not be empty.');
      }

      // Check that balance is a nonnegative number
      if (updateAccountDto.balance < 0) {
        throw new BadRequestException('balance must not be less than 0');
      }

      // 5. Get the last 4 digits of the account number if unavailable
      const accountNumberLast4 = updateAccountDto.account_number_last_4 
        || updateAccountDto.account_number_full.slice(-4);

      // 6. Update account information
      account.bankName = updateAccountDto.bank_name;
      account.accountType = updateAccountDto.account_type;
      account.branchName = updateAccountDto.branch_name || undefined;
      account.accountNumberFull = updateAccountDto.account_number_full;
      account.accountNumberLast4 = accountNumberLast4;
      account.balance = updateAccountDto.balance;

      const updatedAccount = await this.accountRepository.save(account);

      // 7. Return the updated account object
      return {
        account_id: updatedAccount.accountId,
        user_id: updatedAccount.userId,
        bank_name: updatedAccount.bankName,
        account_type: updatedAccount.accountType,
        branch_name: updatedAccount.branchName || null,
        account_number_full: updatedAccount.accountNumberFull,
        account_number_last_4: updatedAccount.accountNumberLast4,
        balance: Number(updatedAccount.balance),
      };
    } catch (error) {
      // If it is a NotFoundException, ForbiddenException, or BadRequestException, rethrow it
      if (
        error instanceof NotFoundException ||
        error instanceof ForbiddenException ||
        error instanceof BadRequestException
      ) {
        throw error;
      }

      // Log errors for debugging (only in development)
      if (process.env.NODE_ENV !== 'production') {
        console.error('Error in update account:', error);
      }

      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'An error occurred while saving data. Please try again later.',
      );
    }
  }

  /**
   * Delete an account and all related transactions
   * @param accountId - ID of the account to delete
   * @param userId - User ID (from JWT)
   * @returns Deleted account information
   */
  async delete(accountId: number, userId: number) {
    // Use a query runner to manage the transaction
    const queryRunner = this.dataSource.createQueryRunner();
    await queryRunner.connect();
    await queryRunner.startTransaction();

    try {
      // 1. Find the account by accountId
      const account = await queryRunner.manager.findOne(Account, {
        where: { accountId },
      });

      // 2. Validation 1: Check whether the account exists
      if (!account) {
        await queryRunner.rollbackTransaction();
        throw new NotFoundException('Account not found or not owned by current user');
      }

      // 3. Validation 2: Check ownership
      if (account.userId !== userId) {
        await queryRunner.rollbackTransaction();
        throw new NotFoundException('Account not found or not owned by current user');
      }

      // 4. Delete all transactions related to this account
      await queryRunner.manager.delete(Transaction, { accountId });

      // 5. Delete an account
      await queryRunner.manager.delete(Account, { accountId });

      // 6. Commit transaction
      await queryRunner.commitTransaction();

      // 7. Return the result
      return {
        deleted_account_id: accountId,
      };
    } catch (error) {
      // Roll back the transaction if an error occurs
      await queryRunner.rollbackTransaction();

      // If it is a NotFoundException, rethrow it
      if (error instanceof NotFoundException) {
        throw error;
      }

      // Log errors for debugging (only in development)
      if (process.env.NODE_ENV !== 'production') {
        console.error('Error in delete account:', error);
      }

      // For other errors, throw InternalServerErrorException
      throw new InternalServerErrorException(
        'A system error occurred, unable to delete the account and related transactions.',
      );
    } finally {
      // Release the query runner
      await queryRunner.release();
    }
  }
}
