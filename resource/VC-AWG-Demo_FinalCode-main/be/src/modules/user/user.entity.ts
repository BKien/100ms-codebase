import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { Account } from '../account/account.entity';
import { Bill } from '../bill/bill.entity';
import { Goal } from '../goal/goal.entity';

@Entity('Users')
export class User {
  @PrimaryGeneratedColumn({ name: 'user_id' })
  userId: number;

  @Column({ name: 'full_name', type: 'varchar', length: 255 })
  fullName: string;

  @Column({ name: 'email', type: 'varchar', length: 255, unique: true })
  email: string;

  @Column({ name: 'username', type: 'varchar', length: 255, unique: true })
  username: string;

  @Column({ name: 'password', type: 'varchar', length: 255 })
  password: string;

  @Column({ name: 'phone_number', type: 'varchar', length: 20, nullable: true })
  phoneNumber: string;

  @Column({
    name: 'profile_picture_url',
    type: 'varchar',
    length: 500,
    nullable: true,
  })
  profilePictureUrl: string;

  @Column({
    name: 'total_balance',
    type: 'decimal',
    precision: 15,
    scale: 2,
    default: 0,
  })
  totalBalance: number;

  @OneToMany(() => Account, (account) => account.user)
  accounts: Account[];

  @OneToMany(() => Bill, (bill) => bill.user)
  bills: Bill[];

  @OneToMany(() => Goal, (goal) => goal.user)
  goals: Goal[];

//   @CreateDateColumn({ name: 'created_at', type: 'timestamp', nullable: true })
//   createdAt: Date;

//   @UpdateDateColumn({ name: 'updated_at', type: 'timestamp', nullable: true })
//   updatedAt: Date;
}

