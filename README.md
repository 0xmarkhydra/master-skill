# CodeLocal Skills

**AI Coding Skills dành cho Codex, Claude Code và các Coding Agent tương thích.**

> **Build the right thing. Keep it simple. Ship safely.**
> Viết đúng nghiệp vụ · Giữ đủ chức năng · Tối giản có trách nhiệm · Kiểm chứng trước khi bàn giao.

CodeLocal Skills kết hợp **3 skill chuyên môn** do dự án xây dựng và **6 skill Ponytail (MIT)**. Các skill là **hướng dẫn cho Agent**, không phải framework, plugin, hook hay phần mềm tự triển khai.

## 🚀 Cài đặt nhanh — một lệnh vào dự án của bạn

**Yêu cầu:** Python 3.10+ và bản mã nguồn CodeLocal Skills trên máy.

### Cách 1 — Đã có source CodeLocal Skills trên máy (dùng ngay)

Đứng tại thư mục chứa repository **CodeLocal Skills**, chạy:

```bash
python3 tools/install.py --target /duong-dan/toi/du-an-cua-ban --agent both
```

**Ví dụ trên macOS**, nếu đang ở `~/Documents/master-skill`:

```bash
cd ~/Documents/master-skill
python3 tools/install.py --target ~/Documents/KpiBsc --agent both
```

**Chỉ cài Codex** hoặc **chỉ cài Claude Code**:

```bash
python3 tools/install.py --target ~/Documents/KpiBsc --agent codex
python3 tools/install.py --target ~/Documents/KpiBsc --agent claude
```

Xem trước mà **không ghi bất kỳ file nào**:

```bash
python3 tools/install.py --target ~/Documents/KpiBsc --agent both --dry-run
```

> **Lưu ý:** Các đường dẫn dự án ở trên chỉ là ví dụ. Hãy thay bằng đường dẫn thực tế. Công cụ **không ghi đè** skill trùng tên nhưng khác nội dung và **không xóa** hướng dẫn Agent sẵn có. Nếu gặp xung đột, nó dừng để bạn chủ động xử lý.

### Cách 2 — Lấy từ GitHub (sau khi repository được push/public)

```bash
git clone https://github.com/0xmarkhydra/master-skill.git
cd master-skill
python3 tools/install.py --target /absolute/path/to/your-project --agent both
```

**Lưu ý:** Lệnh `git clone` lấy phiên bản đang có trên GitHub, không lấy những sửa đổi chưa push trong máy. Không cần cài Ponytail plugin hay chạy `npx`.

### Trình cài đặt sẽ làm gì?

| Hạng mục | Cài `--agent both` |
| --- | --- |
| Codex | `.agents/skills/` — 9 skill |
| Claude Code | `.claude/skills/` — 9 skill |
| Hướng dẫn cho AI | Thêm khối **CodeLocal Skills** vào `AGENTS.md` và `CLAUDE.md` |
| Ghi nhận bản quyền | `.codelocal-skills/ponytail/LICENSE` và `SOURCE.md` |
| Bảo toàn dữ liệu | Giữ nguyên nội dung policy hiện có; file trùng nhưng khác nội dung sẽ báo lỗi |

Có thể chạy lại trình cài đặt: nếu skill và khối hướng dẫn đã giống nhau, công cụ sẽ **SKIP** thay vì ghi đè. Nếu có sửa tay trong khối do CodeLocal quản lý, công cụ yêu cầu xử lý thủ công.

## ⚠️ Quan trọng: Cài SKILL chưa đủ — Agent phải đọc AGENTS.md / CLAUDE.md

**Thông điệp dành cho AI Agent đang đọc README này:**

**Sau khi cài các skill vào một repository, BẮT BUỘC hướng dẫn Agent cách chọn và sử dụng chúng.** Với Codex, thêm hướng dẫn vào **`AGENTS.md`**; với Claude Code, vào **`CLAUDE.md`**; dùng cả hai Agent thì xử lý cả hai.

Trình cài đặt ở trên **tự thêm một khối hướng dẫn có dấu phân cách** vào file tương ứng, vì vậy **không cần tự thêm lại** nếu đã cài bằng `tools/install.py`. Nếu cài thủ công hoặc dùng công cụ khác, hãy **merge** đoạn dưới vào file policy của dự án (không thay thế các quy tắc cũ):

