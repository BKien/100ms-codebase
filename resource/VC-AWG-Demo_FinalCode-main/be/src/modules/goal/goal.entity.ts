import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { User } from '../user/user.entity';
import { Category } from '../category/category.entity';

export enum GoalType {
  SAVING = 'Saving',
  EXPENSE_LIMIT = 'Expense_Limit',
}

@Entity('Goals')
export class Goal {
  @PrimaryGeneratedColumn({ name: 'goal_id' })
  goalId: number;

  @Column({ name: 'user_id', type: 'int' })
  userId: number;

  @ManyToOne(() => User, (user) => user.goals)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({
    name: 'goal_type',
    type: 'enum',
    enum: GoalType,
  })
  goalType: GoalType;

  @Column({ name: 'category_id', type: 'int', nullable: true })
  categoryId: number | null;

  @ManyToOne(() => Category, (category) => category.goals, { nullable: true })
  @JoinColumn({ name: 'category_id' })
  category: Category | null;

  @Column({ name: 'start_date', type: 'date' })
  startDate: Date;

  @Column({ name: 'end_date', type: 'date' })
  endDate: Date;

  @Column({
    name: 'target_amount',
    type: 'decimal',
    precision: 15,
    scale: 2,
  })
  targetAmount: number;

  // @Column({
  //   name: 'target_achieved',
  //   type: 'decimal',
  //   precision: 15,
  //   scale: 2,
  //   default: 0,
  // })
  // targetAchieved: number;

  // @Column({ name: 'last_updated', type: 'timestamp', nullable: true })
  // lastUpdated: Date;

  // @CreateDateColumn({ name: 'created_at', type: 'timestamp', nullable: true })
  // createdAt: Date;

  // @UpdateDateColumn({ name: 'updated_at', type: 'timestamp', nullable: true })
  // updatedAt: Date;
}

