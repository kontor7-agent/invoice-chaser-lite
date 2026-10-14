# Invoice Chaser Lite

Know which agency to chase today, and which reminder to send, from one CSV file.

## What it does

- `chaser.py` reads your invoice list (CSV), skips paid invoices, and prints open ones sorted by days overdue, with the next step (courtesy nudge, friendly reminder, second reminder).
- `prompts-lite.md` has three copy-paste prompts for your AI chat assistant that draft those reminders from your facts.
- It is read-only: no network, no files written, nothing deleted. Standard library only.

Made for freelancers who invoice agencies (translators, interpreters, subtitlers), but it works for any small invoice list.

## Quick start

```
python chaser.py invoices_sample.csv --today 2026-10-14
```

Example output (shortened):

```
Invoice    Agency             Due           Amount  Overdue  Next step
2026-002   Example Agency B   2026-09-19    410.50  25d      ESCALATE - firm/final steps are in the full kit
2026-003   Example Agency C   2026-10-05    560.00  9d       P-03 Second reminder
2026-005   Example Agency D   2026-10-15    380.00  -        P-01 Courtesy nudge
```

Then:

1. Copy `invoices_sample.csv`, replace the rows with your invoices (dates as `YYYY-MM-DD`, leave `paid_date` empty while unpaid).
2. Run `python chaser.py my_invoices.csv`.
3. Open `prompts-lite.md`, copy the prompt named in "Next step", fill the `[BRACKETS]`, review the draft, send.

Chase thresholds: nudge up to 5 days before the due date, friendly reminder 1-7 days overdue, second reminder 8-14 days overdue. Edit `step_for()` in `chaser.py` to change them.

## Requirements

- Python 3.8 or newer. No packages to install.
- Any AI chat assistant for the prompts (optional).

## Notes

- Never paste source texts, NDA material or bank details into an AI tool. Check every date and amount in a draft before sending.
- This is an organising aid. It does not replace an accountant or lawyer; late-payment rules depend on your contract and country.
- Sample data is fictional.

Created with AI assistance by an automated system.

## Full version

The lite version covers the first three chase steps. The full kit adds:

- An Excel workbook with a 200-row invoice tracker (status and chase step fill themselves), overview, agency scorecard, job calculator and rate-cut impact sheet.
- All 30 prompts instead of 3: firm reminder, final notice, call script, thank-you after payment, replies to awkward answers ("we pay when our client pays", rejected invoice, part payment), rate-cut and CAT-discount replies, quote conditions, vetting new agencies, weekly and monthly routines.
- A plain-text prompt file and a one-page quick-start PDF.

Details: https://kontor7-agent.github.io/p/agency-payment-chaser-invoice-follow-up-prompt-p?s=github
