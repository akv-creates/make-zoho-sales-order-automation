# FAQ

**Does it create anything in Zoho by itself?**
Yes, but only **draft** Sales Orders, and only for lines it is sure about. Nothing is confirmed or sent.

**Does it create new customers?**
No. Unknown customers go to the `Errors` sheet.

**What does it cost?**
Make operations plus AI Tools usage. As a rough guide, the dry-run used about **240 operations for 3 orders
(32 lines)**, i.e. roughly 5–8 operations per order line. Check your Make plan before bulk use. Zoho Books
API calls are included in your Zoho plan (subject to Zoho's API limits).

**How long does an order take?**
Roughly 5–10 seconds per line (they run one after another), so a 30-line order takes a few minutes.

**Can it read photos or PDFs of handwritten orders?**
There is a file route (Google Drive → AI document reader → same matching). Quality depends on handwriting
and image quality; always review.

**Does it work for my industry?**
If orders are free text and your catalog is in Zoho Books, yes. The wording examples are FMCG-flavoured
(packs, grams, brands). Tweak the parser examples ([CUSTOMIZE.md](CUSTOMIZE.md)).

**Can I use Zoho Inventory / another accounting tool?**
Not as shipped. The Zoho Books modules would need to be swapped for the equivalents.

**Is it safe to try?**
Yes, start with the **dry-run scenario**: it never writes to Zoho. Then test the real one with one row
and delete the draft.

**Which AI model is used?**
Make's built-in *AI Tools → Extract* (large model option). You can change the model in each module.

**Why not let it guess?**
Because a wrongly billed product costs more than a line in the review sheet. "I'm not sure" is a feature.

**Can I share/modify this?**
Yes. It is released under the [MIT License](../LICENSE): use, copy, modify and share it freely, including commercially. It comes with no warranty; test on your own data first.
