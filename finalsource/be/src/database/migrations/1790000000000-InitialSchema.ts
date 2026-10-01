import { MigrationInterface, QueryRunner } from 'typeorm';

export class InitialSchema1790000000000 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    // Do not adopt pre-existing tables without a researcher-reviewed migration.
    await queryRunner.query(`CREATE TABLE users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(255),
      role VARCHAR(50),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )`);
    await queryRunner.query(`CREATE TABLE posts (
      id INT AUTO_INCREMENT PRIMARY KEY,
      title VARCHAR(255),
      body TEXT COMMENT 'Content of the post',
      user_id INT,
      status ENUM('draft', 'published', 'private') COMMENT 'private: visible via URL only',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )`);
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query('DROP TABLE posts');
    await queryRunner.query('DROP TABLE users');
  }
}
