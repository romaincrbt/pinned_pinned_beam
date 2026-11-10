"""Web app de modélisation et d'analyse vibratoire d'une poutre Euler-Bernoulli.

Lancer avec : streamlit run app.py
"""

import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import beam

st.set_page_config(page_title="Poutre Euler-Bernoulli", layout="wide")
st.title("Analyse vibratoire d'une poutre (Euler-Bernoulli)")
st.caption(
    "Fréquences propres, déformées modales et FRF par superposition modale, "
    "comme dans l'analyse de référence (racines de det(H(w)) = 0)."
)

with st.sidebar:
    st.header("Matériau")
    mat_name = st.selectbox("Preset matériau", list(beam.materials().keys()))
    preset = beam.materials()[mat_name]
    if preset is None:
        E = st.number_input("Module de Young E [Pa]", value=68e9, format="%.3e")
        rho = st.number_input("Masse volumique rho [kg/m^3]", value=2700.0)
    else:
        E, rho = preset
        st.write(f"E = {E:.3e} Pa, rho = {rho:.0f} kg/m³")

    st.header("Géométrie de la section")
    L = st.number_input("Longueur L [m]", value=1.2, min_value=0.05, step=0.05)
    b = st.number_input("Largeur b [m]", value=0.04, min_value=1e-4, format="%.4f")
    h = st.number_input("Hauteur h [m]", value=0.008, min_value=1e-4, format="%.4f")

    st.header("Conditions aux limites")
    bc_left = st.selectbox(
        "Appui à gauche (x = 0)",
        ["pinned", "clamped", "free"],
        format_func=lambda k: {"pinned": "Articulée", "clamped": "Encastrée",
                               "free": "Libre"}[k],
    )
    bc_right = st.selectbox(
        "Appui à droite (x = L)",
        ["pinned", "clamped", "free"],
        format_func=lambda k: {"pinned": "Articulée", "clamped": "Encastrée",
                               "free": "Libre"}[k],
    )

    st.header("Analyse")
    n_modes = st.slider("Nombre de modes", 1, 10, 4)
    ksi = st.slider("Amortissement modal ksi", 0.0, 0.1, 0.01, format="%.3f")

    st.header("FRF")
    x_force = st.slider("Position de la force x_k [m]", 0.0, float(L), float(L))
    default_sensors = [round(L * f, 3) for f in (1 / 6, 1 / 3, 1 / 2, 2 / 3, 5 / 6, 1.0)]
    x_sensors = st.multiselect(
        "Positions des capteurs x_j [m]",
        options=[round(L * i / 100, 4) for i in range(101)],
        default=[s for s in default_sensors if s <= L],
    )

m_l, J, EJ = beam.section_properties(b, h, rho, E)

with st.expander("Grandeurs dérivées", expanded=False):
    st.write(f"Masse linéique m_l = {m_l:.4f} kg/m")
    st.write(f"Inertie de flexion J = {J:.4e} m^4")
    st.write(f"Rigidité EJ = {EJ:.4f} N·m²")

nat_puls, nat_freq, w_sample = beam.natural_frequencies(
    L, b, h, rho, E, bc_left, bc_right, n_modes=n_modes
)
x_grid, shapes = beam.mode_shapes(
    L, b, h, rho, E, bc_left, bc_right, nat_puls
)

bc_label = beam.BC_LABELS.get((bc_left, bc_right), f"{bc_left}-{bc_right}")
st.subheader(f"Poutre {bc_label.lower()} — {len(nat_freq)} premières fréquences propres")

freq_df = pd.DataFrame({
    "Mode": np.arange(1, len(nat_freq) + 1),
    "Pulsation w_n [rad/s]": np.round(nat_puls, 3),
    "Fréquence f_n [Hz]": np.round(nat_freq, 4),
})
st.dataframe(freq_df, use_container_width=True)
st.download_button(
    "Télécharger les fréquences (CSV)",
    freq_df.to_csv(index=False).encode(),
    file_name="frequences_propres.csv",
)

st.subheader("Déformées modales")
fig_modes, ax = plt.subplots(figsize=(9, 4.5))
for i in range(len(nat_puls)):
    ax.plot(x_grid, shapes[i], lw=1.8,
            label=f"Mode {i + 1} : f = {nat_freq[i]:.2f} Hz")
ax.axhline(0, ls="--", color="k")
ax.set_xlabel("Position x [m]")
ax.set_ylabel("Déplacement normalisé")
ax.set_title(f"Déformées modales — {bc_label}")
ax.legend(loc="best")
ax.grid(True)
st.pyplot(fig_modes)

if x_sensors:
    w_max = st.slider(
        "Pulsation max pour la FRF [rad/s]",
        min_value=float(np.ceil(nat_puls[-1] * 0.5)),
        max_value=float(np.ceil(nat_puls[-1] * 2.5)),
        value=float(np.ceil(nat_puls[-1] * 1.5)),
    )
    w_frf = np.linspace(0.1, w_max, 4000)
    ksi_vec = ksi * np.ones(len(nat_puls))
    G = beam.frf(x_grid, shapes, nat_puls, m_l, x_force, x_sensors, ksi_vec, w_frf)

    st.subheader(f"FRF — force en x_k = {x_force:.3f} m, amortissement {ksi:.1%}")
    fig_frf, (ax_mag, ax_phase) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for row, xj in enumerate(x_sensors):
        ax_mag.semilogy(w_frf, np.abs(G[row, :]), lw=1.2,
                        label=f"x_j = {xj:.3f} m")
        ax_phase.plot(w_frf, np.degrees(np.unwrap(np.angle(G[row, :]))), lw=1.2,
                      label=f"x_j = {xj:.3f} m")
    for fn in nat_freq:
        ax_mag.axvline(2 * np.pi * fn, ls=":", color="gray", lw=0.8)
    ax_mag.set_ylabel(r"$|G_{jk}|$ [m/N]")
    ax_mag.set_title("FRF — amplitude (log) et phase")
    ax_mag.legend(loc="best")
    ax_mag.grid(True)
    ax_phase.set_xlabel("Pulsation w [rad/s]")
    ax_phase.set_ylabel("Phase [°]")
    ax_phase.grid(True)
    st.pyplot(fig_frf)

    frf_df = pd.DataFrame({"w [rad/s]": w_frf})
    for row, xj in enumerate(x_sensors):
        frf_df[f"|G| x_j={xj:.3f} [m/N]"] = np.abs(G[row, :])
        frf_df[f"phase x_j={xj:.3f} [deg]"] = np.degrees(
            np.unwrap(np.angle(G[row, :])))
    st.download_button(
        "Télécharger la FRF (CSV)",
        frf_df.to_csv(index=False).encode(),
        file_name="frf.csv",
    )
else:
    st.info("Sélectionnez au moins un capteur dans la barre latérale pour tracer la FRF.")
