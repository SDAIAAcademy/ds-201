# Statistical Inference by Simulation: labs

Hands-on notebooks for the SDAIA Academy course **DS-201 Statistical Inference by Simulation (الاستدلال الإحصائي بالمحاكاة)**. Every lab works on **Zulal Water Utility (مرفق زلال للمياه)**, a fictional regional water utility whose whole population is on file, so every interval and every test is checked against the truth. Each lab starts from supplied files and draws its own seeded sample, so none depends on an earlier one, and each ends with a short verification note: what was checked against the truth and what was not.

**Nothing calls or downloads a model.** A laptop processor or a Colab CPU runtime is enough. The optional hint-only tutor is an instruction file, `tutor_instruction.md`, that you paste into an assistant your Academy has approved.

## Quick start

**Google Colab.** Open a notebook from the [course page](https://sdaiaacademy.github.io/ds-201/), or directly: `https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/<notebook>.ipynb`. Run the first cell: it clones this repository and installs `requirements-colab.txt`.

**Local**
```bash
git clone https://github.com/SDAIAAcademy/ds-201
cd ds-201/labs
uv sync                          # creates the environment from pyproject.toml (uv.lock pins every version)
uv run jupyter lab
```
Run `00_setup_check.ipynb` once before Day 1. It imports the libraries and reads the four population files.

| Setting | Default | Meaning |
|---|---|---|
| `DS201_QUICK` | `0` | `1` runs fewer simulated studies and resamples, for a fast pass |

## Notebooks

| Day | Session | Notebook |
|---|---|---|
| 0 | Setup | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/00_setup_check.ipynb) |
| 0 | Pre-work: sampling and plotting | [`P0_prework_sampling_plotting.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/P0_prework_sampling_plotting.ipynb) |
| 1 | One sample, then a thousand | [`D1_1_sampling_means.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_1_sampling_means.ipynb) |
| 1 | Standard error twice | [`D1_2_standard_error.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_2_standard_error.ipynb) |
| 1 | One ticket left open | [`D1_3_extreme_repair.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_3_extreme_repair.ipynb) |
| 1 | Five numbers and a histogram | [`D1_4_five_numbers.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D1_4_five_numbers.ipynb) |
| 2 | Bootstrap a median | [`D2_1_bootstrap_median.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_1_bootstrap_median.ipynb) |
| 2 | Count the coverage | [`D2_2_coverage.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_2_coverage.ipynb) |
| 2 | Household or district | [`D2_3_resampling_unit.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_3_resampling_unit.ipynb) |
| 2 | Difference and ratio of medians | [`D2_4_difference_ratio.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D2_4_difference_ratio.ipynb) |
| 3 | Shuffle the contractor labels | [`D3_1_permutation_test.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_1_permutation_test.ipynb) |
| 3 | Mark eight report sentences | [`D3_2_report_sentences.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_2_report_sentences.ipynb) |
| 3 | The effect against the threshold | [`D3_3_effect_threshold.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_3_effect_threshold.ipynb) |
| 3 | Thirty districts at once | [`D3_4_thirty_districts.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D3_4_thirty_districts.ipynb) |
| 4 | Consumption on household size | [`D4_1_fit_line.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_1_fit_line.ipynb) |
| 4 | An interval for the slope | [`D4_2_slope_interval.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_2_slope_interval.ipynb) |
| 4 | Add temperature | [`D4_3_residuals_confounding.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_3_residuals_confounding.ipynb) |
| 4 | One paragraph of a brief | [`D4_4_brief_paragraph.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-201/blob/main/labs/D4_4_brief_paragraph.ipynb) |

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in; the cell after each one then uses a stored reference result, so the rest of the notebook still runs. Complete reference versions are in `solutions/`. Cells marked **✱ Stretch** are optional. Self-checks print ✅ or ❌.

**Assistant policy.** Quizzes and each day's first core computation (labs 1.1, 2.1, 3.1 and 4.1, and the marking in lab 3.2) are done without an assistant. In the other steps and the stretch items the tutor instruction may hint one step at a time; it never writes the simulation. The capstone is open to an assistant and is defended live.

## The case study: Zulal Water Utility

Synthetic and deterministic (seed 201), written by `prepare_data.py`. No real utility, household, contractor or district is described.

| Data | File | Contents |
|---|---|---|
| Districts | `data/districts.csv` | 30 districts, from 700 to 10,079 households, each with a mean summer temperature |
| Households (the population) | `data/households.csv` | 80,000 metered households: pseudonymised key, district, household size, temperature, daily consumption in litres |
| Leak repairs (the population) | `data/repairs.csv` | 12,000 repairs: district, contractor A or B, repair time in hours, status; 12 tickets were closed weeks late |
| Survey (the population) | `data/survey.csv` | 9,000 responses: pseudonymised keys, district, contractor of the last repair, satisfaction 1 to 10 |
| One study | `data/study_satisfaction.csv` | 400 responses for each contractor (labs 3.1 and 3.3) |
| One study | `data/metered_2000.csv` | 2,000 households drawn at random (Day 4) |
| Report sentences | `data/report_sentences.json`, `data/report_sentences_key.json` | the eight sentences of lab 3.2 and their key |
| Planted districts | `data/planted_districts.json` | the five districts whose repair time truly differs (opened in lab 3.4, step 2) |
| Reference results | `data/reference/` | what each exercise returns in the solution run, for the safety nets (full and quick mode) |

**Handled as personal data.** The survey is synthetic, and the labs still treat it as personal data under the Personal Data Protection Law: households appear only as pseudonymised keys, results are reported by district or contractor and never by household, and every conclusion names the population it applies to.

What is planted and which lab finds it is in `solutions/answer_key.md`, for the trainer.

## Capstone and follow-up

- `capstone/README.md`: the three questions, the datasets not used in class, what the repository must contain and the rubric.
- `followup/README.md`: the follow-up task, an inference brief on a table of the national Open Data Platform within two weeks.

## For authors

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `solutions/`. Edit the sources, not the notebooks. A solution run with `DS201_STRICT=1` stops at the first failed check; with `DS201_WRITE_REF=1` it rewrites `data/reference/`.
