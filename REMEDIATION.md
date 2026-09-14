# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| Unrelated callers cannot choose or shorten the completion window | `open_route` freezes `completion_window`; `select_remedy` has no duration argument | `test_completion_window_is_bounded_and_frozen` | PASS locally |
| Completion window has appropriate bounds | 1 hour minimum, 30 day maximum in `open_route` | short and long rejection assertions | PASS locally |
| New deployment uses corrected source commit `d939323` | `deployment.json` binds source commit, SHA-256 and deployment transaction | `0x57b2...bbd8` finalized with `MAJORITY_AGREE` | PASS live |
| Live lifecycle uses the corrected contract | `RR-1789399072`; open `0xd94e...fe9a`, select `0x1bd1...ff79` | canonical state is `REMEDY_OPEN`, track `0`, frozen window `3600` | PASS live |
