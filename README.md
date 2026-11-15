# Bible Study Guides

A mobile-friendly, installable (PWA) web app with book-by-book Bible study guides based on the ESV.
It's a static site with no backend. Reading progress and notes are saved in the browser's localStorage.

## Adding a book
1. Create `data/<id>.json` with the same shape as `data/genesis.json` (overview, outline, themes, keyVerses, christInBook, crossReferences, reflection, readingPlan, chapterList).
2. In `js/books.js`, set that book's 4th field to `true` (ready).
3. Add the JSON path to `CORE` in `sw.js` and bump `CACHE` so it's available offline.

Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. Only short quotations are included. Full chapters link out to ESV.org and BibleGateway.

## Reading plans, memory verses, PDFs

- `js/plans.js` builds the reading plans (whole Bible in a year, in Bible order or historical order; New Testament in 90 days; Gospels in 30 days) from the book catalog. Days are saved as chapter checkmarks, so the plan and the guides stay in sync.
- `js/memory.js` holds 154 short memory verses (ESV, © Crossway, used by permission) for the Memory Verses page, flashcards, and verse of the day.
- `pdf/<id>.pdf` are printable guides rendered from `data/<id>.json` by `python3 tools/build_pdfs.py [ids...]` (Playwright + Chrome).
