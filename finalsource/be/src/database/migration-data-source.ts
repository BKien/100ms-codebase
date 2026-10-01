import 'reflect-metadata';
import { DataSource } from 'typeorm';

// Setup-only CLI. Database preparation is deferred; no migration is supplied.
export default new DataSource({
  type: 'mysql',
  host: process.env.DB_HOST ?? 'database',
  port: Number(process.env.DB_PORT ?? 3306),
  username: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
  synchronize: false,
  migrationsRun: false,
  migrationsTableName: 'typeorm_migrations',
  migrations: [__dirname + '/migrations/*.js'],
});
