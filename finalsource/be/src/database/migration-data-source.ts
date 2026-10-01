import 'reflect-metadata';
import { DataSource } from 'typeorm';

// Researcher setup only. The application never imports this CLI DataSource.
function required(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing migration connection setting: ${name}`);
  return value;
}

export default new DataSource({
  type: 'mysql',
  host: required('DB_HOST'),
  port: Number(required('DB_PORT')),
  username: required('DB_USERNAME'),
  password: required('DB_PASSWORD'),
  database: required('DB_DATABASE'),
  entities: [__dirname + '/../**/*.entity.js'],
  migrations: [__dirname + '/migrations/*.js'],
  migrationsTableName: 'typeorm_migrations',
  synchronize: false,
  migrationsRun: false,
  migrationsTransactionMode: 'none',
  logging: false,
});
