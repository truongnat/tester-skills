---
name: bug-report-writer
description: Cấu trúc hóa mô tả bug lộn xộn/thiếu thông tin của user thành bug report chuẩn, đầy đủ, sẵn sàng gửi cho dev. Dùng khi user vừa phát hiện bug và cần viết report, dù mô tả ban đầu có ngắn gọn hay thiếu chi tiết đến đâu.
---

# Bug Report Writer

## Nguyên tắc cốt lõi
User có thể mô tả bug rất lộn xộn hoặc thiếu — nhiệm vụ của Skill này là CHỦ ĐỘNG hỏi lại đúng chỗ thiếu theo checklist cố định, không phải viết report thiếu dựa trên những gì user vô tình cung cấp.

## Checklist bắt buộc (phải đủ trước khi xuất report)

1. **Môi trường**: web hay app, version/build nào, browser/device nào, OS nào (nếu liên quan)
2. **Steps to reproduce**: các bước cụ thể, đánh số rõ ràng, không gộp nhiều hành động vào 1 bước
3. **Expected result**: kết quả đúng ra phải như thế nào
4. **Actual result**: kết quả thực tế xảy ra là gì
5. **Tần suất**: luôn xảy ra hay thỉnh thoảng (nếu thỉnh thoảng, có pattern gì không)
6. **Mức độ nghiêm trọng** (Severity): block luồng chính hay chỉ ảnh hưởng nhỏ, thẩm mỹ
7. **Ảnh/video/log đính kèm**: có không, nếu có nội dung liên quan gì cần nhắc tới trong report

## Quy trình

### Bước 1 — Đọc mô tả ban đầu của user
Dù dài hay ngắn, lộn xộn hay rõ ràng, đối chiếu ngay với 7 mục checklist ở trên.

### Bước 2 — Hỏi lại CHỈ những mục còn thiếu, theo từng câu cụ thể
Không hỏi gộp "bạn cho tôi thêm thông tin nhé". Hỏi thẳng, ví dụ:
- "Bug này xảy ra trên web hay app? Version bao nhiêu?"
- "Bạn có làm lại được ngay bây giờ không, hay chỉ gặp 1 lần?"
- "Trước khi bấm nút Save, bạn đã làm những bước gì? Kể theo thứ tự nhé."

Nếu user trả lời tiếp vẫn còn thiếu, tiếp tục hỏi cho tới khi đủ 7 mục — không xuất report thiếu.

Ngoại lệ: nếu user nói rõ "cứ viết report với thông tin hiện có, tôi sẽ bổ sung sau", được phép xuất report với các mục còn thiếu ghi rõ "[Cần bổ sung: ...]" thay vì bịa hoặc bỏ trống.

### Bước 3 — Xuất report theo template chuẩn

```
## [Tiêu đề bug — mô tả ngắn gọn 1 dòng, nêu rõ hiện tượng]

**Môi trường:** [web/app, version, browser/device, OS]
**Mức độ nghiêm trọng:** [Critical/High/Medium/Low]
**Tần suất:** [Luôn xảy ra / Thỉnh thoảng — pattern nếu có]

**Các bước tái hiện:**
1. ...
2. ...
3. ...

**Kết quả mong đợi:**
[mô tả]

**Kết quả thực tế:**
[mô tả]

**Đính kèm:** [ảnh/video/log nếu có]

**Ghi chú thêm:** [nếu có thông tin liên quan khác, VD: chỉ xảy ra với tài khoản role admin]
```

## Xử lý khi có input từ browser-investigator
Nếu user đã chạy qua Skill `browser-investigator` trước đó và có sẵn thông tin console/network, tự động đưa phần đó vào mục "Ghi chú thêm" hoặc "Đính kèm" của report, không yêu cầu user gõ lại.
