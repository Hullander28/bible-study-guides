# Bible Study Guides

A mobile-friendly, installable (PWA) web app with book-by-book Bible study guides. You can read quoted verses in the Berean Standard Bible (default), the ESV, NIV, KJV, WEB, MSB, LSV, FBV, ASV, RV, YLT, DBY, WBS, BBE, and GNV (15 translations).
It's a static site with no backend. Reading progress and notes are saved in the browser's localStorage.

## Adding a book
1. Create `data/<id>.json` with the same shape as `data/genesis.json` (overview, outline, themes, keyVerses, christInBook, crossReferences, reflection, readingPlan, chapterList).
2. In `js/books.js`, set that book's 4th field to `true` (ready).
3. Add the JSON path to `CORE` in `sw.js` and bump `CACHE` so it's available offline.

## Translations

Quoted verse text (key verses, memory verses, flashcards, and the verse of the day) comes from `data/verses.json`, which stores only the verses this app actually quotes. The text is copied, unmodified, from Hidden Word's bundled Bible files (public domain, or CC BY-SA 4.0 for LSV and FBV). The default translation is the Berean Standard Bible (BSB). The NIV (2011) is also included for these quoted verses, under Biblica’s general-use rule (310 verses, not a complete book, about 6% of the product’s text by word count (well under the 25% limit), with the required copyright notice). Pick a translation in the header or under Backup & settings; the choice is saved in localStorage. Full-chapter links open BibleGateway in the chosen version (or ESV.org when ESV is selected). Attribution in the footer follows the selected translation. NIV shows Biblica’s required notice, ESV shows Crossway’s current notice (“Scripture quotations marked (ESV) are from the ESV® Bible … ESV Text Edition: 2025 …”), and LSV and FBV show their CC BY-SA 4.0 notices. ESV quotations (the same 310 verses, `data/verses-esv.json`) are used under Crossway’s standard-use rule: at most 500 verses, never half of any book, under 25% of the app’s text, with the notice. NIV and ESV are both included in the website and the store builds.

### ESV and PDF flags

`js/config.js` has `ESV_ENABLED` (default `true`, for the website and the store builds) and `PDF_ENABLED` (website only). If ESV ever has to be pulled from a build:

```
python3 tools/set_esv.py --off
```

That sets `ESV_ENABLED` to `false`, removes `data/verses-esv.json` from the service-worker cache list, and deletes `data/verses-esv.json` so no ESV text is shipped. Do not run `--off` on the git checkout if you are going to commit. `python3 tools/set_esv.py --on` restores `data/verses-esv.json` from `tools/esv-quotes.json`.

ESV quotations live in `data/verses-esv.json` (copy of `tools/esv-quotes.json`). To regenerate verse text from Hidden Word's bundled Bibles:

```
python3 tools/build_verses.py --bible /path/to/bible-memory-v2/public/bible
```

## Reading plans, memory verses, PDFs

- `js/plans.js` builds the reading plans (whole Bible in a year, in Bible order or historical order; New Testament in 90 days; Gospels in 30 days) from the book catalog. Days are saved as chapter checkmarks, so the plan and the guides stay in sync.
- `js/memory.js` lists 154 memory-verse references for the Memory Verses page, flashcards, and verse of the day. The text is looked up in the chosen translation.
- `pdf/<id>.pdf` are printable guides rendered from `data/<id>.json` (key-verse text from `data/verses-esv.json`) by `python3 tools/build_pdfs.py [ids...]` (Playwright + Chrome). They quote the ESV with Crossway’s notice. PDFs are website-only: store packages omit `pdf/`, and `PDF_ENABLED: false` hides the Download PDF button there.

## Tests

```
python3 test/test_translations.py
```

Runs the translation picker and offline checks in iPhone and Android viewports (Playwright). Screenshots are written to `test/screenshots/`.

## Store packaging (Android / iOS)

Capacitor 8 wrapper in `mobile/`, app id `org.thecreedofink.studyguides`, display name **Bible Study Guides**. This is a native package of the same static app, with all 15 translations (BSB default) but without the printable PDFs.

```
cd mobile
npm ci
npm run build:web    # copy without pdf/, PDF button off, into mobile/www
npx cap sync
```

- Android: `minSdk` 24, `targetSdk` / `compileSdk` 36. A signed release AAB is built with an upload keystore stored outside the repo (never committed). `mobile/android/keystore.properties` is gitignored. The Android Gradle build needs JDK 21.
- iOS: iOS 15+, iPhone only, portrait. `PrivacyInfo.xcprivacy` and `ITSAppUsesNonExemptEncryption` are set. `.github/workflows/ios-testflight.yml` uploads to TestFlight on `workflow_dispatch` or a tag `ios-v*`, using the same App Store Connect secret names as Hidden Word. Do not run that workflow until an App ID and App Store Connect record exist; the workflow does not create them.
- Backup export on a device uses the Capacitor Share / Filesystem plugins; the website still downloads a JSON file.
- `mobile/assets/` holds the 1024×1024 no-alpha App Store icon (`icon-only.png`), adaptive icon layers, and cream/brown splash images.

App Store Connect and Google Play listings are created separately; this repo only contains the project and CI workflow.
