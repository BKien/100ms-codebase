# Kế hoạch chuyển repo sang codebase thực nghiệm 100ms

Ngày khảo sát: 2026-10-01 (Asia/Saigon). Trạng thái: kế hoạch chuẩn bị, chưa thực hiện làm sạch hoặc thay đầu vào.

Repo: `D:\100ms-codebase`.
Nguồn chính thức do researcher chọn trong lượt này: bộ Markdown tại `D:\figma_spec\100ms Video Conferencing and Live Streaming`.
Figma mục tiêu: file `lCvn1rB7IdRchqAuEatJJp`, node trong URL `4732:52930`.

## Kết quả khảo sát và các điều kiện cần giải quyết

| Mục | Hiện trạng quan sát | Hệ quả cho kế hoạch |
|---|---|---|
| Git | Working tree sạch trước khảo sát; HEAD `ad24d09` | Có điểm phục hồi trước chuyển đổi. |
| Project profile | Vẫn là Financial Management; UC/API trỏ sheet Financial; API tab còn placeholder | Cập nhật danh tính và nguồn dự án, không mang provenance cũ sang 100ms. |
| Frozen inputs hiện tại | 16 UC Financial, 17 API Financial | Thay cả inventory khi nhập nguồn mới; tránh giữ hai bộ cùng mẫu `uc-*.md`. |
| Bộ đặc tả mới | 18 UC, 15 API nghiệp vụ, shared domain model, common API contract, assumptions, DBML và persistence supplement | Phải nhập cả các tài liệu phụ thuộc, không chỉ UC/API/OCL. |
| Metadata mới | UC/API còn `Draft`; OCL utility mang `source_spreadsheet_id` của Financial | Chuẩn hóa và ghi retrieval receipt thật trước khi đánh dấu Frozen. |
| Figma provenance mới | `FIGMA.md` trỏ file copy `ANYtlDoAyDRNwH6AByKGKK` | Node ID được ghi trong bộ spec là ứng viên; phải xác minh trên file mục tiêu mới. |
| Kết nối Figma | Lệnh liệt kê page trả `UNAUTHORIZED`, `Reauthentication required` | Chưa quét được page nào trên file mục tiêu. Không thể xác nhận root frame hoặc capture complete. |
| Figma review hiện tại | Ánh xạ 16 UC Financial sang Finebank | Resolver chưa có mapping hợp lệ cho 100ms. |
| Database | Spec mới ghi MySQL 8.0; repo yêu cầu MySQL 8.4 | Cần review tương thích trước khi chuẩn bị baseline database. |
| Persistence supplement | Có procedure `assert_participant_capacity` và hai trigger `participant_capacity_guard_*` | Validator `mysql84-tables-v1` hiện chặn routines/triggers. Đây là xung đột chặn preflight, không được âm thầm bỏ supplement. |
| Runtime | Docker 29.2.1, Compose 5.0.2; Docker daemon không truy cập được | Chưa xác minh database hoặc chạy FE/BE. Tài liệu repo chấp nhận Compose CLI major 2 hoặc 5; giữ mô hình Compose. |
| finalsource | Có scaffolding và các trang Financial; thiếu `finalsource/.env` | Cần baseline 100ms sạch và chuẩn bị môi trường riêng. |

Đây là khảo sát cấu trúc và hợp đồng đầu vào, chưa phải audit đầy đủ từng BR hoặc xác nhận đặc tả không còn mâu thuẫn.

Quyết định đã chốt: bộ Markdown được cung cấp là nguồn chính thức của UC/API. Không cần link Excel/Google Sheets cho hai đầu vào này. Metadata spreadsheet Financial không được kế thừa sang projection 100ms.

Các điều kiện và quyết định còn thiếu:

1. Chốt cách biểu diễn provenance local-file tương thích validator trước khi Frozen. Nguồn đã được chọn; không cần researcher xác nhận lại nguồn. Nếu validator đang bắt buộc Google Sheets, việc điều chỉnh cần thuộc setup được yêu cầu và giữ nguyên kiểm tra identity/checksum, không lách validation bằng nguồn giả.
2. Researcher giải quyết xung đột persistence supplement với chính sách database: giữ procedure/trigger và cho phép mở rộng fingerprint/hợp đồng phương pháp, hoặc cung cấp revision đặc tả tương thích chính sách hiện tại. Phải giữ yêu cầu capacity, transactionality và concurrency. Không tự chọn giải pháp hoặc sửa baseline rule.
3. Xác thực lại kết nối Figma để khảo sát toàn file mục tiêu. Chưa thể suy ra cùng node ID ở hai file copy có cùng thiết kế.
4. Chốt ranh giới adapter media/provisioning/provider completion và dữ liệu đầu vào runtime. `CONTEXT.md` loại trừ account creation, scheduling và provider internals; baseline không tự thêm các API này.

