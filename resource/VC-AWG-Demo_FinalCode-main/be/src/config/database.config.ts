import { registerAs } from '@nestjs/config';
import { TypeOrmModuleOptions } from '@nestjs/typeorm';

export default registerAs(
  'database',
  (): TypeOrmModuleOptions => ({
    type: 'mysql',
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '3306', 10),
    username: process.env.DB_USERNAME || 'root',
    password: process.env.DB_PASSWORD || 'aod@123',
    database: process.env.DB_DATABASE || 'financial1',
    entities: [__dirname + '/../**/*.entity{.ts,.js}'],
    synchronize: false, // The database has already been created, do not synchronize automatically
    logging: process.env.NODE_ENV === 'development',
  }),
);

