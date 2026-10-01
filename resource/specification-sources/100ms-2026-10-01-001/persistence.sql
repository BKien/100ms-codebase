-- Apply after compiling schema.dbml to MySQL 8.0 SQL.
-- Conditional uniqueness and foreign keys are generated from DBML.
-- This supplement enforces aggregate capacities under a locked session row.

DELIMITER $$

CREATE PROCEDURE assert_participant_capacity(
  IN p_participant_id CHAR(36),
  IN p_session_id CHAR(36),
  IN p_principal_id CHAR(36),
  IN p_role VARCHAR(32),
  IN p_status VARCHAR(32)
)
BEGIN
  DECLARE v_session_count INT DEFAULT 0;
  DECLARE v_kind VARCHAR(32);
  DECLARE v_status VARCHAR(32);
  DECLARE v_host_principal_id CHAR(36);
  DECLARE v_member_count INT DEFAULT 0;
  DECLARE v_stage_count INT DEFAULT 0;

  SELECT COUNT(*) INTO v_session_count FROM sessions WHERE id = p_session_id;
  IF v_session_count = 0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Session unavailable';
  END IF;

  SELECT kind, status, designated_host_principal_id
    INTO v_kind, v_status, v_host_principal_id
  FROM sessions
  WHERE id = p_session_id
  FOR UPDATE;

  IF p_status = 'JOINED' THEN
    IF v_status = 'ENDED' THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Session ended';
    END IF;
    IF (p_role = 'HOST') <> (p_principal_id = v_host_principal_id) THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Host identity mismatch';
    END IF;

    SELECT COUNT(*) INTO v_member_count
    FROM participants
    WHERE session_id = p_session_id AND status = 'JOINED' AND id <> p_participant_id;
    IF v_member_count >= IF(v_kind = 'VIDEO_CONFERENCE', 100, 1000) THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Session capacity exceeded';
    END IF;

    IF v_kind = 'LIVE_STREAM' AND p_role <> 'VIEWER' THEN
      SELECT COUNT(*) INTO v_stage_count
      FROM participants
      WHERE session_id = p_session_id
        AND status = 'JOINED'
        AND role <> 'VIEWER'
        AND id <> p_participant_id;
      IF v_stage_count >= 10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stage capacity exceeded';
      END IF;
    END IF;
  END IF;
END$$

CREATE TRIGGER participant_capacity_guard_insert
BEFORE INSERT ON participants
FOR EACH ROW
BEGIN
  CALL assert_participant_capacity(NEW.id, NEW.session_id, NEW.principal_id, NEW.role, NEW.status);
END$$

CREATE TRIGGER participant_capacity_guard_update
BEFORE UPDATE ON participants
FOR EACH ROW
BEGIN
  IF NOT (NEW.session_id <=> OLD.session_id)
     OR NOT (NEW.principal_id <=> OLD.principal_id) THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Membership identity is immutable';
  END IF;
  CALL assert_participant_capacity(NEW.id, NEW.session_id, NEW.principal_id, NEW.role, NEW.status);
END$$

DELIMITER ;

ALTER TABLE participants
  ADD CONSTRAINT participant_display_name
    CHECK (display_name = TRIM(display_name) AND CHAR_LENGTH(display_name) BETWEEN 1 AND 50);
ALTER TABLE chat_messages
  ADD CONSTRAINT message_body_shape
    CHECK (body = TRIM(body) AND CHAR_LENGTH(body) BETWEEN 1 AND 1000),
  ADD CONSTRAINT message_sequence_positive CHECK (sequence > 0);
ALTER TABLE reaction_events
  ADD CONSTRAINT reaction_sequence_positive CHECK (sequence > 0);
ALTER TABLE content_shares
  ADD CONSTRAINT share_source_present CHECK (CHAR_LENGTH(TRIM(source_reference)) > 0);
ALTER TABLE idempotency_records
  ADD CONSTRAINT idempotency_key_present CHECK (CHAR_LENGTH(TRIM(idempotency_key)) > 0),
  ADD CONSTRAINT idempotency_expiry
    CHECK (expires_at = TIMESTAMPADD(HOUR, 24, completed_at));

-- All application mutations and trusted provider completions use SERIALIZABLE
-- InnoDB transactions. They lock sessions.id before membership/resource reads and
-- write the receipt in the same transaction. Deadlocks and serialization failures
-- are retried at the gateway; no partial HTTP success is returned.
