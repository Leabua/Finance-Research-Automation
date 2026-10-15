# File provenance

The portfolio was organised from the supplied research collection. The [source manifest](source-manifest.json) records the original relative filename, published filename and SHA-256 digest for each copied file before presentation and script-path updates.

## Main deliverables

| Published file | Original file |
| :--- | :--- |
| [Calgro completed model](../research/calgro-m3/models/CGR-Full-with-Models.xlsx) | `Calgro Complete/CGR_Full_with_models.xlsx` |
| [Calgro report](../research/calgro-m3/reports/Calgro-May-2026-Analysis.pdf) | `Calgro Complete/Calgro May 2026 Analysis.pdf` |
| [Calgro editable write-up](../research/calgro-m3/reports/source/Calgro-write-up.odt) | `calgrom3/Calgro write up.odt` |
| [SSK research model](../research/stefanutti-stocks/models/SSK-Full-Model.xlsx) | `steff/SSK_full.xlsx` |
| [SSK report](../research/stefanutti-stocks/reports/Stefanutti-Stocks-Equity-Research.md) | `steff/Stefanutti_v2.md` |
| [SSK company results](../research/stefanutti-stocks/sources/SSK-FY2026-Reviewed-Results.pdf) | `steff/FY2026.pdf` |
| [Spreadsheet foundations](../foundations/Standards-and-Curves.ods) | `Standards and curves (pre-ai).ods` |

The SSK report was present in the collection as a later Markdown write-up dated 26 May 2026. Its earlier draft is preserved in the SSK archive. The main SSK report and both main Excel workbooks retain their original contents.

## Publication changes

- Files are grouped by company, with models, reports, data, figures, scripts and earlier versions in separate folders.
- The repeated Calgro report, charts and CSV exports are represented by a single published copy. Earlier distinct models and the earlier PDF are retained in the Calgro archive.
- Python scripts resolve paths from their own location. New exports go to ignored `generated/` folders, keeping the saved research outputs intact.
- The earlier SSK draft has its opening heading cleaned up, its Obsidian marker removed and its machine-local CSV links replaced by repository-relative links. Its analysis is otherwise preserved.
- The legacy foundations workbook is unchanged, including its historical external references. These are documented in the [foundations notes](../foundations/README.md).
- Duplicate archives, Python bytecode, office lock files, local editor configuration and the generated PDF indexing XML are omitted from publication.

The original local collection is retained separately and is excluded from the public repository.
