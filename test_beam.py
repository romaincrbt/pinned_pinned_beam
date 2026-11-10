import numpy as np

import beam

# Géométrie/matériau de l'énoncé (aluminium)
L, b, h, rho, E = 1.2, 0.04, 0.008, 2700.0, 68e9


def test_pinned_pinned_matches_analytic():
    _, nat_freq, _ = beam.natural_frequencies(
        L, b, h, rho, E, "pinned", "pinned", n_modes=4)
    m_l, _, EJ = beam.section_properties(b, h, rho, E)
    n = np.arange(1, 5)
    expected = (n * np.pi / L) ** 2 * np.sqrt(EJ / m_l) / (2 * np.pi)
    assert np.allclose(nat_freq, expected, rtol=1e-6)


def test_pinned_pinned_mode_shapes_are_sines():
    nat_puls, _, _ = beam.natural_frequencies(
        L, b, h, rho, E, "pinned", "pinned", n_modes=4)
    x, shapes = beam.mode_shapes(L, b, h, rho, E, "pinned", "pinned", nat_puls)
    for i in range(4):
        expected = np.sin((i + 1) * np.pi * x / L)
        expected /= np.max(np.abs(expected))
        assert np.allclose(np.abs(shapes[i]), np.abs(expected), atol=1e-3)


def test_cantilever_matches_cos_cosh_minus_one():
    _, nat_freq, _ = beam.natural_frequencies(
        L, b, h, rho, E, "clamped", "free", n_modes=4)
    m_l, _, EJ = beam.section_properties(b, h, rho, E)
    beta_L = np.array([1.875104, 4.694091, 7.854757, 10.995541])
    expected = beta_L**2 / L**2 * np.sqrt(EJ / m_l) / (2 * np.pi)
    assert np.allclose(nat_freq, expected, rtol=1e-4)


def test_frf_peaks_at_natural_frequencies():
    nat_puls, _, _ = beam.natural_frequencies(
        L, b, h, rho, E, "pinned", "pinned", n_modes=4)
    x, shapes = beam.mode_shapes(L, b, h, rho, E, "pinned", "pinned", nat_puls)
    m_l, _, _ = beam.section_properties(b, h, rho, E)
    w = np.linspace(0.1, nat_puls[-1] * 1.2, 20000)
    ksi = 0.01 * np.ones(4)
    G = beam.frf(x, shapes, nat_puls, m_l, x_force=0.3 * L, x_sensors=[0.7 * L],
                 ksi=ksi, w_sample=w)
    mag = np.abs(G[0])
    # chaque fréquence propre doit correspondre à un pic local de |G|
    for wp in nat_puls:
        k = np.argmin(np.abs(w - wp))
        assert mag[k] >= mag[max(k - 50, 0)] and mag[k] >= mag[min(k + 50, len(w) - 1)]