## Thứ tự thực hiện

| Bước | Công việc | Đầu ra và tiêu chí hoàn tất |
|---|---|---|
| 0 | Ghi điểm phục hồi, lập manifest tài nguyên Financial cần tách khỏi phạm vi hoạt động | Danh sách đường dẫn, checksum và commit trước chuyển đổi; dữ liệu/evidence cũ có thể phục hồi. |
| 1 | Xác định nguồn UC/API và khảo sát toàn bộ Figma | Provenance rõ ràng; page inventory đầy đủ; root frame được connector xác minh. |
| 2 | Giải quyết bất tương thích nguồn/database, cập nhật profile và nhập frozen specs | 18 UC, 15 API và phụ thuộc đã xác minh; không còn metadata Financial hoặc placeholder trong đầu vào hoạt động. |
| 3 | Tạo scaffolding sạch và chuẩn bị database ngoài run | FE/BE/build/runtime nền tảng; schema, migrations và dữ liệu khởi đầu được researcher review. |
| 4 | Tạo ZIP baseline và pin SHA-256 | ZIP đúng hai prefix; checksum profile khớp byte của ZIP; nền tảng source được cố định. |
| 5 | Hoàn tất FIGMA-LINK-REVIEW và capture dataset bất biến | Mapping đủ 18 UC; tài nguyên toàn file đã phân loại; artifact/checksum hợp lệ. |
| 6 | Nghiệm thu repo và chuẩn bị đầu vào cho run đầu tiên | Repo READY; bốn JSON và database pins hợp lệ trước Phase 1. |

### Bước 0 — Làm sạch phạm vi hoạt động, bảo toàn khả năng phục hồi

- Giữ framework phương pháp: `AGENTS.md`, workflow contracts, templates, metrics schema, input helpers và các skill dùng chung.
- Lập danh sách thay thế cho profile, connected sources, UC/API/OCL, DBML, Figma review, ZIP baseline và source Financial.
- Các dataset Finebank cũ, demo source `resource/VC-AWG-Demo_FinalCode-main` và artifact Financial nếu có được đưa ra khỏi phạm vi hoạt động theo manifest lưu trữ riêng trong repo. Archive không được đặt trong `docs/01-inception/use-cases` vì glob `uc-*.md` quyết định inventory.
- Không xem hoặc dùng kết quả experiment cũ làm nội dung thế hệ mới. Không chọn dataset mới nhất bằng cách quét thư mục.
- Trước mọi di chuyển/xóa đệ quy khi triển khai, kiểm tra đường dẫn tuyệt đối thuộc đúng repo và đúng danh sách đã lập. Không xóa Git history hoặc dữ liệu Docker trong bước này.
- Đặt Compose project/database/volume identity riêng cho 100ms để runtime mới không vô tình dùng volume Financial.

### Bước 1 — Nguồn đầu vào và khảo sát tất cả Figma page

Kết nối Figma cần được xác thực lại trước. Kế hoạch khảo sát:

1. Liệt kê toàn bộ page từ file `lCvn1rB7IdRchqAuEatJJp`; lưu page ID, tên, thời điểm và kết quả truy cập.
2. Đọc cấu trúc từng page, kể cả cover, foundations, components và các page ngoài màn hình sản phẩm. Lưu loại node, root frame ID, kích thước và URL.
3. Phân loại thiết kế Live Streaming/Video Conferencing, desktop/mobile, preview/features/layouts; đây là nhóm từ bộ spec, không phải inventory đã xác minh trên Figma mới.
4. Đối chiếu UI references của 18 UC trên file mục tiêu; kiểm tra trạng thái chính, alternative/exception, modal và overlay. Các node từ file copy chỉ được coi là ứng viên.
5. Ghi page/node bị thiếu, bị hạn chế hoặc thay đổi; không đoán node ID.
6. Lập coverage matrix page → root frame → UC/flow/state hoặc shared asset. Page trang trí/thư viện được ghi rõ, không biến thành UC mới.

Quét toàn bộ page và đóng băng dataset là hai mốc khác nhau: một page được thấy tên chưa có nghĩa mọi frame/assets đã capture đầy đủ. Inventory phải chứng minh toàn bộ page đã được kiểm tra; dataset phải đáp ứng CAPTURE-SPEC cho từng node thuộc phạm vi capture đã thống kê.

