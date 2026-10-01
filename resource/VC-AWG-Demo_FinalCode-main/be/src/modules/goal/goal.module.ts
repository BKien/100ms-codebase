import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { GoalController } from './goal.controller';
import { GoalService } from './goal.service';
import { Goal } from './goal.entity';
import { Account } from '../account/account.entity';
import { Transaction } from '../transaction/transaction.entity';
import { Category } from '../category/category.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Goal, Account, Transaction, Category])],
  controllers: [GoalController],
  providers: [GoalService],
  exports: [GoalService],
})
export class GoalModule {}

