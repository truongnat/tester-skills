# Support Scripts

Các script trong `scripts/support/` được thiết kế để hỗ trợ skill làm việc với file, URL và artifact theo nguyên tắc:

- mặc định chạy `--report`
- chỉ ghi file khi có `--execute`
- in rõ `Session timestamp`
- mô tả trước input, output và rủi ro

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

### `compare_json.py`

So sánh actual JSON và expected JSON.

```bash
python3 scripts/support/compare_json.py actual.json expected.json --report
python3 scripts/support/compare_json.py actual.json expected.json --execute
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

Nếu thiếu dependency, script vẫn report được và sẽ nói rõ không thể `--execute`.
