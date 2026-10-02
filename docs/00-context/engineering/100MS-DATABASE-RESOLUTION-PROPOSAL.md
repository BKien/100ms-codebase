> Phân tích lịch sử, đã được thay thế ngày 2026-10-02: researcher yêu cầu ưu tiên database policy của repo và thực hiện setup. Quyết định đang áp dụng là [100MS-DATABASE-ADAPTATION.md](100MS-DATABASE-ADAPTATION.md): MySQL 8.4/tables-only, TEXT + non-unique digest lookup, application MutationGateway enforcement. Database đã được tạo và pins đã capture; các điều kiện pending bên dưới chỉ ghi lại thời điểm đề xuất.

# Đề xuất xử lý database 100ms

Ngày: 2026-10-02 (Asia/Saigon). Trạng thái: đề xuất để researcher quyết định; chưa đổi schema, DBML, migration, policy, validator database hay nguồn frozen.

Khuyến nghị giữ MySQL 8.4 và enforcement tại database, bổ sung một phiên bản fingerprint hỗ trợ đúng các procedure/trigger được yêu cầu. Cách này giữ cơ chế chống vượt capacity của persistence supplement. Cần chốt thêm cách lưu và so sánh Idempotency-Key trước khi tạo migration.

## Bằng chứng và tác động

