# Support Scripts

Các script trong `scripts/support/` được thiết kế để hỗ trợ skill làm việc với file, URL và artifact theo nguyên tắc:

- mặc định chạy `--report`
- chỉ ghi file khi có `--execute`
- in rõ `Session timestamp`
- mô tả trước input, output và rủi ro

Vị trí script:

- Khi dùng repo local hoặc plugin bundle: `scripts/support/`
- Khi cài skill trực tiếp vào `~/.claude/skills`: `~/.claude/skills/.tester-skills-support/scripts/support/`

## Danh sách hiện có

### `artifact_init.py`

Tạo trước thư mục artifact và metadata cho một lần chạy skill.

```bash
python3 scripts/support/artifact_init.py bug-report-writer login-error --report
python3 scripts/support/artifact_init.py bug-report-writer login-error --execute
```

### `safe_download.py`

Kiểm tra và tải file từ URL với giới hạn size.

```bash
python3 scripts/support/safe_download.py https://example.com/spec.pdf --report
python3 scripts/support/safe_download.py https://example.com/spec.pdf --execute --out /tmp/spec.pdf
```

### `read_excel.py`

Đọc `.csv` hoặc `.xlsx`, báo sheet/header/sample rows.

```bash
python3 scripts/support/read_excel.py sample.xlsx --report
python3 scripts/support/read_excel.py sample.csv --execute --out artifacts/2026-07-07/testcase-generator/demo
```

### `read_pdf.py`

Kiểm tra file PDF và trích text nếu có `pypdf`.

```bash
python3 scripts/support/read_pdf.py spec.pdf --report
python3 scripts/support/read_pdf.py spec.pdf --execute
```

### `parse_openapi.py`

Parse file OpenAPI JSON/YAML để lấy endpoint, response code, security scheme.

```bash
python3 scripts/support/parse_openapi.py openapi.json --report
python3 scripts/support/parse_openapi.py openapi.yaml --execute
```

### `parse_postman.py`

Parse Postman collection JSON để liệt kê request, auth type, URL và body mode.

```bash
python3 scripts/support/parse_postman.py collection.json --report
python3 scripts/support/parse_postman.py collection.json --execute
```

### `postman_env_redactor.py`

Che giá trị nhạy cảm trong Postman environment export trước khi lưu artifact hoặc chia sẻ cho người khác.

```bash
python3 scripts/support/postman_env_redactor.py env.json --report
python3 scripts/support/postman_env_redactor.py env.json --execute
```

### `compare_json.py`

So sánh actual JSON và expected JSON.

```bash
python3 scripts/support/compare_json.py actual.json expected.json --report
python3 scripts/support/compare_json.py actual.json expected.json --execute
```

### `json_to_markdown_table.py`

Đổi JSON object hoặc list thành bảng Markdown dễ review trong chat hoặc artifact.

```bash
python3 scripts/support/json_to_markdown_table.py response.json --report
python3 scripts/support/json_to_markdown_table.py response.json --execute
```

### `read_docx.py`

Đọc file Word `.docx`, báo số đoạn, số bảng và sample nội dung; có thể extract text khi đủ dependency.

```bash
python3 scripts/support/read_docx.py spec.docx --report
python3 scripts/support/read_docx.py spec.docx --execute
```

### `har_summarizer.py`

Tóm tắt HAR thành danh sách request, status, host và request chậm.

```bash
python3 scripts/support/har_summarizer.py session.har --report
python3 scripts/support/har_summarizer.py session.har --execute
```

### `artifact_index.py`

Index toàn bộ artifact của đúng một ngày để dùng cho daily report hoặc review activity.

```bash
python3 scripts/support/artifact_index.py 2026-07-07 --report
python3 scripts/support/artifact_index.py 2026-07-07 --execute
```

### `session_timeline_builder.py`

Dựng timeline file trong một artifact run để xem evidence được tạo theo thứ tự nào.

```bash
python3 scripts/support/session_timeline_builder.py artifacts/2026-07-07/bug-report-writer/101500-login-bug --report
python3 scripts/support/session_timeline_builder.py artifacts/2026-07-07/bug-report-writer/101500-login-bug --execute
```

### `markdown_table_to_csv.py`

Đổi bảng Markdown pipe table sang CSV.

```bash
python3 scripts/support/markdown_table_to_csv.py testcases.md --report
python3 scripts/support/markdown_table_to_csv.py testcases.md --execute
```

### `evidence_manifest.py`

Chuẩn hóa danh sách file evidence, đoán MIME type và đếm pattern nhạy cảm với file text/log phổ biến.

```bash
python3 scripts/support/evidence_manifest.py error.png error.har console.log --report
python3 scripts/support/evidence_manifest.py error.png error.har console.log --execute --title checkout-failure
```

### `artifact_packager.py`

Nén một artifact directory thành file `.zip` để gửi dev, lead hoặc lưu trữ.

```bash
python3 scripts/support/artifact_packager.py artifacts/2026-07-07/browser-investigator/111000-checkout-fail --report
python3 scripts/support/artifact_packager.py artifacts/2026-07-07/browser-investigator/111000-checkout-fail --execute
```

### `redact_sensitive.py`

Phát hiện và che token, email, phone và một số pattern nhạy cảm cơ bản.

```bash
python3 scripts/support/redact_sensitive.py raw-log.txt --report
python3 scripts/support/redact_sensitive.py raw-log.txt --execute
```

## Dependency tùy chọn

- `openpyxl`: cần cho `.xlsx`
- `pypdf`: cần cho `.pdf`
- `PyYAML`: cần cho OpenAPI YAML
- `python-docx`: cần cho `.docx`

Nếu thiếu dependency, script vẫn report được và sẽ nói rõ không thể `--execute`.