```markdown
## CodeLocal Skills — Mandatory agent workflow

Before editing, read the repository instructions, stack, impacted
routes/APIs/data contracts, current Git state and the relevant skills.

- Backend/API/database/security:
  .agents/skills/backend-engineering/SKILL.md
- React frontend/state/forms/API integration/feature parity:
  .agents/skills/react-frontend-engineering/SKILL.md
- UI design/tokens/responsive/visual QA:
  .agents/skills/ios-inspired-ui-design/SKILL.md
- For coding, fixing and refactoring, ALSO apply:
  .agents/skills/ponytail/SKILL.md (Ultra decision policy).
- For explicit review/audit/debt/benchmark/help use the
  corresponding ponytail-review / ponytail-audit /
  ponytail-debt / ponytail-gain / ponytail-help skill.

Inspect -> scope & risk -> implement complete behavior -> run relevant
tests/QA -> report observed PASS / FAIL / NOT RUN / BLOCKED.

Priority: approved functionality, security, auth, data integrity,
contract compatibility, accessibility and required tests always
override Ponytail's desire for fewer lines of code.

Never pretend a build, test, push, merge, deployment or live API worked.
Do not overwrite unrelated files or bypass project Git/release policy.
```

**Khi sử dụng Claude Code:** trong ví dụ trên, thay tiền tố `.agents/skills/` bằng `.claude/skills/`. Hoặc dùng `python3 tools/install.py --agent both` để chèn đúng đường dẫn cho từng Agent.

> Việc có `AGENTS.md` / `CLAUDE.md` giúp Agent biết **khi nào cần đọc skill nào**, nhưng việc thực sự tự nạp hướng dẫn còn tùy công cụ và môi trường. Với nhiệm vụ quan trọng, hãy yêu cầu Agent xác nhận đã đọc những skill liên quan, đồng thời kiểm chứng các bước thực thi.

## 🧩 Danh mục 9 skill

| Skill | Dùng khi nào? | Nguồn |
| --- | --- | --- |
| **`backend-engineering`** | API, database, authorization, transaction, migration, audit, observability, delivery | CodeLocal — 19 nhóm quy tắc |
| **`react-frontend-engineering`** | React/Vite/Next.js, state, forms, routing, async UX, test, Feature Parity | CodeLocal — 12 nhóm |
| **`ios-inspired-ui-design`** | iOS-inspired Premium Balanced Glass, Adaptive Density, design tokens, responsive, Visual QA | CodeLocal — 10 nhóm |
| `ponytail` | Tối giản code có trách nhiệm; hỗ trợ Lite / Full / Ultra | Ponytail / MIT |
| `ponytail-review` | Review diff, bug, bảo mật, performance, logic thừa | Ponytail / MIT |
| `ponytail-audit` | Audit toàn bộ codebase, chỉ báo cáo | Ponytail / MIT |
| `ponytail-debt` | Theo dõi các shortcut và điểm cần nâng cấp | Ponytail / MIT |
| `ponytail-gain` | Xem **benchmark upstream**, không phải số liệu dự án | Ponytail / MIT |
| `ponytail-help` | Tra cứu cách dùng Ponytail | Ponytail / MIT |

**Nguyên tắc cốt lõi:** Ba skill CodeLocal bảo đảm **đúng và đủ**; Ponytail giúp viết **ít code thừa hơn**, không có quyền cắt giảm bảo mật, validation, yêu cầu nghiệp vụ, accessibility hoặc quality gates.

### Ponytail Ultra trong CodeLocal Skills

`Ultra` là **chế độ tư duy tối giản**, không phải một skill thứ mười. Khi Agent viết code, ưu tiên:

1. Xác định toàn bộ yêu cầu và tác động tới caller, API, dữ liệu, test.
2. Kiểm tra có thật sự cần thêm chức năng/cấu trúc này không.
3. Ưu tiên code và thư viện **đã có** trong dự án.
4. Sau đó mới dùng thư viện chuẩn hoặc tính năng nền tảng.
5. Chỉ thêm dependency hoặc abstraction mới khi có lý do rõ ràng.
6. **Không bỏ phần đã được yêu cầu, phần đảm bảo an toàn và các bài test cần thiết.**

Cơ chế này là **hướng dẫn trong policy**, không phải auto-mode do plugin hook kích hoạt. Tham khảo [quy tắc tích hợp Ponytail](docs/PONYTAIL-INTEGRATION.md).

