# Bộ Skill cho Tester Manual

## Danh sách Skill trong bộ này

| # | Skill | Nhóm | Cần MCP? |
|---|---|---|---|
| 1 | testcase-generator | Thiết kế test | Không |
| 2 | requirement-gap-checker | Trước khi test | Không |
| 3 | testcase-coverage-reviewer | Thiết kế test | Không |
| 4 | sql-analyzer | Thực thi & Điều tra | Có — MCP Database (read-only) |
| 5 | browser-investigator | Thực thi & Điều tra | Có — MCP Browser (Claude in Chrome) |
| 6 | automation-script-builder | Thực thi & Điều tra | Không (khuyến khích dùng trong Claude Code) |
| 7 | bug-report-writer | Ghi nhận & Báo cáo | Không |
| 8 | repro-steps-verifier | Ghi nhận & Báo cáo | Không |
| 9 | daily-report-writer | Tổng hợp & Giao tiếp | Không |

(Skill `testcase-generator` đã gửi ở lượt trước, không nằm trong file zip này — dùng chung với 8 skill trên.)

## Về "context-completeness-checker"

Đây KHÔNG phải một Skill riêng để cài đặt. Đây là nguyên tắc thiết kế đã nhúng vào phần "Bước 1" hoặc "Checklist" của từng Skill ở trên: mọi Skill đều tự kiểm tra thiếu thông tin gì trước khi xử lý, và chủ động hỏi lại cụ thể thay vì xử lý với dữ liệu thiếu. Bạn không cần làm gì thêm cho phần này — nó đã có sẵn trong từng file.

## Thứ tự nên dùng thử trước

1. `bug-report-writer` — dùng ngay, hiệu quả thấy rõ nhất
2. `requirement-gap-checker` → `testcase-generator` — dùng khi nhận feature mới
3. `repro-steps-verifier` — dùng trước khi gửi bug đã viết cho dev
4. `daily-report-writer` — dùng cuối ngày/tuần
5. `testcase-coverage-reviewer` — dùng khi rà lại bộ test case cũ trước release
6. `sql-analyzer`, `browser-investigator` — cần thiết lập MCP trước (nhờ dev/IT hỗ trợ kết nối DB read-only và Claude in Chrome)
7. `automation-script-builder` — dùng khi bắt đầu học automation, nên dùng trong Claude Code để có thể chạy thử script luôn

## Cách cài đặt
1. Vào **Customize > Skills** trên claude.ai (cần bật Code execution and file creation trước)
2. Upload từng thư mục Skill dưới dạng file zip riêng (mỗi Skill 1 file zip chứa SKILL.md của nó)
3. Với Claude Code: copy thư mục Skill vào `.claude/skills/<tên-skill>/` trong project

## Lưu ý khi chỉnh sửa
Nếu team có format riêng (template test case, template bug report khác với mẫu trong các Skill này), chỉnh trực tiếp phần "Format output"/"Template" trong từng file SKILL.md cho khớp — không cần viết lại toàn bộ Skill.
