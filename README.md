# 🧾 Messy order → Zoho Books draft Sales Order (Make.com template)

Your salespeople send orders like this:

```
Customer: Green Valley Mart
Nut & Berri-400gm-4pc
NAS-1kg-4pc
Charcol brush 12
```

This template reads them, finds the right **customer** and the right **Zoho Books items**, and creates a
**draft Sales Order**. Anything it isn't sure about is **not billed**. It goes to a review sheet with the
reason, so a human can decide.

> **Rule it follows: a wrong product or wrong customer is worse than an unresolved order.**

| You send | It does |
|---|---|
| `Nut & Berri-400gm-4pc` | ✅ **MATCHED** → line item *Acme Muesli – Nuts & Berries – 400 gm* × 4 |
| `Dark chocolate Granola-1kg-4pc` (catalog only has 900 gm) | ⛔ **NOT_FOUND** → review sheet, never swaps in a "close" size |
| `Mint 4` (soap? lip balm? oil?) | ❓ **AMBIGUOUS** → review sheet, lists the options |
| `Charcol brush 12` | ✅ fixes the typo → *Charcoal Toothbrush* × 12 |

No coding needed. You import two files into Make.com, click a few connections, and test safely first.

---

## What you need (about 30–45 minutes)

- [ ] A **Make.com** account (free works for testing, see [FAQ](docs/FAQ.md) for usage)
- [ ] A **Zoho Books** account with your customers and items already in it
- [ ] A **Google** account (Google Form + Google Sheet)
- [ ] Python 3 *(optional, only for the one-command ID helper)*

## Quick start

1. **Get the files** – click **Code → Download ZIP** on this page and unzip it.
2. **Make your Google Form + Sheet** – copy the column layout from [`templates/`](templates).
3. **Fill in your IDs** – one command, or edit by hand:
   ```bash
   python3 tools/fill_placeholders.py --zoho-org YOUR_ORG_ID --spreadsheet "YOUR_SHEET_URL"
   ```
4. **Import the files from `my-scenarios/` into Make** and pick your Zoho / Google / AI connections.
5. **Test with the dry-run first** (it never creates anything in Zoho), then with one real row.

👉 **Full click-by-click guide: [docs/SETUP.md](docs/SETUP.md)**

## The two scenarios

| File | What it does | Risk |
|---|---|---|
| `scenarios/dry-run-harness/…` | Runs sample orders through the whole "brain" and writes the results to a Make data store so you can *see* every decision. **Never creates a sales order.** | none |
| `scenarios/sales-order-intake/…` | The real thing: Google Sheet row → match → **draft** Sales Order in Zoho Books. | creates drafts |

Start with the dry-run. When you trust its answers on *your* products, switch on the real one.

## Docs

| | |
|---|---|
| 🚀 [SETUP.md](docs/SETUP.md) | Step-by-step install, with a checklist and a first test |
| 🧠 [HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md) | What happens to one order line, in plain words |
| 🛠 [CUSTOMIZE.md](docs/CUSTOMIZE.md) | Change the form columns, brand hint, wording, tax, stricter/looser matching |
| 🩺 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Every error we hit while building this, with the fix |
| ❓ [FAQ.md](docs/FAQ.md) | Cost, speed, safety, "can it also…?" |

## Good to know (honest limits)

- It uses an AI model, so it can occasionally misread a line. It is built to **say "not sure"** rather than
  guess, but keep a person reviewing the draft orders and the review sheet.
- It does **not create customers**; the customer must already exist in Zoho Books.
- A few late prompt fixes in the dry-run scenario have not been re-tested; see
  [Unverified changes](docs/TROUBLESHOOTING.md#unverified-changes-in-the-dry-run).
- The real intake scenario has the older prompts; copy improvements over only after the dry-run
  proves them on your data.

Built for an FMCG distributor (many similar products, typos, long orders), but it works for any catalog
where orders arrive as free text. Questions or fixes welcome via GitHub issues.
