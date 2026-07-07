# Bộ kỹ năng hỗ trợ Tester Manual

Repository này tập hợp các Claude Skill dành cho tester manual, tập trung vào những công việc lặp lại trong quá trình kiểm thử phần mềm: phân tích yêu cầu, thiết kế test case, kiểm thử API, lập kế hoạch test, exploratory testing, điều tra lỗi, viết bug report và tổng hợp báo cáo.

Mục tiêu của bộ kỹ năng là giúp tester làm việc có cấu trúc hơn, đặt câu hỏi đúng hơn, giảm thời gian viết lại prompt, và tạo ra output có thể dùng ngay để trao đổi với dev, BA, PM hoặc QA lead.

## Danh sách kỹ năng

| # | Skill | Mục đích chính | Nhóm công việc | Cần MCP? |
|---|---|---|---|---|
| 1 | `testcase-generator` | Sinh test case từ requirement, flow, rule và edge case | Thiết kế test | Không |
| 2 | `requirement-gap-checker` | Tìm điểm thiếu, mơ hồ hoặc mâu thuẫn trong requirement | Trước khi test | Không |
| 3 | `testcase-coverage-reviewer` | Rà soát độ phủ của bộ test case đã có | Thiết kế test | Không |
| 4 | `api-testcase-generator` | Sinh test case API từ Swagger/OpenAPI, Postman hoặc mô tả endpoint | API testing | Không |
| 5 | `api-response-validator` | So sánh response API thật với expected response hoặc schema | API testing | Không |
| 6 | `test-plan-writer` | Viết test plan cho sprint, release hoặc nhóm feature | Test strategy | Không |
| 7 | `risk-based-prioritizer` | Xếp hạng module/test case theo rủi ro khi thiếu thời gian test | Test strategy | Không |
| 8 | `exploratory-charter-builder` | Tạo charter cho một phiên exploratory testing có định hướng | Exploratory testing | Không |
| 9 | `edge-case-brainstormer` | Brainstorm edge case và câu hỏi "điều gì xảy ra nếu..." | Exploratory testing | Không |
| 10 | `accessibility-checklist-runner` | Chạy checklist accessibility cơ bản cho UI | Chất lượng chuyên biệt | Không |
| 11 | `i18n-checklist-runner` | Chạy checklist i18n/l10n cho sản phẩm đa ngôn ngữ | Chất lượng chuyên biệt | Không |
| 12 | `sql-analyzer` | Hỗ trợ đọc, viết và giải thích truy vấn dữ liệu dạng read-only | Thực thi và điều tra | Có, MCP Database read-only |
| 13 | `browser-investigator` | Điều tra lỗi trên trình duyệt qua console, network và DOM | Thực thi và điều tra | Có, MCP Browser |
| 14 | `root-cause-hypothesis` | Tạo giả thuyết nguyên nhân cho bug thỉnh thoảng xảy ra hoặc khó tái hiện | Điều tra nguyên nhân | Không |
| 15 | `automation-script-builder` | Chuyển test case thủ công thành script automation dễ hiểu | Automation cơ bản | Không |
| 16 | `test-data-generator` | Sinh dữ liệu test giả, valid/invalid/boundary theo locale | Test data | Không |
| 17 | `bug-report-writer` | Chuyển ghi chú lỗi rời rạc thành bug report rõ ràng | Ghi nhận và báo cáo | Không |
| 18 | `repro-steps-verifier` | Kiểm tra độ rõ ràng của các bước tái hiện lỗi | Ghi nhận và báo cáo | Không |
| 19 | `daily-report-writer` | Tổng hợp công việc trong ngày, blocker, rủi ro và kế hoạch tiếp theo | Tổng hợp và giao tiếp | Không |
| 20 | `standup-notes-summarizer` | Tạo bản cập nhật standup cực ngắn để nói hoặc gửi chat | Tổng hợp và giao tiếp | Không |

## Bộ kỹ năng này giải quyết vấn đề gì?

Trong thực tế, tester manual thường gặp các vấn đề lặp lại:

- Requirement chưa rõ nhưng vẫn phải bắt đầu phân tích test.
- Test case có happy path nhưng thiếu negative path, boundary, permission, API contract hoặc business rule.
- Khi gặp lỗi, thông tin gửi cho dev thiếu môi trường, dữ liệu test, evidence hoặc bước tái hiện.
- Báo cáo hằng ngày không đồng đều về cấu trúc, thiếu blocker, rủi ro hoặc next action.
- Tester muốn mở rộng sang API testing, test strategy, exploratory testing hoặc quality checklist nhưng chưa có quy trình bắt đầu.

