import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus } from '@nestjs/common';
import type { Request, Response } from 'express';

@Catch()
export class PublicExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost): void {
    const context = host.switchToHttp();
    const request = context.getRequest<Request>();
    const response = context.getResponse<Response>();
    const statusCode = exception instanceof HttpException ? exception.getStatus() : HttpStatus.INTERNAL_SERVER_ERROR;
    const details: unknown = exception instanceof HttpException ? exception.getResponse() : null;
    let message: string | string[] = 'Internal server error';
    if (exception instanceof HttpException) {
      if (typeof details === 'string') message = details;
      else if (details && typeof details === 'object' && 'message' in details) {
        const candidate: unknown = details.message;
        if (typeof candidate === 'string' || (Array.isArray(candidate) && candidate.every((item: unknown) => typeof item === 'string'))) {
          message = candidate;
        }
      }
    }
    const businessFields: Record<string, string> = {};
    if (details && typeof details === 'object') {
      for (const field of ['code', 'requestId']) {
        if (field in details) {
          const value: unknown = (details as Record<string, unknown>)[field];
          if (typeof value === 'string') businessFields[field] = value;
        }
      }
    }
    response.status(statusCode).json({ success: false, statusCode, message, timestamp: new Date().toISOString(), path: request.path, ...businessFields });
  }
}
