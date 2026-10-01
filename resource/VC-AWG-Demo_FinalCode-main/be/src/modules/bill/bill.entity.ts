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

@Entity('Bills')
export class Bill {
  @PrimaryGeneratedColumn({ name: 'bill_id' })
  billId: number;

  @Column({ name: 'user_id', type: 'int' })
  userId: number;

  @ManyToOne(() => User, (user) => user.bills)
  @JoinColumn({ name: 'user_id' })
  user: User;

  @Column({ name: 'due_date', type: 'date' })
  dueDate: Date;

  @Column({ name: 'logo_url', type: 'varchar', length: 500, nullable: true })
  logoUrl: string;

  @Column({ name: 'item_description', type: 'varchar', length: 500 })
  itemDescription: string;

  @Column({ name: 'last_charge_date', type: 'date', nullable: true })
  lastChargeDate: Date;

  @Column({
    name: 'amount',
    type: 'decimal',
    precision: 15,
    scale: 2,
  })
  amount: number;

  // @CreateDateColumn({ name: 'created_at', type: 'timestamp', nullable: true })
  // createdAt: Date;

  // @UpdateDateColumn({ name: 'updated_at', type: 'timestamp', nullable: true })
  // updatedAt: Date;
}