### Bước 2 — PROJECT_PROFILE và bộ frozen specifications

`PROJECT_PROFILE.json` sẽ có project identity 100ms và nguồn Markdown đã chốt. Trong giai đoạn đầu, baseline SHA chưa có giá trị hợp lệ; bỏ giá trị Financial, đánh dấu repo chưa READY cho generation cho đến khi ZIP mới được pin.

- `authoritative_sources.figma.root_node_urls` chỉ chứa URL của root FRAME đã xác minh. Không điền URL chỉ có file key, page/canvas, component con hoặc coi `4732:52930` là root frame khi chưa xác minh. Loại bỏ tham số phiên `t=...` khỏi URL ổn định.
- `authoritative_sources.use_case_specification` và `api_specification` khai báo loại nguồn Markdown local và thư mục `01-inception/uc/`, `01-inception/api/` thuộc package đã chọn. Tên trường nguồn local cần thống nhất với validator khi triển khai; không điền link Financial để thỏa mãn cấu trúc.
- Cập nhật `CONNECTED-SOURCES.md` với bản ghi retrieval, nguồn, revision và checksum. `PROJECT_CONTEXT.md` giữ thuật ngữ researcher/application user và phương pháp hai pha; sửa những mô tả source cần thiết nếu chính thức hỗ trợ Markdown local.
- Tạo index/inventory mới, ghi rõ dự án 100ms và 18 UC; không hard-code số này vào logic skill dùng chung.

**UC frozen:** nhập 18 file `uc-01-...md` đến `uc-18-...md` từ `01-inception/uc/` vào `docs/01-inception/use-cases/` theo cấu trúc Financial: YAML front matter, Functional Use-Case Specification, UML Model, Business Rules, UI/API references và source provenance. Giữ nguyên toàn bộ Rule ID, OCL, natural-language constraints và các flow; chỉ chỉnh cấu trúc/provenance đã được phép. Ghi `status: Frozen` sau khi xác minh nguồn và byte của projection.

Front matter giữ `artifact_type`, `status`, `uc_id`/`api_id` và tên/quan hệ tương ứng; provenance local cần biểu diễn loại nguồn, đường dẫn nguồn, checksum byte của nguồn và `retrieved_at` thật. Đây là yêu cầu thông tin cho hợp đồng setup, không phải schema validator đã được xác nhận. Lưu bản source snapshot có checksum trong repo để việc tái lập không phụ thuộc đường dẫn ngoài repo tồn tại mãi; receipt ghi cả vị trí gốc và snapshot. Format nội dung tiếp tục theo mẫu Financial, không chép các trường spreadsheet không còn đúng.

**Các phụ thuộc:** bộ mới dùng `shared-domain-model.md` và assumptions A-01…A-23. Phải bảo toàn model/helper/assumption semantics qua các projection đã pin hoặc đưa phần cần thiết vào UC theo hợp đồng đầu vào được researcher chốt. Sửa relative links theo vị trí mới; không để prompt một UC mất classifier/enum hay BR context từ UC khác. Không tự tạo rule mới.

**OCL utility:** đặt tại `docs/01-inception/use-cases/OCL-UTILITY-DEFINITIONS.md`. Giữ nội dung utility 100ms, thay provenance Financial bằng nguồn thực tế và receipt mới. Header hiện tại của nguồn không đủ chứng minh file là projection từ sheet 100ms.

**API:** nhập 15 API nghiệp vụ vào `docs/01-inception/api-contracts/`, đặt tên theo API ID để dễ kiểm tra; nhập và pin cả `common-contract.md` vì endpoint kế thừa representations/envelopes/errors. Bảo toàn liên kết Related API IDs/Related UC IDs, thứ tự API và versioned paths `/api/v1/...`.

Áp dụng normalization theo repo ở downstream: success `{ success: true, message, data }`, error `{ success: false, statusCode, message, timestamp, path }`. Spec mới có `code` và optional `requestId`; việc chuẩn hóa phải bảo toàn business code/message/status semantics và có mapping rõ ràng. Không bỏ field nghiệp vụ hoặc đổi frozen source để giải quyết khác biệt envelope. `/api/v1` nằm dưới prefix `/api`; tránh thêm prefix hai lần.

Nghiệm thu: identity/front matter hợp lệ; không mất BR/flow/API inventory; mọi relative link và UML dependency được giải quyết; checksum dựa trên byte cuối cùng của projection; không còn placeholder giả. Mâu thuẫn material được ghi exact location và chờ researcher quyết định trước khi Frozen.

### Bước 3 — finalsource sạch và database

