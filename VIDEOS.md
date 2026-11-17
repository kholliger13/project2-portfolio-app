# Three recording briefs

Open each recording with an accurate AI disclosure. For example, “AI assisted with preparation and validation. This presentation is for education, not investment advice.”

## 1. How it changed

**Audience:** Course reviewer. **Show:** The baseline table, then the two portfolio windows side by side.

- Start with Lab 13. The benchmark clears the 6.5% modeled return objective and misses the 3% reserve floor. The other two baselines clear the floor and miss the return objective.
- Move to Lab 14. Keep its separate 8% objective and 20% reserve floor fixed. Switch from all 59 monthly returns to the last 36. LQD rises from 55% to 80%.
- Close with the change in the work. A static baseline comparison became an app that makes the assumptions and sensitivity visible. The vintage work later added a check on which inputs were knowable on the decision date. Name one AI output you personally checked, describe your check, and say what you concluded.

## 2. Technical walkthrough

**Audience:** A reviewer reproducing the result. **Show:** README, terminal checks, source CSVs and the PAYEMS control.

- Run `sh review.sh`. Pause at the classroom known answer and point out why April publications are excluded from the March 31 signal.
- Open the September 6 and October 4 PAYEMS sources. In the rates app, change the same-day option for October 4 and show September appearing only when same-day publications are included.
- Point to the two fixed expectations in `payems_verify.py`. End with the date-level limit of the captured evidence.

## 3. Committee decision

**Audience:** An investment committee. **Show:** The decision and must-fix list.

- Lead with the vote. Hold pilot funding until the committee or instructor confirms which portfolio the 8% estimate screens. Recommend applying it to the funded sleeve.
- Show the replay result and the funding check. The constrained mix passed both replay vetoes. On the same 23-month fit, the 25/75 blend estimates 3.49% and the equal-weight fallback 1.88%. The pilot and fallback both fail if the screen applies to the sleeve.
- State what would reopen the decision. If the screen applies to the constrained allocation and the remaining sleeve checks pass, start at 25%. Review any proposed fund weight change above 15 percentage points. A binding mandate failure blocks funding or continued use.

These briefs are ready for recording. Submission links can be added once the three recordings exist.
