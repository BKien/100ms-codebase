import { IsEmail, IsNotEmpty, IsString } from 'class-validator';

export class LoginDto {
  @IsEmail({}, { message: 'Invalid email' })
  @IsNotEmpty({ message: 'Email must not be empty' })
  email: string;

  @IsString()
  @IsNotEmpty({ message: 'Password must not be empty' })
  password: string;
}

