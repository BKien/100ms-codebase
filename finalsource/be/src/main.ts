import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import type { CorsOptions } from '@nestjs/common/interfaces/external/cors-options.interface';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Configure CORS
  const allowedOrigins = process.env.CORS_ORIGINS
    ? process.env.CORS_ORIGINS.split(',')
    : ['http://localhost:3000', 'http://localhost:5173'];

  const corsOptions: CorsOptions = {
    origin: (origin, callback) => {
      // Allow requests without an origin (mobile apps, Postman, etc.)
      if (!origin) {
        return callback(null, true);
      }
      // Check whether the origin is in the allowed list
      if (allowedOrigins.indexOf(origin) !== -1 || process.env.NODE_ENV === 'development') {
        callback(null, true);
      } else {
        callback(new Error('Not allowed by CORS'));
      }
    },
    credentials: true, // Allow cookies and authorization headers to be sent
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Accept'],
    exposedHeaders: ['Authorization'],
  };

  app.enableCors(corsOptions);

  // Configure Swagger
  const config = new DocumentBuilder()
    .setTitle('Financial Management API')
    .setDescription('API documentation for the financial management application')
    .setVersion('1.0')
    .addBearerAuth(
      {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
        name: 'JWT',
        description: 'Enter JWT token',
        in: 'header',
      },
      'JWT-auth', // This name here is important for matching up with @ApiBearerAuth() in your controller!
    )
    .addTag('auth', 'User authentication')
    .addTag('users', 'User management')
    .addTag('accounts', 'Account management')
    .addTag('transactions', 'Transaction management')
    .addTag('bills', 'Bill management')
    .addTag('goals', 'Goal management')
    .addTag('expenses', 'Expense management')
    .addTag('categories', 'Category management')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document, {
    swaggerOptions: {
      persistAuthorization: true,
    },
  });

  await app.listen(process.env.PORT ?? 8000);
  console.log(`🚀 Application is running on: http://localhost:${process.env.PORT ?? 8000}`);
  console.log(`📚 Swagger documentation: http://localhost:${process.env.PORT ?? 8000}/api/docs`);
}
bootstrap();
