#!/usr/bin/env python3
"""
Vibrateam - Analyse vibratoire des poutres
Application complète pour l'analyse modale et FRF des poutres
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import streamlit as st
from scipy import signal

# Configuration de la page
st.set_page_config(
    page_title="Vibrateam - Analyse Vibratoire des Poutres",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stSelectbox, .stNumberInput, .stSlider {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# CLASSE PRINCIPALE POUR L'ANALYSE DES POUTRES
# ============================================================================

class PoutreVibratoire:
    """
    Classe pour l'analyse vibratoire des poutres selon la théorie d'Euler-Bernoulli
    """
    
    def __init__(self, L=1.0, E=210e9, rho=7800, I=1e-8, A=1e-4):
        """
        Initialisation des propriétés de la poutre
        
        Paramètres:
        -----------
        L : float - Longueur de la poutre (m)
        E : float - Module de Young (Pa)
        rho : float - Masse volumique (kg/m³)
        I : float - Moment d'inertie (m⁴)
        A : float - Aire de la section (m²)
        """
        self.L = L
        self.E = E  # Module de Young (acier par défaut)
        self.rho = rho  # Masse volumique (acier par défaut)
        self.I = I  # Moment d'inertie
        self.A = A  # Aire de la section
        
        # Calcul des propriétés dérivées
        self.masse_lineique = rho * A  # kg/m
        self.rigidite_flexion = E * I  # N·m²
        
    def calculer_beta_n(self, n, condition_bord):
        """
        Calcule les valeurs de beta_n pour différentes conditions aux limites
        
        Paramètres:
        -----------
        n : int - Numéro du mode
        condition_bord : str - Type de condition aux limites
        
        Retourne:
        ---------
        beta_n : float - Valeur de beta pour le mode n
        """
        if condition_bord == "Encastre-Encastre":
            # Pour poutre encastrée-encastrée
            if n == 1:
                return 4.730040744862704
            elif n == 2:
                return 7.853204624095737
            elif n == 3:
                return 10.99560783800167
            elif n == 4:
                return 14.13716549125746
            elif n == 5:
                return 17.27875965739948
            elif n == 6:
                return 20.42035224533365
            elif n == 7:
                return 23.56194490192345
            elif n == 8:
                return 26.70353755551367
            elif n == 9:
                return 29.84513020910345
            elif n == 10:
                return 32.98672286269324
            else:
                # Approximation pour n > 10
                return (2 * n + 1) * np.pi / 2
                
        elif condition_bord == "Encastre-Libre":
            # Pour poutre encastrée-libre (console)
            if n == 1:
                return 1.875104068711961
            elif n == 2:
                return 4.694068489942059
            elif n == 3:
                return 7.854757434837964
            elif n == 4:
                return 10.99554017203124
            elif n == 5:
                return 14.13716839254428
            elif n == 6:
                return 17.27875959474386
            elif n == 7:
                return 20.42035224533364
            elif n == 8:
                return 23.56194490192345
            elif n == 9:
                return 26.70353755551367
            elif n == 10:
                return 29.84513020910345
            else:
                # Approximation pour n > 10
                return (2 * n - 1) * np.pi / 2
                
        elif condition_bord == "Libre-Libre":
            # Pour poutre libre-libre
            if n == 1:
                return 0.0  # Mode rigide - translation
            elif n == 2:
                return 0.0  # Mode rigide - rotation
            elif n == 3:
                return 4.730040744862704
            elif n == 4:
                return 7.853204624095737
            elif n == 5:
                return 10.99560783800167
            elif n == 6:
                return 14.13716549125746
            elif n == 7:
                return 17.27875965739948
            elif n == 8:
                return 20.42035224533365
            elif n == 9:
                return 23.56194490192345
            elif n == 10:
                return 26.70353755551367
            else:
                return n * np.pi
                
        elif condition_bord == "Articule-Articule":
            # Pour poutre articulée-articulée (simplement supportée)
            return n * np.pi
            
        elif condition_bord == "Encastre-Articule":
            # Pour poutre encastrée-articulée
            if n == 1:
                return 3.926602310881065
            elif n == 2:
                return 7.068583470577034
            elif n == 3:
                return 10.21017612416108
            elif n == 4:
                return 13.35176875420415
            elif n == 5:
                return 16.49336140586018
            elif n == 6:
                return 19.63495405751621
            elif n == 7:
                return 22.77654670917225
            elif n == 8:
                return 25.91813936082828
            elif n == 9:
                return 29.05973201248431
            elif n == 10:
                return 32.20132466414034
            else:
                # Approximation pour n > 10
                return (2 * n + 1) * np.pi / 2
        
        else:
            raise ValueError(f"Condition aux limites inconnue: {condition_bord}")
    
    def calculer_frequence_naturelle(self, n, condition_bord):
        """
        Calcule la fréquence naturelle du mode n
        
        Paramètres:
        -----------
        n : int - Numéro du mode
        condition_bord : str - Type de condition aux limites
        
        Retourne:
        ---------
        f_n : float - Fréquence naturelle en Hz
        """
        beta_n = self.calculer_beta_n(n, condition_bord)
        
        # Éviter la division par zéro pour les modes rigides
        if beta_n == 0:
            return 0.0
            
        # Formule : f_n = (beta_n^2 / (2*pi*L^2)) * sqrt(E*I/(rho*A))
        f_n = (beta_n ** 2) / (2 * np.pi * self.L ** 2) * np.sqrt(self.rigidite_flexion / self.masse_lineique)
        
        return f_n
    
    def calculer_deformee_modale(self, x, n, condition_bord):
        """
        Calcule la déformée modale pour le mode n à la position x
        
        Paramètres:
        -----------
        x : float ou array - Position(s) le long de la poutre (m)
        n : int - Numéro du mode
        condition_bord : str - Type de condition aux limites
        
        Retourne:
        ---------
        phi_n : array - Déformée modale normalisée
        """
        x = np.asarray(x)
        L = self.L
        beta_n = self.calculer_beta_n(n, condition_bord)
        
        if condition_bord == "Encastre-Encastre":
            # Déformée modale pour poutre encastrée-encastrée
            # phi_n(x) = cosh(beta_n*x/L) - cos(beta_n*x/L) - 
            #           (sinh(beta_n) - sin(beta_n))/(cosh(beta_n) - cos(beta_n)) * 
            #           (sinh(beta_n*x/L) - sin(beta_n*x/L))
            
            cosh_beta = np.cosh(beta_n)
            cos_beta = np.cos(beta_n)
            sinh_beta = np.sinh(beta_n)
            sin_beta = np.sin(beta_n)
            
            denominator = cosh_beta - cos_beta
            if abs(denominator) < 1e-10:
                ratio = 0
            else:
                ratio = (sinh_beta - sin_beta) / denominator
            
            phi_n = (np.cosh(beta_n * x / L) - np.cos(beta_n * x / L) - 
                    ratio * (np.sinh(beta_n * x / L) - np.sin(beta_n * x / L)))
            
        elif condition_bord == "Encastre-Libre":
            # Déformée modale pour poutre encastrée-libre
            # phi_n(x) = cosh(beta_n*x/L) - cos(beta_n*x/L) - 
            #           (cosh(beta_n) + cos(beta_n))/(sinh(beta_n) + sin(beta_n)) * 
            #           (sinh(beta_n*x/L) - sin(beta_n*x/L))
            
            cosh_beta = np.cosh(beta_n)
            cos_beta = np.cos(beta_n)
            sinh_beta = np.sinh(beta_n)
            sin_beta = np.sin(beta_n)
            
            denominator = sinh_beta + sin_beta
            if abs(denominator) < 1e-10:
                ratio = 0
            else:
                ratio = (cosh_beta + cos_beta) / denominator
            
            phi_n = (np.cosh(beta_n * x / L) - np.cos(beta_n * x / L) - 
                    ratio * (np.sinh(beta_n * x / L) - np.sin(beta_n * x / L)))
            
        elif condition_bord == "Libre-Libre":
            # Déformée modale pour poutre libre-libre
            if n == 1:  # Mode rigide - translation
                phi_n = np.ones_like(x)
            elif n == 2:  # Mode rigide - rotation
                phi_n = x / L - 0.5
            else:
                # Pour les modes flexibles (n >= 3)
                # Utiliser la même forme que encastré-encastré mais avec ajustement
                beta_n_encastre = self.calculer_beta_n(n-2, "Encastre-Encastre")
                
                cosh_beta = np.cosh(beta_n_encastre)
                cos_beta = np.cos(beta_n_encastre)
                sinh_beta = np.sinh(beta_n_encastre)
                sin_beta = np.sin(beta_n_encastre)
                
                denominator = cosh_beta - cos_beta
                if abs(denominator) < 1e-10:
                    ratio = 0
                else:
                    ratio = (sinh_beta - sin_beta) / denominator
                
                phi_n = (np.cosh(beta_n_encastre * x / L) - np.cos(beta_n_encastre * x / L) - 
                        ratio * (np.sinh(beta_n_encastre * x / L) - np.sin(beta_n_encastre * x / L)))
                        
        elif condition_bord == "Articule-Articule":
            # Déformée modale pour poutre articulée-articulée
            phi_n = np.sin(n * np.pi * x / L)
            
        elif condition_bord == "Encastre-Articule":
            # Déformée modale pour poutre encastrée-articulée
            # phi_n(x) = sin(beta_n*x/L) - (sin(beta_n)/sinh(beta_n)) * sinh(beta_n*x/L)
            
            sin_beta = np.sin(beta_n)
            sinh_beta = np.sinh(beta_n)
            
            if abs(sinh_beta) < 1e-10:
                ratio = 0
            else:
                ratio = sin_beta / sinh_beta
            
            phi_n = np.sin(beta_n * x / L) - ratio * np.sinh(beta_n * x / L)
        
        else:
            raise ValueError(f"Condition aux limites inconnue: {condition_bord}")
        
        # Normalisation pour que le maximum soit 1
        max_phi = np.max(np.abs(phi_n))
        if max_phi > 1e-10:
            phi_n = phi_n / max_phi
        
        return phi_n
    
    def calculer_FRF(self, x_force, x_mesure, omega, n_modes, condition_bord, damping_ratio=0.01):
        """
        Calcule la Fonction de Réponse en Fréquence (FRF) entre x_force et x_mesure
        
        Paramètres:
        -----------
        x_force : float - Position de l'application de la force (m)
        x_mesure : float - Position de mesure (m)
        omega : array - Tableau de fréquences angulaires (rad/s)
        n_modes : int - Nombre de modes à considérer
        condition_bord : str - Type de condition aux limites
        damping_ratio : float - Coefficient d'amortissement (default: 0.01)
        
        Retourne:
        ---------
        H : array - FRF complexe
        H_magnitude : array - Magnitude de la FRF
        contributions : list - Contributions de chaque mode
        """
        H = np.zeros_like(omega, dtype=complex)
        contributions = []
        
        for n in range(1, n_modes + 1):
            # Fréquence naturelle en rad/s
            f_n = self.calculer_frequence_naturelle(n, condition_bord)
            omega_n = 2 * np.pi * f_n
            
            # Éviter la division par zéro pour les modes rigides
            if omega_n < 1e-10:
                continue
            
            # Calcul des déformées modales
            phi_n_force = self.calculer_deformee_modale(x_force, n, condition_bord)
            phi_n_mesure = self.calculer_deformee_modale(x_mesure, n, condition_bord)
            
            # Masse généralisée
            # m_n = rho*A*L * integral(phi_n^2) dx
            # Pour simplifier, on utilise une approximation
            x_integral = np.linspace(0, self.L, 1000)
            phi_n_integral = self.calculer_deformee_modale(x_integral, n, condition_bord)
            integral_phi_sq = np.trapezoid(phi_n_integral**2, x_integral)
            m_n = self.masse_lineique * integral_phi_sq
            
            # Raideur généralisée
            # k_n = E*I * integral(phi_n'')^2 dx = (beta_n/L)^4 * E*I * integral(phi_n^2) dx
            # = omega_n^2 * m_n
            k_n = (omega_n ** 2) * m_n
            
            # Contribution du mode n
            numerator = phi_n_force * phi_n_mesure / m_n
            denominator = omega_n**2 - omega**2 + 2j * damping_ratio * omega_n * omega
            
            H_n = numerator / denominator
            H += H_n
            contributions.append(H_n)
        
        H_magnitude = np.abs(H)
        
        return H, H_magnitude, contributions


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_condition_bord_description(condition):
    """Retourne une description de la condition aux limites"""
    descriptions = {
        "Encastre-Encastre": "Poutre encastrée aux deux extrémités (fixée rigidement)",
        "Encastre-Libre": "Poutre encastrée à une extrémité, libre à l'autre (console)",
        "Libre-Libre": "Poutre libre aux deux extrémités (volante)",
        "Articule-Articule": "Poutre articulée aux deux extrémités (simplement supportée)",
        "Encastre-Articule": "Poutre encastrée à une extrémité, articulée à l'autre"
    }
    return descriptions.get(condition, "")


def get_condition_bord_emoji(condition):
    """Retourne un emoji pour la condition aux limites"""
    emojis = {
        "Encastre-Encastre": "🔒🔒",
        "Encastre-Libre": "🔒🚀",
        "Libre-Libre": "🚀🚀",
        "Articule-Articule": "🔗🔗",
        "Encastre-Articule": "🔒🔗"
    }
    return emojis.get(condition, "❓")


# ============================================================================
# INTERFACE STREAMLIT
# ============================================================================

def main():
    """Fonction principale de l'application"""
    
    # En-tête de l'application
    st.markdown('<div class="main-header">📊 Vibrateam - Analyse Vibratoire des Poutres</div>', unsafe_allow_html=True)
    
    # Introduction
    with st.expander("ℹ️ À propos de l'application", expanded=False):
        st.markdown("""
        Cette application permet d'analyser le comportement vibratoire des poutres selon la théorie d'Euler-Bernoulli.
        
        **Fonctionnalités :**
        - Sélection des conditions aux limites de la poutre
        - Calcul des fréquences naturelles et déformées modales
        - Visualisation des modes de vibration
        - Calcul et affichage des Fonctions de Réponse en Fréquence (FRF)
        - Analyse des contributions modales
        
        **Théorie :**
        L'application utilise l'équation différentielle des vibrations transversales des poutres :
        EI * d⁴w/dx⁴ + ρA * ∂²w/∂t² = 0
        
        Où w(x,t) est le déplacement transversal, E le module de Young, I le moment d'inertie,
        ρ la masse volumique, et A l'aire de la section.
        """)
    
    # Barre latérale pour les paramètres
    st.sidebar.title("⚙️ Paramètres de la poutre")
    
    # Paramètres matériels
    with st.sidebar.expander("📐 Propriétés géométriques", expanded=True):
        L = st.number_input("Longueur (m)", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
        
        col1, col2 = st.columns(2)
        with col1:
            largeur = st.number_input("Largeur (m)", value=0.05, min_value=0.01, max_value=1.0, step=0.01)
        with col2:
            hauteur = st.number_input("Hauteur (m)", value=0.02, min_value=0.01, max_value=1.0, step=0.01)
        
        # Calcul du moment d'inertie pour section rectangulaire
        I = largeur * hauteur**3 / 12
        A = largeur * hauteur
        
        st.info(f"Moment d'inertie: {I:.2e} m⁴\nAire: {A:.2e} m²")
    
    with st.sidebar.expander("🏗️ Propriétés matérielles", expanded=True):
        E = st.number_input("Module de Young (Pa)", value=210e9, min_value=1e9, max_value=1e12, 
                           step=1e9, format="%.2e")
        rho = st.number_input("Masse volumique (kg/m³)", value=7800, min_value=100, max_value=30000, 
                              step=100)
    
    # Condition aux limites
    st.sidebar.markdown("---")
    st.sidebar.title("🎯 Conditions aux limites")
    
    conditions_disponibles = [
        "Encastre-Encastre",
        "Encastre-Libre", 
        "Libre-Libre",
        "Articule-Articule",
        "Encastre-Articule"
    ]
    
    condition_bord = st.sidebar.selectbox(
        "Sélectionnez la condition aux limites",
        conditions_disponibles,
        format_func=lambda x: f"{get_condition_bord_emoji(x)} {x}"
    )
    
    # Afficher la description
    description = get_condition_bord_description(condition_bord)
    if description:
        st.sidebar.info(description)
    
    # Nombre de modes
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Approximation modale")
    n_modes = st.sidebar.slider("Nombre de modes à calculer", min_value=1, max_value=10, value=5)
    
    # Coefficient d'amortissement
    damping_ratio = st.sidebar.slider("Coefficient d'amortissement", min_value=0.001, max_value=0.1, 
                                       value=0.01, step=0.001, format="%.3f")
    
    # Création de l'objet poutre
    poutre = PoutreVibratoire(L=L, E=E, rho=rho, I=I, A=A)
    
    # ============================================================================
    # SECTION 1: FRÉQUENCES NATURELLES ET DÉFORMÉES MODALES
    # ============================================================================
    
    st.markdown('<div class="sub-header">🔊 Fréquences naturelles et déformées modales</div>', unsafe_allow_html=True)
    
    # Calcul des fréquences naturelles
    frequences = []
    for n in range(1, n_modes + 1):
        f_n = poutre.calculer_frequence_naturelle(n, condition_bord)
        frequences.append(f_n)
    
    # Affichage des fréquences dans un tableau
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Tableau des fréquences naturelles :**")
        freq_data = {"Mode": [f"Mode {n}" for n in range(1, n_modes + 1)],
                     "Fréquence (Hz)": [f"{f:.2f}" for f in frequences]}
        st.table(freq_data)
    
    with col2:
        # Métriques
        if frequences:
            st.metric("Première fréquence naturelle", f"{frequences[0]:.2f} Hz")
            if len(frequences) > 1:
                st.metric("Écart entre mode 1 et 2", f"{frequences[1] - frequences[0]:.2f} Hz")
    
    # Visualisation des déformées modales
    st.markdown("**Visualisation des déformées modales :**")
    
    # Options de visualisation
    col1, col2 = st.columns([3, 1])
    with col1:
        show_all_modes = st.checkbox("Afficher toutes les déformées sur un seul graphique", value=True)
    with col2:
        if not show_all_modes:
            mode_to_show = st.selectbox("Mode à afficher", range(1, n_modes + 1), key="mode_select")
    
    # Création du graphique
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    x_plot = np.linspace(0, L, 500)
    colors = plt.cm.viridis(np.linspace(0, 1, n_modes))
    
    if show_all_modes:
        # Afficher toutes les déformées sur un seul graphique
        for n in range(1, n_modes + 1):
            phi_n = poutre.calculer_deformee_modale(x_plot, n, condition_bord)
            # Déplacement vertical pour séparer les modes
            offset = (n - 1) * 2
            ax.plot(x_plot, phi_n + offset, color=colors[n-1], 
                   label=f'Mode {n} ({frequences[n-1]:.2f} Hz)', linewidth=2)
            
            # Ajouter une ligne horizontale pour la référence
            ax.axhline(offset, color='gray', linestyle='--', alpha=0.3)
        
        ax.set_ylim(-1, n_modes * 2)
        ax.set_yticks([(n - 1) * 2 + 1 for n in range(1, n_modes + 1)])
        ax.set_yticklabels([f'Mode {n}' for n in range(1, n_modes + 1)])
        ax.set_ylabel("Amplitude normalisée")
        
    else:
        # Afficher un seul mode
        phi_n = poutre.calculer_deformee_modale(x_plot, mode_to_show, condition_bord)
        ax.plot(x_plot, phi_n, color=colors[mode_to_show-1], 
               label=f'Mode {mode_to_show} ({frequences[mode_to_show-1]:.2f} Hz)', linewidth=3)
        ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
        ax.set_ylim(-1.2, 1.2)
        ax.set_ylabel("Amplitude normalisée")
    
    ax.set_xlabel("Position le long de la poutre (m)")
    ax.set_xlim(0, L)
    ax.set_title(f"Déformées modales - {condition_bord}", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    # Ajouter des informations sur les conditions aux limites
    if condition_bord == "Encastre-Encastre":
        ax.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
        ax.axvline(L, color='red', linestyle='-', linewidth=3, alpha=0.7)
    elif condition_bord == "Encastre-Libre":
        ax.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
        ax.axvline(L, color='green', linestyle='--', linewidth=2, alpha=0.7)
    elif condition_bord == "Libre-Libre":
        ax.axvline(0, color='green', linestyle='--', linewidth=2, alpha=0.7)
        ax.axvline(L, color='green', linestyle='--', linewidth=2, alpha=0.7)
    elif condition_bord == "Articule-Articule":
        ax.axvline(0, color='blue', linestyle=':', linewidth=2, alpha=0.7)
        ax.axvline(L, color='blue', linestyle=':', linewidth=2, alpha=0.7)
    elif condition_bord == "Encastre-Articule":
        ax.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
        ax.axvline(L, color='blue', linestyle=':', linewidth=2, alpha=0.7)
    
    # Ajouter une légende pour les conditions aux limites
    legend_elements = []
    if condition_bord == "Encastre-Encastre":
        legend_elements.append(Patch(facecolor='red', edgecolor='red', label='Encastrement', linewidth=2))
    elif condition_bord == "Encastre-Libre":
        legend_elements.append(Patch(facecolor='red', edgecolor='red', label='Encastrement', linewidth=2))
        legend_elements.append(Patch(facecolor='green', edgecolor='green', label='Libre', linestyle='--'))
    elif condition_bord == "Libre-Libre":
        legend_elements.append(Patch(facecolor='green', edgecolor='green', label='Libre', linestyle='--'))
    elif condition_bord == "Articule-Articule":
        legend_elements.append(Patch(facecolor='blue', edgecolor='blue', label='Articulation', linestyle=':'))
    elif condition_bord == "Encastre-Articule":
        legend_elements.append(Patch(facecolor='red', edgecolor='red', label='Encastrement', linewidth=2))
        legend_elements.append(Patch(facecolor='blue', edgecolor='blue', label='Articulation', linestyle=':'))
    
    if legend_elements:
        ax.legend(handles=legend_elements, loc='upper right', title="Conditions aux limites")
    
    st.pyplot(fig)
    plt.close(fig)
    
    # ============================================================================
    # SECTION 2: FONCTION DE RÉPONSE EN FRÉQUENCE (FRF)
    # ============================================================================
    
    st.markdown("---")
    st.markdown('<div class="sub-header">📈 Fonction de Réponse en Fréquence (FRF)</div>', unsafe_allow_html=True)
    
    # Sélection des points de force et de mesure
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Position de la force d'excitation :**")
        x_force = st.slider("Position x_force (m)", min_value=0.0, max_value=L, 
                           value=L/4, step=L/100, key="x_force")
        
    with col2:
        st.markdown("**Position de mesure :**")
        x_mesure = st.slider("Position x_mesure (m)", min_value=0.0, max_value=L, 
                            value=L/2, step=L/100, key="x_mesure")
    
    # Visualisation des positions sur la poutre
    st.markdown("**Schéma de la poutre :**")
    
    fig_schema, ax_schema = plt.subplots(1, 1, figsize=(10, 2))
    
    # Dessiner la poutre
    ax_schema.plot([0, L], [0, 0], 'k-', linewidth=8)
    
    # Ajouter les conditions aux limites
    if "Encastre" in condition_bord.split('-')[0]:
        ax_schema.plot(0, 0, 'rs', markersize=15, label='Encastrement')
    elif "Articule" in condition_bord.split('-')[0]:
        ax_schema.plot(0, 0, 'bo', markersize=12, label='Articulation')
    else:
        ax_schema.plot(0, 0, 'g^', markersize=12, label='Libre')
    
    if "Encastre" in condition_bord.split('-')[1]:
        ax_schema.plot(L, 0, 'rs', markersize=15)
    elif "Articule" in condition_bord.split('-')[1]:
        ax_schema.plot(L, 0, 'bo', markersize=12)
    else:
        ax_schema.plot(L, 0, 'g^', markersize=12)
    
    # Ajouter les positions de force et de mesure
    ax_schema.plot(x_force, 0, 'r^', markersize=15, label=f'Force @ {x_force:.2f}m')
    ax_schema.plot(x_mesure, 0, 'b*', markersize=15, label=f'Mesure @ {x_mesure:.2f}m')
    
    ax_schema.set_xlim(-L*0.05, L*1.05)
    ax_schema.set_ylim(-0.5, 0.5)
    ax_schema.set_xlabel("Position (m)")
    ax_schema.set_title(f"Configuration : {condition_bord}")
    ax_schema.grid(True, alpha=0.3)
    ax_schema.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=3)
    ax_schema.set_yticks([])
    
    st.pyplot(fig_schema)
    plt.close(fig_schema)
    
    # Calcul de la FRF
    st.markdown("**Calcul de la FRF :**")
    
    # Paramètres de la FRF
    col1, col2, col3 = st.columns(3)
    
    with col1:
        f_min = st.number_input("Fréquence minimale (Hz)", value=0, min_value=0, max_value=1000, step=10)
    with col2:
        f_max = st.number_input("Fréquence maximale (Hz)", value=1000, min_value=100, max_value=10000, step=100)
    with col3:
        n_points = st.number_input("Nombre de points", value=1000, min_value=100, max_value=10000, step=100)
    
    # Calcul
    omega = 2 * np.pi * np.linspace(f_min, f_max, n_points)
    H, H_magnitude, contributions = poutre.calculer_FRF(x_force, x_mesure, omega, n_modes, condition_bord, damping_ratio)
    
    # Conversion en dB pour une meilleure visualisation
    H_magnitude_db = 20 * np.log10(H_magnitude + 1e-20)  # +1e-20 pour éviter log(0)
    
    # Création du graphique FRF
    fig_frf, ax_frf = plt.subplots(1, 1, figsize=(14, 8))
    
    # Tracer la FRF globale (plus visible)
    f_axis = omega / (2 * np.pi)
    ax_frf.plot(f_axis, H_magnitude_db, 'k-', linewidth=3, label='FRF Globale', zorder=10)
    
    # Tracer les contributions modales (moins visibles)
    colors_frf = plt.cm.tab10(np.linspace(0, 1, n_modes))
    for n in range(n_modes):
        if n < len(contributions):
            contrib_mag_db = 20 * np.log10(np.abs(contributions[n]) + 1e-20)
            ax_frf.plot(f_axis, contrib_mag_db, '--', color=colors_frf[n], 
                       linewidth=1.5, alpha=0.7, 
                       label=f'Mode {n+1} ({frequences[n]:.2f} Hz)')
    
    # Ajouter des marqueurs pour les fréquences naturelles
    for n in range(n_modes):
        if frequences[n] > 0:
            ax_frf.axvline(frequences[n], color=colors_frf[n], linestyle=':', 
                          alpha=0.5, label=f'f{n+1}={frequences[n]:.2f}Hz')
    
    ax_frf.set_xlabel("Fréquence (Hz)", fontsize=12)
    ax_frf.set_ylabel("Amplitude (dB)", fontsize=12)
    ax_frf.set_title(f"FRF : Force @ {x_force:.2f}m → Mesure @ {x_mesure:.2f}m", 
                     fontsize=14, fontweight='bold')
    ax_frf.grid(True, alpha=0.3, which='both')
    ax_frf.set_xlim(f_min, f_max)
    
    # Légende avec gestion du chevauchement
    handles, labels = ax_frf.get_legend_handles_labels()
    if len(handles) > 20:  # Si trop d'éléments, simplifier
        # Garder seulement la FRF globale et les marqueurs de fréquence
        new_handles = [handles[0]] + [handles[i] for i in range(len(handles)) if i % 2 == 1 and i < len(handles)]
        new_labels = [labels[0]] + [labels[i] for i in range(len(labels)) if i % 2 == 1 and i < len(labels)]
        ax_frf.legend(new_handles, new_labels, loc='upper right', fontsize=10)
    else:
        ax_frf.legend(handles, labels, loc='upper right', fontsize=10, 
                     bbox_to_anchor=(1.05, 1) if len(handles) > 10 else None)
    
    # Ajouter un cadre
    for spine in ax_frf.spines.values():
        spine.set_linewidth(1.5)
    
    st.pyplot(fig_frf)
    plt.close(fig_frf)
    
    # Afficher les informations sur les pics de la FRF
    st.markdown("**Analyse des pics de la FRF :**")
    
    # Trouver les pics de la FRF
    peaks, _ = signal.find_peaks(H_magnitude_db, height=max(H_magnitude_db) - 40, distance=10)
    
    if len(peaks) > 0:
        peak_data = []
        for peak_idx in peaks[:n_modes]:  # Limiter au nombre de modes
            f_peak = f_axis[peak_idx]
            mag_peak = H_magnitude_db[peak_idx]
            
            # Trouver le mode le plus proche
            closest_mode = 1
            min_diff = abs(f_peak - frequences[0])
            for n in range(1, n_modes):
                diff = abs(f_peak - frequences[n])
                if diff < min_diff:
                    min_diff = diff
                    closest_mode = n + 1
            
            peak_data.append({
                "Fréquence (Hz)": f"{f_peak:.2f}",
                "Amplitude (dB)": f"{mag_peak:.2f}",
                "Mode associé": f"Mode {closest_mode}",
                "Écart (Hz)": f"{abs(f_peak - frequences[closest_mode-1]):.2f}"
            })
        
        st.table(peak_data)
    else:
        st.info("Aucun pic détecté dans la plage de fréquences sélectionnée.")
    
    # ============================================================================
    # SECTION 3: ANALYSE MODALE DÉTAILLÉE
    # ============================================================================
    
    st.markdown("---")
    st.markdown('<div class="sub-header">🔬 Analyse modale détaillée</div>', unsafe_allow_html=True)
    
    # Sélection d'un mode spécifique
    mode_selected = st.selectbox("Sélectionnez un mode pour l'analyse détaillée", 
                                  range(1, n_modes + 1), key="mode_detailed")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Mode {mode_selected} :**")
        f_selected = frequences[mode_selected - 1]
        st.metric("Fréquence naturelle", f"{f_selected:.2f} Hz")
        
        # Calcul de la déformée
        x_detailed = np.linspace(0, L, 100)
        phi_detailed = poutre.calculer_deformee_modale(x_detailed, mode_selected, condition_bord)
        
        # Trouver les nœuds (zéros de la déformée)
        nodes = x_detailed[np.abs(phi_detailed) < 0.01]
        if len(nodes) > 0:
            st.markdown("**Nœuds (points de déplacement nul) :**")
            for node in nodes:
                st.write(f"- x = {node:.3f} m")
        
        # Trouver les ventres (maxima)
        from scipy.signal import argrelextrema
        maxima_idx = argrelextrema(phi_detailed, np.greater)[0]
        if len(maxima_idx) > 0:
            st.markdown("**Ventres (points de déplacement maximal) :**")
            for idx in maxima_idx:
                st.write(f"- x = {x_detailed[idx]:.3f} m (amplitude: {phi_detailed[idx]:.3f})")
    
    with col2:
        # Visualisation de la déformée du mode sélectionné
        fig_mode, ax_mode = plt.subplots(1, 1, figsize=(8, 6))
        
        ax_mode.plot(x_detailed, phi_detailed, 'b-', linewidth=3, label=f'Mode {mode_selected}')
        ax_mode.axhline(0, color='k', linestyle='--', alpha=0.5)
        
        # Ajouter les nœuds
        if len(nodes) > 0:
            ax_mode.plot(nodes, np.zeros_like(nodes), 'ro', markersize=8, label='Nœuds')
        
        # Ajouter les ventres
        if len(maxima_idx) > 0:
            ax_mode.plot(x_detailed[maxima_idx], phi_detailed[maxima_idx], 'g^', 
                        markersize=10, label='Ventres')
        
        # Ajouter les conditions aux limites
        if condition_bord == "Encastre-Encastre":
            ax_mode.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
            ax_mode.axvline(L, color='red', linestyle='-', linewidth=3, alpha=0.7)
        elif condition_bord == "Encastre-Libre":
            ax_mode.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
            ax_mode.axvline(L, color='green', linestyle='--', linewidth=2, alpha=0.7)
        elif condition_bord == "Libre-Libre":
            ax_mode.axvline(0, color='green', linestyle='--', linewidth=2, alpha=0.7)
            ax_mode.axvline(L, color='green', linestyle='--', linewidth=2, alpha=0.7)
        elif condition_bord == "Articule-Articule":
            ax_mode.axvline(0, color='blue', linestyle=':', linewidth=2, alpha=0.7)
            ax_mode.axvline(L, color='blue', linestyle=':', linewidth=2, alpha=0.7)
        elif condition_bord == "Encastre-Articule":
            ax_mode.axvline(0, color='red', linestyle='-', linewidth=3, alpha=0.7)
            ax_mode.axvline(L, color='blue', linestyle=':', linewidth=2, alpha=0.7)
        
        ax_mode.set_xlabel("Position (m)")
        ax_mode.set_ylabel("Amplitude normalisée")
        ax_mode.set_title(f"Déformée modale - Mode {mode_selected} ({f_selected:.2f} Hz)", 
                         fontweight='bold')
        ax_mode.grid(True, alpha=0.3)
        ax_mode.legend()
        ax_mode.set_ylim(-1.2, 1.2)
        
        st.pyplot(fig_mode)
        plt.close(fig_mode)
    
    # ============================================================================
    # SECTION 4: EXPORT DES DONNÉES
    # ============================================================================
    
    st.markdown("---")
    st.markdown('<div class="sub-header">💾 Export des données</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Exporter les fréquences naturelles"):
            # Créer un CSV avec les fréquences
            csv_data = "Mode,Fréquence (Hz)\n"
            for n in range(1, n_modes + 1):
                csv_data += f"{n},{frequences[n-1]:.6f}\n"
            
            st.download_button(
                label="Télécharger CSV",
                data=csv_data,
                file_name=f"frequences_naturelles_{condition_bord}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Exporter la FRF"):
            # Créer un CSV avec la FRF
            csv_data = "Fréquence (Hz),Amplitude (dB)\n"
            for f, mag in zip(f_axis, H_magnitude_db):
                csv_data += f"{f:.6f},{mag:.6f}\n"
            
            st.download_button(
                label="Télécharger CSV",
                data=csv_data,
                file_name=f"FRF_{x_force}m_{x_mesure}m.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Exporter les déformées modales"):
            # Créer un CSV avec les déformées
            csv_data = "Position (m)"
            for n in range(1, n_modes + 1):
                csv_data += f",Mode {n}"
            csv_data += "\n"
            
            x_export = np.linspace(0, L, 100)
            for x in x_export:
                csv_data += f"{x:.6f}"
                for n in range(1, n_modes + 1):
                    phi = poutre.calculer_deformee_modale(x, n, condition_bord)
                    csv_data += f",{phi:.6f}"
                csv_data += "\n"
            
            st.download_button(
                label="Télécharger CSV",
                data=csv_data,
                file_name=f"deformees_modales_{condition_bord}.csv",
                mime="text/csv"
            )
    
    # ============================================================================
    # PIED DE PAGE
    # ============================================================================
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📊 Vibrateam - Analyse Vibratoire des Poutres</p>
        <p>Développé avec Streamlit, NumPy, Matplotlib | Théorie d'Euler-Bernoulli</p>
        <p>Version 1.0 - 2024</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# EXÉCUTION DE L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