```text
finalsource/
├── be/                 # NestJS 11, TypeScript, TypeORM, MySQL
│   ├── src/
│   ├── Dockerfile
│   └── package.json, lockfile, tsconfig, lint config
├── fe/                 # React 18, TypeScript, Vite, Tailwind
│   ├── src/
│   ├── Dockerfile
│   └── package.json, lockfile, configs, nginx.conf
├── compose.yaml
├── .env                # local, ignored; không ghi giá trị vào báo cáo
└── .env.example        # chỉ tên biến/placeholder
```

- Giữ hạ tầng tái sử dụng phù hợp sau review: health endpoint, bootstrap, validation, error normalization, CORS, Dockerfiles, Nginx và các config.
- Loại bỏ domain/routes/pages/entities Financial; frontend baseline chỉ là shell, backend baseline là hạ tầng. Không cài sẵn hành vi của 18 UC trước thí nghiệm.
- Database CLI/migrations/entity mappings cần để chuẩn bị input được xác định rõ là hạ tầng baseline; phân biệt với service nghiệp vụ được sinh trong run.
- Dùng dependencies/lockfiles có thể cài đặt và build được; kiểm tra version nền tảng theo hợp đồng repo, không cập nhật toàn bộ dependency không cần thiết.
- Đặt `synchronize: false`, `migrationsRun: false` ở ứng dụng. Compose giữ database/migration/backend/frontend, healthcheck và thứ tự startup ngoài run.
- `docs/00-context/engineering/schema.dbml` là projection database đã được review của 100ms. Schema mới hiện khai báo 16 application tables, gồm sessions, principals, participants và các bảng collaboration/idempotency; DBML một mình không bao gồm toàn bộ persistence supplement.
- Sau khi researcher giải quyết procedure/trigger và MySQL 8.0/8.4, chuẩn bị migration TypeORM đầy đủ trên database mới; không chạy trực tiếp supplement để lách migration history.
- Researcher chuẩn bị ngoài run: provisioning session/designated-host/principal và credential issuance, catalog/media adapter/provider completion cần cho runtime. Tài liệu phải chốt input và ranh giới này trước khi bắt đầu UC cần chúng; không bổ sung unapproved public API.
- Capture `migration_head`, `dbml_sha256`, `schema_fingerprint_sha256` sau khi schema được review và runtime có thể truy cập. Giữ dữ liệu tích lũy giữa các UC.

Docker daemon hiện BLOCKED. Setup/runtime/migration là bước triển khai riêng khi được researcher yêu cầu; kế hoạch này không khởi động container hoặc sửa schema. Trong run chỉ rebuild `backend frontend` với `--no-deps`; không gọi migration service.

### Bước 4 — source-baseline.zip và SHA-256

Tạo ZIP sau khi baseline source và hạ tầng database đã cố định, trước sinh UC đầu tiên:

```text
source-baseline.zip
└── baseline/
    ├── be/src/...
    └── fe/src/...
```

- Sao chép đúng `finalsource/be/src` và `finalsource/fe/src` vào thư mục staging có cấu trúc trên.
- Lưu ZIP tại `.codex/skills/restore-source-baseline/assets/source-baseline.zip`.
- Kiểm tra entry bắt đầu bằng `baseline/be/src/` và `baseline/fe/src/`; không thêm tầng staging bên ngoài, không có path traversal/absolute entries.
- Không đưa `.env`, credentials, node_modules, dist hoặc evidence vào ZIP.
- Giải nén kiểm tra trong thư mục tạm thuộc repo; đối chiếu file inventory và checksum source với baseline vừa tạo. Không gọi restore skill như một phần kế hoạch.
- Tính raw-byte SHA-256 của ZIP; điền `PROJECT_PROFILE.json.clean_source_baseline_sha256` theo dạng `sha256:<64 hex>`. Đây là checksum ZIP, không phải Git commit SHA hoặc checksum thư mục finalsource.
- Giữ package/lockfiles/Compose/Dockerfiles bằng Git revision tương ứng vì ZIP chỉ phục hồi hai thư mục `src`.

### Bước 5 — FIGMA-LINK-REVIEW và immutable dataset

