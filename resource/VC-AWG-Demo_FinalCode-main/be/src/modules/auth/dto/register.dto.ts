import { IsEmail, IsNotEmpty, IsString, Matches } from 'class-validator';

export class RegisterDto {
  @IsString()
  @IsNotEmpty({ message: 'Full name must not be empty' })
  fullName: string;

  @IsEmail({}, { message: 'Invalid email' })
  @IsNotEmpty({ message: 'Email must not be empty' })
  email: string;

  @IsString()
  @IsNotEmpty({ message: 'Password must not be empty' })
  password: string;

  @IsString()
  @IsNotEmpty({ message: 'Confirm password must not be empty' })
  confirmPassword: string;
}

