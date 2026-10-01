import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { Transaction } from '../transaction/transaction.entity';
import { Goal } from '../goal/goal.entity';

@Entity('Categories')
export class Category {
  @PrimaryGeneratedColumn({ name: 'category_id' })
  categoryId: number;

  @Column({ name: 'category_name', type: 'varchar', length: 255, unique: true })
  categoryName: string;

  @OneToMany(() => Transaction, (transaction) => transaction.category)
  transactions: Transaction[];

  @OneToMany(() => Goal, (goal) => goal.category)
  goals: Goal[];

  // @CreateDateColumn({ name: 'created_at', type: 'timestamp', nullable: true })
  // createdAt: Date;

  // @UpdateDateColumn({ name: 'updated_at', type: 'timestamp', nullable: true })
  // updatedAt: Date;
}

