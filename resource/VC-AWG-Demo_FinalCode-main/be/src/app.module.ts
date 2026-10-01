import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { DatabaseModule } from './database/database.module';
import { AuthModule } from './modules/auth/auth.module';
import { AccountModule } from './modules/account/account.module';
import { TransactionModule } from './modules/transaction/transaction.module';
import { CategoryModule } from './modules/category/category.module';
import { BillModule } from './modules/bill/bill.module';
import { ExpensesModule } from './modules/expenses/expenses.module';
import { GoalModule } from './modules/goal/goal.module';
import { SavingsModule } from './modules/savings/savings.module';

@Module({
  imports: [DatabaseModule, AuthModule, AccountModule, TransactionModule, CategoryModule, BillModule, ExpensesModule, GoalModule, SavingsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

