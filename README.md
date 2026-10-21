# lot-expiry-ledger

Replay lot receipts, all-or-nothing FEFO issues and disposals with allocation witnesses and exact stock conservation.

For warehouse planners checking a small whole-unit lot allocation scenario before importing it into an operational system.

## Quickstart

Python3.10+; no external service or runtime dependencies. Linux shell:

```sh
git clone https://github.com/nripankadas07/lot-expiry-ledger.git
cd lot-expiry-ledger
python -m venv .venv
. .venv/bin/activate
python -m pip install .
lot-expiry-ledger example.json
```

The invented issue allocates the earlier-expiring lot before the later lot; conservation remains exact. [Expected JSON](example-output.json).

## Input and interpretation

Use the exact object in [example.json](example.json). Unknown keys, duplicate JSON keys and nonfinite numbers reject. The JSON file is read only, <=1MiB. Identifiers are nonempty strings <=128 characters; booleans are not integers.

Whole positive integer units, logical integer days in nondecreasing event order, globally unique event and lot IDs; <=5000 events and integer inputs within +/-10^15. Lot expiry strictly greater than issue day is eligible. Sort by earliest expires then lexical lot ID; stockouts allocate nothing and replay continues. Expired receipts remain visible; disposal may remove expired or unexpired stock, but cannot overdraw. No returns, transfers, reservations, costs, calendars, ERP connection or operational safety certification. This own simplified policy differs from ERP removal-date/reservation workflows.

Exit0: completed result without a finding/conflict; exit1: documented schema/shared-formula/stockout finding or merge conflict; exit2: malformed/unsupported input, stderr and no partial JSON report. Event-time drops are normal policy decisions and use exit0. A completed report is evidence only about the supplied model and supported subset. No automatic live-system changes.

## Verification

```sh
python -m unittest -v
python -m compileall -q lot_expiry_ledger.py
python -m pip wheel --no-deps . -w dist
```

Unit-expansion priority oracle across12 request quantities, tie/expiry boundary, atomic stockout, multi-SKU isolation, disposal conservation and invalid-state rejection. [Validation record](VALIDATION.md). CI checks Python3.10/3.12/3.14 and a wheel-installed console from outside the checkout. Windows/macOS and production-size workloads are not verified. No benchmark or superiority claim.

## Scope and provenance

Alpha utility, original AI-assisted implementation and invented fixtures. Standard algorithms were reimplemented; no third-party implementation/prose copied. MIT. [Candidate brief](BRIEF.json), [dated research and alternatives](RESEARCH.md), [support](SUPPORT.md), [contribution guide](CONTRIBUTING.md), [security](SECURITY.md).

bom-rollup-ledger explodes assembly quantities; invoice rounding accounts for monetary units. This tracks expiry-qualified lot-level stock through ordered events and rejects overdraws.
