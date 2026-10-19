# Customising

You can change almost everything from the Make editor, no code. Do changes in the **dry-run** first.

## Where the "brains" live

Open the scenario and look for modules named **AI Tools → Extract** (they have a long text box):

| Module | Job |
|---|---|
| first one after the trigger | **Parser** (reads the order) |
| the one right after the customer searches | **Customer matcher** |
| the one right after the item searches | **Item comparator** |

Each prompt is a numbered list of rules. Change wording, not rule numbers: rules refer to each other.

## Common tweaks

| I want to… | Do this |
|---|---|
| **Use different form columns** | In *Watch Rows*, columns are referenced as `` {{171.`4`}} `` (0 = Timestamp, 1 = Salesperson, 2 = Shop, 3 = Area, 4 = Order, 5 = Notes (unused), 6 = File, 7 = Phone). Edit those mappings. |
| **Put a brand first** | Add a line like `* Acme Foods` above the products. It is a *soft* preference: it breaks ties but can't override size or required words. |
| **Be stricter** (fewer wrong matches) | In the comparator add: "If confidence is not HIGH answer AMBIGUOUS." |
| **Be looser** (fewer review items) | Remove rule 6 of the comparator (unrequested variants) for catalogs where extras are harmless. |
| **Handle your promo naming** | Rule 4 of the comparator lists words that mark promo/legacy listings (OFF, offline, combo…). Add yours. |
| **Another language / spelling style** | Add 2–3 examples to the parser's "generic examples" section. |
| **Change the review sheet** | Edit the 4 *Google Sheets → Add a row* modules (columns map to the header in `templates/errors-header.csv`). |
| **More / fewer candidates** | In the *List items* modules change **Limit** (default 150). |
| **Order date or other fields** | Edit the *Set variable* module just before *Create a sales order*. |
| **Tax** | Tax is copied from the matched Zoho item. Fix tax on the item in Zoho, not here. |

## Make Zoho items easier to match (best accuracy gain!)

- Put the **size in the name** (`… – 400 gm`).
- Keep **one active listing per product + size**; deactivate duplicates.
- Don't add words that aren't part of the product to names (the matcher treats extra words as a difference).

## Adding your own test cases

Put them in the dry-run's first module (separate orders with `§`) and keep a note of the answer you
*expect* for each line. A good set includes: a size that doesn't exist, a typo, an item with no size given,
a very short name like `Mint 4`, and a customer name that has a near-twin in Zoho.
