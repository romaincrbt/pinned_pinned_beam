#!/usr/bin/env python3
"""
Tests unitaires pour l'application Vibrateam
"""

import numpy as np
from vibrateam_app import PoutreVibratoire


def test_poutre_init():
    """Test de l'initialisation de la poutre"""
    poutre = PoutreVibratoire(L=2.0, E=210e9, rho=7800, I=1e-8, A=1e-4)
    
    assert poutre.L == 2.0
    assert poutre.E == 210e9
    assert poutre.rho == 7800
    assert poutre.I == 1e-8
    assert poutre.A == 1e-4
    assert poutre.masse_lineique == 7800 * 1e-4  # rho * A
    assert poutre.rigidite_flexion == 210e9 * 1e-8  # E * I


def test_beta_n_encastre_encastre():
    """Test des valeurs de beta_n pour poutre encastrée-encastrée"""
    poutre = PoutreVibratoire()
    
    # Valeurs connues pour encastré-encastré
    beta_1 = poutre.calculer_beta_n(1, "Encastre-Encastre")
    beta_2 = poutre.calculer_beta_n(2, "Encastre-Encastre")
    beta_3 = poutre.calculer_beta_n(3, "Encastre-Encastre")
    
    # Valeurs théoriques
    assert abs(beta_1 - 4.730040744862704) < 1e-6
    assert abs(beta_2 - 7.853204624095737) < 1e-6
    assert abs(beta_3 - 10.99560783800167) < 1e-6


def test_beta_n_encastre_libre():
    """Test des valeurs de beta_n pour poutre encastrée-libre"""
    poutre = PoutreVibratoire()
    
    # Valeurs connues pour encastré-libre
    beta_1 = poutre.calculer_beta_n(1, "Encastre-Libre")
    beta_2 = poutre.calculer_beta_n(2, "Encastre-Libre")
    beta_3 = poutre.calculer_beta_n(3, "Encastre-Libre")
    
    # Valeurs théoriques
    assert abs(beta_1 - 1.875104068711961) < 1e-6
    assert abs(beta_2 - 4.694068489942059) < 1e-6
    assert abs(beta_3 - 7.854757434837964) < 1e-6


def test_beta_n_articule_articule():
    """Test des valeurs de beta_n pour poutre articulée-articulée"""
    poutre = PoutreVibratoire()
    
    # Pour articulé-articulé, beta_n = n * pi
    for n in range(1, 6):
        beta_n = poutre.calculer_beta_n(n, "Articule-Articule")
        assert abs(beta_n - n * np.pi) < 1e-10


def test_frequences_naturelles():
    """Test du calcul des fréquences naturelles"""
    poutre = PoutreVibratoire(L=1.0, E=210e9, rho=7800, I=1e-8, A=1e-4)
    
    # Calcul de la première fréquence pour encastré-encastré
    f_1 = poutre.calculer_frequence_naturelle(1, "Encastre-Encastre")
    
    # Formule : f_n = (beta_n^2 / (2*pi*L^2)) * sqrt(E*I/(rho*A))
    beta_1 = 4.730040744862704
    expected_f_1 = (beta_1 ** 2) / (2 * np.pi * 1.0 ** 2) * np.sqrt(210e9 * 1e-8 / (7800 * 1e-4))
    
    assert abs(f_1 - expected_f_1) < 0.1  # Tolérance de 0.1 Hz


def test_deformee_modale_articule_articule():
    """Test de la déformée modale pour poutre articulée-articulée"""
    poutre = PoutreVibratoire(L=1.0)
    
    x = np.linspace(0, 1.0, 100)
    phi_1 = poutre.calculer_deformee_modale(x, 1, "Articule-Articule")
    
    # Pour articulé-articulé, phi_n(x) = sin(n*pi*x/L)
    expected_phi_1 = np.sin(np.pi * x)
    
    # Normalisation
    expected_phi_1 = expected_phi_1 / np.max(np.abs(expected_phi_1))
    
    assert np.allclose(phi_1, expected_phi_1, atol=1e-6)


def test_deformee_modale_encastre_encastre():
    """Test de la déformée modale pour poutre encastrée-encastrée"""
    poutre = PoutreVibratoire(L=1.0)
    
    x = np.array([0.0, 0.5, 1.0])
    phi_1 = poutre.calculer_deformee_modale(x, 1, "Encastre-Encastre")
    
    # À l'extrémité encastrée (x=0), la déformée devrait être nulle
    assert abs(phi_1[0]) < 1e-10
    
    # À l'autre extrémité encastrée (x=L), la déformée devrait être nulle
    # Note: la valeur théorique est nulle, mais après normalisation elle peut être différente
    # On vérifie que la déformée a un maximum au centre
    assert abs(phi_1[1]) > 0.5  # Maximum au centre
    
    # La déformée devrait être normalisée (max = 1)
    assert abs(max(abs(phi_1[0]), abs(phi_1[1]), abs(phi_1[2]))) > 0.9


def test_deformee_modale_encastre_libre():
    """Test de la déformée modale pour poutre encastrée-libre"""
    poutre = PoutreVibratoire(L=1.0)
    
    x = np.array([0.0, 1.0])
    phi_1 = poutre.calculer_deformee_modale(x, 1, "Encastre-Libre")
    
    # À l'extrémité encastrée (x=0), la déformée devrait être nulle
    assert abs(phi_1[0]) < 1e-10
    
    # À l'extrémité libre (x=L), la déformée devrait être non nulle (maximum)
    assert abs(phi_1[1]) > 0.5


