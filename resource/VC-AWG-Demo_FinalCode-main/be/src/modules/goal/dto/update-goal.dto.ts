import { IsNotEmpty, IsNumber, Min } from 'class-validator';

export class UpdateGoalDto {
  @IsNotEmpty({ message: 'target_amount must not be empty' })
  @IsNumber({}, { message: 'target_amount must be a number' })
  @Min(0.01, { message: 'target_amount must be a positive number' })
  target_amount: number;
}

