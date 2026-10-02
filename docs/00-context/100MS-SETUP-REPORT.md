# Database setup hoàn tất — 2026-10-02

Database đã được setup theo ưu tiên repository và chỉ dẫn Google Docs. MySQL 8.4.11, unchanged mysql84-tables-v1; migration Initial100msSchema1790916544190 đã áp dụng thành công. FE/BE/MySQL đều healthy; migration exited 0; frontend HTTP 200 và backend health HTTP 200 với database connected.

| Kết quả | Bằng chứng |
|---|---|
| Cấu trúc | 16 bảng ứng dụng + typeorm_migrations, 28 FK, 13 CHECK, 5 conditional unique indexes. DBML/live columns, defaults, nullability, PK/FK correspondence PASS. |
| Lịch sử | 1 migration đã áp dụng, không pending; file migration giữ nguyên sau apply. |
| Baseline | Ba database pins đã capture bằng helper hiện có; application tables rỗng. Không seed, reset, volume cleanup hoặc tests. |
| Source baseline | ZIP mới gồm 12 file source/infrastructure, checksum khớp current source. ZIP/receipt cũ được lưu riêng. |
| Design/source | Desktop dataset 74 node/18 UC không đổi; 18 UC, 15 API, 167 BR, 47 source documents/39 projections giữ nguyên checksum. |
| Secret | Researcher đã thay placeholder; finalsource/.env ignored/untracked, giá trị không được lưu trong báo cáo. Literal quoting bảo toàn ký tự đặc biệt. |
| Điều kiện generation | Database input đã chuẩn bị; bốn research JSON inputs vẫn cần chuẩn bị/chốt riêng. Không tạo experiment configuration/run hoặc kết luận BR met/unmet. |

Giữ MySQL 8.4 và tables-only theo yêu cầu repo. Capacity, HOST identity, membership immutability, transaction/replay phải được triển khai trong MutationGateway của UC. Idempotency-Key vẫn TEXT, digest index không unique và không thay thế full-key byte-exact comparison; không thêm giới hạn 255 byte.

MySQL connection: 127.0.0.1:3307. Database/user/password lấy từ finalsource/.env. Frontend: http://localhost:18080. Backend health: http://localhost:13000/api/health.

