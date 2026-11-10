"""Analyse modale et FRF d'une poutre Euler-Bernoulli.

Reprend l'analyse du notebook fourni : recherche des racines de det(H(w)) = 0
par balayage + brentq, déformées modales par vecteur propre nul de H, et FRF
par superposition modale avec amortissement visqueux.

La poutre est modélisée par y(x) = A cos(gx) + B sin(gx) + C cosh(gx) + D sinh(gx)
avec g = (m_l w^2 / EJ)^(1/4). Chaque condition aux limites fournit deux lignes
dans la matrice 4x4 H(w) ; les fréquences propres annulent det(H).
"""

import numpy as np
from scipy.optimize import brentq

# (ligne à x=0, ligne à x=L) pour chaque type d'appui, dans la base [A, B, C, D]
# lignes : y, theta/g, -y''/g^2 (moment), -y'''/g^3 (effort tranchant)
_BC_ROWS = {
    "pinned": (("y", "M"), ("y", "M")),
    "clamped": (("y", "theta"), ("y", "theta")),
    "free": (("M", "V"), ("M", "V")),
}

BC_LABELS = {
    ("pinned", "pinned"): "Articulée-Articulée",
    ("clamped", "clamped"): "Encastrée-Encastrée",
    ("clamped", "free"): "Encastrée-Libre (console)",
    ("free", "free"): "Libre-Libre",
    ("clamped", "pinned"): "Encastrée-Articulée",
    ("pinned", "free"): "Articulée-Libre",
}

_MATERIALS = {
    "Aluminium (E=68 GPa, rho=2700)": (68e9, 2700.0),
    "Acier (E=210 GPa, rho=7850)": (210e9, 7850.0),
    "Titane (E=110 GPa, rho=4500)": (110e9, 4500.0),
    "Cuivre (E=120 GPa, rho=8960)": (120e9, 8960.0),
    "Laiton (E=100 GPa, rho=8500)": (100e9, 8500.0),
    "Personnalisé": None,
}


def materials():
    return dict(_MATERIALS)


def section_properties(b, h, rho, E):
    """Masse linéique, inertie de flexion et rigidité EJ."""
    m_l = rho * b * h
    J = b * h**3 / 12.0
    return m_l, J, E * J


def gamma(w, m_l, EJ):
    return (m_l * w**2 / EJ) ** 0.25


def _row(kind, gL, at_end):
    c, s, ch, sh = np.cos(gL), np.sin(gL), np.cosh(gL), np.sinh(gL)
    if at_end == 0:
        table = {
            "y": [1.0, 0.0, 1.0, 0.0],
            "theta": [0.0, 1.0, 0.0, 1.0],
            "M": [1.0, 0.0, -1.0, 0.0],
            "V": [0.0, 1.0, 0.0, -1.0],
        }
    else:
        table = {
            "y": [c, s, ch, sh],
            "theta": [-s, c, sh, ch],
            "M": [c, s, -ch, -sh],
            "V": [-s, c, -sh, -ch],
        }
    return np.array(table[kind], dtype=float)


def H_matrix(w, L, m_l, EJ, bc_left, bc_right):
    gL = gamma(w, m_l, EJ) * L
    rows = []
    for kind in _BC_ROWS[bc_left][0]:
        rows.append(_row(kind, gL, 0))
    for kind in _BC_ROWS[bc_right][1]:
        rows.append(_row(kind, gL, L))
    return np.array(rows)


def _omega_estimate(n_modes, L, m_l, EJ):
    """Borne supérieure de pulsation couvrant au moins n_modes modes."""
    return ((n_modes + 2) * np.pi / L) ** 2 * np.sqrt(EJ / m_l)


def natural_frequencies(L, b, h, rho, E, bc_left, bc_right, n_modes=4,
                        n_samples=20000):
    """Pulsations et fréquences propres (Hz) via les changements de signe de det(H)."""
    m_l, _, EJ = section_properties(b, h, rho, E)

    def detH(w):
        return np.linalg.det(H_matrix(w, L, m_l, EJ, bc_left, bc_right))

    w_max = _omega_estimate(n_modes, L, m_l, EJ)
    w_sample = np.linspace(1e-6, w_max, n_samples)
    det_val = np.array([detH(w) for w in w_sample])
    idx = np.where(det_val[:-1] * det_val[1:] < 0)[0]
    nat_puls = np.array([brentq(detH, w_sample[k], w_sample[k + 1]) for k in idx])
    nat_puls = nat_puls[:n_modes]
    return nat_puls, nat_puls / (2.0 * np.pi), w_sample


def mode_shapes(L, b, h, rho, E, bc_left, bc_right, nat_puls, n_points=500):
    """Déformées modales normalisées (max |phi| = 1) sur x_grid."""
    m_l, _, EJ = section_properties(b, h, rho, E)
    x_grid = np.linspace(0.0, L, n_points)
    shapes = []
    for w in nat_puls:
        g = gamma(w, m_l, EJ)
        _, _, vh = np.linalg.svd(H_matrix(w, L, m_l, EJ, bc_left, bc_right))
        z = vh[-1]
        phi = (z[0] * np.cos(g * x_grid) + z[1] * np.sin(g * x_grid)
               + z[2] * np.cosh(g * x_grid) + z[3] * np.sinh(g * x_grid))
        shapes.append(phi / np.max(np.abs(phi)))
    return x_grid, np.array(shapes)


def frf(x_grid, shapes, nat_puls, m_l, x_force, x_sensors, ksi, w_sample):
    """FRF G(x_j, x_k, w) par superposition modale.

    G = sum_i Phi_i(x_j) Phi_i(x_k) / (m_i * (w_i^2 - w^2 + 2j ksi w_i w))
    avec m_i = ∫ m_l Phi_i^2 dx (invariant par normalisation de Phi_i).
    Retourne un tableau complexe (n_sensors, n_frequences).
    """
    x_sensors = np.atleast_1d(np.asarray(x_sensors, dtype=float))
    n_modes = len(nat_puls)
    modal_mass = np.array([
        np.trapezoid(m_l * shapes[i] ** 2, x_grid) for i in range(n_modes)
    ])
    phi_j = np.array([np.interp(x_sensors, x_grid, shapes[i]) for i in range(n_modes)])
    phi_k = np.array([np.interp(x_force, x_grid, shapes[i]) for i in range(n_modes)])

    G = np.zeros((len(x_sensors), len(w_sample)), dtype=complex)
    for i in range(n_modes):
        num = phi_j[i][:, None] * phi_k[i]
        den = (-w_sample**2 + 2j * ksi[i] * nat_puls[i] * w_sample
               + nat_puls[i] ** 2)
        G += num / (modal_mass[i] * den[None, :])
    return G
