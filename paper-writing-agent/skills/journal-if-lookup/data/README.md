# Journal data

This installation includes a 2025 local journal metrics snapshot:

- `journals_index.json`: ready-to-query index built from the accompanying workbook.
- `2025IF.xlsx`: source workbook retained for inspection or an explicitly requested rebuild.

Direct query uses the bundled index:

`python query.py "journal name"`

To use an authorized replacement index, pass it explicitly:

`python query.py "journal name" --data-file "<project>/journals_index.json"`

Build a new index only when needed:

`python build_index.py --data-file "<project>/journals.xlsx" --output "<project>/journals_index.json"`

The bundled records are an offline, year-labelled snapshot. They are not automatically current metrics; report the data year and use date-aware official verification when the task asks for current information. The query tool never turns a missing index into a zero match.
