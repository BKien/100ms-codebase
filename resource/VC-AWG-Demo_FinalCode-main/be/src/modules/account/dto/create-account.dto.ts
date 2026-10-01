import { IsNotEmpty, IsString, IsNumber, Min, IsOptional, IsEnum } from 'class-validator';
import { AccountType } from '../account.entity';

export class CreateAccountDto {
  @IsNotEmpty({ message: 'The bank name cannot be left blank.' })
  @IsString({ message: 'The bank name must be a string.' })
  bank_name: string;

  @IsNotEmpty({ message: 'Account type cannot be left blank.' })
  @IsEnum(AccountType, { message: 'Invalid account type.' })
  account_type: AccountType;

  @IsOptional()
  @IsString({ message: 'The branch name must be a string.' })
  branch_name?: string;

  @IsNotEmpty({ message: 'The account number cannot be left blank.' })
  @IsString({ message: 'The account number must be a string.' })
  account_number_full: string;

  @IsNumber({}, { message: 'The balance must be a number.' })
  @Min(0, { message: 'The balance must be greater than or equal to 0.' })
  balance: number;
}

