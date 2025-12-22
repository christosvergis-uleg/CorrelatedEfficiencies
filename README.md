# Comparing Correlated Efficiencies: A Statistically Correct Framework

## 1. Motivation

In many applications, we compare the efficiency of two selection or decision approaches, A and B, applied to the **same underlying population** of events.  
Examples include:
- Two physics selection algorithms acting on the same dataset
- Two credit approval rules evaluated on the same customers
- Two trading signals evaluated on the same market days

A common but incorrect approach is to treat the efficiencies of A and B as **independent binomial proportions**, assigning uncertainties of the form:

$$
\sigma(p) = \sqrt{\frac{p(1-p)}{N}}
$$

This assumption fails whenever the two selections are **not mutually exclusive**, which is almost always the case in practice. Since A and B act on the same events, their efficiencies are statistically **correlated**.

This project develops a statistically correct framework to:
- Compare correlated efficiencies
- Compute the uncertainty on their difference
- Quantify *true behavioral change* rather than superficial differences

---

## 2. Problem Definition

Consider a dataset of $N$ events.  
Each event can either pass or fail selection A, and independently pass or fail selection B.

Define the following counts:

| Outcome | Description |
|------|------------|
| $n_{11}$ | Event passes both A and B |
| $n_{10}$ | Event passes A only |
| $n_{01}$ | Event passes B only |
| $n_{00}$ | Event passes neither |

By construction:
$$N = n_{11} + n_{10} + n_{01} + n_{00}$$

The efficiencies are:

$$\hat e_A = \frac{n_{11} + n_{10}}{N}, \quad
\hat e_B = \frac{n_{11} + n_{01}}{N}
$$

The quantity of interest is the **difference in efficiencies**:

$$
\Delta = \hat e_A - \hat e_B
$$

---

## 3. Why the Naive Approach Fails

If one treats $\hat e_A$ and $\hat e_B$ as independent binomial estimators, the variance of $\Delta$ is incorrectly written as:

$$
\mathrm{Var}(\Delta) = \mathrm{Var}(\hat e_A) + \mathrm{Var}(\hat e_B)
$$

This ignores the fact that:
- The same events contribute to both efficiencies
- Fluctuations in A and B are correlated
- Shared successes and failures cancel in the difference

As a result, naive error estimates typically **overestimate** the uncertainty and misrepresent the actual significance of the comparison.

---

## 4. Correct Statistical Treatment

The efficiency difference can be rewritten using the disagreement counts:

$$
\Delta = \frac{n_{10} - n_{01}}{N}
$$

Only events where A and B **disagree** contribute to the difference.

The exact variance is:

$$
\mathrm{Var}(\Delta) = \frac{n_{10} + n_{01}}{N^2} - \frac{(n_{10} - n_{01})^2}{N^3}
$$

For large $N$, this simplifies to:

$$
\sigma(\Delta) \approx \frac{\sqrt{n_{10} + n_{01}}}{N}
$$

This result shows that:
- Events where A and B agree do **not** contribute to the uncertainty
- The uncertainty is controlled entirely by the **rate of disagreement**
- Two highly overlapping selections can be compared with high precision, even if their individual efficiencies are large

This framework is mathematically equivalent to **McNemar’s test**, commonly used for paired binary outcomes.

---

## 5. Interpretation

The comparison of correlated efficiencies reduces to answering a simple question:

> How often do A and B make different decisions on the same event?

Key implications:
- Large overlap → small uncertainty on the difference
- Small overlap → large uncertainty, even if headline efficiencies differ
- Apparent improvements driven by shared events are correctly discounted

This prevents over-interpreting changes that arise from statistical correlation rather than genuine differences in behavior.

---

## 6. Broader Relevance

Although motivated by efficiency comparisons in physics, this framework applies directly to:

- Model replacement and A/B testing
- Risk and credit decision systems
- Trading strategy comparison
- Funnel and conversion optimization
- Any setting with paired binary decisions on a shared population

In all such cases, the disagreement-based uncertainty correctly captures the **true impact** of switching from one approach to another.

---

## 7. Project Goals

The goals of this project are:
1. Provide a clear statistical derivation for comparing correlated efficiencies
2. Demonstrate the failure of naive binomial uncertainty estimates
3. Offer an interpretable, disagreement-based metric for impact assessment
4. Build a foundation for applications beyond physics, including market-relevant use cases

---

## 8. Next Steps

Planned extensions include:
- Toy Monte Carlo studies comparing naive and correct uncertainties
- Visualization of overlap vs uncertainty
- Translation of the framework to business and finance case studies
- Extension to weighted events and non-binary decisions

---

## 9. Summary

Comparing efficiencies without accounting for correlation is statistically incorrect and practically misleading.  
By focusing on disagreement rates rather than headline proportions, this framework provides a robust and interpretable method to assess true differences between competing approaches.

It is less glamorous than naive error bars, but also less wrong.