---
name: daily-report-writer
description: Tổng hợp công việc đã làm trong ngày/tuần thành report gửi lead, dựa trên mô tả rời rạc của user (task đã làm, bug đã tìm, test case đã viết...). Dùng khi user cần gửi báo cáo tiến độ hàng ngày hoặc cuối tuần nhưng chỉ nhớ được lộn xộn những gì đã làm.
---

# Daily Report Writer

## Mục tiêu
Nhận danh sách công việc user kể lại (có thể rời rạc, không theo thứ tự, thiếu ngữ cảnh) và tổng hợp thành report rõ ràng, có cấu trúc, dễ đọc cho lead.

## Quy trình

### Bước 1 — Thu thập nội dung
Hỏi user (nếu chưa cung cấp đủ): hôm nay/tuần này làm những task/feature nào, có phát hiện bug gì không, có gì đang bị block/cần hỗ trợ không.

Nếu user chỉ liệt kê ngắn gọn, không cần hỏi dồn dập — có thể tổng hợp trước với thông tin hiện có rồi hỏi bổ sung 1 lần nếu thấy thiếu mục quan trọng (VD: user không nhắc gì tới việc có bị block hay không).

### Bước 2 — Phân loại nội dung theo nhóm

- **Đã hoàn thành**: task/feature đã test xong, bug đã report
- **Đang thực hiện**: task đang làm dở, tiến độ bao nhiêu %
- **Phát hiện vấn đề**: bug/blocker tìm được, mức độ ảnh hưởng
- **Cần hỗ trợ/đang chờ**: đang chờ dev fix, chờ thông tin từ ai, hoặc bị block bởi gì

### Bước 3 — Xuất report theo format ngắn gọn, dễ đọc (không dài dòng)

```
## Báo cáo [ngày/tuần]

**Đã hoàn thành:**
- [task/feature] — [kết quả ngắn gọn]

**Đang thực hiện:**
- [task] — [tiến độ]

**Vấn đề phát hiện:**
- [bug/issue] — [mức độ, đã report chưa]

**Cần hỗ trợ:**
- [nội dung cần hỗ trợ/đang chờ]
```

## Nguyên tắc viết
- Ngắn gọn, mỗi dòng 1 ý, không viết văn dài dòng — lead cần đọc nhanh, không cần kể chuyện
- Không tự thêm task mà user không nhắc tới
- Nếu một mục không có gì (VD: không có gì cần hỗ trợ), bỏ qua mục đó thay vì viết "Không có" cho tất cả các mục rỗng
