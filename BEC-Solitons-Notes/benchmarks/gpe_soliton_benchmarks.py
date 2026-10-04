"""Reproducible dimensionless 1D GPE benchmarks for the 5 Oct meeting.

Units: hbar=m=1; i psi_t = -(1/2) psi_xx + g |psi|^2 psi.
The bright simulation uses g=-1, N=2 and a periodic box large enough that
the exponentially small tails do not interact with the boundary on [0, 3].
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["svg.fonttype"] = "none"


def sech(x):
    return 1.0 / np.cosh(x)


def energy(psi, k, dx, g):
    dpsi = np.fft.ifft(1j * k * np.fft.fft(psi))
    return dx * np.sum(0.5 * np.abs(dpsi) ** 2 + 0.5 * g * np.abs(psi) ** 4).real


def propagate_bright():
    nx = 2048
    length = 60.0
    dx = length / nx
    x = -length / 2 + dx * np.arange(nx)
    k = 2 * np.pi * np.fft.fftfreq(nx, d=dx)
    v = 0.7
    g = -1.0
    t_final = 3.0
    dt = 0.002
    nsteps = round(t_final / dt)
    psi = sech(x) * np.exp(1j * v * x)
    density_initial = np.abs(psi) ** 2
    initial_norm = dx * np.sum(density_initial)
    initial_energy = energy(psi, k, dx, g)
    kinetic = np.exp(-0.5j * k**2 * dt)

    for _ in range(nsteps):
        psi *= np.exp(-0.5j * g * np.abs(psi) ** 2 * dt)
        psi = np.fft.ifft(kinetic * np.fft.fft(psi))
        psi *= np.exp(-0.5j * g * np.abs(psi) ** 2 * dt)

    density_final = np.abs(psi) ** 2
    predicted = sech(x - v * t_final) ** 2
    final_norm = dx * np.sum(density_final)
    final_energy = energy(psi, k, dx, g)
    results = {
        "N_initial": initial_norm,
        "N_final": final_norm,
        "relative_N_drift": abs(final_norm - initial_norm) / initial_norm,
        "E_initial": initial_energy,
        "E_final": final_energy,
        "relative_E_drift": abs(final_energy - initial_energy) / abs(initial_energy),
        "max_density_error": np.max(np.abs(density_final - predicted)),
        "peak_position": x[np.argmax(density_final)],
        "expected_peak_position": v * t_final,
    }
    return x, density_initial, density_final, predicted, results


def make_figure(output):
    x, density_initial, density_final, predicted, results = propagate_bright()
    xp = x[::8]  # display sampling only; the solver uses the full grid
    fig, axes = plt.subplots(2, 2, figsize=(10, 7.4), constrained_layout=True)
    ax = axes[0, 0]
    for G in [0.5, 1.0, 2.0]:
        N = 2.0
        L = 2 / (G * N)
        ax.plot(xp, N / (2 * L) * sech(xp / L) ** 2, label=fr"$|g_{{1D}}|={G:g}$")
    ax.set(xlim=(-6, 6), xlabel=r"$x$", ylabel=r"$n(x)$", title="Bright: attraction narrows the peak")
    ax.legend(fontsize=9)

    ax = axes[0, 1]
    for beta in [0.0, 0.5, 0.8]:
        gamma = np.sqrt(1 - beta**2)
        density = 1 - gamma**2 * sech(gamma * xp) ** 2
        ax.plot(xp, density, label=fr"$v/c={beta:g}$")
    ax.set(xlim=(-6, 6), ylim=(-0.03, 1.06), xlabel=r"$x-vt$", ylabel=r"$n(x)/n_0$", title="Dark to grey: velocity fills the notch")
    ax.legend(fontsize=9)

    ax = axes[1, 0]
    indices = np.flatnonzero((x > -6) & (x < 8))[::4]
    ax.plot(x[indices], density_initial[indices], label=r"$t=0$")
    ax.plot(x[indices], density_final[indices], label=r"split-step, $t=3$")
    ax.plot(x[indices], predicted[indices], "--", label=r"exact, $t=3$")
    ax.set(xlabel=r"$x$", ylabel=r"$n(x,t)$", title="Moving bright soliton: numerical check")
    ax.legend(fontsize=9)

    ax = axes[1, 1]
    k = np.linspace(0, 4, 250)
    eps = k**2 / 2
    ax.plot(k, np.sqrt(eps * (eps + 2)), label=r"Bogoliubov $\omega(k)$")
    ax.plot(k, k, "--", label=r"sound $ck$, $c=1$")
    ax.plot(k, eps, ":", label=r"free $k^2/2$")
    ax.set(xlabel=r"$k$", ylabel=r"$\omega$", title="Repulsive condensate: sound to particles")
    ax.legend(fontsize=9)

    fig.suptitle(r"BEC soliton benchmarks  |  dimensionless $\hbar=m=1$", fontsize=14)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=170)
    plt.close(fig)
    return results


def make_source_branches_figure(output):
    """Two source-specific checks: Bethe binding and HCB coherent-state density."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
    n = np.arange(2, 31)
    axes[0].plot(n, 1 - 1 / n**2, "o-", ms=3.5)
    axes[0].axhline(1, color="0.45", ls="--", lw=1)
    axes[0].set(
        xlabel=r"particle number $N$",
        ylabel=r"$E_{\rm Bethe}/E_{\rm GP}$",
        ylim=(0.72, 1.02),
        title="Söhn: exact binding / leading GP binding",
    )
    rho = np.linspace(0, 1, 250)
    axes[1].plot(rho, rho * (1 - rho), label=r"$\rho_s=\rho(1-\rho)$")
    axes[1].plot(rho, rho, "--", label=r"total filling $\rho$")
    axes[1].set(
        xlabel=r"total filling $\rho$",
        ylabel=r"density per site",
        xlim=(0, 1),
        ylim=(0, 1.02),
        title="Balakrishnan–Satija: HCB coherent-state result",
    )
    axes[1].legend(fontsize=9)
    fig.savefig(output, format="svg")
    fig.savefig(output.with_suffix(".png"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    output = Path(__file__).with_name("gpe_soliton_benchmarks.svg")
    for name, value in make_figure(output).items():
        print(f"{name}: {value:.10g}")
    print(f"figure: {output}")
    branches = output.with_name("source_branches.svg")
    make_source_branches_figure(branches)
    print(f"figure: {branches}")