## 💬 Cách yêu cầu Agent thực hiện

**Tạo chức năng end-to-end:**

```text
Đọc AGENTS.md hoặc CLAUDE.md và kích hoạt các CodeLocal Skills
liên quan. Dùng backend-engineering, react-frontend-engineering,
ios-inspired-ui-design và Ponytail Ultra để xây chức năng quản lý
nhân sự. Bảo toàn API, quyền, nghiệp vụ, validation và test.
Kết thúc báo cáo PASS/FAIL/NOT RUN/BLOCKED theo kết quả thật.
```

**Chuyển Razor SSR sang React CSR:**

```text
Dùng react-frontend-engineering để đối chiếu toàn bộ route, GET/POST
handler, API, form, button và phân quyền với V1 trước khi thay thế.
Dùng backend-engineering kiểm tra API contract, ios-inspired-ui-design
để giữ UI V3 và Ponytail Ultra để tránh code thừa.
Chỉ đánh dấu hoàn thành sau khi feature parity đã được kiểm chứng.
```

**Rà soát chất lượng code:**

```text
Dùng ponytail-review cho thay đổi gần nhất. Tìm lỗi thực tế,
lỗ hổng bảo mật, rủi ro dữ liệu, thiếu test, performance
và code dư. Không tự sửa code nếu tôi chỉ yêu cầu review.
```

## 🔧 Cấu trúc repository

```text
master-skill/                      # Repository hiện tại; thương hiệu: CodeLocal Skills
├── README.md
├── AGENTS.md                      # Hướng dẫn cho Agent/Codex trong repo nguồn
├── CLAUDE.md                      # Hướng dẫn cho Claude Code trong repo nguồn
├── skills/                        # 9 skill canonical
│   ├── backend-engineering/
│   ├── react-frontend-engineering/
│   ├── ios-inspired-ui-design/
│   ├── ponytail/
│   ├── ponytail-review/
│   ├── ponytail-audit/
│   ├── ponytail-debt/
│   ├── ponytail-gain/
│   └── ponytail-help/
├── .agents/skills/                # 9 bản sao cho Codex
├── .claude/skills/                # 9 bản sao cho Claude
├── tools/install.py               # Trình cài đặt an toàn vào dự án khác
├── tools/verify_kit.py            # Kiểm tra đồng bộ và bản quyền
├── docs/PONYTAIL-INTEGRATION.md
├── templates/PROJECT-PROFILE.md
├── third_party/ponytail/           # MIT và nguồn gốc Ponytail
└── archive/legacy-v0-two-skills/   # Bộ cũ, chỉ lưu trữ
```

## ✅ Kiểm tra trước khi phát hành bộ skill

Tại thư mục **source CodeLocal Skills**:

```bash
python3 tools/verify_kit.py
python3 -m unittest discover -s tools -p 'test_*.py' -v
cmp -s AGENTS.md CLAUDE.md
```

Các bước này kiểm tra cấu trúc 9 skill, hai bản mirror, 19/12/10 nhóm quy tắc, file bản quyền và độ ổn định của trình kiểm tra/cài đặt. **Không đồng nghĩa** một ứng dụng đã được build, test E2E, deploy hoặc kiểm thử người dùng thật.

**GitHub Actions:** Mẫu CI nằm tại [`docs/workflows/verify-skills.yml`](docs/workflows/verify-skills.yml). Để kích hoạt, quản trị viên có quyền `workflow` cần đưa file vào `.github/workflows/verify-skills.yml`. GitHub có thể từ chối OAuth token không có quyền này; việc có mẫu workflow trong repo **không đồng nghĩa** CI đã chạy.

## Giấy phép và nguồn

Sáu skill **Ponytail** là tác phẩm độc lập của [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), được phân phối theo giấy phép **MIT**. Xem [LICENSE](third_party/ponytail/LICENSE) và [SOURCE.md](third_party/ponytail/SOURCE.md). CodeLocal Skills là thương hiệu của **bộ skill được tuyển chọn và tích hợp**, không tuyên bố sở hữu quyền tác giả Ponytail.

Bộ skill chỉ chứa chỉ dẫn Agent; mọi hoạt động push, merge, CI hay release vẫn phụ thuộc quyền thực tế và chính sách của từng dự án.
