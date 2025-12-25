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

As a result, naive error estimates can significantly misestimate the uncertainty, often underestimating it in correlated regimes.

---

## 4. Correct Statistical Treatment

The efficiency difference can be rewritten using the disagreement counts:

$$
\Delta = \frac{n_{10} - n_{01}}{N}
$$

Only events where A and B **disagree** contribute to the difference.

A finite-sample variance estimator is:

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

This framework is closely related to **McNemar’s test** for paired binary outcomes.

---

## 5. Interpretation

The comparison of correlated efficiencies reduces to answering a simple question:

> How often do A and B make different decisions on the same event?

Key implications:
- Large overlap → small uncertainty on the difference
- Small overlap → large uncertainty, even if headline efficiencies differ
- Apparent improvements driven by shared events are correctly discounted

This prevents over-interpreting changes that arise from statistical correlation rather than genuine differences in behavior. 

This work focuses on validating the uncertainty estimator required for hypothesis testing; applying a specific decision threshold or p-value is left to the user.

---

## 6. Extension to Weighted Events

The framework above assumes equal event contributions. In practice, events often carry heterogeneous weights, and so events do not contribute equally.  
Instead of binary outcomes counted once per event, each event carries a **weight** reflecting, for example:
- exposure or importance
- expected value or cost
- simulation or importance-sampling weights
- revenue, profit, or risk contribution

This section outlines how the framework for comparing correlated efficiencies extends to **weighted events**.

---

### Problem Setup (Weighted Case)

Now, each event $i$ is characterized by:
- $A_i \in \{0,1\}$: outcome of method A
- $B_i \in \{0,1\}$: outcome of method B
- $w_i > 0$: event weight

The weighted efficiencies are defined as:

$$
\hat e_A^{(w)} = \frac{\sum_i w_i A_i}{\sum_i w_i},
\quad
\hat e_B^{(w)} = \frac{\sum_i w_i B_i}{\sum_i w_i}
$$

The quantity of interest remains the **difference** $\Delta_w = \hat e_A^{(w)} - \hat e_B^{(w)}$

This can be written compactly as:

$$
\Delta_w = \frac{\sum_i w_i (A_i - B_i)}{\sum_i w_i}
$$

As in the unweighted case, only **disagreement events** ($A_i \neq B_i$) contribute to the difference.

---

### Frequentist Treatment (Weighted)

From a frequentist perspective, $\Delta_w$ is treated as a sample estimator constructed from independent events with fixed weights.

Define per-event contributions:

$$
x_i = w_i (A_i - B_i)
$$

Then:

$$
\widehat{\Delta}_w = \frac{\sum_i x_i}{\sum_i w_i}
$$

An approximate standard error, valid under standard large-sample assumptions, is:

$$
\sigma_w
= \frac{\sqrt{\sum_i x_i^2}}{\sum_i w_i}
$$

Key properties:
- Events where $A_i = B_i$ do not contribute to the uncertainty
- Larger weights increase the uncertainty through $x_i^2$
- The result reduces to the unweighted formula when all $w_i = 1$

This provides a closed-form frequentist uncertainty estimate without requiring toy Monte Carlo.

---

### Bayesian Treatment (Weighted)

For weighted events, the Dirichlet–multinomial conjugate model used in the unweighted case no longer applies, since weighted sums are not multinomial counts.

Instead, a **Bayesian bootstrap** approach is used:

- The empirical distribution of observed events is treated as uncertain
- A Dirichlet prior is placed on the probability mass assigned to each observed event
- Posterior samples are generated by resampling event weights via a Dirichlet distribution

For each posterior draw $\boldsymbol{\pi}$:

$$
\Delta_w(\boldsymbol{\pi})
= \frac{\sum_i \pi_i w_i (A_i - B_i)}{\sum_i \pi_i w_i}
$$

Repeating this procedure yields posterior samples of $\Delta_w$, from which one can compute:
- posterior mean and standard deviation
- credible intervals
- posterior probabilities such as $P(\Delta_w > 0)$

---

### Relationship Between Approaches

For sufficiently large effective sample size:
- The Bayesian posterior for $\Delta_w$ becomes approximately Gaussian
- The posterior mean approaches the frequentist estimator
- The posterior standard deviation matches the frequentist standard error

Thus, both approaches encode the same information:
- the frequentist method emphasizes sampling variability
- the Bayesian method provides direct probability statements

The choice between them depends on interpretational preference rather than statistical correctness.

---

### Summary of the Weighted Extension

- The disagreement-based structure of the problem is preserved
- Weights modify the contribution and uncertainty through squared-weight effects
- Frequentist inference admits a simple closed-form estimator
- Bayesian inference is naturally handled via the Bayesian bootstrap
- No independence or multinomial assumptions are violated

This weighted extension allows the framework to be applied directly to real-world problems where event contributions are heterogeneous.

--

## 7. Broader Relevance

Although motivated by efficiency comparisons in physics, such as trigger efficiencies, this framework applies directly to:

- Model replacement and A/B testing
- Risk and credit decision systems
- Trading strategy comparison
- Funnel and conversion optimization
- Any setting with paired binary decisions on a shared population

In all such cases, the disagreement-based uncertainty correctly captures the **true impact** of switching from one approach to another.

---

## 8. Project Goals

The goals of this project are:
1. Provide a clear statistical derivation for comparing correlated efficiencies
2. Demonstrate the failure of naive binomial uncertainty estimates
3. Offer an interpretable, disagreement-based metric for impact assessment
4. Build a foundation for applications beyond physics, including market-relevant use cases

---

## 9. Next Steps

This repository has completed the following:
- Toy Monte Carlo studies comparing naive and correct uncertainties
- Visualization of overlap vs uncertainty
- Bayesian interpretation of the efficiency difference using a Dirichlet–multinomial model ([start_Bayes.ipynb](start_Bayes.ipynb))
- Extension to weighted events and examples are shown in ([test_dataset.ipynb](test_dataset.ipynb))

Possible future extensions include:
- Application of the framework to business and finance case studies (e.g. A/B testing with shared populations)
- Extension to non-binary decisions

---

## 10. Summary

Comparing efficiencies without accounting for correlation is statistically incorrect and practically misleading.  
By focusing on disagreement rates rather than headline proportions, this framework provides a robust and interpretable method to assess true differences between competing approaches.

It is less glamorous than naive error bars, but statistically correct.