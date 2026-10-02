import { MigrationInterface, QueryRunner } from 'typeorm';

// Researcher-authorized setup. MySQL 8.4, mysql84-tables-v1; source snapshot remains immutable.
// Digest lookup is NON-unique. MutationGateway must lock session and compare the complete key.
export class Initial100msSchema1790916544190 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query("SET SESSION time_zone = '+00:00'");
    await queryRunner.query(`CREATE TABLE \`users\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`display_name\` VARCHAR(50) NOT NULL,
  \`created_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`principals\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`user_id\` CHAR(36) NULL,
  \`created_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`virtual_backgrounds\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`name\` VARCHAR(160) NOT NULL,
  \`asset_reference\` VARCHAR(255) NOT NULL UNIQUE,
  \`active\` BOOLEAN NOT NULL DEFAULT TRUE,
  \`created_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`sessions\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`kind\` ENUM('LIVE_STREAM','VIDEO_CONFERENCE') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`status\` ENUM('LOBBY','LIVE','ENDED') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT 'LOBBY',
  \`designated_host_principal_id\` CHAR(36) NOT NULL,
  \`host_participant_id\` CHAR(36) NULL,
  \`spotlighted_participant_id\` CHAR(36) NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`sessions_version_positive\` CHECK (version > 0),
  \`created_at\` DATETIME NOT NULL,
  \`ended_at\` DATETIME NULL,
  INDEX \`sessions_status_created_at_idx\` (\`status\`, \`created_at\`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`participants\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`user_id\` CHAR(36) NULL,
  \`principal_id\` CHAR(36) NOT NULL,
  \`microphone_enabled\` BOOLEAN NOT NULL DEFAULT FALSE,
  \`camera_enabled\` BOOLEAN NOT NULL DEFAULT FALSE,
  \`display_name\` VARCHAR(50) NOT NULL,
  \`role\` ENUM('HOST','BROADCASTER','VIEWER','STAGE_PARTICIPANT') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`status\` ENUM('JOINED','LEFT') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`joined_at\` DATETIME NOT NULL,
  \`left_at\` DATETIME NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`participants_version_positive\` CHECK (version > 0),
  INDEX \`participants_session_id_status_idx\` (\`session_id\`, \`status\`),
  INDEX \`participants_session_id_user_id_idx\` (\`session_id\`, \`user_id\`),
  UNIQUE INDEX \`participants_session_identity\` (\`session_id\`, \`id\`),
  UNIQUE INDEX \`one_joined_membership\` (session_id, ((CASE WHEN status = 'JOINED' THEN principal_id ELSE NULL END))),
  UNIQUE INDEX \`one_joined_host\` (((CASE WHEN status = 'JOINED' AND role = 'HOST' THEN session_id ELSE NULL END))),
  CONSTRAINT \`participant_display_name\` CHECK (display_name = TRIM(display_name) AND CHAR_LENGTH(display_name) BETWEEN 1 AND 50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`live_streams\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL UNIQUE,
  \`status\` ENUM('READY','STARTING','LIVE','ENDED') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`live_streams_version_positive\` CHECK (version > 0),
  \`started_at\` DATETIME NULL,
  \`ended_at\` DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`stage_requests\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`participant_id\` CHAR(36) NOT NULL,
  \`status\` ENUM('PENDING','ACCEPTED','REJECTED','CANCELLED') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`decided_by_participant_id\` CHAR(36) NULL,
  \`created_at\` DATETIME NOT NULL,
  \`decided_at\` DATETIME NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`stage_requests_version_positive\` CHECK (version > 0),
  INDEX \`stage_requests_session_id_participant_id_status_idx\` (\`session_id\`, \`participant_id\`, \`status\`),
  UNIQUE INDEX \`one_pending_stage_request\` (session_id, participant_id, ((CASE WHEN status = 'PENDING' THEN 1 ELSE NULL END)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`chat_messages\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`sender_participant_id\` CHAR(36) NOT NULL,
  \`body\` TEXT NOT NULL,
  \`sent_at\` DATETIME NOT NULL,
  \`sequence\` BIGINT NOT NULL,
  UNIQUE INDEX \`chat_messages_sequence\` (\`session_id\`, \`sequence\`),
  CONSTRAINT \`message_body_shape\` CHECK (body = TRIM(body) AND CHAR_LENGTH(body) BETWEEN 1 AND 1000),
  CONSTRAINT \`message_sequence_positive\` CHECK (sequence > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`reaction_events\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`participant_id\` CHAR(36) NOT NULL,
  \`reaction\` ENUM('LIKE','CLAP','HEART','CELEBRATE','HAND','SURPRISE') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`created_at\` DATETIME NOT NULL,
  \`sequence\` BIGINT NOT NULL,
  UNIQUE INDEX \`reaction_events_sequence\` (\`session_id\`, \`sequence\`),
  CONSTRAINT \`reaction_sequence_positive\` CHECK (sequence > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`content_shares\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`owner_participant_id\` CHAR(36) NOT NULL,
  \`kind\` ENUM('SCREEN','PDF') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`status\` ENUM('ACTIVE','STOPPED') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`source_reference\` TEXT NOT NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`content_shares_version_positive\` CHECK (version > 0),
  \`started_at\` DATETIME NOT NULL,
  \`stopped_at\` DATETIME NULL,
  INDEX \`content_shares_session_id_status_idx\` (\`session_id\`, \`status\`),
  UNIQUE INDEX \`one_active_share\` (((CASE WHEN status = 'ACTIVE' THEN session_id ELSE NULL END))),
  CONSTRAINT \`share_source_present\` CHECK (CHAR_LENGTH(TRIM(source_reference)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`media_preferences\` (
  \`participant_id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`microphone_device_id\` TEXT NULL,
  \`camera_device_id\` TEXT NULL,
  \`speaker_device_id\` TEXT NULL,
  \`virtual_background_id\` CHAR(36) NULL,
  \`updated_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`view_preferences\` (
  \`participant_id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`layout\` ENUM('EQUAL_PROMINENCE','SIDEBAR','PRESENTER') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT 'EQUAL_PROMINENCE',
  \`focused_participant_id\` CHAR(36) NULL,
  \`side_panel\` ENUM('CHAT','PARTICIPANTS','SETTINGS') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL,
  \`picture_in_picture\` BOOLEAN NOT NULL DEFAULT FALSE,
  \`updated_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`recordings\` (
  \`created_at\` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`started_by_participant_id\` CHAR(36) NOT NULL,
  \`status\` ENUM('IDLE','STARTING','RECORDING','STOPPED','FAILED') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`provider_reference\` VARCHAR(255) NULL,
  \`version\` INT NOT NULL DEFAULT 1,
  CONSTRAINT \`recordings_version_positive\` CHECK (version > 0),
  \`started_at\` DATETIME NULL,
  \`stopped_at\` DATETIME NULL,
  INDEX \`recordings_session_id_status_idx\` (\`session_id\`, \`status\`),
  UNIQUE INDEX \`one_active_recording\` (((CASE WHEN status IN ('STARTING', 'RECORDING') THEN session_id ELSE NULL END)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`departures\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`session_id\` CHAR(36) NOT NULL,
  \`participant_id\` CHAR(36) NOT NULL,
  \`kind\` ENUM('LEAVE','END') CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  \`created_at\` DATETIME NOT NULL,
  INDEX \`departures_session_id_participant_id_created_at_idx\` (\`session_id\`, \`participant_id\`, \`created_at\`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`mutation_responses\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`http_status\` INT NOT NULL,
  \`response_body\` JSON NOT NULL,
  \`created_at\` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`CREATE TABLE \`idempotency_records\` (
  \`id\` CHAR(36) NOT NULL PRIMARY KEY,
  \`principal_id\` CHAR(36) NOT NULL,
  \`session_id\` CHAR(36) NOT NULL,
  \`operation\` VARCHAR(160) NOT NULL,
  \`idempotency_key\` TEXT NOT NULL,
  \`idempotency_key_digest\` BINARY(32) GENERATED ALWAYS AS (UNHEX(SHA2(CAST(idempotency_key AS BINARY), 256))) STORED,
  \`payload_hash\` CHAR(64) NOT NULL,
  \`response_reference\` CHAR(36) NOT NULL,
  \`completed_at\` DATETIME NOT NULL,
  \`expires_at\` DATETIME NOT NULL,
  INDEX \`idempotency_key_lookup\` (principal_id, session_id, operation, idempotency_key_digest),
  CONSTRAINT \`idempotency_key_present\` CHECK (CHAR_LENGTH(TRIM(idempotency_key)) > 0),
  CONSTRAINT \`idempotency_expiry\` CHECK (expires_at = TIMESTAMPADD(HOUR, 24, completed_at))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin ROW_FORMAT=DYNAMIC`);
    await queryRunner.query(`ALTER TABLE \`principals\` ADD CONSTRAINT \`principals_user_id_fk\` FOREIGN KEY (\`user_id\`) REFERENCES \`users\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`sessions\` ADD CONSTRAINT \`sessions_designated_host_principal_id_fk\` FOREIGN KEY (\`designated_host_principal_id\`) REFERENCES \`principals\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`participants\` ADD CONSTRAINT \`participants_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`participants\` ADD CONSTRAINT \`participants_user_id_fk\` FOREIGN KEY (\`user_id\`) REFERENCES \`users\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`participants\` ADD CONSTRAINT \`participants_principal_id_fk\` FOREIGN KEY (\`principal_id\`) REFERENCES \`principals\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`live_streams\` ADD CONSTRAINT \`live_streams_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`stage_requests\` ADD CONSTRAINT \`stage_requests_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`chat_messages\` ADD CONSTRAINT \`chat_messages_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`reaction_events\` ADD CONSTRAINT \`reaction_events_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`content_shares\` ADD CONSTRAINT \`content_shares_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`media_preferences\` ADD CONSTRAINT \`media_preferences_participant_id_fk\` FOREIGN KEY (\`participant_id\`) REFERENCES \`participants\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`media_preferences\` ADD CONSTRAINT \`media_preferences_virtual_background_id_fk\` FOREIGN KEY (\`virtual_background_id\`) REFERENCES \`virtual_backgrounds\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`view_preferences\` ADD CONSTRAINT \`view_preferences_participant_id_fk\` FOREIGN KEY (\`participant_id\`) REFERENCES \`participants\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`view_preferences\` ADD CONSTRAINT \`view_preferences_focused_participant_id_fk\` FOREIGN KEY (\`focused_participant_id\`) REFERENCES \`participants\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`recordings\` ADD CONSTRAINT \`recordings_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`departures\` ADD CONSTRAINT \`departures_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`idempotency_records\` ADD CONSTRAINT \`idempotency_records_principal_id_fk\` FOREIGN KEY (\`principal_id\`) REFERENCES \`principals\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`idempotency_records\` ADD CONSTRAINT \`idempotency_records_session_id_fk\` FOREIGN KEY (\`session_id\`) REFERENCES \`sessions\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`idempotency_records\` ADD CONSTRAINT \`idempotency_records_response_reference_fk\` FOREIGN KEY (\`response_reference\`) REFERENCES \`mutation_responses\` (\`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`sessions\` ADD CONSTRAINT \`session_host\` FOREIGN KEY (\`id\`, \`host_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`stage_requests\` ADD CONSTRAINT \`stage_requests_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`stage_requests\` ADD CONSTRAINT \`stage_requests_decided_by_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`decided_by_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`chat_messages\` ADD CONSTRAINT \`chat_messages_sender_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`sender_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`reaction_events\` ADD CONSTRAINT \`reaction_events_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`content_shares\` ADD CONSTRAINT \`content_shares_owner_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`owner_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`recordings\` ADD CONSTRAINT \`recordings_started_by_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`started_by_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`departures\` ADD CONSTRAINT \`departures_participant_id_scope\` FOREIGN KEY (\`session_id\`, \`participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
    await queryRunner.query(`ALTER TABLE \`sessions\` ADD CONSTRAINT \`sessions_spotlighted_participant_scope\` FOREIGN KEY (\`id\`, \`spotlighted_participant_id\`) REFERENCES \`participants\` (\`session_id\`, \`id\`) ON DELETE RESTRICT ON UPDATE RESTRICT`);
  }

  // Destructive rollback: execute only on an explicit researcher request outside a run.
  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.query(`ALTER TABLE \`sessions\` DROP FOREIGN KEY \`session_host\``);
    await queryRunner.query(`ALTER TABLE \`sessions\` DROP FOREIGN KEY \`sessions_spotlighted_participant_scope\``);
    await queryRunner.query(`DROP TABLE \`idempotency_records\``);
    await queryRunner.query(`DROP TABLE \`mutation_responses\``);
    await queryRunner.query(`DROP TABLE \`departures\``);
    await queryRunner.query(`DROP TABLE \`recordings\``);
    await queryRunner.query(`DROP TABLE \`view_preferences\``);
    await queryRunner.query(`DROP TABLE \`media_preferences\``);
    await queryRunner.query(`DROP TABLE \`content_shares\``);
    await queryRunner.query(`DROP TABLE \`reaction_events\``);
    await queryRunner.query(`DROP TABLE \`chat_messages\``);
    await queryRunner.query(`DROP TABLE \`stage_requests\``);
    await queryRunner.query(`DROP TABLE \`live_streams\``);
    await queryRunner.query(`DROP TABLE \`participants\``);
    await queryRunner.query(`DROP TABLE \`sessions\``);
    await queryRunner.query(`DROP TABLE \`virtual_backgrounds\``);
    await queryRunner.query(`DROP TABLE \`principals\``);
    await queryRunner.query(`DROP TABLE \`users\``);
  }
}
