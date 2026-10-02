import 'reflect-metadata';
import { DataSource } from 'typeorm';

// Setup-only CLI. Run reviewed migrations outside experiment runs.
export default new DataSource({
  type: 'mysql',
  host: process.env.DB_HOST ?? 'database',
  port: Number(process.env.DB_PORT ?? 3306),
  username: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  charset: 'utf8mb4',
  timezone: 'Z',
  synchronize: false,
  migrationsRun: false,
  migrationsTableName: 'typeorm_migrations',
  migrations: [__dirname + '/migrations/*.js'],
});
