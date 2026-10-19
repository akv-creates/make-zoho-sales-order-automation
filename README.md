# Make.com + Zoho Books: messy order → draft Sales Order

Template Make.com scenarios that turn messy, hurried sales-order text (Google Form rows, typed lists,
PDFs/photos) into **draft Sales Orders in Zoho Books**, and park anything uncertain in a review sheet instead.

Built for an FMCG distributor, where orders look like `Nut & Berri-400gm-4pc`, `NAS-1kg-4pc`,
`Charcol brush 12`, with typos, abbreviations, 10–30 lines per order and a catalog full of duplicate or
promotional listings. **Guiding rule: a wrong customer or wrong product is worse than an unresolved one.**

> Status: working template, not a drop-in product. Read [Known limitations](#known-limitations) first.

## What's inside

| File | Purpose |
|---|---|
| `scenarios/sales-order-intake/sales-order-intake.blueprint.json` | Full scenario: Google Sheets trigger → AI parser → Zoho customer + item lookup → AI comparators → `Create Sales Order`. Text route and file (PDF/image) route. |
| `scenarios/dry-run-harness/dry-run.blueprint.json` | On-demand copy of the same *intelligence layer* that **never creates a sales order**. It writes every step's result to a Make data store so you can inspect it. Contains the newer prompt/guard changes. |

The harness is the place to iterate on prompts. Port proven changes into the intake scenario afterwards.

## How matching works

```
order text ─▶ Parser (AI) ─▶ per-line retrieval (Zoho) ─▶ Comparator (AI) ─▶ MATCHED ─▶ Sales Order line
                │                                                │            AMBIGUOUS / NOT_FOUND
                └─▶ customer name/phone ─▶ customer search ─▶ Customer matcher (AI) + exact-name/phone guard
                                                                  └─▶ anything uncertain ─▶ "Errors" sheet
```

1. **Parser** – extracts customer name/phone/address, an optional brand line (`* Acme Foods`) and one entry
   per product: `term_a|term_b|term_c|product_text|package_size|normalized_size|quantity`.
   It prepares *retrieval* only and never picks products. Numbers inside a name (`28gm`) stay in the product
   text; the ordered size (`400gm`) and the quantity are separate fields; quantity is never part of the name.
2. **Retrieval** – substring search on Zoho item names for `term_a`, then `term_b`; `term_c` (obvious
   spelling fix, e.g. `charcol→charcoal`) is only used if nothing was found. Inactive items are dropped.
3. **Comparator** – chooses **only from the retrieved Zoho candidates**; item IDs always come from Zoho,
   never from the AI. A stated size is a hard constraint (900 gm is not 1 kg); no stated size is neutral.
   Clean listings beat promotional/legacy duplicates, identical `item_id`s count once, unrequested
   variants/ingredients or mixed product categories give `AMBIGUOUS`, a missing size gives `NOT_FOUND`.
4. **Customer match** – full name, relaxed name (`and`/`&`), two words, first word and phone searches;
   the AI chooses among candidates and, in the harness, a deterministic check requires an exact normalised
   name or phone match before `MATCHED` is accepted.
5. Only `MATCHED` lines are billed; the rest go to the `Errors` sheet for a human.

## Setup

1. In Make: *Create scenario → ⋯ → Import Blueprint* for each file.
2. Reconnect: **Zoho Books** (scopes: contacts READ, items READ, salesorders CREATE/READ), **Google Sheets**,
   **Google Drive** (file route only), and the **Make AI** connection used by the *AI Tools → Extract* modules.
3. Replace the placeholders:

| Placeholder | Meaning |
|---|---|
| `YOUR_ZOHO_ORG_ID` | Zoho Books organisation ID |
| `/YOUR_SPREADSHEET_ID` | Google Sheet with form responses and an `Errors` tab |
| `/YOUR_DRIVE_FOLDER_ID/YOUR_DRIVE_SUBFOLDER_ID` | Drive folder where form uploads land (file route) |
| connection / data store IDs (`0`) | pick your own in the module dialogs |

4. **Sheet layout.** `Form Responses 1` columns (0-based): `0` timestamp, `1` salesperson, `2` shop,
   `3` area/address, `4` order text, `5` notes, `6` uploaded file, `7` phone.
   `Errors` tab columns: shop, salesperson, area, product/line, quantity, timestamp, reason.
5. **Harness data store.** Create a data structure `DryRunRecord` with text fields `run`, `kind`, `c1`…`c10`
   and a number field `seq`, then a data store using it, and select it in the harness's three *Add/replace
   a record* modules. Keep the store small: the Make API returns at most 100 records per listing.
6. Edit the sample orders in the first module of the harness (entries separated by `§`) to use your own
   customers and products, run it, and read the data store (`kind` = `customer`, `parse`, `line`).

## Customising

* **Prompts** live in the *AI Tools → Extract* modules (parser, item comparator, customer matcher). Rule
  numbers are referenced between them; edit with care.
* **Brand hint** – a line like `* Brand Name` before the product lines is treated as a *soft* preference.
* **Regional / catalog quirks** – adjust the "promotional listing" and "legacy abbreviation" wording in rule 4
  of the comparator to match how your catalog marks promos and duplicates.
* **Tax and accounts** are taken from the matched Zoho item; check the line-item mapping in the
  `Create Sales Order` module for your tax setup.

## Known limitations

These come from the last end-to-end dry run on three sample orders (about 32 lines):

* The three prompt/normaliser changes listed under *Unverified changes* were made after that run and have
  **not been re-run**. Verify them in the harness before relying on them.
* An LLM comparator can still misread its candidate list or answer two near-identical lines differently.
  Anything not `MATCHED` goes to review, but a wrong `MATCHED` is possible; keep a human check on drafts.
* The intake scenario predates the harness's newer prompts (brand hint, customer exact-match guard,
  category rule). Port them after verifying in the harness.
* Zoho text search is substring-based; retrieval depends on the parser's `term_a`/`term_b`.
* Create Sales Order creates **drafts** only; review before confirming.

### Unverified changes (harness)

1. Customer name normaliser now lower-cases *before* replacing `stores→store` (it previously missed "Stores").
2. Category rule only applies to candidates that survive size/variant rules; pack-count, size, colour and
   age-group differences are not categories.
3. Comparator must re-scan candidates for the ordered size before answering `NOT_FOUND`, and apply the
   "unrequested extra word" rule consistently across sizes.

## Safety

No credentials are stored in the blueprints (Make keeps connections separately). Never point the harness'
sample orders at production data you don't want logged to the data store, and never run the intake
scenario's *Create Sales Order* against test data.
