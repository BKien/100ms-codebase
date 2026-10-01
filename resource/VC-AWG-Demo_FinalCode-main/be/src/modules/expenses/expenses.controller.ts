import {
  Controller,
  Get,
  UseGuards,
  Request,
  HttpCode,
  HttpStatus,
  Query,
  BadRequestException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { ExpensesService } from './expenses.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@ApiTags('expenses')
@Controller('v1/expenses')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class ExpensesController {
  constructor(private readonly expensesService: ExpensesService) {}

  @Get('summary')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get a summary of monthly expenses for the current year.' })
  @ApiResponse({
    status: 200,
    description: 'Get expense summary successfully',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getExpenseSummary(@Request() req) {
    const userId = req.user.userId;
    const summary = await this.expensesService.getExpenseSummary(userId);
    return {
      data: summary,
    };
  }

  @Get('breakdown')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get expenses breakdown by category for a specific month' })
  @ApiQuery({
    name: 'month',
    required: true,
    type: String,
    description: 'Month in YYYY-MM format (e.g., 2025-11)',
    example: '2025-11',
  })
  @ApiResponse({
    status: 200,
    description: 'Get expenses breakdown successfully',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 404,
    description: 'No expense data found for this month',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getExpensesBreakdown(@Request() req, @Query('month') month: string) {
    // Validation month parameter
    if (!month || !/^\d{4}-\d{2}$/.test(month)) {
      throw new BadRequestException({
        error: 'Invalid month parameter. Please use the format YYYY-MM (e.g., 2025-11)',
      });
    }

    const userId = req.user.userId;
    const breakdown = await this.expensesService.getExpensesBreakdown(userId, month);
    return {
      data: breakdown,
    };
  }
}

