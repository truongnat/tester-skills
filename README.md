# Bo Skill Cho Tester Manual

Bo repository nay tap hop cac skill thuc dung danh cho tester manual, tap trung vao 4 nhom cong viec chinh:

- phan tich yeu cau va tim lo hong truoc khi test
- thiet ke test case va ra soat do bao phu
- dieu tra van de trong luc thuc thi test
- viet bug report, xac minh buoc tai hien va tong hop bao cao

Muc tieu cua bo skill nay la giup tester lam viec nhanh hon, dat cau hoi dung hon, va tao ra output de ban giao cho dev, BA, PM hoac lead ma khong can viet prompt lai tu dau moi lan.

## Danh sach skill

| # | Skill | Muc dich chinh | Nhom | Can MCP? |
|---|---|---|---|---|
| 1 | `testcase-generator` | Sinh test case tu requirement, flow, rule, va edge case | Thiet ke test | Khong |
| 2 | `requirement-gap-checker` | Tim diem mo ho, thieu, mau thuan trong requirement | Truoc khi test | Khong |
| 3 | `testcase-coverage-reviewer` | Rasoat bo test case de tim lo hong coverage | Thiet ke test | Khong |
| 4 | `sql-analyzer` | Ho tro doc va phan tich du lieu truy van khi dieu tra bug | Thuc thi va dieu tra | Co - MCP Database read-only |
| 5 | `browser-investigator` | Dieu tra hanh vi tren trinh duyet, DOM, network, console | Thuc thi va dieu tra | Co - MCP Browser |
| 6 | `automation-script-builder` | Ho tro tao script phu tro cho test va dieu tra | Thuc thi va dieu tra | Khong |
| 7 | `bug-report-writer` | Chuyen ghi chu tho thanh bug report ro rang, de giao dev | Ghi nhan va bao cao | Khong |
| 8 | `repro-steps-verifier` | Kiem tra bo buoc tai hien co du ro, dung thu tu, va tai hien duoc khong | Ghi nhan va bao cao | Khong |
| 9 | `daily-report-writer` | Tong hop cap nhat ngay, blockers, risk, next steps | Tong hop va giao tiep | Khong |

## Skill nay giai quyet van de gi

Trong thuc te, tester manual thuong gap 4 van de lap lai:

- requirement chua du ro nhung van bat dau test
- test case liet ke duoc happy path nhung bo sot negative path va business rule
- khi gap loi thi mat nhieu thoi gian tong hop thong tin cho de hieu
- bao cao hang ngay hoac report cho lead khong dong deu ve chat luong

Bo skill nay duoc viet de giam cac van de do bang cach bien nhung workflow lap lai thanh quy trinh co cau truc. Moi skill deu huong den output cu the, co the dung ngay trong cong viec hang ngay.

## Khi nao nen dung tung skill

`requirement-gap-checker`
- Dung ngay khi moi nhan feature, user story, mockup, hoac rule tu BA/PM.
- Phu hop de tim cho mo ta thieu, acceptance criteria yeu, dependency chua noi ro, va edge case chua duoc nghi toi.

`testcase-generator`
- Dung sau khi da co input tuong doi ro.
- Hop khi can sinh nhanh danh sach test case co cau truc de review hoac import ve template noi bo.

`testcase-coverage-reviewer`
- Dung khi da co mot bo test case nhung nghi rang coverage chua tot.
- Hop truoc release, regression, hoac truoc khi giao test set cho nguoi khac.

`sql-analyzer`
- Dung khi can xac minh data state, record mapping, status, timestamp, rule xu ly trong DB.
- Nen chi cap quyen read-only va co quy dinh ro ve bang/schema duoc phep doc.

`browser-investigator`
- Dung khi can dieu tra UI bug, request/response, log console, cookie, local storage, va luong thao tac tren browser.
- Huu ich cho bug kho tai hien bang mo ta thong thuong.

`automation-script-builder`
- Dung khi can tao script nho de seed data, convert file, sinh input hang loat, parse log, hoac mo phong buoc lap lai.
- Phu hop nhat khi chay trong moi truong co the tao va thu script ngay.

`bug-report-writer`
- Dung khi da co raw notes, screenshot, video, log, hoac mo ta loi roi rac.
- Skill nay giup chuan hoa thanh bug report de dev co the doc va vao viec nhanh.

`repro-steps-verifier`
- Dung truoc khi gui bug sang dev hoac truoc khi escalate.
- Muc tieu la loai bo nhung buoc mo ho, thieu dieu kien, hoac khong tai hien on dinh.

