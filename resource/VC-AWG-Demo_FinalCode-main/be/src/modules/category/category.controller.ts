import {
  Controller,
  Get,
  Param,
  HttpCode,
  HttpStatus,
  ParseIntPipe,
  NotFoundException,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { CategoryService } from './category.service';

@ApiTags('categories')
@Controller('categories')
export class CategoryController {
  constructor(private readonly categoryService: CategoryService) {}

  @Get()
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get a list of all categories' })
  @ApiResponse({
    status: 200,
    description: 'Get list of categories successfully',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getCategories() {
    const categories = await this.categoryService.findAll();

    return {
      success: true,
      message: 'Get list of categories successfully',
      data: categories,
    };
  }

  @Get(':id')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Get details of a category' })
  @ApiResponse({
    status: 200,
    description: 'Get category details successfully',
  })
  @ApiResponse({
    status: 404,
    description: 'Category not found',
  })
  @ApiResponse({
    status: 500,
    description: 'System error',
  })
  async getCategory(@Param('id', ParseIntPipe) id: number) {
    const category = await this.categoryService.findOne(id);

    if (!category) {
      throw new NotFoundException('Category not found');
    }

    return {
      success: true,
      message: 'Get category details successfully',
      data: category,
    };
  }
}

