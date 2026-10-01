import {
  IsNotEmpty,
  IsString,
  IsNumber,
  Min,
  IsOptional,
  IsEnum,
  IsDateString,
} from 'class-validator';
import { TransactionType, TransactionStatus } from '../transaction.entity';

export class CreateTransactionDto {
  @IsNotEmpty({ message: 'Account ID must not be empty' })
  @IsNumber({}, { message: 'Account ID must be a number' })
  accountId: number;

  @IsNotEmpty({ message: 'Transaction date must not be empty' })
  @IsDateString({}, { message: 'Invalid transaction date' })
  transactionDate: string;

  @IsNotEmpty({ message: 'Transaction type must not be empty' })
  @IsEnum(TransactionType, { message: 'Transaction type must be Revenue or Expense' })
  type: TransactionType;

  @IsNotEmpty({ message: 'Transaction description must not be empty' })
  @IsString({ message: 'Transaction description must be a string' })
  itemDescription: string;

  @IsOptional()
  @IsNumber({}, { message: 'Category ID must be a number' })
  category_id?: number;

  @IsOptional()
  @IsString({ message: 'Store name must be a string' })
  shopName?: string;

  @IsNotEmpty({ message: 'Amount must not be empty' })
  @IsNumber({}, { message: 'Amount must be a number' })
  @Min(0.01, { message: 'Amount must be greater than 0' })
  amount: number;

  @IsOptional()
  @IsString({ message: 'Payment method must be a string' })
  paymentMethod?: string;

  @IsOptional()
  @IsEnum(TransactionStatus, { message: 'Invalid status' })
  status?: TransactionStatus;
}