`daily-report-writer`
- Dung cuoi ngay, cuoi sprint, hoac khi can cap nhat nhanh cho lead/PM.
- Phu hop de tong hop da test gi, phat hien gi, blocker nao dang ton, va ke hoach tiep theo.

## Thu tu de bat dau dung thu

Neu muon thay hieu qua som, nen thu theo thu tu nay:

1. `bug-report-writer`
2. `requirement-gap-checker`
3. `testcase-generator`
4. `repro-steps-verifier`
5. `daily-report-writer`
6. `testcase-coverage-reviewer`
7. `browser-investigator`
8. `sql-analyzer`
9. `automation-script-builder`

## Cach cai dat

### Tren Claude.ai

1. Vao `Customize > Skills`
2. Bat `Code execution and file creation` neu he thong yeu cau
3. Upload tung skill thanh tung goi rieng
4. Moi skill can co file `SKILL.md` o dung cau truc thu muc cua no

### Tren Claude Code

Copy tung thu muc skill vao:

```bash
.claude/skills/<ten-skill>/
```

Vi du:

```bash
.claude/skills/bug-report-writer/SKILL.md
```

## Yeu cau moi truong

Khong can MCP cho phan lon skill. Tuy nhien:

- `sql-analyzer` can MCP Database, uu tien ket noi read-only
- `browser-investigator` can MCP Browser hoac moi truong browser automation tuong duong
- `automation-script-builder` se huu ich hon neu duoc chay trong moi truong co the tao file va thu script

## Nguyen tac thiet ke chung

Tat ca skill trong bo nay deu theo mot so nguyen tac:

- uu tien hoi thieu thong tin truoc khi tra loi
- khi bat dau chay skill, luon ghi `Session timestamp`
- neu co tao file output, luu theo cau truc artifact theo ngay va skill
- output phai huong den tai lieu co the dung ngay
- tranh prompt chung chung, thay bang checklist va buoc xu ly ro rang
- tap trung vao cong viec thuc te cua tester manual, khong viet theo kieu ly thuyet

Phan y tuong "context-completeness-checker" khong phai la mot skill rieng. No da duoc nhung san vao checklist hoac buoc dau cua tung skill, de skill tu phat hien du lieu con thieu va hoi lai cu the khi can.

## Tuỳ bien theo quy trinh team

Neu team cua ban da co:

- template test case rieng
- format bug report rieng
- mau daily report rieng
- quy tac severity/priority rieng

thi chi can sua phan `Format output`, `Checklist`, hoac `Template` trong tung file `SKILL.md` cho khop quy trinh noi bo. Khong can viet lai toan bo skill.

## Artifact va timestamp

Moi lan chay skill nen co timestamp rieng:

```text
Session timestamp: YYYY-MM-DD HH:mm:ss Z
```

Neu skill tao file output, luu theo cau truc:

```text
artifacts/YYYY-MM-DD/<skill-name>/HHmmss-short-topic/
```

Vi du:

```text
artifacts/2026-07-07/bug-report-writer/143005-login-error/bug-report.md
artifacts/2026-07-07/testcase-generator/150210-checkout-flow/testcases.csv
artifacts/2026-07-07/browser-investigator/160455-payment-500/browser-investigation.md
```

Chi commit file huong dan trong `artifacts/README.md`. Output sinh ra trong qua trinh dung hang ngay nen duoc git ignore mac dinh, vi co the chua du thong tin, chua redact, hoac chi phuc vu mot lan test.

Rieng `daily-report-writer` chi lay activity trong dung ngay report, bang cach doc `artifacts/YYYY-MM-DD/` cua ngay do. Khong tron activity ngay khac vao daily report tru khi user yeu cau report tuan hoac report nhieu ngay.

## Cau truc repository

```text
artifacts/
automation-script-builder/
browser-investigator/
bug-report-writer/
daily-report-writer/
repro-steps-verifier/
requirement-gap-checker/
sql-analyzer/
testcase-coverage-reviewer/
testcase-generator/
skills-README.md
README.md
```

## Huong phat trien tiep

Repository nay phu hop de mo rong them:

- skill viet test summary theo release
- skill phan tich log backend cho tester
- skill review traceability giua requirement va test case
- skill ho tro test data design

Neu bo skill nay duoc dung trong team, nen version hoa tung skill va ghi ro nhung thay doi ve template hoac workflow de tranh mat dong bo.
