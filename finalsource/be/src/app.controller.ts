import { Controller, Get, ServiceUnavailableException } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Controller('health')
export class AppController {
  constructor(private readonly database: DataSource) {}

  @Get()
  async health(): Promise<{ success: true; message: string; data: { status: string; database: string } }> {
    try {
      await this.database.query('SELECT 1');
    } catch {
      throw new ServiceUnavailableException('Database unavailable');
    }
    return { success: true, message: 'Backend is healthy', data: { status: 'ok', database: 'connected' } };
  }
}
