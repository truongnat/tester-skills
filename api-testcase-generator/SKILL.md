---
name: api-testcase-generator
description: "Sinh test case API từ Swagger/OpenAPI spec, Postman collection, tài liệu endpoint hoặc mô tả request/response. Dùng khi tester cần kiểm thử API mà không cần đọc source code: status code, schema, required params, auth, permission, boundary, negative case và error handling."
---

# API Testcase Generator

## Quy ước timestamp và artifact
Ngay khi bắt đầu chạy Skill, lấy timestamp hiện tại theo timezone của user/project, format `YYYY-MM-DD HH:mm:ss Z`.

Nếu có tạo file output, lưu theo cấu trúc:

```text
artifacts/YYYY-MM-DD/api-testcase-generator/HHmmss-api-or-feature/
```

Mỗi output chính phải ghi `Session timestamp`, nguồn spec, assumption, endpoint được cover và case bị giới hạn do thiếu thông tin.

## Mục tiêu
Tạo test case API thực dụng cho tester manual từ Swagger/OpenAPI, Postman collection, curl, sample request/response hoặc mô tả endpoint.

## Quy trình

### Bước 1 - Đọc input và hỏi thiếu thông tin
Xác định:

- Base URL hoặc môi trường test.
- Endpoint, method, path param, query param, body, header.
- Auth type: bearer token, API key, session, role/permission.
- Response schema, status code kỳ vọng, error format.
- Rule nghiệp vụ liên quan tới endpoint.

Nếu thiếu thông tin, hỏi tối đa 3 câu quan trọng nhất trước. Nếu user nói cứ generate với thông tin hiện có, tiếp tục và ghi rõ assumption.

### Bước 2 - Sinh case theo nhóm

- Positive: request hợp lệ, status code đúng, response schema đúng.
- Required field: thiếu từng param/body field bắt buộc.
- Type/format: sai kiểu dữ liệu, sai format email/date/UUID/number.
- Boundary: min/max, rỗng, null, quá dài, list trống/list lớn.
- Auth: thiếu token, token hết hạn, token sai, role không đủ quyền.
- Permission: user A truy cập dữ liệu user B, role thấp gọi endpoint role cao.
- Business rule: trạng thái không hợp lệ, workflow sai thứ tự, dữ liệu không tồn tại.
- Error handling: 400/401/403/404/409/422/500 nếu áp dụng.
- Contract: response thiếu field, thừa field quan trọng, sai enum, sai nullable.

Chỉ sinh case phù hợp với endpoint. Nếu nhóm không áp dụng, ghi lý do skip.

## Format output

```text
Session timestamp: [YYYY-MM-DD HH:mm:ss Z]
API source: [Swagger/Postman/curl/spec text]
Assumptions: [...]

| ID | Endpoint | Method | Title | Type | Priority | Preconditions | Request Data | Expected Status | Expected Response | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
```

Priority:

- `P0`: luồng chính, auth/permission quan trọng, case có rủi ro cao.
- `P1`: negative/boundary thường gặp.
- `P2`: edge case ít gặp hoặc phụ thuộc môi trường.

## Lưu ý
- Không tự bịa schema nếu spec không có. Chỉ suy luận có đánh dấu `Assumption`.
- Không sinh request chứa token thật, password thật hoặc dữ liệu cá nhân thật.
- Nếu user cần file CSV, tạo `api-testcases.csv` trong artifact folder với cùng cột.
