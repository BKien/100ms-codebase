export class LoginResponseDto {
  accessToken: string;
  user: {
    id: number;
    fullName: string;
    email: string;
  };
}

