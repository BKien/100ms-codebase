import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class AppController {
  @Get()
  health(): { success: true; message: string; data: { status: string; database: string } } {
    return { success: true, message: 'Backend is healthy', data: { status: 'ok', database: 'not-configured' } };
  }
}