Các skill trong repository này biến những việc trên thành checklist và quy trình rõ ràng. Mỗi skill hướng tới một output cụ thể, đủ gọn để dùng trong công việc hằng ngày nhưng vẫn có cấu trúc để giảm sai sót.

## Khi nào dùng từng skill?

`requirement-gap-checker`
- Dùng ngay khi nhận feature, user story, mockup, API spec hoặc business rule từ BA/PM.
- Phù hợp để tìm acceptance criteria yếu, dependency chưa rõ, role chưa đủ, luồng lỗi bị thiếu hoặc edge case chưa được nêu.

`testcase-generator`
- Dùng sau khi requirement đã đủ rõ để tạo test case có ý nghĩa.
- Phù hợp khi cần sinh nhanh test case dạng bảng để review, chỉnh sửa hoặc import vào template nội bộ.

`testcase-coverage-reviewer`
- Dùng khi đã có bộ test case và muốn kiểm tra còn thiếu nhóm case nào.
- Phù hợp trước regression, trước release hoặc trước khi bàn giao test set cho người khác.

`api-testcase-generator`
- Dùng khi có Swagger/OpenAPI spec, Postman collection, curl hoặc mô tả endpoint.
- Phù hợp để sinh case cho status code, required param, sai kiểu dữ liệu, auth, permission, schema và error handling.

`api-response-validator`
- Dùng khi có actual response JSON và expected response/schema.
- Phù hợp để tìm field thiếu, field thừa, sai type, sai format, sai enum hoặc sai business rule trong response.

`test-plan-writer`
- Dùng ở tầm sprint, release hoặc nhóm feature, trước khi đi vào từng test case.
- Phù hợp để xác định scope, out of scope, test approach, môi trường, dữ liệu, risk, entry criteria và exit criteria.

`risk-based-prioritizer`
- Dùng khi thời gian test không đủ và cần chọn phần nào phải test trước.
- Phù hợp để xếp hạng module hoặc test case theo impact, tần suất dùng, độ phức tạp, lịch sử bug và dependency.

`exploratory-charter-builder`
- Dùng khi cần khám phá feature mới hoặc nghiệp vụ chưa rõ bằng session-based testing.
- Phù hợp để tạo mục tiêu, phạm vi, timebox, test ideas và evidence cần thu thập.

`edge-case-brainstormer`
- Dùng khi cần nghĩ thêm case ngoài spec.
- Phù hợp để brainstorm câu hỏi kiểu "điều gì xảy ra nếu..." cho workflow, form, API hoặc business rule.

`accessibility-checklist-runner`
- Dùng khi cần kiểm tra accessibility cơ bản.
- Phù hợp cho keyboard navigation, focus state, contrast, label, alt text, screen reader text và error message.

`i18n-checklist-runner`
- Dùng khi sản phẩm có nhiều ngôn ngữ hoặc nhiều locale.
- Phù hợp để kiểm tra bản dịch, độ dài chuỗi, format ngày giờ, tiền tệ, số, Unicode và layout khi đổi ngôn ngữ.

`sql-analyzer`
- Dùng khi cần xác minh trạng thái dữ liệu, mapping record, trạng thái đơn hàng, timestamp hoặc rule xử lý trong database.
- Chỉ nên dùng với kết nối database read-only. Skill này không được chạy câu lệnh ghi, sửa hoặc xóa dữ liệu.

`browser-investigator`
- Dùng khi cần điều tra lỗi UI, request/response, console log, cookie, local storage hoặc trạng thái DOM.
- Hữu ích với các lỗi khó mô tả bằng mắt thường hoặc khó tái hiện nếu thiếu evidence kỹ thuật.

`root-cause-hypothesis`
- Dùng khi bug xảy ra thỉnh thoảng, khó tái hiện hoặc có nhiều nguyên nhân có thể xảy ra.
- Phù hợp để đặt giả thuyết theo dữ liệu, môi trường, timing, permission, API, integration hoặc UI state trước khi báo dev.

`automation-script-builder`
- Dùng khi muốn chuyển một flow kiểm thử thủ công thành script Playwright hoặc Selenium.
- Phù hợp cho tester mới học automation vì skill ưu tiên code dễ hiểu, selector ổn định, assertion rõ ràng và giải thích từng phần.

`test-data-generator`
- Dùng khi cần dữ liệu test giả cho form, API hoặc import file.
- Phù hợp để sinh dữ liệu valid, invalid, boundary, tiếng Việt có dấu, email giả, số điện thoại VN giả và dữ liệu Unicode.

