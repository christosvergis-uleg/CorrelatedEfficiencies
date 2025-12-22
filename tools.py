import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_rect_overlap(l, p11, p10, p01, p00, title="Exact area partition"):
    """
    Function to plot rectangular area partitioning of the events A, B in a box.
    
    :param l: Length of the sides of the outer box.
    :param p11: Probability of A and B both occurring.
    :param p10: Probability of A occurring but B not occurring.
    :param p01: Probability of B occurring but A not occurring.
    :param p00: Probability of neither A nor B occurring.
    :param title: Title for the plot.
    """
    
    ps = np.array([p11, p10, p01, p00], dtype=float)
    if np.any(ps < 0):
        raise ValueError("Probabilities must be non-negative.")
    if not np.isclose(ps.sum(), 1.0):
        raise ValueError(f"Probabilities must sum to 1. Got {ps.sum():.6f}")

    effA = p11 + p10
    effB = p11 + p01
    A_box = l**2

    # handle degenerate cases cleanly
    eps = 1e-12
    wL = effA * l
    wR = (1 - effA) * l

    fig, ax = plt.subplots(figsize=(6.5, 6.0))

    # draw outer box
    ax.add_patch(Rectangle((0, 0), l, l, fill=False, linewidth=2))

    # LEFT column: A region
    if wL > eps:
        h11 = (p11 * A_box) / wL
        h10 = (p10 * A_box) / wL

        # bottom-left: A & B (p11)
        ax.add_patch(Rectangle((0, 0), wL, h11, alpha=0.35, color="purple"))
        ax.text(wL/2, h11/2, r"$A\cap B$"+"\n"+rf"$p_{{11}}={p11:.2f}$",
                ha="center", va="center", fontsize=11)
        # top-left: A only (p10)
        ax.add_patch(Rectangle((0, h11), wL, h10, alpha=0.20, color="blue"))
        ax.text(wL/2, h11 + h10/2, r"$A\ \mathrm{only}$"+"\n"+rf"$p_{{10}}={p10:.2f}$",
                ha="center", va="center", fontsize=11)

    else:
        # effA = 0 => no left column
        h11 = h10 = 0.0

    # RIGHT column: not A region
    if wR > eps:
        h01 = (p01 * A_box) / wR
        h00 = (p00 * A_box) / wR

        # bottom-right: B only (p01)
        ax.add_patch(Rectangle((wL, 0), wR, h01, alpha=0.35, color="red"))
        ax.text(wL + wR/2, h01/2, r"$B\ \mathrm{only}$"+"\n"+rf"$p_{{01}}={p01:.2f}$",
                ha="center", va="center", fontsize=11)
        # top-right: neither (p00)
        ax.add_patch(Rectangle((wL, h01), wR, h00, alpha=0.10, color="white"))
        ax.text(wL + wR/2, h01 + h00/2, r"$\mathrm{neither}$"+"\n"+rf"$p_{{00}}={p00:.2f}$",
                ha="center", va="center", fontsize=11)
    else:
        # effA = 1 => no right column
        h01 = h00 = 0.0

    # annotations
    ax.set_title(title)
    ax.text(l/2, l + 0.25,
            #rf"$l={l}$, $A_{{box}}={A_box}$"+"\n"+
            rf"$\hat e_A=p_{{11}}+p_{{10}}={effA:.2f}$,"+"\n"+
            rf"$\hat e_B=p_{{11}}+p_{{01}}={effB:.2f}$",
            ha="center", va="bottom", fontsize=10)

    ax.set_aspect("equal")
    ax.set_xlim(-0.5, l + 0.5)
    ax.set_ylim(-0.5, l + 0.9)
    ax.axis("off")
    plt.show()

def run_toys(Nevents, Ntoys, probabilities, rng):
    """
    Run toy Monte Carlo for correlated efficiencies.

    Returns
    -------
    deltas : array
    sigma_corrs : array
    sigma_naives : array
    eff_A : array
    eff_B : array
    """

    counts = rng.multinomial(Nevents, probabilities, size=Ntoys) 
    n11 = counts[:, 0]
    n10 = counts[:, 1]
    n01 = counts[:, 2]

    eff_A = (n11 + n10) / Nevents
    eff_B = (n11 + n01) / Nevents
    deltas = eff_A - eff_B

    sigma_corrs = np.sqrt(n10 + n01) / Nevents
    sigma_naives = np.sqrt(
        ( eff_A * (1 - eff_A)  + eff_B * (1 - eff_B) ) / Nevents
    )

    return deltas, sigma_corrs, sigma_naives, eff_A, eff_B