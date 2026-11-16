# Independent Verification of Version 6

Checker: src/check_v6.py, a routine written separately from the build code in src/allocation_model_v6.py
Date: 16 November 2026
Solvers: the build used CBC through PuLP. Two headline items were replayed under HiGHS, a different solver.

## Result in one line

Fifteen of sixteen checks pass. One check fails: the distributionally robust ordering check. The failure is printed in full below and is not softened.

## The checks

1. **Consumer price bridge factor. PASS.** The factor from 2022 to 2025 was recomputed from the workbook Egypt_Pakistan_Farm_Costs.xlsx itself: 1.959039. The model carries 1.959039.

2. **Wheat cost on the Agricultural Research Center bridge. PASS.** The workbook budget for 2024/25 is 34,468 pounds per feddan including rent, which is 82,066.67 pounds per hectare. The model carries 82,066.67 pounds per hectare.

3. **All other crop costs on the same bridge. PASS.** Every non wheat cost in the model equals its official 2022 value, as carried in the version 5 code, times the workbook factor. Berseem equals its 2021 to 2022 ministry budget of 9,792 pounds per feddan, converted and bridged the same way.

4. **Release rule factors. PASS.** All nine release factors recompute from the inflow series file and the stated rule: the inflow ratio of the year type, plus the storage adjustment, bounded between 0.70 and 1.05.

5. **Scenario weights sum to one. PASS.** The 27 scenario weights sum to 1.000000000000.

6. **Berseem study area construction. PASS.** 1,253,666 feddans times the Delta share of 0.6824 times 0.42 hectares per feddan gives 359,310.7 hectares. The model carries 359,310.7 hectares.

7. **Capped ladder strictly falling. PASS.** The saved capped margins fall at every rung: 221,699,177,650; 210,189,613,497; 202,170,306,859; 192,795,390,204 pounds.

8. **Capped ceiling above the top rung. PASS.** The capped ceiling is 27.83 percent cover and the top feasible rung is 25 percent, so the ladder and the ceiling agree.

9. **Cover and months conversion. PASS.** At 25 percent cover the stock unit is exactly 3.00 months of consumption.

10. **Headline plan inside the rice decree. PASS.** The saved capped plan at 25 percent cover plants no rice in any water state, so its largest state rice area is 0.0 hectares against the decree bound of 451,164 hectares. The check passes trivially, and the reason is itself a result: under the caps at this rung, the optimiser crowds rice out entirely.

11. **HiGHS replay of the headline capped rung. PASS.** HiGHS returns an expected margin of 192,795,391,421 pounds for the capped problem at 25 percent cover. CBC saved 192,795,390,204 pounds. The difference is 1,217 pounds on 192.8 billion, inside solver tolerance.

12. **HiGHS replay of the capped ceiling. PASS.** HiGHS returns a ceiling of 27.83 percent cover, matching the CBC figure of 27.83 percent.

13. **Distributionally robust ordering. FAIL.** The check required the robust plan to hold a worst case at least as high as the nominal plan at every level, with both plans replayed under the same per scenario margin seeking recourse. At cover of 20 percent the nominal plan replays to a worst case of 200,522,333,750 pounds and the robust plan to 200,501,882,707 pounds, which is 20,451,044 pounds lower. At cover of 25 percent the nominal plan replays to 191,162,395,056 pounds and the robust plan to 191,139,824,167 pounds, which is 22,570,889 pounds lower. The ordering the check required does not hold under replay. What does hold is narrower: inside the robust solve itself, the robust plan attains its stated worst case value, and the price of robustness in expected margin is at most 38,316,508 pounds across the tested levels. No claim that the robust plan dominates the nominal plan under replay survives this check, and the repair log and the memo make no such claim.

14. **Monte Carlo hold share recomputed. PASS.** The share of drawn years in which the capped plan at 25 percent cover holds its floor, recomputed from the saved sample file, is 18.5 percent, matching the saved 18.5 percent.

15. **Blank template equals the no template path. PASS.** With the shipped decision maker template present and every cell blank, budgets, costs and prices are identical to a run with no template at all.

16. **One filled template cell changes only its named input. PASS.** A copy of the template with one filled cell, the wheat cost set to 99,999 pounds per hectare, changed the wheat cost and nothing else: every other cost, every price and every water budget stayed at its default value.

## What this verification does not do

It does not validate the model against the real Delta. It checks that the build computes what it says it computes, that the bridges and rules recompute from their sources, and that two headline numbers survive a second solver. The empirical label stays closed, for the reasons the repair log states.
