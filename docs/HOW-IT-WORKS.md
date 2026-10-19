# How it works (in plain words)

Think of three helpers handing work along, with a strict rule: **only continue when sure.**

```
 Order text ──▶ 1. READER ──▶ 2. FINDER ──▶ 3. CHECKER ──▶ ✅ billed
                (AI)          (Zoho search)   (AI)           ❓/⛔ goes to the "Errors" sheet
```

## 1 · The Reader (AI "parser")

It only **organises** the message; it never picks products. For every line it writes down:

| Field | Example for `Chocolate High Protein Muesli 28gm-400gm-4pc` |
|---|---|
| search words | `muesli`, `protein` (short, broad, so a typo can't make it miss) |
| product text | `Chocolate High Protein Muesli 28gm` (numbers that belong to the name stay!) |
| ordered size | `400gm` → normalised `400g` (so 1kg = 1000 g = 1000 gm) |
| quantity | `4` (never mixed into the product name) |

It also reads the customer name, phone, address and an optional **brand line** (`* Acme Foods`).

## 2 · The Finder (Zoho search)

It asks Zoho Books for items whose **name contains** the search words. Getting 40–90 candidates is normal;
what matters is that the right one is among them. If nothing comes back it retries with an obvious spelling
fix (`charcol` → `charcoal`). It never searches the whole catalog blindly and **only active items count**.

## 3 · The Checker (AI "comparator")

It picks **only from the list Zoho returned**; item IDs always come from Zoho, never from the AI. Its rules:

1. **Size:** if the customer gave a size it must match exactly (900 gm ≠ 1 kg). If no size was given, size
   is ignored and the product alone decides.
2. **Every typed word counts.** "High Protein" typed → candidates without it are wrong. Typos are accepted
   only if a candidate confirms them.
3. **Extras that weren't asked for** (a flavour, "Kids", "Seeds"…) mean it won't silently choose that item
   → **AMBIGUOUS**.
4. **Clean beats promo:** names like "…100 OFF", "offline discount" or old abbreviations lose to the clean
   listing of the same product.
5. **Duplicates:** the same item returned twice counts once; two different items that look identical are
   only accepted if rate, tax and the other fields really match.
6. **Mixed kinds** (a toothbrush *and* a soap both called "charcoal") → **AMBIGUOUS**; it asks a human.

## The customer

Searches by full name, relaxed name (`and` = `&`), first two words, first word and **phone**. The AI chooses
among what Zoho returns; in the dry-run a **non-AI check** additionally requires an *exact* name (ignoring
case/punctuation/Store-vs-Stores) or a phone match. "Centre" and "Central" are *not* the same word.

## The three outcomes

| Status | Meaning | What happens |
|---|---|---|
| ✅ **MATCHED** | exactly one right product/customer | goes into the draft Sales Order |
| ❓ **AMBIGUOUS** | two or more plausible, or an unrequested variant | **not billed** → `Errors` tab with the options |
| ⛔ **NOT_FOUND** | no valid candidate (e.g. size doesn't exist) | **not billed** → `Errors` tab |

If the **customer** isn't confidently matched, the whole order goes to `Errors` and nothing is created.