- Thay review Financial bằng inventory 100ms đã xác minh: UC ID/name, frozen path, file key, node ID, occurrence count, Replacement URL và connector verification.
- Mỗi UC có một primary replacement rõ ràng hoặc `NOT_APPLICABLE` có căn cứ; bổ sung mappings cho desktop/mobile, states và shared foundations/assets cần capture. Một node dùng chung cho nhiều UC chỉ capture một lần.
- Profile chỉ lưu root frame URLs; review lưu capture targets đã xác minh. Primary root cần bao quát các trạng thái liên quan hoặc supplement phải nêu đầy đủ để không mất bằng chứng.
- Chọn version mới rõ ràng, đề xuất `100ms-2026-10-01-001`; đây chỉ là tên dự kiến, chưa được chọn hoặc tạo. Không tự lấy version từ dataset Financial.
- Chạy `$resolve-figma-design-dataset` sau khi inventory Frozen mới và review không còn thiếu/conflict. Capture chỉ dùng cột `Replacement URL`, không dùng Figma URL từ UC provenance.
- Với từng capture node: `design-context.md`, `metadata.json`, `screenshot.png`, `export.png`, assets, `asset-map.json`, checksums; ghi truncation và xử lý đầy đủ trước `complete`.
- Shared assets trùng nội dung được lưu checksum-addressed trong dataset chưa Frozen. Loại URL asset ngắn hạn khỏi context; không lưu token/cookie.
- Validate tất cả bằng resolver với `--validate-all --dataset-version <version-đã-chốt>`; resolve từng UC bằng chính version này. Không đánh dấu complete nếu pending rate limit hoặc partial content.
- Cấu hình run sẽ pin version và manifest checksum. Frozen dataset không bị ghi đè; refresh tạo version mới.

Skill áp dụng: [resolve-figma-design-dataset](../../.codex/skills/resolve-figma-design-dataset/SKILL.md). Điều kiện trực tiếp: “Stop if any placeholder, conflict or missing mapping remains.” Review hiện chỉ ánh xạ Financial nên chưa thể capture dataset 100ms theo hợp đồng. Lỗi reauthentication là blocker bổ sung từ connector; khảo sát toàn page vẫn chưa hoàn tất.

### Bước 6 — Nghiệm thu và đầu vào thí nghiệm đầu tiên

- Rà Financial references trong tài nguyên hoạt động bằng tìm kiếm có phạm vi, phân biệt archive/provenance lịch sử với nguồn đang dùng.
- Kiểm tra profile/provenance, 18 Frozen UC, 14 Frozen API cùng common dependency, OCL/model/assumptions, DBML/migration history, ZIP checksum và Figma completeness.
- Chạy source inspection, deterministic validators, typecheck/lint/build phù hợp; sau setup được yêu cầu, kiểm tra Docker health/reachability và quan sát runtime có giới hạn. Không tạo/chạy tests hoặc chạy script DB probe của spec tạo schema/test data.
- Nghiệm thu khả năng phục hồi source từ ZIP bằng checksum, không reset database. Ghi commit của bộ input + scaffolding + lockfiles đã hoàn tất.
- Sau đó chuẩn bị riêng cho UC/model/variant đầu tiên: Confirmed configuration, complete ordered BR baseline, complete ordered flow baseline và Draft Canonical Run JSON. UC-01 là client-local theo spec, không tự gán API nghiệp vụ cho nó.
- Pin UC/API inventories/checksums, Figma version/manifest checksum, ba database pins và configuration checksum. Giữ rubric `completion-critical-flow-runtime-v2` và timing protocol `generation_execution_with_repair_audit_v2`.
- Các JSON này được chuẩn bị trước generation, không tạo hoặc sửa thiếu sót trong prompt/source preflight. Prompt close phê duyệt Draft và tạo/validate activation; không thêm activation turn.

Repo chỉ READY khi các mục trên đạt yêu cầu. Sau đó researcher bắt đầu quy trình hai pha bằng `$gen-coding-prompt` cho đúng frozen UC; các lệnh close/source/audit/repair/finalize vẫn thực hiện ở những turn riêng theo FILE-DRIVEN-WORKFLOW.md.

## Phạm vi đã thực hiện trong lượt lập kế hoạch

Đã đọc hướng dẫn repo, skill resolver, mô hình đầu vào/database/capture; khảo sát cấu trúc repo và bộ spec do researcher cung cấp; kiểm tra Docker read-only; gọi Figma page inventory một lần và nhận lỗi xác thực. Đã tạo tài liệu kế hoạch này. Chưa thay profile, frozen inputs, source, ZIP, schema, Figma review hoặc dataset; chưa thực hiện workflow generation/audit/repair.

## Kết quả thực hiện kế hoạch

Researcher yêu cầu thực hiện và tạm hoãn database. Xem [100MS-SETUP-REPORT.md](100MS-SETUP-REPORT.md) cho artifact, validation và các blocker thực tế. Nguồn thực tế có 15 API; README nguồn ghi 14. Toàn bộ 69 page đã quét; capture Figma bị giới hạn MCP Education plan.
