# RemedyRoute

> **CASE FILE RR-01** · Record the issue, select a proportionate remedy, then verify completion.

RemedyRoute is a source-bound remedy workflow, not a generic claim classifier. Two independent records determine the least-escalatory applicable track. A named recipient then has a limited window to submit independent completion evidence. Validators bind both the selected track and the completion decision with full-response digests.

Lifecycle: `OPEN -> REMEDY_OPEN -> COMPLETED | DISPUTED | EXPIRED`; insufficient evidence becomes `UNRESOLVED`.

## Case progression

`open_route` records the issue, its permitted remedy tracks, a named recipient, two distinct source records, and a completion window between one hour and 30 days. That duration is frozen at creation. `select_remedy` accepts no caller-supplied deadline and makes validators retrieve the records and choose the supported least-escalatory track. Once a remedy is selected, the deadline is derived from the frozen duration. The result is not a private recommendation: the selected track and source digests are stored for later inspection.

Only the assigned recipient can call `submit_completion`, and its completion URL must use a host separate from the original evidence. If the evidence is insufficient the route becomes `UNRESOLVED`; if the recipient does not complete in time it can become `EXPIRED`; a conflicting completion is `DISPUTED` rather than silently accepted.

## Case controls

The contract rejects duplicate routes, same-host source pairs, invalid transitions, unauthorized completion, and replay. `get_route(id)` returns the precise selected track, evidence attribution, state, and final completion decision.

StudioNet: [`0xA456Ea341F0B3935310917C8172C0Fde46b7D1bF`](https://explorer-studio.genlayer.com/address/0xA456Ea341F0B3935310917C8172C0Fde46b7D1bF)
