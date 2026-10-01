import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, MoreThanOrEqual } from 'typeorm';
import { Bill } from './bill.entity';

@Injectable()
export class BillService {
  constructor(
    @InjectRepository(Bill)
    private billRepository: Repository<Bill>,
  ) {}

  /**
   * Get the user's upcoming bills
   * @param userId - User ID
   * @returns Filtered and sorted bill list
   */
  async findUpcomingBillsByUserId(userId: number) {
    try {
      const currentDate = new Date();
      // Set the time to 00:00:00 to compare dates only
      currentDate.setHours(0, 0, 0, 0);

      const bills = await this.billRepository.find({
        where: {
          userId,
          dueDate: MoreThanOrEqual(currentDate),
        },
        order: {
          dueDate: 'ASC',
        },
      });

      // Map data to return the correct format
      return bills.map((bill) => ({
        billId: bill.billId,
        userId: bill.userId,
        itemDescription: bill.itemDescription,
        logoUrl: bill.logoUrl || null,
        dueDate: this.formatDate(bill.dueDate),
        lastChargeDate: bill.lastChargeDate ? this.formatDate(bill.lastChargeDate) : null,
        amount: Number(bill.amount),
      }));
    } catch (error) {
      // Log errors for debugging (only in development)
      if (process.env.NODE_ENV !== 'production') {
        console.error('Error in findUpcomingBillsByUserId:', error);
      }

      throw new InternalServerErrorException({
        message: 'Failed to fetch bills',
      });
    }
  }

  /**
   * Format date as a YYYY-MM-DD string
   * @param date - Date object or string
   * @returns String date format YYYY-MM-DD
   */
  private formatDate(date: Date | string): string {
    if (date instanceof Date) {
      return date.toISOString().split('T')[0];
    } else if (typeof date === 'string') {
      // If it is a string, get the date portion (YYYY-MM-DD)
      return date.split('T')[0];
    }
    // Fallback
    return new Date(date as any).toISOString().split('T')[0];
  }
}

