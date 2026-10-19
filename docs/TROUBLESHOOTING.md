# Troubleshooting

Look for your message, apply the fix. Everything below was met while building this.

| Message / symptom | Why | Fix |
|---|---|---|
| `[15] Please ensure that the "name_contains" has less than 100 characters` (List items) | A search word was too long (e.g. the whole line was used). | The template shortens words to 40 characters. If you changed the parser, keep `term_a`/`term_b` to **one short word** each. |
| `[15] … "search_text" has less than 100 characters` | Same, with the simple search. | Same. |
| `[15] Please ensure that the "area" has less than 100 characters` (Create sales order) | Long free text went into a line item. | Line items must carry only item id, quantity, tax fields. Don't add notes/addresses to them. |
| `[57] You are not authorized to perform this operation` (Create contact) | Your Zoho connection lacks **contacts create** permission. | This template never creates customers. If you add that step, re-create the Zoho connection with the contacts-create scope. |
| `[400] Unsupported alt type "media"` (Google Drive → Get a file) | The file was addressed by name instead of ID. | The template reads the file ID from the form's upload link. Make sure the upload column contains the Drive link. |
| *"line_items field was empty"* | No line could be confidently matched. | Not a bug: look at the **Errors** tab; each line has the reason. |
| Only **1** line of a long order is created | The reader's output was split wrongly. | The template separates lines with `§`. If you edited the parser prompt, keep that instruction. |
| Order goes to Errors: **customer not confirmed** | Customer missing in Zoho, or the name differs by a real word ("Centre" vs "Central"). | Create the customer in Zoho, or spell the name as in Zoho. Phone on the Zoho contact helps a lot. |
| Run takes minutes | One AI call per line, one after another. | Normal (≈ 4–5 min for ~30 lines). |
| Same line gives different answers on two runs | AI models aren't perfectly consistent. | Keep human review. Tighten the prompt ([CUSTOMIZE.md](CUSTOMIZE.md)) and re-test in the dry-run. |
| Data store listing shows only 100 records / old rows | The Make API returns max 100 per request. | Delete old rows between dry-runs. |
| Old sheet rows get processed | Trigger started from the beginning. | Watch Rows → **Choose where to start → From now on**. |
| Editing in Make then re-importing loses changes | Import replaces the scenario. | Export a blueprint (⋯ → Export Blueprint) before big edits. |

## Unverified changes in the dry-run

These were made after the last end-to-end test and have **not** been re-run; test them on your data:

1. Customer name normaliser lower-cases first, so "Store" and "Stores" now match exactly.
2. The category rule applies only to candidates that survived the size/variant rules; pack-of-2, size,
   colour and kids/adult differences are *not* different categories.
3. The comparator must re-scan every candidate for the ordered size before answering NOT_FOUND, and apply
   the "unrequested extra word" rule consistently at every size.

## Still stuck?

Open a GitHub issue with: the order text, the dry-run row (`kind` = `line`), and the exact error text.
Please **remove customer names and phone numbers** first.