`bug-report-writer`
- Dùng khi đã có ghi chú lỗi, screenshot, video, log hoặc mô tả ban đầu nhưng chưa thành bug report hoàn chỉnh.
- Skill giúp chuẩn hóa title, environment, steps, expected result, actual result, frequency, severity và attachment.

`repro-steps-verifier`
- Dùng trước khi gửi bug sang dev hoặc trước khi escalate.
- Mục tiêu là phát hiện bước mơ hồ, thiếu dữ liệu test, thiếu role/account, thiếu build version hoặc thiếu evidence.

`daily-report-writer`
- Dùng cuối ngày để tổng hợp đúng activity của ngày đó.
- Skill chỉ lấy activity trong đúng `Report date`, không trộn dữ liệu của ngày khác trừ khi user yêu cầu report tuần hoặc nhiều ngày.

`standup-notes-summarizer`
- Dùng trước daily standup để tạo bản nói ngắn: hôm qua, hôm nay, blocker.
- Khác `daily-report-writer` vì output ngắn hơn, dùng để nói hoặc gửi chat nhanh.

## Thứ tự nên dùng thử

Nếu muốn áp dụng dần, nên bắt đầu theo thứ tự sau:

1. `bug-report-writer`
2. `requirement-gap-checker`
3. `testcase-generator`
4. `repro-steps-verifier`
5. `daily-report-writer`
6. `api-testcase-generator`
7. `api-response-validator`
8. `testcase-coverage-reviewer`
9. `test-plan-writer`
10. `risk-based-prioritizer`
11. `exploratory-charter-builder`
12. `edge-case-brainstormer`
13. `browser-investigator`
14. `root-cause-hypothesis`
15. `test-data-generator`
16. `sql-analyzer`
17. `accessibility-checklist-runner`
18. `i18n-checklist-runner`
19. `standup-notes-summarizer`
20. `automation-script-builder`

## Cách cài đặt

Xem hướng dẫn đầy đủ tại [docs/INSTALL_CLAUDE.md](docs/INSTALL_CLAUDE.md).

### Cài từ remote, không cần clone repo

Claude Code chạy plugin trực tiếp từ GitHub Release:

```bash
claude --plugin-url https://github.com/truongnat/tester-skills/releases/latest/download/tester-skills-plugin.zip
```

Claude Code cài skill trực tiếp vào `~/.claude/skills`:

```bash
curl -fsSL https://raw.githubusercontent.com/truongnat/tester-skills/main/scripts/install_remote.py | python3 - --force
```

Claude Code cài qua marketplace remote:

```bash
claude plugin marketplace add https://github.com/truongnat/tester-skills
claude plugin install tester-skills@tester-skills
```

Claude Desktop/Web tải zip từ:

```text
https://github.com/truongnat/tester-skills/releases/latest
```

### Claude.ai / Claude Desktop

1. Vào `Customize > Skills`.
2. Bật `Code execution and file creation` nếu hệ thống yêu cầu.
3. Upload từng file `<skill-name>.zip` tải từ GitHub Release.
4. Mỗi gói skill cần có file `SKILL.md` đúng trong thư mục của skill đó.

Có thể tạo sẵn file zip để upload:

```bash
make package-desktop
```

### Claude Code

Copy từng thư mục skill vào:

```bash
.claude/skills/<ten-skill>/
```

Ví dụ:

```bash
.claude/skills/bug-report-writer/SKILL.md
```

Hoặc cài toàn bộ vào user-level `~/.claude/skills`:

```bash
make install-claude
```

Repository này cũng có thể load như Claude Code plugin:

```bash
claude --plugin-dir .
```

Khi load bằng plugin, skill được gọi theo namespace:

```text
/tester-skills:bug-report-writer
/tester-skills:api-testcase-generator
```

## Yêu cầu môi trường

Phần lớn skill không cần MCP. Một số skill cần môi trường bổ sung để phát huy đầy đủ:

- `sql-analyzer` cần MCP Database với quyền read-only.
- `browser-investigator` cần MCP Browser hoặc môi trường browser automation tương đương.
- `automation-script-builder` hữu ích hơn khi chạy trong môi trường có thể tạo file và thử script.
- Các skill API có thể dùng Swagger/OpenAPI, Postman collection, curl hoặc JSON paste trực tiếp trong chat.

## Nguyên tắc thiết kế chung

Tất cả skill trong bộ này tuân theo các nguyên tắc sau:

