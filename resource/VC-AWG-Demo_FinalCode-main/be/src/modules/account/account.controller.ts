import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  UseGuards,
  Request,
  Body,
  HttpCode,
  HttpStatus,
  Param,
  UnauthorizedException,
  BadRequestException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { AccountService } from './account.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { CreateAccountDto } from './dto/create-account.dto';
import { UpdateAccountDto } from './dto/update-account.dto';

@ApiTags('accounts')
@Controller('v1/accounts')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class AccountController {
  constructor(private readonly accountService: AccountService) {}

  @Get()
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get a list of user accounts.' })
  @ApiResponse({
    status: 200,
    description: 'Get list of successful accounts',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getAccounts(@Request() req) {
    const userId = req.user.userId;
    const accounts = await this.accountService.findAllByUserId(userId);

    return {
      success: true,
      message: 'Get list of accounts successfully',
      data: {
        user_id: userId,
        accounts,
      },
    };
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create a new account' })
  @ApiResponse({
    status: 201,
    description: 'Account created successfully',
  })
  @ApiResponse({
    status: 400,
    description: 'Invalid input data',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 409,
    description: 'Account already exists',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async createAccount(@Request() req, @Body() createAccountDto: CreateAccountDto) {
    const userId = req.user.userId;
    const account = await this.accountService.create(userId, createAccountDto);

    return {
      message: 'Account created successfully',
      account,
    };
  }

  @Get(':id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get account details with recent transactions' })
  @ApiResponse({
    status: 200,
    description: 'Get account details successfully',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 403,
    description: 'Forbidden - Permission not granted to view this account',
  })
  @ApiResponse({
    status: 404,
    description: 'Not Found - Account not found',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getAccountDetail(@Request() req, @Param('id') id: string) {
    // Check and get userId from the JWT payload
    if (!req.user || !req.user.userId) {
      throw new UnauthorizedException('User authentication failed. Please log in again.');
    }
    
    const userId = req.user.userId;
    const accountId = parseInt(id, 10);
    
    if (isNaN(accountId)) {
      throw new BadRequestException('Invalid account ID.');
    }
    
      const accountData = await this.accountService.findOneWithTransactions(accountId, userId);

    return accountData;
  }

  @Put(':id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Update account information' })
  @ApiResponse({
    status: 200,
    description: 'Account updated successfully',
  })
  @ApiResponse({
    status: 400,
    description: 'Invalid input data',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 403,
    description: 'Forbidden - Permission not granted to edit this account',
  })
  @ApiResponse({
    status: 404,
    description: 'Not Found - Account not found',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async updateAccount(
    @Request() req,
    @Param('id') id: string,
    @Body() updateAccountDto: UpdateAccountDto,
  ) {
    // Check and get userId from the JWT payload
    if (!req.user || !req.user.userId) {
      throw new UnauthorizedException('User authentication failed. Please log in again.');
    }

    const userId = req.user.userId;
    const accountId = parseInt(id, 10);

    if (isNaN(accountId)) {
      throw new BadRequestException('Invalid account ID.');
    }

    const updatedAccount = await this.accountService.update(accountId, userId, updateAccountDto);

    return {
      message: 'Account updated successfully',
      account: updatedAccount,
    };
  }

  @Delete(':id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Delete account and all related transactions' })
  @ApiResponse({
    status: 200,
    description: 'Account deleted successfully',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 404,
    description: 'Not Found - Account not found or not owned by the user',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async deleteAccount(@Request() req, @Param('id') id: string) {
    // Check and get userId from the JWT payload
    if (!req.user || !req.user.userId) {
      throw new UnauthorizedException('User authentication failed. Please log in again.');
    }

    const userId = req.user.userId;
    const accountId = parseInt(id, 10);

    if (isNaN(accountId)) {
      throw new BadRequestException('Invalid account ID.');
    }

    const result = await this.accountService.delete(accountId, userId);

    return {
      message: 'Account deleted successfully',
      deleted_account_id: result.deleted_account_id,
    };
  }
}

