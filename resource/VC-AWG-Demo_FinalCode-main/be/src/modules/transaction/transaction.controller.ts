import {
  Controller,
  Get,
  Post,
  UseGuards,
  Request,
  Body,
  Query,
  HttpCode,
  HttpStatus,
  ParseIntPipe,
  DefaultValuePipe,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { TransactionService } from './transaction.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { CreateTransactionDto } from './dto/create-transaction.dto';

@ApiTags('transactions')
@Controller('v1/transactions')
@ApiBearerAuth()
export class TransactionController {
  constructor(private readonly transactionService: TransactionService) {}

  @Get()
  @UseGuards(JwtAuthGuard)
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get a list of user transactions.' })
  @ApiResponse({
    status: 200,
    description: 'Get list of transactions successfully',
  })
  @ApiResponse({
    status: 400,
    description: 'Invalid type parameter',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getTransactions(
    @Request() req,
    @Query('type') type: string,
    @Query('limit', new DefaultValuePipe(10), ParseIntPipe) limit: number,
    @Query('offset', new DefaultValuePipe(0), ParseIntPipe) offset: number,
  ) {
    const userId = req.user.userId;
    const result = await this.transactionService.findAllByUserId(
      userId,
      type,
      limit,
      offset,
    );

    return result;
  }

  @Post()
  @UseGuards(JwtAuthGuard)
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create a new transaction' })
  @ApiResponse({
    status: 201,
    description: 'Create transaction successfully',
  })
  @ApiResponse({
    status: 400,
    description: 'Invalid or missing transaction data',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async createTransaction(@Request() req, @Body() createTransactionDto: CreateTransactionDto) {
    const userId = req.user.userId;
    const result = await this.transactionService.create(userId, createTransactionDto);
    return result;
  }
}