- Luôn kiểm tra thiếu thông tin trước khi tạo output.
- Khi cần hỏi thêm, ưu tiên tối đa 3 câu hỏi quan trọng nhất trước.
- Khi bắt đầu chạy skill, luôn ghi `Session timestamp`.
- Nếu tạo file output, lưu theo cấu trúc artifact theo ngày và skill.
- Output phải là tài liệu có thể dùng ngay, không chỉ là gợi ý chung chung.
- Không tự bịa dữ liệu, không tự lấp khoảng trống requirement bằng giả định.
- Tập trung vào công việc thực tế của tester manual, tránh viết theo hướng lý thuyết.

Ý tưởng `context-completeness-checker` không phải là một skill riêng. Nguyên tắc này đã được nhúng vào checklist hoặc bước đầu của từng skill để phát hiện dữ liệu còn thiếu và hỏi lại đúng chỗ.

## Tùy biến theo quy trình của team

Nếu team đã có quy chuẩn riêng, có thể chỉnh trực tiếp trong từng file `SKILL.md`:

- Template test case.
- Template bug report.
- Mẫu daily report.
- Quy tắc severity và priority.
- Cách đặt tên test case ID.
- Checklist release hoặc regression.

Không cần viết lại toàn bộ skill. Thường chỉ cần sửa phần `Format output`, `Checklist`, `Template` hoặc quy tắc ưu tiên.

## Timestamp và artifact

Mỗi lần chạy skill nên ghi lại timestamp riêng:

```text
Session timestamp: YYYY-MM-DD HH:mm:ss Z
```

Nếu skill tạo file output, lưu theo cấu trúc:

```text
artifacts/YYYY-MM-DD/<skill-name>/HHmmss-short-topic/
```

Ví dụ:

```text
artifacts/2026-07-07/bug-report-writer/143005-login-error/bug-report.md
artifacts/2026-07-07/testcase-generator/150210-checkout-flow/testcases.csv
artifacts/2026-07-07/browser-investigator/160455-payment-500/browser-investigation.md
```

Chỉ commit file hướng dẫn trong `artifacts/README.md`. Các output sinh ra khi dùng skill hằng ngày được git ignore mặc định vì có thể chứa dữ liệu nhạy cảm, dữ liệu tạm thời hoặc evidence chưa được redact.

Riêng `daily-report-writer`, khi tạo daily report chỉ đọc activity trong đúng thư mục ngày cần báo cáo:

```text
artifacts/YYYY-MM-DD/
```

Không đưa activity của ngày khác vào daily report, trừ khi user yêu cầu report tuần hoặc report nhiều ngày.

## Tổ chức artifact

Repository dùng cấu trúc artifact theo ngày để dễ truy vết activity:

```text
artifacts/
  YYYY-MM-DD/
    skill-name/
      HHmmss-short-topic/
        output.md
        output.csv
        evidence.json
        screenshots/
        logs/
```

Quy tắc đặt thư mục:

- `YYYY-MM-DD` là ngày theo timezone của user hoặc project.
- `HHmmss` là thời điểm bắt đầu chạy skill.
- `short-topic` là mô tả ngắn bằng chữ thường, ví dụ `login-error`, `checkout-flow`, `payment-500`.
- Một lần chạy skill tương ứng với một thư mục riêng.
- Không trộn nhiều feature, bug hoặc investigation khác nhau vào cùng một thư mục.
- Evidence nhạy cảm phải được che trước khi lưu hoặc chia sẻ.

## Cấu trúc repository

```text
artifacts/
automation-script-builder/
accessibility-checklist-runner/
api-response-validator/
api-testcase-generator/
browser-investigator/
bug-report-writer/
daily-report-writer/
edge-case-brainstormer/
exploratory-charter-builder/
i18n-checklist-runner/
repro-steps-verifier/
requirement-gap-checker/
risk-based-prioritizer/
root-cause-hypothesis/
sql-analyzer/
standup-notes-summarizer/
test-data-generator/
test-plan-writer/
testcase-coverage-reviewer/
testcase-generator/
README.md
skills-README.md
```

## Hướng phát triển tiếp theo

Repository này có thể mở rộng thêm các skill khác cho QA workflow:

- Skill viết test summary theo release.
- Skill phân tích log backend cho tester.
- Skill rà soát traceability giữa requirement và test case.
- Skill hỗ trợ thiết kế test data.
- Skill tổng hợp release risk trước khi go-live.

Nếu bộ skill này được dùng trong team, nên version hóa từng skill và ghi rõ thay đổi về template, checklist hoặc workflow để tránh mất đồng bộ giữa các tester.
