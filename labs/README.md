# Statistical Inference by Simulation: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · A sample is one draw of many | [`D1_1_draw_1_000.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_1_draw_1_000.ipynb) |
| Day 1 | Session 2 · Standard error by simulation and by formula | [`D1_2_compare_simulated_formula.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_2_compare_simulated_formula.ipynb) |
| Day 1 | Session 3 · Skew, outliers and the median | [`D1_3_measure_how_one.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_3_measure_how_one.ipynb) |
| Day 1 | Session 4 · Describing a sample honestly | [`D1_4_summarise_repair_times.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_4_summarise_repair_times.ipynb) |
| Day 2 | Session 1 · The bootstrap idea | [`D2_1_bootstrap_median_repair.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_1_bootstrap_median_repair.ipynb) |
| Day 2 | Session 2 · Coverage is a testable claim | [`D2_2_count_how_often.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_2_count_how_often.ipynb) |
| Day 2 | Session 3 · Resample the right unit | [`D2_3_bootstrap_satisfaction_household.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_3_bootstrap_satisfaction_household.ipynb) |
| Day 2 | Session 4 · Intervals for differences and ratios | [`D2_4_build_intervals_difference.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_4_build_intervals_difference.ipynb) |
| Day 3 | Session 1 · A test is a shuffling rule | [`D3_1_run_permutation_test.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_1_run_permutation_test.ipynb) |
| Day 3 | Session 2 · p-values and their misreadings | [`D3_2_mark_eight_report.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_2_mark_eight_report.ipynb) |
| Day 3 | Session 3 · Effect size and practical significance | [`D3_3_report_contractor_effect.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_3_report_contractor_effect.ipynb) |
| Day 3 | Session 4 · Thirty districts, many false alarms | [`D3_4_test_30_districts.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_4_test_30_districts.ipynb) |
| Day 4 | Session 1 · Least squares as a summary | [`D4_1_fit_consumption_household.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_1_fit_consumption_household.ipynb) |
| Day 4 | Session 2 · Slopes with intervals | [`D4_2_bootstrap_slope_compare.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_2_bootstrap_slope_compare.ipynb) |
| Day 4 | Session 3 · Residuals and confounding | [`D4_3_add_temperature_plot.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_3_add_temperature_plot.ipynb) |
| Day 4 | Session 4 · Writing an inference brief | [`D4_4_draft_estimate_interval.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_4_draft_estimate_interval.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
