import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { databaseConfig } from './config/database.config';

@Module({ imports: [TypeOrmModule.forRoot(databaseConfig())], controllers: [AppController] })
export class AppModule {}
