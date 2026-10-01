import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Get('api/health')
  getHealth(): {
    success: true;
    message: string;
    data: { status: 'ok' };
  } {
    return {
      success: true,
      message: 'Backend is healthy',
      data: { status: 'ok' },
    };
  }
}
