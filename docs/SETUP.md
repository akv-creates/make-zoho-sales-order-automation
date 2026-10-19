# Setup guide (step by step)

Follow in order. Tick the boxes as you go. Plan on **30–45 minutes**.

---

## Step 0 · Collect three things

| What | Where to find it |
|---|---|
| **Zoho Books Organization ID** | Zoho Books → **Settings → Organization Profile** → "Organization ID" |
| **Zoho data centre** | The domain you log in on: `zoho.com`, `zoho.in`, `zoho.eu`, `zoho.com.au`… |
| **Google Sheet URL** | You create it in Step 1 |

- [ ] Zoho Organization ID noted
- [ ] Zoho data centre noted

## Step 1 · Create the Google Form and Sheet

1. Create a **Google Form** with these questions **in this exact order** (the scenario reads columns by
   position):

   | # | Question | Type |
   |---|---|---|
   | 1 | Salesperson | Short answer / dropdown |
   | 2 | Shop name | Short answer |
   | 3 | Area / address | Short answer |
   | 4 | Order (one product per line: `name-size-qty`) | **Paragraph** |
   | 5 | Notes | Paragraph (optional; keeps column order, not read by the scenario) |
   | 6 | Upload order file (photo/PDF) | File upload (optional) |
   | 7 | WhatsApp / phone | Short answer |

   Google adds **Timestamp** as column A, so the sheet columns end up as: Timestamp, Salesperson, Shop,
   Area, Order, Notes, File, Phone. A header line to copy is in
   [`templates/form-responses-header.csv`](../templates/form-responses-header.csv).
2. In the Form, open **Responses → Link to Sheets** and create the response sheet. Keep the tab name
   **`Form Responses 1`** (Google's default).
3. In the **same spreadsheet**, add a second tab named exactly **`Errors`** and paste this header into
   row 1 ([`templates/errors-header.csv`](../templates/errors-header.csv)):

   `Shop | Salesperson | Area / address | Product line | Quantity | Timestamp | Reason`

   Every unresolved line and every unconfirmed customer is written here.
4. Copy the sheet's URL.

- [ ] Form created, columns in the right order
- [ ] Tab `Form Responses 1` exists
- [ ] Tab `Errors` exists with the header row

> **Text vs. photo orders:** if the *Upload order file* answer is empty the **text route** is used;
> if a file is attached the **file route** reads it (needs Google Drive access, Step 4).

## Step 2 · Prepare Zoho Books

- [ ] Your **customers exist** in Zoho Books (the template never creates customers).
- [ ] Your **items are active** and named clearly, ideally with the size in the name
      (`Acme Muesli – Nuts & Berries – 400 gm`). Inactive items are ignored.
- [ ] Optional but helpful: delete or deactivate obvious duplicate items.

## Step 3 · Fill in your IDs

From the folder you unzipped:

```bash
python3 tools/fill_placeholders.py \
  --zoho-org YOUR_ORG_ID \
  --spreadsheet "https://docs.google.com/spreadsheets/d/…/edit"
```

This writes ready-to-import copies into a new folder **`my-scenarios/`** and does not touch the originals.
For photo/PDF orders add `--drive-folder "<Drive folder URL>"` (the folder Google Forms uploads land in).

No Python? Open the two `.blueprint.json` files in any text editor and replace `YOUR_ZOHO_ORG_ID`,
`/YOUR_SPREADSHEET_ID` (keep the leading `/`) and, if you use the file route, the two Drive placeholders.

- [ ] `my-scenarios/` contains two files

## Step 4 · Import into Make and connect your accounts

Do the **dry-run first**.

1. Make → **Scenarios → Create a new scenario**.
2. Click the **⋯ (More)** menu at the bottom of the editor → **Import Blueprint** → choose
   `my-scenarios/dry-run.blueprint.json`.
3. Modules with a red warning need a **connection**. Open each and pick / create:

   | Module type | Connection |
   |---|---|
   | **Zoho Books** | Create one. Choose the **same data centre** you noted in Step 0. Make sure the scopes include reading **contacts** and **items/settings**, and reading + creating **sales orders**. |
   | **AI Tools → Extract** | Your Make AI connection (Make offers it when you open the module). |
   | **Google Sheets / Google Drive** | Your Google account (intake scenario only). |

4. **Create the data store for the dry-run results** (the dry-run only):
   - Make → **Data structures → Add** → name `DryRunRecord`, add these fields:
     `run` (text), `kind` (text), `seq` (number), `c1` … `c10` (text).
   - Make → **Data stores → Add** → name `DryRun Results`, structure `DryRunRecord`.
   - In the dry-run scenario open the three modules named **Add/replace a record** and select that data
     store in each.
5. Save the scenario.

- [ ] Dry-run scenario imported and saved, no red warnings

## Step 5 · First test: the dry-run (safe)

1. Open the first module of the dry-run. It contains three sample orders separated by `§`. Replace the
   customers and products with real ones **from your Zoho** (see
   [`templates/sample-orders.txt`](../templates/sample-orders.txt) for the format).
2. Click **Run once**. It takes **a few minutes** (one AI call per order line, run one after another).
3. Open **Data stores → DryRun Results**. Each row is one result:

   | `kind` | What you see |
   |---|---|
   | `customer` | `c4` decision (MATCHED / AMBIGUOUS / NOT_FOUND), `c5` the matched customer, `c6` the reason |
   | `parse` | `c1` how your order was split into lines |
   | `line` | `c1` the line, `c4` the candidates Zoho returned, `c5` decision, `c6` chosen item, `c7` reason |

4. Is it right? Fix the catalog / wording ([CUSTOMIZE.md](CUSTOMIZE.md)) and run again. Delete old rows
   between runs to keep the store small (the Make API lists at most 100 records).

- [ ] The dry-run gives the answers you expect on *your* products

## Step 6 · Import the real scenario and test with ONE row

1. Import `my-scenarios/sales-order-intake.blueprint.json` the same way and connect the modules.
2. On the **Google Sheets → Watch Rows** module choose **Choose where to start → From now on**, so old rows
   are not processed.
3. Submit **one test order** through your Form for a customer and items you're happy to see as a draft.
4. Click **Run once**. Then check:
   - Zoho Books → **Sales Orders**: a **Draft** appears with the right customer and lines, **or**
   - your **Errors** tab: the lines it wasn't sure about, with the reason.
5. Delete the test draft in Zoho if you don't need it.

- [ ] One real row produced a correct draft (or a sensible Errors entry)

## Step 7 · Go live

- Turn the scenario **ON** and choose how often it checks the sheet (e.g. every 15 minutes).
- Make it a habit: **check the Errors tab daily** and **review drafts before confirming** them in Zoho.

Something went wrong? → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
