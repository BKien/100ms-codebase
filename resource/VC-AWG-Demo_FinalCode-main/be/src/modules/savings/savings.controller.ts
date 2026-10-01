import {
  Controller,
  Get,
  UseGuards,
  Request,
  Query,
  HttpCode,
  HttpStatus,
  UnauthorizedException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth, ApiQuery } from '@nestjs/swagger';
import { SavingsService } from './savings.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { SavingsSummaryResponse } from './dto/savings-summary-response.dto';

@ApiTags('savings')
@Controller('v1/savings')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class SavingsController {
  constructor(private readonly savingsService: SavingsService) {}

  @Get('summary')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Calculate the total monthly savings for the specified year.' })
  @ApiQuery({
    name: 'year',
    required: false,
    type: Number,
    description: 'Year to get data (default is the current year)',
    example: 2025,
  })
  @ApiResponse({
    status: 200,
    description: 'Get savings summary successfully',
    schema: {
      type: 'object',
      properties: {
        user_id: { type: 'number', example: 1 },
        year: { type: 'number', example: 2025 },
        summary: {
          type: 'object',
          properties: {
            this_year: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  month: { type: 'string', example: '01' },
                  amount: { type: 'number', example: 1500000 },
                },
              },
            },
            last_year: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  month: { type: 'string', example: '01' },
                  amount: { type: 'number', example: 1200000 },
                },
              },
            },
          },
        },
      },
    },
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getSavingsSummary(
    @Request() req,
    @Query('year') year?: string,
  ): Promise<SavingsSummaryResponse> {
    // Check and get userId from the JWT payload
    if (!req.user || !req.user.userId) {
      throw new UnauthorizedException('User authentication failed. Please log in again.');
    }

    const userId = req.user.userId;

    // Handle the year parameter: if missing or invalid, default to the current year
    let targetYear: number;
    if (year) {
      const parsedYear = parseInt(year, 10);
      if (isNaN(parsedYear) || parsedYear < 1900 || parsedYear > 2100) {
        // If year is invalid, use the current year
        targetYear = new Date().getFullYear();
      } else {
        targetYear = parsedYear;
      }
    } else {
      targetYear = new Date().getFullYear();
    }

    const result = await this.savingsService.getSavingsSummary(userId, targetYear);

    return result;
  }
}

