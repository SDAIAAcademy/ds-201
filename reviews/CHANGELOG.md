# Changes

## 2027.2.0 (2026-11-24)

- Added: oversampling a rare group and restoring the population mean with design weights, `oversample-rare-group` and `design-weights` (day 2, session 3); stretch 2 of lab 2.3 oversamples the six smallest districts of the survey and weights them back.
- Added: regression to the mean when the most extreme districts are singled out, and the comparison by lot that removes it, `worst-five-recover` and `extremes-need-a-control` (day 3, session 4); stretch 2 of lab 3.4 audits the five slowest districts again with nothing changed.
- Added: precision and prevalence of a flag checked on a test set drawn by class, corrected for the population mix, `balanced-test-precision` and `precision-reweighted` (day 4, session 4).
- Added: three practice questions, `q-weights-01`, `q-extremes-01` and `q-precision-01`.
- Added: `labs/_tools/weights_and_extremes.py`, which computes every number on the new slides.
- Tightened: `rows-not-independent` (day 2), `forking-paths` (day 3) and `question-to-estimand` (day 4) lose one line each to keep the sessions at their length.
