# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| Unrelated callers cannot choose or shorten the completion window | `open_route` freezes `completion_window`; `select_remedy` has no duration argument | `test_completion_window_is_bounded_and_frozen` | PASS locally |
| Completion window has appropriate bounds | 1 hour minimum, 30 day maximum in `open_route` | short and long rejection assertions | PASS locally |
| New deployment matches corrected source | deployment manifest and Explorer source comparison | StudioNet deployment | UNVERIFIED |
| Live lifecycle uses the corrected contract | open, select, complete transactions | StudioNet smoke run | UNVERIFIED |
