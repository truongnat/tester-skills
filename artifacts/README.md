# Artifact Organization

Generated outputs should be stored by report date, skill, and run timestamp:

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

Rules:

- Use the user's/project's timezone for `YYYY-MM-DD` and `HHmmss`.
- Every artifact must include `Session timestamp: YYYY-MM-DD HH:mm:ss Z`.
- Keep one skill run in one folder; do not mix multiple features or bug investigations in the same run folder.
- Use short lowercase slugs for topic names, for example `143005-login-error`.
- Store sensitive evidence redacted by default. Do not write raw tokens, passwords, or unnecessary personal data.
- Daily reports must read only `artifacts/YYYY-MM-DD/` for the target report date unless the user explicitly asks for a weekly or multi-day report.

Suggested files:

- `bug-report.md`
- `requirement-gaps.md`
- `testcases.md`
- `testcases.csv`
- `coverage-review.md`
- `browser-investigation.md`
- `sql-analysis.md`
- `automation.spec.ts` or `automation.py`
- `daily-report.md`
