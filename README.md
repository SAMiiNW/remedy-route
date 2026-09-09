# RemedyRoute

RemedyRoute is a source-bound remedy workflow, not a generic claim classifier. Two independent records determine the least-escalatory applicable track. A named recipient then has a limited window to submit independent completion evidence. Validators bind both the selected track and the completion decision with full-response digests.

Lifecycle: `OPEN -> REMEDY_OPEN -> COMPLETED | DISPUTED | EXPIRED`; insufficient evidence becomes `UNRESOLVED`.
