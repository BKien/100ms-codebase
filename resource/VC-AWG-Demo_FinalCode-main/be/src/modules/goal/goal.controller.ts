import {
  Controller,
  Get,
  Post,
  Put,
  UseGuards,
  Request,
  HttpCode,
  HttpStatus,
  Param,
  Body,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { GoalService } from './goal.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { UpdateGoalDto } from './dto/update-goal.dto';
import { CreateGoalDto } from './dto/create-goal.dto';

@ApiTags('goals')
@Controller('v1/goals')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class GoalController {
  constructor(private readonly goalService: GoalService) {}

  @Get()
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Take into account the user\'s savings and spending goals.' })
  @ApiResponse({
    status: 200,
    description: 'Get list of goals successfully',
  })
  @ApiResponse({
    status: 401,
    description: 'Unauthorized - Invalid or expired token',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getGoals(@Request() req) {
    const userId = req.user.userId;
    const goalsData = await this.goalService.getGoals(userId);

    return {
      success: true,
      message: 'Get list of goals successfully',
      data: goalsData,
    };
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create a new savings or spending goal' })
  @ApiResponse({
    status: 201,
    description: 'Goal created successfully',
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
    status: 500,
    description: 'System error',
  })
  async createGoal(@Request() req, @Body() createGoalDto: CreateGoalDto) {
    const userId = req.user.userId;
    const result = await this.goalService.createGoal(userId, createGoalDto);

    return {
      message: 'Goal created successfully',
      goal_id: result.goalId,
    };
  }

  @Put(':goalId')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Update a savings or spending goal' })
  @ApiResponse({
    status: 200,
    description: 'Goal updated successfully',
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
    description: 'Forbidden - I do not have permission to edit this target.',
  })
  @ApiResponse({
    status: 404,
    description: 'Not Found - Goal not found',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async updateGoal(
    @Request() req,
    @Param('goalId') goalId: string,
    @Body() updateGoalDto: UpdateGoalDto,
  ) {
    const userId = req.user.userId;
    const result = await this.goalService.updateGoal(
      parseInt(goalId, 10),
      userId,
      updateGoalDto,
    );

    return {
      message: 'Goal updated successfully',
      updated_goal: {
        goal_id: result.goalId,
        target_amount: Number(result.targetAmount),
      },
    };
  }
}

