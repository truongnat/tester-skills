# Bộ Skill cho Tester Manual

## Danh sách Skill trong bộ này

| # | Skill | Nhóm | Cần MCP? |
|---|---|---|---|
| 1 | testcase-generator | Thiết kế test | Không |
| 2 | requirement-gap-checker | Trước khi test | Không |
| 3 | testcase-coverage-reviewer | Thiết kế test | Không |
| 4 | api-testcase-generator | API testing | Không |
| 5 | api-response-validator | API testing | Không |
| 6 | test-plan-writer | Test strategy | Không |
| 7 | risk-based-prioritizer | Test strategy | Không |
| 8 | exploratory-charter-builder | Exploratory testing | Không |
| 9 | edge-case-brainstormer | Exploratory testing | Không |
| 10 | accessibility-checklist-runner | Chất lượng chuyên biệt | Không |
| 11 | i18n-checklist-runner | Chất lượng chuyên biệt | Không |
| 12 | sql-analyzer | Thực thi & Điều tra | Có — MCP Database (read-only) |
| 13 | browser-investigator | Thực thi & Điều tra | Có — MCP Browser (Claude in Chrome) |
| 14 | root-cause-hypothesis | Điều tra nguyên nhân | Không |
| 15 | automation-script-builder | Automation cơ bản | Không (khuyến khích dùng trong Claude Code) |
| 16 | test-data-generator | Test data | Không |
| 17 | bug-report-writer | Ghi nhận & Báo cáo | Không |
| 18 | repro-steps-verifier | Ghi nhận & Báo cáo | Không |
| 19 | daily-report-writer | Tổng hợp & Giao tiếp | Không |
| 20 | standup-notes-summarizer | Tổng hợp & Giao tiếp | Không |

## Về "context-completeness-checker"

Đây KHÔNG phải một Skill riêng để cài đặt. Đây là nguyên tắc thiết kế đã nhúng vào phần "Bước 1" hoặc "Checklist" của từng Skill ở trên: mọi Skill đều tự kiểm tra thiếu thông tin gì trước khi xử lý, và chủ động hỏi lại cụ thể thay vì xử lý với dữ liệu thiếu. Bạn không cần làm gì thêm cho phần này — nó đã có sẵn trong từng file.

## Quy ước timestamp và artifact

Khi bắt đầu chạy bất kỳ Skill nào, ghi lại `Session timestamp` theo timezone của user/project, format:

```text
YYYY-MM-DD HH:mm:ss Z
```

Nếu Skill tạo file output, lưu theo cấu trúc:

```text
artifacts/YYYY-MM-DD/<skill-name>/HHmmss-short-topic/
```

Daily report chỉ lấy activity trong đúng ngày report, tức là chỉ đọc `artifacts/YYYY-MM-DD/` của ngày đó, trừ khi user yêu cầu report tuần hoặc nhiều ngày.

## Thứ tự nên dùng thử trước

1. `bug-report-writer` — dùng ngay, hiệu quả thấy rõ nhất
2. `requirement-gap-checker` → `testcase-generator` — dùng khi nhận feature mới
3. `repro-steps-verifier` — dùng trước khi gửi bug đã viết cho dev
4. `daily-report-writer` — dùng cuối ngày/tuần
5. `api-testcase-generator`, `api-response-validator` — dùng khi bắt đầu test API từ Swagger/Postman/JSON response
6. `testcase-coverage-reviewer` — dùng khi rà lại bộ test case cũ trước release
7. `test-plan-writer`, `risk-based-prioritizer` — dùng ở tầm sprint/release hoặc khi thời gian test gấp
8. `exploratory-charter-builder`, `edge-case-brainstormer` — dùng khi cần khám phá nghiệp vụ hoặc nghĩ case ngoài spec
9. `sql-analyzer`, `browser-investigator` — cần thiết lập MCP trước nếu muốn đọc DB/browser trực tiếp
10. `test-data-generator`, `accessibility-checklist-runner`, `i18n-checklist-runner` — dùng bổ trợ theo nhu cầu dự án
11. `standup-notes-summarizer` — dùng cho cập nhật cực ngắn trong daily standup
12. `automation-script-builder` — dùng khi bắt đầu học automation, nên dùng trong Claude Code để có thể chạy thử script luôn

## Cách cài đặt
1. Vào **Customize > Skills** trên claude.ai (cần bật Code execution and file creation trước)
2. Upload từng thư mục Skill dưới dạng file zip riêng (mỗi Skill 1 file zip chứa SKILL.md của nó)
3. Với Claude Code: copy thư mục Skill vào `.claude/skills/<tên-skill>/` trong project

## Lưu ý khi chỉnh sửa
Nếu team có format riêng (template test case, template bug report khác với mẫu trong các Skill này), chỉnh trực tiếp phần "Format output"/"Template" trong từng file SKILL.md cho khớp — không cần viết lại toàn bộ Skill.