| Vấn đề | Nguồn và vị trí | Tác động |
|---|---|---|
| Phiên bản MySQL | Snapshot `schema.dbml:3`, `persistence.sql:1`, `README.md` mục Persistence build yêu cầu 8.0; `finalsource/compose.yaml` dùng `mysql:8.4`; `DATABASE-SCHEMA.md` yêu cầu 8.4. | Chưa có bằng chứng migration tương thích 8.4. Đây là khác biệt target cần researcher chốt, chưa phải một lỗi runtime đã được tái hiện. |
| Procedure/trigger bị preflight từ chối | `persistence.sql:7` tạo `assert_participant_capacity`; dòng 62 và 69 tạo hai trigger INSERT/UPDATE. `DATABASE-SCHEMA.md` mục Fingerprint protocol và `database_baseline.py:214-228` từ chối routine/trigger/event. | Import supplement nguyên vẹn sẽ làm preflight bị chặn; bỏ supplement sẽ loại cơ chế enforcement đã được nguồn yêu cầu. |
| Index Idempotency-Key không thể giữ nguyên DDL dạng hiện tại | Snapshot `schema.dbml:252` khai báo `idempotency_key text`; dòng 257 đặt cột này trong composite unique index toàn phần. API join dòng 71-77 khai báo opaque string, không có giới hạn chiều dài. | MySQL yêu cầu prefix khi index TEXT. Unique prefix có thể coi hai key khác phần đuôi là trùng; tự đổi sang VARCHAR có giới hạn sẽ thêm yêu cầu đầu vào. [MySQL Column Indexes](https://dev.mysql.com/doc/refman/8.4/en/column-indexes.html). |
| Enforcement không chỉ nằm trong DBML | `persistence.sql:82-96` bổ sung bảy CHECK; dòng 98-101 yêu cầu SERIALIZABLE, khóa session trước resource reads và receipt cùng transaction. `ASSUMPTIONS.md` A-18 và UC-02 BR-UC-02-14…17 quy định replay/atomicity. | Chỉ compile DBML không đủ. Fingerprint cũng không chứng minh ứng dụng sử dụng transaction và thứ tự khóa đúng. |
| Runtime credentials chưa chuẩn bị | Kiểm tra chỉ trạng thái cho thấy `MYSQL_PASSWORD` và `JWT_SECRET` trong `finalsource/.env` còn placeholder. | Chưa đủ điều kiện chạy database/JWT. Không có giá trị secret được ghi vào báo cáo. |

Capacity nguồn cần giữ: tối đa 100 conference members, 1.000 live-stream members, 10 người trên stage gồm host; membership identity bất biến; HOST tương ứng designated principal; không JOIN khi session ENDED. Bằng chứng: `ASSUMPTIONS.md` A-02, UC-02 BR-UC-02-06/17 và `persistence.sql:33-59,73-77`.

## Các phương án

| Phương án | Thay đổi cần quyết định | Đánh giá |
|---|---|---|
| A — MySQL 8.4, giữ DB enforcement | Researcher chấp nhận target 8.4; bổ sung fingerprint có kiểm tra routine/trigger; review migration chuyển nguyên semantics của supplement. | Khuyến nghị. Giữ lớp enforcement của nguồn, nhưng cần cập nhật hợp đồng hạ tầng trước run đầu tiên. |
| B — MySQL 8.4, tables-only | Researcher sửa persistence contract để chuyển capacity/identity guard sang MutationGateway trong NestJS; giữ constraint/index tại DB. | Giữ được validator hiện tại, nhưng thay đổi vị trí enforcement. Mọi đường ghi và provider completion phải đi qua gateway; DML trực tiếp sẽ thiếu aggregate guard. Cần nguồn mới và retrieval receipt, không thể tự bỏ trigger. |
| C — MySQL 8.0, giữ supplement | Đổi Compose, database policy và validator phiên bản; vẫn phải thêm fingerprint routine/trigger. | Đổi rộng hơn A, vẫn không giải quyết TEXT unique index. Không ưu tiên. |

Không chọn cách xóa câu kiểm tra unsupported objects, bỏ supplement hoặc ghi lại expected pins để preflight PASS. Những cách đó không xác nhận đúng database đã chuẩn bị.

## Thiết kế cụ thể cho phương án A

1. Giữ `mysql84-tables-v1` cho các baseline cũ. Bổ sung protocol mới, dự kiến `mysql84-schema-v2`, với lựa chọn protocol rõ ràng ở policy/helper được review trước run. Không sửa thuật toán của fingerprint cũ âm thầm. Configuration vẫn chỉ có ba database pins; protocol được cố định bởi repository revision của điều kiện nghiên cứu.
2. Fingerprint mới giữ toàn bộ metadata bảng/index/FK/CHECK hiện tại, thêm inventory và definition của đúng một procedure, hai trigger. Routine cần body, ordered parameters, SQL SECURITY, SQL mode, charset/collation và deterministic/data-access attributes. Trigger cần table, event, timing, action order, body, SQL mode, charset/collation và definer identity. Metadata lấy bằng tài khoản setup có đủ quyền; definition null hoặc object thiếu/thừa phải BLOCKED. MySQL có các nguồn metadata [ROUTINES](https://dev.mysql.com/doc/refman/8.4/en/information-schema-routines-table.html), [TRIGGERS](https://dev.mysql.com/doc/refman/8.4/en/information-schema-triggers-table.html) và [PARAMETERS](https://dev.mysql.com/doc/refman/8.4/en/information-schema-parameters-table.html).
3. Không bỏ DEFINER/SQL SECURITY khỏi fingerprint một cách tùy tiện: chúng ảnh hưởng thực thi. Pin definer setup cố định hoặc xây dựng quy tắc ánh xạ vai trò có kiểm tra quyền riêng, được researcher chấp nhận. Timestamp tạo/sửa object không phải nội dung semantics. Views/events và object ngoài inventory vẫn bị từ chối.
4. Chuẩn bị migration TypeORM tạo đủ 16 bảng, enum domains, conditional uniqueness, composite FK cùng session, bảy CHECK trong supplement, procedure và hai trigger. `DELIMITER` là lệnh của mysql client; migration cần gửi từng CREATE statement hoàn chỉnh qua QueryRunner. Giữ `synchronize: false`, `migrationsRun: false`; migration service là setup-only. [TypeORM migrations](https://typeorm.io/docs/advanced-topics/migrations/).
5. Giữ MutationGateway theo nguồn: bắt đầu SERIALIZABLE; khóa `sessions.id`; lookup/replay trước dispatch; cùng transaction cho mutation, result serialization, immutable response và receipt; commit trước HTTP success. Deadlock/serialization retry phải bounded và giữ idempotency. `FOR UPDATE` cần transaction; giới hạn capacity phải được kiểm tra sau khóa. [MySQL locking reads](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html).
6. Tách quyền setup/migration và application; chỉ tuyên bố app DML-only sau khi kiểm tra grants. Backend chỉ phụ thuộc migration thành công khi đã có schema được review. Trước thời điểm đó giữ profile `database-setup` tách khỏi scaffold runtime.
7. Review DBML và migrated schema tương ứng, kiểm tra health/history/fingerprint và quan sát runtime được phép. Sau đó mới capture `migration_head`, `dbml_sha256`, `schema_fingerprint_sha256` và chuẩn bị configuration/run mới. Không tạo tests/test cases, không seed/reset dữ liệu để làm kiểm tra PASS.

Đây là thiết kế đề xuất, chưa có migration được áp dụng hoặc concurrency proof; thành công khi deploy không thay thế BR/flow audit của run.

## Quyết định Idempotency-Key cần chốt riêng

Khuyến nghị researcher chốt key tối đa 255 byte và so sánh byte-exact, sau đó dùng `VARBINARY(255)` cùng full composite unique index. API phải công bố giới hạn byte và cách từ chối key quá dài; OCL/natural-language/source storage phải được revision đồng bộ nếu thay đổi miền đầu vào. Đây là đề xuất mới, không phải giới hạn đã tồn tại trong nguồn frozen.

Nếu cần giữ TEXT và toàn bộ miền đầu vào hiện tại, có thể giữ key đầy đủ, thêm digest để tra cứu bằng index không unique, và kiểm tra full key theo equality đã chốt bên trong SERIALIZABLE/session lock. Cần researcher sửa thiết kế storage, xác nhận mọi writer tuân thủ gateway hoặc bổ sung enforcement tương ứng, và quy định collision không được coi là cùng key. Không coi hash unique đơn thuần hay unique prefix là tương đương tuyệt đối với String equality.

## Điều kiện để tiếp tục database setup

- Researcher chọn A/B/C và quyết định miền/equality của Idempotency-Key.
- Nguồn/policy được revision theo quyết định; các snapshot frozen hiện tại giữ nguyên. Nếu refresh nguồn có thay đổi semantics, cần yêu cầu researcher rõ ràng và retrieval receipt mới.
- Researcher thay hai placeholder trực tiếp trong `finalsource/.env`; chỉ báo đã cập nhật, không gửi secret qua chat.
- Sau đó review migration/DBML, chạy setup Docker ngoài active run và capture ba pins. Không chạy migration từ một run đang bị chặn.
