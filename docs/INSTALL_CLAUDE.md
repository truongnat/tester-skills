# Cài đặt bộ Tester Skills cho Claude

Tài liệu này có 3 cách dùng, tùy môi trường Claude của bạn.

## 1. Claude Code: cài skill trực tiếp

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

## 2. Claude Code: load như plugin

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

## 3. Claude Desktop hoặc Claude Web: upload qua Skills UI

Claude Desktop/Web quản lý skill qua UI `Customize > Skills`. Desktop extension `.mcpb` là cơ chế cho MCP/Extensions, không phải cách cài `SKILL.md`.

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
