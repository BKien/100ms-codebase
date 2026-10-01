import { Injectable, UnauthorizedException, ConflictException, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import { User } from '../user/user.entity';
import { LoginDto } from './dto/login.dto';
import { LoginResponseDto } from './dto/login-response.dto';
import { RegisterDto } from './dto/register.dto';

@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private jwtService: JwtService,
  ) {}

  async login(loginDto: LoginDto): Promise<LoginResponseDto> {
    const { email, password } = loginDto;

    // Find the user by email
    const user = await this.userRepository.findOne({
      where: { email },
    });

    // Check whether the user exists
    if (!user) {
      throw new UnauthorizedException('Incorrect email or password.');
    }

    // Compare the password with the hash
    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      throw new UnauthorizedException('Incorrect email or password.');
    }

    // Create a JWT token
    const payload = { sub: user.userId, email: user.email };
    const accessToken = this.jwtService.sign(payload);

    // Return accessToken and user information
    return {
      accessToken,
      user: {
        id: user.userId,
        fullName: user.fullName,
        email: user.email,
      },
    };
  }

  async register(registerDto: RegisterDto) {
    const { fullName, email, password, confirmPassword } = registerDto;

    // Check whether password and confirmPassword match
    if (password !== confirmPassword) {
      throw new BadRequestException({ error: 'Passwords do not match.' });
    }

    // Check whether the email already exists
    const existingUser = await this.userRepository.findOne({
      where: { email },
    });

    if (existingUser) {
      throw new ConflictException({ error: 'This email is already registered.' });
    }

    // Hash the password
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create a username from the email (take the portion before @)
    let username = email.split('@')[0];
    let usernameCounter = 1;
    
    // Check and create a unique username if needed
    let existingUsername = await this.userRepository.findOne({
      where: { username },
    });
    
    while (existingUsername) {
      username = `${email.split('@')[0]}${usernameCounter}`;
      existingUsername = await this.userRepository.findOne({
        where: { username },
      });
      usernameCounter++;
    }

    // Create a new user
    const newUser = this.userRepository.create({
      fullName,
      email,
      username,
      password: hashedPassword,
      totalBalance: 0,
    });

    const savedUser = await this.userRepository.save(newUser);

    // Create a JWT token
    const payload = { sub: savedUser.userId, email: savedUser.email };
    const accessToken = this.jwtService.sign(payload);

    // Return user information and the token
    return {
      message: 'Registration successful',
      user: {
        id: savedUser.userId,
        fullName: savedUser.fullName,
        email: savedUser.email,
      },
      token: accessToken,
    };
  }
}