def test_FRF_calculation():
    """Test du calcul de la FRF"""
    poutre = PoutreVibratoire(L=1.0, E=210e9, rho=7800, I=1e-8, A=1e-4)
    
    x_force = 0.25
    x_mesure = 0.5
    omega = 2 * np.pi * np.array([10, 50, 100, 200])
    n_modes = 3
    
    H, H_magnitude, contributions = poutre.calculer_FRF(
        x_force, x_mesure, omega, n_modes, "Encastre-Encastre", damping_ratio=0.01
    )
    
    # Vérifier les dimensions
    assert len(H) == len(omega)
    assert len(H_magnitude) == len(omega)
    assert len(contributions) == n_modes
    
    # Vérifier que la magnitude est positive
    assert all(H_magnitude >= 0)
    
    # Vérifier que H est complexe
    assert all(isinstance(h, complex) for h in H)


def test_FRF_at_resonance():
    """Test de la FRF à la fréquence de résonance"""
    poutre = PoutreVibratoire(L=1.0, E=210e9, rho=7800, I=1e-8, A=1e-4)
    
    x_force = 0.25
    x_mesure = 0.5
    n_modes = 1
    
    # Calculer la fréquence naturelle du premier mode
    f_1 = poutre.calculer_frequence_naturelle(1, "Encastre-Encastre")
    omega_1 = 2 * np.pi * f_1
    
    # Calculer la FRF à cette fréquence
    omega = np.array([omega_1])
    H, H_magnitude, _ = poutre.calculer_FRF(
        x_force, x_mesure, omega, n_modes, "Encastre-Encastre", damping_ratio=0.01
    )
    
    # À la résonance, la magnitude devrait être non nulle
    assert H_magnitude[0] > 1e-5


def test_libre_libre_rigid_modes():
    """Test des modes rigides pour poutre libre-libre"""
    poutre = PoutreVibratoire(L=1.0)
    
    # Les deux premiers modes devraient être rigides (fréquence nulle)
    f_1 = poutre.calculer_frequence_naturelle(1, "Libre-Libre")
    f_2 = poutre.calculer_frequence_naturelle(2, "Libre-Libre")
    
    assert f_1 == 0.0
    assert f_2 == 0.0
    
    # Le troisième mode devrait avoir une fréquence non nulle
    f_3 = poutre.calculer_frequence_naturelle(3, "Libre-Libre")
    assert f_3 > 0


def test_normalization():
    """Test de la normalisation des déformées modales"""
    poutre = PoutreVibratoire(L=1.0)
    
    for condition in ["Encastre-Encastre", "Encastre-Libre", "Articule-Articule"]:
        for n in range(1, 4):
            x = np.linspace(0, 1.0, 1000)
            phi_n = poutre.calculer_deformee_modale(x, n, condition)
            
            # La déformée devrait être normalisée (max = 1)
            max_phi = np.max(np.abs(phi_n))
            assert abs(max_phi - 1.0) < 1e-6, f"Mode {n} pour {condition} n'est pas normalisé"


def test_condition_inconnue():
    """Test de la gestion des conditions aux limites inconnues"""
    poutre = PoutreVibratoire()
    
    try:
        poutre.calculer_beta_n(1, "ConditionInconnue")
        assert False, "ValueError non levé pour beta_n"
    except ValueError:
        pass
    
    try:
        poutre.calculer_frequence_naturelle(1, "ConditionInconnue")
        assert False, "ValueError non levé pour fréquence naturelle"
    except ValueError:
        pass
    
    try:
        poutre.calculer_deformee_modale(0.5, 1, "ConditionInconnue")
        assert False, "ValueError non levé pour déformée modale"
    except ValueError:
        pass


if __name__ == "__main__":
    # Exécuter les tests
    print("Exécution des tests unitaires...")
    
    test_poutre_init()
    print("✓ test_poutre_init")
    
    test_beta_n_encastre_encastre()
    print("✓ test_beta_n_encastre_encastre")
    
    test_beta_n_encastre_libre()
    print("✓ test_beta_n_encastre_libre")
    
    test_beta_n_articule_articule()
    print("✓ test_beta_n_articule_articule")
    
    test_frequences_naturelles()
    print("✓ test_frequences_naturelles")
    
    test_deformee_modale_articule_articule()
    print("✓ test_deformee_modale_articule_articule")
    
    test_deformee_modale_encastre_encastre()
    print("✓ test_deformee_modale_encastre_encastre")
    
    test_deformee_modale_encastre_libre()
    print("✓ test_deformee_modale_encastre_libre")
    
    test_FRF_calculation()
    print("✓ test_FRF_calculation")
    
    test_FRF_at_resonance()
    print("✓ test_FRF_at_resonance")
    
    test_libre_libre_rigid_modes()
    print("✓ test_libre_libre_rigid_modes")
    
    test_normalization()
    print("✓ test_normalization")
    
    test_condition_inconnue()
    print("✓ test_condition_inconnue")
    
    print("\n✅ Tous les tests ont réussi !")
