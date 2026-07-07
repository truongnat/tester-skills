# Cài đặt bộ Tester Skills cho Claude

Tài liệu này ưu tiên cách cài từ remote GitHub, không cần clone repository.

## 1. Claude Code: chạy plugin remote một lần

Claude Code hỗ trợ load plugin zip trực tiếp từ URL:

```bash
claude --plugin-url https://github.com/truongnat/tester-skills/releases/latest/download/tester-skills-plugin.zip
```

Khi load bằng plugin, skill được namespace theo plugin:

```text
/tester-skills:bug-report-writer
/tester-skills:api-testcase-generator
/tester-skills:test-plan-writer
```

## 2. Claude Code: cài marketplace remote

Nếu muốn install plugin từ GitHub để dùng lâu dài:

```bash
claude plugin marketplace add https://github.com/truongnat/tester-skills
claude plugin install tester-skills@tester-skills
```

Sau khi install hoặc update plugin, mở session mới hoặc chạy:

```text
/reload-plugins
```

## 3. Claude Code: cài skill remote vào `~/.claude/skills`

Cách này copy toàn bộ skill vào thư mục skills của user, không cần clone repo:

```bash
curl -fsSL https://raw.githubusercontent.com/truongnat/tester-skills/main/scripts/install_remote.py | python3 - --force
```

Sau đó mở lại Claude Code. Các skill có thể gọi bằng tên trực tiếp:

```text
/bug-report-writer
/api-testcase-generator
/daily-report-writer
```

## 4. Claude Desktop hoặc Claude Web: upload từ GitHub Release

Claude Desktop/Web quản lý skill qua UI `Customize > Skills`. Desktop extension `.mcpb` là cơ chế cho MCP/Extensions, không phải cách cài `SKILL.md`.

Tải file zip từ GitHub Release:

```text
https://github.com/truongnat/tester-skills/releases/latest
```

Trong release sẽ có:

- `tester-skills-plugin.zip`: dùng cho Claude Code `--plugin-url`.
- `<skill-name>.zip`: upload từng skill riêng vào Claude Desktop/Web.
- `tester-skills-all.zip`: gói tổng hợp để lưu trữ hoặc chia sẻ.

Khuyến nghị upload từng `<skill-name>.zip` riêng nếu Claude Desktop/Web yêu cầu mỗi skill là một gói riêng.

## 5. Local development: chỉ dùng khi đã clone repo

Các lệnh dưới đây dành cho người phát triển repo.

### Cài skill trực tiếp

Cài toàn bộ skill vào thư mục user-level `~/.claude/skills`:

```bash
make install-claude
```

Hoặc chạy trực tiếp:

```bash
python3 scripts/install_claude_skills.py --scope user --force
```

Sau đó mở lại Claude Code. Các skill có thể gọi bằng tên trực tiếp, ví dụ:

```text
/bug-report-writer
/api-testcase-generator
/daily-report-writer
```

Nếu chỉ muốn cài trong project hiện tại:

```bash
make install-claude-project
```

Lệnh này copy skill vào:

```text
.claude/skills/
```

### Load repo local như plugin

Repository này đã có manifest:

```text
.claude-plugin/plugin.json
```

Có thể load trực tiếp repo hiện tại như plugin:

```bash
claude --plugin-dir .
```

Khi load bằng plugin, skill được namespace theo plugin:

```text
/tester-skills:bug-report-writer
/tester-skills:api-testcase-generator
/tester-skills:test-plan-writer
```

Nếu muốn tạo plugin package sạch trong `dist/`:

```bash
make build-plugin
```

Kết quả:

```text
dist/tester-skills-plugin/
dist/tester-skills-plugin.zip
```

Load bản build:

```bash
claude --plugin-dir ./dist/tester-skills-plugin
```

Nếu đang mở Claude Code và vừa sửa plugin, chạy:

```text
/reload-plugins
```

### Build package local

Tạo file zip để upload:

```bash
make package-desktop
```

Kết quả nằm ở:

```text
dist/claude-desktop-skills/
```

Có 2 kiểu file:

- `<skill-name>.zip`: upload từng skill riêng.
- `tester-skills-all.zip`: gói toàn bộ skill để lưu trữ hoặc chia sẻ.

Khuyến nghị upload từng skill riêng nếu Claude Desktop/Web yêu cầu mỗi skill là một gói riêng.

## Kiểm tra nhanh

Validate cấu trúc `SKILL.md`:

```bash
make validate-skills
```

Đếm số skill:

```bash
find . -maxdepth 2 -name SKILL.md | wc -l
```

Hiện repository có 20 skill.
