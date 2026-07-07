---
name: sql-analyzer
description: Dịch yêu cầu kiểm tra dữ liệu bằng ngôn ngữ tự nhiên thành câu lệnh SQL, chạy qua kết nối database (MCP) nếu có sẵn, và giải thích kết quả bằng ngôn ngữ dễ hiểu cho tester không rành SQL. Dùng khi user cần verify dữ liệu trong DB, hoặc khi dev đưa một câu SQL và user cần hiểu nó đang làm gì.
---

# SQL Analyzer

## Điều kiện tiên quyết
Skill này cần một kết nối MCP tới database (read-only) đã được thiết lập sẵn trong Claude Desktop/claude.ai. Nếu không có kết nối MCP database nào khả dụng trong phiên làm việc, KHÔNG tự bịa kết quả — báo cho user rằng cần kết nối MCP database trước, và có thể đề xuất tìm connector phù hợp.

## Hai chế độ sử dụng

### Chế độ 1 — User mô tả điều cần kiểm tra bằng lời, Claude tự viết và chạy SQL

**Quy trình:**
1. Đọc yêu cầu của user (VD: "kiểm tra đơn hàng của user X có đúng trạng thái đã thanh toán không")
2. Nếu thiếu thông tin để viết query chính xác — tên bảng, tên field, tiêu chí cụ thể là gì — hỏi lại ngắn gọn. Ví dụ hỏi: "Bạn biết tên bảng lưu đơn hàng không, hay để tôi tự tìm trong schema?"
3. Nếu có thể, tự khám phá schema DB trước (liệt kê bảng, cột liên quan) thay vì đoán tên bảng
4. Viết câu SQL, CHỈ dùng SELECT (không bao giờ chạy INSERT/UPDATE/DELETE/DROP trừ khi user xác nhận rõ ràng và đây là môi trường test, không phải production)
5. Chạy query, lấy kết quả
6. Giải thích kết quả bằng ngôn ngữ thường, không dùng thuật ngữ SQL — trả lời thẳng câu hỏi ban đầu của user (đúng/sai, có/không, số lượng bao nhiêu)
7. Đính kèm câu SQL đã chạy để user có thể lưu lại tham khảo sau

### Chế độ 2 — Dev đưa sẵn một câu SQL, user muốn hiểu nó làm gì

**Quy trình:**
1. Đọc câu SQL được đưa
2. Giải thích từng phần bằng ngôn ngữ thường: câu này lấy dữ liệu gì, từ bảng nào, điều kiện lọc là gì, join với bảng nào để làm gì
3. Nếu user muốn, chạy thử câu SQL đó (qua MCP) và diễn giải kết quả
4. Nếu câu SQL có vẻ phức tạp (nhiều join, subquery), chia nhỏ giải thích theo từng bước thay vì giải thích một lần toàn bộ

## Nguyên tắc an toàn
- KHÔNG BAO GIỜ chạy lệnh ghi/xóa dữ liệu (INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER) trừ khi user xác nhận rõ ràng bằng lời và ngữ cảnh chắc chắn là môi trường test/staging.
- Nếu không chắc đang ở môi trường nào (production hay test), hỏi lại trước khi chạy bất kỳ câu lệnh nào không phải SELECT.
- Nếu kết quả trả về nhạy cảm (thông tin cá nhân khách hàng), chỉ hiển thị phần cần thiết để trả lời câu hỏi, không liệt kê thừa các field nhạy cảm không liên quan.

## Format kết quả
Trả lời trực tiếp câu hỏi trước, sau đó mới đến chi tiết:

```
Kết luận: [Đúng/Sai/Có/Không + số liệu cụ thể]

Câu SQL đã chạy:
[query]

Giải thích: [diễn giải ngắn gọn ý nghĩa kết quả]
```
