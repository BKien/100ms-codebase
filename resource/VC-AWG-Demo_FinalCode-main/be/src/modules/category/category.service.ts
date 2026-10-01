import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Category } from './category.entity';

@Injectable()
export class CategoryService {
  constructor(
    @InjectRepository(Category)
    private categoryRepository: Repository<Category>,
  ) {}

  /**
   * Get a list of all categories
   * @returns Category list
   */
  async findAll() {
    try {
      const categories = await this.categoryRepository.find({
        select: ['categoryId', 'categoryName'],
        order: {
          categoryName: 'ASC',
        },
      });

      // Map data to return the correct format
      return categories.map((category) => ({
        category_id: category.categoryId,
        category_name: category.categoryName,
      }));
    } catch (error) {
      throw new InternalServerErrorException(
        'A system error occurred while retrieving the category list. Please try again later.',
      );
    }
  }

  /**
   * Get details of a category
   * @param categoryId - Category ID
   * @returns Category details
   */
  async findOne(categoryId: number) {
    try {
      const category = await this.categoryRepository.findOne({
        where: { categoryId },
        select: ['categoryId', 'categoryName'],
      });

      if (!category) {
        return null;
      }

      return {
        category_id: category.categoryId,
        category_name: category.categoryName,
      };
    } catch (error) {
      throw new InternalServerErrorException(
        'A system error occurred while retrieving category details. Please try again later.',
      );
    }
  }
}

