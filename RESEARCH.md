# Research — 21 October 2026

Demand is **inferred**, not a verified request for this tool. A stock total hides expired lots, FEFO tie decisions and partial mutations caused by an unfulfillable issue.

[Exact Most-stars search](https://github.com/search?q=inventory%20expiry&type=repositories&s=stars&o=desc), observed 2026-10-21T06:19:19.175Z. Highest-star relevant comparable found in the inspected pool: `odoo/odoo`. This is not an exhaustive global ranking.

| Comparable | Stars | Last push | License metadata | Observed workflow |
| --- | ---: | --- | --- | --- |
| [odoo/odoo](https://github.com/odoo/odoo) | 55207 | 2026-10-21T05:43:48Z | NOASSERTION | Full ERP, inventory and reservation workflows; FEFO uses product removal-date configuration. |
| [frappe/erpnext](https://github.com/frappe/erpnext) | 40412 | 2026-10-21T05:55:34Z | GPL-3.0 | Full ERP with stock and business workflows on Frappe. |
| [metasfresh/metasfresh](https://github.com/metasfresh/metasfresh) | 2455 | 2026-10-21T05:47:35Z | unknown | Full ERP and warehouse/business workflows. |

## Choice and tradeoffs

Replay lot receipts, all-or-nothing FEFO issues and disposals with allocation witnesses and exact stock conservation. bom-rollup-ledger explodes assembly quantities; invoice rounding accounts for monetary units. This tracks expiry-qualified lot-level stock through ordered events and rejects overdraws.

The established alternatives are broader and often the better choice for their supported ecosystems. This tool provides one bounded inspectable report with an invented example and no runtime dependencies. READMEs/docs were read for install and example workflow; competitor clean install, time to first useful result, reliability, support response and performance were not measured. Own tests prove only the documented subset. Stars are research context, not performance or adoption evidence.

Keyword search coverage is narrow: Avro results include generators/profilers, event-time results include general streaming platforms, inventory-expiry results include unrelated homelab/certificate inventory, and three-way results include plugins and unrelated scraped text. Known relevant established tools were added directly. Spreadsheet comparison uses Excelize rather than an obsolete GitHub openpyxl mirror.

[Exact metadata and sampled current issues/PRs](RESEARCH_PROVENANCE.json). The samples are context, not verified competitor defects or requests for our new tool. Relevant Avro compatibility, POI SharedFormula and Git merge-file source was inspected; standard algorithms are original reimplementations. Microsoft CellFormula and Beam semantics informed the bounded contracts. No third-party code, branding or prose is copied.

Primary references:
- https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/shipping_receiving/removal_strategies/fefo.html
