import {
  IsNotEmpty,
  IsNumber,
  IsEnum,
  IsDateString,
  Min,
  IsOptional,
  ValidateIf,
} from 'class-validator';
import { GoalType } from '../goal.entity';

export class CreateGoalDto {
  @IsNotEmpty({ message: 'goal_type must not be empty' })
  @IsEnum(GoalType, { message: 'goal_type must be Saving or Expense_Limit' })
  goal_type: GoalType;

  @ValidateIf((o) => o.goal_type === GoalType.EXPENSE_LIMIT)
  @IsNotEmpty({ message: 'category_id must not be empty when goal_type is Expense_Limit' })
  @IsNumber({}, { message: 'category_id must be a number' })
  category_id?: number | null;

  @IsNotEmpty({ message: 'start_date must not be empty' })
  @IsDateString({}, { message: 'start_date must be in a valid date format (YYYY-MM-DD)' })
  start_date: string;

  @IsNotEmpty({ message: 'end_date must not be empty' })
  @IsDateString({}, { message: 'end_date must be in a valid date format (YYYY-MM-DD)' })
  end_date: string;

  @IsNotEmpty({ message: 'target_amount must not be empty' })
  @IsNumber({}, { message: 'target_amount must be a number' })
  @Min(0.01, { message: 'target_amount must be greater than 0' })
  target_amount: number;
}

