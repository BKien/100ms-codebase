import { IsNotEmpty, IsString, IsNumber, Min, IsOptional, IsEnum } from 'class-validator';
import { AccountType } from '../account.entity';

export class UpdateAccountDto {
  @IsNotEmpty({ message: 'Bank name must not be empty' })
  @IsString({ message: 'Bank name must be a string' })
  bank_name: string;

  @IsNotEmpty({ message: 'Account type must not be empty' })
  @IsEnum(AccountType, { message: 'Invalid account type' })
  account_type: AccountType;

  @IsOptional()
  @IsString({ message: 'Branch name must be a string' })
  branch_name?: string;

  @IsNotEmpty({ message: 'Full account number must not be empty' })
  @IsString({ message: 'Full account number must be a string' })
  account_number_full: string;

  @IsOptional()
  @IsString({ message: 'The last 4 digits of the account number must be a string' })
  account_number_last_4?: string;

  @IsNumber({}, { message: 'Balance must be a number' })
  @Min(0, { message: 'balance must not be less than 0' })
  balance: number;
}