- [Active DBML](engineering/schema.dbml)
- [Migration](../../finalsource/be/src/database/migrations/1790916544190-Initial100msSchema.ts)
- [Quyết định adaptation](engineering/100MS-DATABASE-ADAPTATION.md)
- [Ba database pins và validation](sources/100ms-database-baseline.json)
- [Setup operation](../03-audit/docker-deployment/operations/20261002-100ms-database-setup.json)
- [Baseline ZIP receipt](sources/100ms-source-baseline.json)
- [Google Docs: Database](https://docs.google.com/document/d/1R9Z4LQ_FEbEop_TmGMTyCPnM3HdNau9JvLBV4uB8ZMg/edit?tab=t.7vwf3xf4pxs9)

Migration head: Initial100msSchema1790916544190.
DBML SHA-256: sha256:7281415d0e1cfda9788fae848d4df7d6ebe1bf902a944260a6abdf1e97afabad.
Schema fingerprint: sha256:e0b8e2833611589303c491f5691d04474e836b3543289a3f547e3063b92672bd.

## Báo cáo trước database setup — lịch sử

# Cập nhật setup 100ms — 2026-10-02

Đã hoàn tất dataset Figma **desktop only** đủ làm đầu vào thiết kế cho 18 UC. Database vẫn deferred; repo chưa đủ điều kiện generation khi thiếu schema và research inputs đã pin.

| Hạng mục | Trạng thái hiện hành |
|---|---|
| Dataset | 100ms-2026-10-02-001, complete/frozen; 74/74 required node, 18/18 UC, 8 page. |
| Phạm vi | Desktop và component liên quan; mobile bị loại theo researcher. Không khẳng định mobile readiness. |
| Quota | 74 thay cho 604 target; loại 530 target (87,7% số target kế hoạch). Cache và shared assets tránh capture trùng; không suy ra quota thực tế từ tỷ lệ này. |
| Evidence | 18 primary có reference code; tất cả required node có full native subtree, screenshot và referenced assets cục bộ. Truncation bắt buộc đã xử lý, không còn pending required assets. |
| Integrity | Ledger 1.929 file; 455 asset records xác minh byte size, SHA-256 và định dạng ảnh; source UC hashes không đổi. |
| UC/API | Structural validator PASS: 18 UC, 15 endpoint API, 167 BR, 47 source documents, 39 active projections. Không thực hiện BR/flow audit. |
| Baseline/archive | 10 file baseline khớp ZIP; 1.332 archive file đã xác minh. |
| Docker | Compose config, FE/BE lint/build PASS; FE/BE healthy, frontend HTTP 200 và backend health HTTP 200. Database/migration không khởi động. |
| Database | Còn mâu thuẫn MySQL 8.0/8.4, trigger/procedure fingerprint và TEXT idempotency unique index. Đã viết phương án; chưa đổi DBML, migration hoặc schema. |

- [Frozen manifest](../../resource/figma-design-dataset/100ms-2026-10-02-001/manifest.json)
- [Validation receipt: checksum và 18 UC](sources/100ms-desktop-dataset-validation.json)
- [UC desktop coverage và giới hạn](../../resource/figma-design-dataset/100ms-2026-10-02-001/uc-design-coverage.json)
- [Kế hoạch capture đã chỉnh](100MS-REPOSITORY-MIGRATION-PLAN.md)
- [Phương án database](engineering/100MS-DATABASE-RESOLUTION-PROPOSAL.md)
- [Runtime receipt](../03-audit/docker-deployment/operations/20261002-100ms-setup-follow-up.json)

Manifest pin: sha256:ead5b6aa248f3c132950dc533b5b3392052cfdcfec6efc029c3fb01e6845c298.

Coverage giữ hành vi/error semantics theo frozen UC/API. Không khẳng định mỗi lỗi server/device có màn hình Figma riêng, không đổi frozen BR/flow inventory và không tạo experiment configuration/run. Resolver trả cả primary và supplementary desktop directories.

## Báo cáo lịch sử 2026-10-01 — trạng thái đã được cập nhật ở trên

# Báo cáo chuẩn bị codebase thực nghiệm 100ms

Ngày: 2026-10-01 (Asia/Saigon). Researcher đã yêu cầu thực hiện kế hoạch và sau đó yêu cầu tạm hoãn database.

Đã thay bộ đầu vào và source hoạt động của Financial bằng 100ms. Phần source/scaffolding đã được kiểm tra và pin baseline; repo chưa READY cho thí nghiệm vì Figma capture bị giới hạn MCP và database đang hoãn.

| Hạng mục | Kết quả |
|---|---|
| PROJECT_PROFILE | Danh tính 100ms; nguồn chính thức Markdown; 18 URL root FRAME đã xác minh; SHA-256 ZIP mới. |
| UC | 18 Frozen projections; toàn bộ flow/OCL được giữ nguyên; shared UML vocabulary được nhúng vào từng UC. |
| OCL utility | Nhập từ Markdown đã cung cấp; header ghi provenance local thay cho spreadsheet Financial. |
| API | 15 endpoint contracts và common contract. README nguồn ghi 14 nhưng inventory file thực tế có 15; không bỏ endpoint nào. |
| Source provenance | 47 tài liệu nguồn được snapshot byte-exact; 40 projections được pin checksum/retrieval receipt. |
| BR | Structural validator xác nhận 167 Rule ID/OCL blocks được bảo toàn; không thực hiện BR audit hoặc kết luận met/unmet. |
| finalsource | FE/BE framework sạch, neutral shell và health endpoint; chưa triển khai hành vi của UC. |
| ZIP baseline | 10 file source, đúng prefix baseline/be/src và baseline/fe/src; byte mỗi entry khớp source. |
| Figma inventory | Đã quét tất cả 69 page qua Plugin API; gồm product, components, foundations, documentation và page trống. |
| Figma dataset | 35 node có payload toàn phần hoặc một phần; 18 primary node có context/screenshot/export/asset-map, nhưng SVG còn truncated. Chưa complete/frozen. |
| Database | DEFERRED theo researcher; không migration, MySQL startup, DDL, schema sync hoặc DB pins. |
| Runtime | FE/BE healthy, frontend HTTP 200, backend health PASS. MySQL/migration không được khởi động. |
| Git/evidence | Financial được lưu cold archive; đã xác minh checksum 1.332 file archive. Working tree thay đổi, chưa tạo commit. |

## Tài nguyên hiện tại

- [PROJECT_PROFILE.json](../../PROJECT_PROFILE.json)
- [Connected sources](sources/CONNECTED-SOURCES.md)
- [Source retrieval receipt](sources/100ms-source-retrieval.json)
- [Baseline receipt](sources/100ms-source-baseline.json)
- [UC folder](../01-inception/use-cases/)
- [API folder](../01-inception/api-contracts/)
- [Figma mapping](FIGMA-LINK-REVIEW.md)
- [Page inventory](sources/100ms-figma-page-inventory.json)
- [Partial dataset manifest](../../resource/figma-design-dataset/100ms-2026-10-01-001/manifest.json)
- [Cold archive manifest](../../archive/financial-management/pre-100ms-2026-10-01/archive-manifest.json)

Clean source ZIP: `.codex/skills/restore-source-baseline/assets/source-baseline.zip`.

```text
sha256:e7a5d8b5c5624ba29af74209ae0cfce51a93e2a8d0fe817ded1de864f9973f20
```

ZIP chỉ phục hồi hai thư mục src. Compose, Dockerfiles, lockfiles và công cụ setup vẫn ở finalsource/repo. `.gitattributes` giữ byte của frozen inputs, snapshot, dataset và archive khi Git checkout để checksum không bị thay đổi vì line endings.

## Figma: đã quét toàn bộ page, capture còn bị chặn

Quyền truy cập đã hoạt động trở lại. Endpoint get_metadata không liệt kê toàn bộ document khi page chưa load; Plugin API đã liệt kê đủ 69 page, sau đó từng page được load/đọc trong một lệnh riêng. Node `4732:52930` là PAGE `Hello World`; các URL profile dùng FRAME thật, không dùng canvas này làm root frame.

Mapping mới lấy file chuẩn `lCvn1rB7IdRchqAuEatJJp`, gồm primary cho đủ 18 UC, các supplementary target và các root FRAME descendants đã được xác minh. Snapshot nguồn vẫn giữ nguyên lịch sử file copy; downstream provenance được thay theo chỉ dẫn researcher.

Lỗi chặn thực tế từ connector: `You've reached the Figma MCP tool call limit on the Education plan.` Đã dừng lệnh capture mới khi gặp giới hạn. Một số HTTP asset download trả nội dung rỗng; các context đã lấy được vẫn được lưu với missing/pending state, không có bằng chứng download giả. Temporary asset URLs được loại khỏi dữ liệu lưu; scratch response đã được xóa từng file sau xử lý.

Dataset được giữ ở `pending-rate-limit`, `frozen: false`. Checksum ledger hiện có 457 file và `integrity_ok: true`. Integrity của phần đã lưu không đồng nghĩa completeness. 604 capture targets trong request gồm primary, top-level full-file targets và descendants để bổ sung sparse context. Không dùng dataset này như input complete cho prompt/source.

[Skill resolve-figma-design-dataset](../../.codex/skills/resolve-figma-design-dataset/SKILL.md) yêu cầu: “If status is `partial-content` or `pending-rate-limit`, stop design-dependent generation and report the exact missing capture state.” Đây là lý do phần đóng băng toàn bộ Figma chưa hoàn tất; nguồn không bị thay bằng thiết kế khác.

Khi quota MCP khả dụng, tiếp tục capture theo version đã chọn và mapping, bổ sung screenshot/context còn thiếu và asset subtrees cho tất cả truncation. Chỉ pin complete manifest vào cấu hình run sau khi CAPTURE-SPEC và validator đều đạt yêu cầu.

## Database được hoãn

DBML và persistence.sql của 100ms nằm trong source snapshot để giữ bằng chứng. Chưa nhập DBML thành input hoạt động ở `docs/00-context/engineering/schema.dbml`; Financial DBML đã được archive để không dùng nhầm. Backend baseline không mở kết nối database. CLI TypeORM chỉ là scaffolding, không chứa migration hoặc entity nghiệp vụ.

Compose có database/migration trong profile `database-setup`; mặc định chỉ chạy FE/BE. Hợp đồng và validator `mysql84-tables-v1` không bị sửa. Khi researcher tiếp tục phần database, cần giải quyết MySQL 8.0/8.4 và procedure/trigger trong persistence supplement trước khi chuẩn bị migration, schema và ba database pins. Không thể bỏ supplement mà vẫn tuyên bố baseline giữ nguyên capacity/concurrency semantics.

Local `.env` đã được tạo từ example, được ignore và không tracked. Các credential vẫn là placeholder theo chính sách setup; researcher cần điền giá trị thật trước các bước cần database/JWT. Giá trị `.env` không được in hoặc đưa vào source ZIP.

## Kiểm tra đã thực hiện

- Source/receipt structural validator PASS: 18 UC, 15 API, 167 BR; mọi flow section và OCL block khớp nguồn; mọi relative Markdown link được giải quyết; checksum nguồn/projection/archive/ZIP khớp.
- Docker Compose config PASS; backend ESLint/Nest TypeScript build PASS; frontend ESLint/TypeScript/Vite production build PASS. Kiểm tra chạy trong Docker, không dùng host Node/MySQL thay runtime.
- Cả backend/frontend được recreate từ image cuối cùng và healthy. Backend `http://localhost:13000/api/health` trả success; frontend `http://localhost:18080/` trả HTTP 200.
- Nginx cho phép camera/microphone/display capture từ self thay vì chính sách cũ chặn media; không tạo UI hoặc API nghiệp vụ mới.
- Xung đột cổng 3000 được giải quyết bằng cổng riêng 13000/18080, không dừng listener khác.
- Resolver được sửa thiếu import `Optional` để chạy được trên Python hiện tại; `--validate-all` PASS về checksum, resolve UC-01 trả pending-rate-limit đúng trạng thái, không complete giả.
- `git diff --check` PASS theo cấu hình repo. Không tạo hoặc chạy tests/test cases; không bắt đầu generation/audit/repair/measurement.

## Còn lại trước khi bắt đầu thí nghiệm

1. Hoàn tất Figma capture sau khi quota MCP khả dụng; không cần sửa quyền lại vì truy cập đã thành công.
2. Tiếp tục database khi researcher yêu cầu, review/schema/migration và capture database pins.
3. Chọn UC/model/variant/run order và chuẩn bị Confirmed configuration, complete BR/flow baselines, Draft Canonical Run JSON. Chưa tự tạo assignment hoặc bốn JSON này khi database/input còn thiếu.
4. Ghi Git revision của bộ input/scaffolding đã nghiệm thu và bắt đầu `$gen-coding-prompt` cho frozen UC được chỉ định.

Overall: `NOT_READY_FOR_EXPERIMENT`, với source baseline và framework runtime đã chuẩn bị; Figma bị chặn bởi quota, database được researcher hoãn.
