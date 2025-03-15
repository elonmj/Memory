# Plan de Vérification des Méthodes Numériques

Ce document présente une méthodologie détaillée pour vérifier l'implémentation des méthodes numériques dans `src/utils/numerical_methods.py`, en s'assurant de leur exactitude, stabilité et cohérence avec la théorie sous-jacente.

## 1. Analyse Comparative du Code avec la Théorie

### 1.1 Schéma de Godunov Standard

#### Description théorique
Le schéma de Godunov résout l'équation de conservation du trafic en utilisant la formulation suivante:
```
ρ_i^(n+1) = ρ_i^n - (Δt/Δx) · (F_{i+1/2}^n - F_{i-1/2}^n)
```

Où le flux numérique F_{i+1/2}^n est obtenu par résolution d'un problème de Riemann à l'interface:
```
F_{i+1/2}^n = min[flux(ρ_L), flux(ρ_R)] si ρ_L ≤ ρ_R et ρ_L ≤ ρ_c et ρ_R ≥ ρ_c
            = flux(ρ_c) si ρ_L ≤ ρ_c ≤ ρ_R 
            = min[flux(ρ_L), flux(ρ_R)] pour les autres cas
```
avec ρ_c la densité critique.

#### Vérification de l'implémentation
1. Examiner la fonction `godunov_flux(rho_left, rho_right, model)` pour vérifier:
   - Présence correcte de la condition pour flux maximum (capacité)
   - Calcul de minimum pour les autres cas
   - Traitement correct des flux pour toutes les relations possibles entre ρ_L et ρ_R

2. Comparaison ligne à ligne avec la formulation théorique:
   - Identifier des potentielles simplifications ou approximations
   - Vérifier la notation et l'utilisation cohérente des variables

#### Tests spécifiques
1. Cas test 1: ρ_L < ρ_c < ρ_R (devrait retourner le flux maximal)
2. Cas test 2: ρ_L < ρ_R < ρ_c (devrait retourner le flux à ρ_L)
3. Cas test 3: ρ_c < ρ_L < ρ_R (devrait retourner le flux à ρ_R)
4. Cas test 4: ρ_R < ρ_L (devrait retourner le minimum des deux flux)

### 1.2 Extension Multiclasse

#### Description théorique
L'extension multiclasse du schéma de Godunov doit tenir compte des interactions entre classes de véhicules, notamment:
```
F_i = mathcal{F}_i(boldsymbol{ρ}_j, boldsymbol{ρ}_{j+1}, x_{j+1/2})
```

Ce flux est généralement calculé en considérant:
- La densité totale dans chaque cellule
- L'impact relatif des différentes classes (particulièrement des motos)
- Les vitesses calculées à partir de ces densités

#### Vérification de l'implémentation
1. Examiner la fonction `godunov_flux_multiclass(rho_left, rho_right, model)` pour vérifier:
   - Calcul correct des densités totales
   - Traitement approprié des interactions entre classes
   - Structure de données utilisée pour représenter les densités multiclasses

2. Identifier les différences avec la formulation théorique présentée dans le chapitre sur les schémas numériques:
   - Simplifications potentielles
   - Adaptations algorithmiques
   - Optimisations pour l'implémentation pratique

#### Tests spécifiques
1. Test avec 2 classes symétriques (mêmes paramètres)
2. Test avec classes asymétriques (motos et voitures)
3. Test avec configurations extrêmes (100% motos vs. 100% voitures)

## 2. Validation de la Correction des Algorithmes

### 2.1 Tests Unitaires pour le Flux de Godunov

#### Création de cas de test vérifiables
Développer des tests unitaires automatisés pour valider `godunov_flux`:

1. **Cas de conservation**: Vérifier que le flux respecte F(ρ=0) = 0 et F(ρ=ρ_max) = 0
2. **Cas de capacité maximale**: Vérifier que le flux correspond à la capacité maximale lorsque ρ_L < ρ_c < ρ_R
3. **Cas d'onde de choc**: Valider le calcul du flux pour une configuration générant une onde de choc
4. **Cas d'onde de raréfaction**: Valider le calcul du flux pour une configuration générant une raréfaction

#### Validation avec solutions analytiques
Pour des cas où une solution analytique est connue:

1. Problème de Riemann simple:
   - Conditions initiales: ρ(x,0) = ρ_L pour x < 0, ρ_R pour x > 0
   - Comparer le flux calculé numériquement avec la solution analytique
   - Mesurer l'erreur et vérifier qu'elle est dans les limites acceptables

2. Solution auto-similaire:
   - Utiliser des solutions auto-similaires (ρ(x,t) = ρ(x/t)) pour valider le flux
   - Vérifier la convergence vers la solution exacte

### 2.2 Validation de l'Algorithme d'Actualisation de la Densité

#### Tests fonctionnels
1. Conservation de la masse:
   - Simuler un domaine fermé
   - Vérifier que la somme des densités reste constante
   - Tolérance d'erreur: < 10^-10

2. Propagation des discontinuités:
   - Initialiser une discontinuité dans la densité
   - Suivre sa propagation au fil du temps
   - Comparer la vitesse de propagation avec la valeur théorique (|Δf/Δρ|)

#### Analyse d'erreur de discrétisation
1. Étude de convergence:
   - Implémenter une étude de convergence avec raffinage progressif du maillage
   - Calculer l'ordre de convergence empirique
   - Vérifier qu'il correspond à l'ordre théorique (1 pour Godunov)

2. Analyse de sensibilité au pas de temps:
   - Faire varier le rapport Δt/Δx tout en respectant la condition CFL
   - Quantifier l'impact sur la précision de la solution

## 3. Examen de la Gestion des Conditions aux Limites

### 3.1 Identification des Types de Conditions aux Limites

#### Analyse du code
1. Rechercher dans le code des implémentations de conditions aux limites:
   - Conditions périodiques
   - Conditions de Dirichlet (densité imposée)
   - Conditions de Neumann (gradient nul)
   - Conditions absorbantes

2. Vérifier le traitement des conditions aux limites dans la fonction `update_density`:
   - Comment sont gérés les indices de bord?
   - Les flux aux frontières sont-ils correctement définis?

#### Tests des conditions aux limites
1. **Condition périodique**:
   - Tester avec une onde se propageant à travers la frontière
   - Vérifier la continuité du profil de densité

2. **Condition de Dirichlet**:
   - Imposer une densité constante à l'entrée
   - Observer la propagation correcte dans le domaine

3. **Condition absorbante**:
   - Vérifier l'absence de réflexions non physiques à la sortie
   - Analyser la conservation de la masse lorsqu'une onde quitte le domaine

### 3.2 Influence des Conditions aux Limites sur les Simulations

#### Tests comparatifs
1. Comparer différentes conditions aux limites pour un même scénario:
   - Impact sur la formation des embouteillages
   - Différences dans les ondes de choc
   - Comportement près des frontières

2. Tester la stabilité sous différentes conditions:
   - Flux d'entrée élevé
   - Transition brusque de densité à la sortie

#### Recommandations
1. Identifier les conditions aux limites optimales selon les scénarios:
   - Pour simuler un tronçon d'autoroute
   - Pour simuler une intersection urbaine
   - Pour étudier un phénomène localisé

## 4. Évaluation de la Stabilité Numérique

### 4.1 Analyse de la Condition CFL

#### Vérification théorique
1. Examiner la fonction `cfl_condition(dt, dx, v_max)`:
   - Vérifier que la formulation correspond à la théorie: dt ≤ Δx/v_max
   - S'assurer qu'elle est appliquée correctement dans le code principal
   - Vérifier si un facteur de sécurité est utilisé (typiquement 0.9)

2. Vérifier son application au modèle multiclasse:
   - La vitesse maximale considère-t-elle toutes les classes?
   - Les termes additionnels dus aux interactions entre classes sont-ils pris en compte?

#### Tests de stabilité
1. Tests de stabilité pour différentes valeurs du nombre de Courant (C = v_max·dt/dx):
   - C = 0.9 (proche de la limite de stabilité)
   - C = 0.5 (valeur intermédiaire)
   - C = 0.1 (très conservateur)

2. Observer les effets de la violation de la condition CFL:
   - Créer intentionnellement une situation instable (C > 1)
   - Documenter les artefacts numériques qui en résultent

### 4.2 Analyse de Stabilité pour le Système Complet

#### Tests de robustesse
1. Tester la stabilité face à des conditions initiales extrêmes:
   - Discontinuités fortes
   - Gradients très raides
   - Densités proches des valeurs limites

2. Examiner la stabilité pour des longues simulations:
   - Vérifier l'absence d'accumulation d'erreurs
   - S'assurer que les propriétés de conservation sont maintenues

#### Analyse des oscillations
1. Quantifier les oscillations numériques:
   - Mesurer l'amplitude des oscillations près des discontinuités
   - Comparer avec la solution exacte attendue

2. Évaluer l'impact des paramètres numériques:
   - Tester différentes résolutions spatiales
   - Analyser l'impact du ratio Δt/Δx

## 5. Programme de Tests Systématiques

### 5.1 Batterie de Tests Unitaires

1. Créer une suite de tests unitaires automatiques pour:
   - `godunov_flux`
   - `cfl_condition`
   - `update_density`
   - `godunov_flux_multiclass`

2. Développer un script qui exécute tous les tests et génère un rapport de conformité:
   ```python
   def test_godunov_flux():
       # Création d'un modèle de test simple
       model = MockModel(rho_max=180, v_max=100)
       
       # Test cas 1: rho_left < rho_crit < rho_right (capacité maximale)
       rho_left = model.densite_critique() * 0.5
       rho_right = model.densite_critique() * 1.5
       flux = godunov_flux(rho_left, rho_right, model)
       assert abs(flux - model.capacite()) < 1e-10
       
       # Test cas 2: rho_left < rho_right < rho_crit
       # [...]
   ```

### 5.2 Tests d'Intégration avec les Modèles de Trafic

1. Tests d'intégration avec différents modèles:
   - Modèle LWR standard
   - Modèle multiclasse
   - Variations du modèle avec paramètres différents

2. Vérification des résultats attendus:
   - Conservation de la masse
   - Propagation correcte des ondes
   - Comportement aux singularités (intersections, changements de revêtement)

### 5.3 Benchmarks de Performance

1. Évaluer l'efficacité des méthodes numériques:
   - Temps de calcul en fonction de la résolution
   - Consommation mémoire
   - Scalabilité par rapport à la taille du problème



## 6. Documentation et Améliorations Potentielles

### 6.1 Points Critiques Identifiés

1. Documenter les limitations connues:
   - Ordre de convergence limité (1 pour Godunov)
   - Diffusion numérique près des discontinuités
   - Contraintes de stabilité restrictives

2. Noter les cas particuliers requérant une attention spéciale:
   - Congestion sévère (ρ → ρ_max)
   - Transitions abruptes dans la qualité de la route

### 6.2 Recommandations d'Amélioration

1. Pistes d'amélioration à court terme:
   - Optimisation des calculs de flux
   - Meilleure gestion des conditions aux limites
   - Documentation complémentaire du code

2. Améliorations algorithmiques potentielles:
   - Implémentation de schémas d'ordre supérieur (WENO, ENO)
   - Adaptation du pas de temps dynamique
   - Techniques de maillage adaptatif

## Annexe: Script de Vérification

```python
# Script Python pour la vérification automatisée des méthodes numériques

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.numerical_methods import godunov_flux, cfl_condition, update_density, godunov_flux_multiclass

class TestModel:
    """Modèle simple pour les tests"""
    def __init__(self, rho_max=180, v_max=100):
        self.rho_max = rho_max
        self.v_max = v_max
    
    def densite_critique(self):
        return self.rho_max / 2
    
    def capacite(self):
        return self.flux(self.densite_critique())
    
    def flux(self, rho):
        return rho * self.v_max * (1 - rho / self.rho_max)

def test_godunov_flux_conservation():
    """Teste que le flux est nul aux densités extrêmes"""
    model = TestModel()
    
    # Flux à densité nulle
    assert abs(godunov_flux(0, 0, model)) < 1e-10
    
    # Flux à densité maximale
    assert abs(godunov_flux(model.rho_max, model.rho_max, model)) < 1e-10
    
    print("Test de conservation des flux aux extrêmes: RÉUSSI")

def test_godunov_flux_capacity():
    """Teste que le flux égale la capacité dans les conditions appropriées"""
    model = TestModel()
    rho_c = model.densite_critique()
    
    # Test avec rho_left < rho_c < rho_right
    flux = godunov_flux(rho_c * 0.5, rho_c * 1.5, model)
    assert abs(flux - model.capacite()) < 1e-10
    
    print("Test de capacité maximale: RÉUSSI")

def test_cfl_condition():
    """Vérifie le calcul de la condition CFL"""
    # CFL respectée
    assert cfl_condition(0.01, 1.0, 90) == True
    
    # CFL violée
    assert cfl_condition(0.02, 1.0, 90) == False
    
    print("Test de condition CFL: RÉUSSI")

def test_update_density_conservation():
    """Vérifie que la mise à jour de densité conserve la masse"""
    # Configuration de test
    dx = 1.0
    dt = 0.01
    density = np.ones(10) * 50
    flux_left = np.ones(10) * 2000
    flux_right = np.ones(10) * 2000
    
    # Calcul de la masse initiale
    initial_mass = np.sum(density) * dx
    
    # Mise à jour
    new_density = update_density(density, flux_left, flux_right, dt, dx)
    
    # Calcul de la nouvelle masse
    new_mass = np.sum(new_density) * dx
    
    # Vérification de la conservation
    assert abs(new_mass - initial_mass) < 1e-10
    
    print("Test de conservation de la masse: RÉUSSI")

def run_all_tests():
    """Exécute tous les tests de vérification"""
    print("DÉMARRAGE DES TESTS DE VÉRIFICATION\n" + "="*40)
    
    test_godunov_flux_conservation()
    test_godunov_flux_capacity()
    test_cfl_condition()
    test_update_density_conservation()
    
    # Ajouter d'autres tests au besoin
    
    print("="*40 + "\nTOUS LES TESTS ONT RÉUSSI")

if __name__ == "__main__":
    run_all_tests()
```

## Conclusion

Cette méthodologie de vérification fournit un cadre rigoureux pour valider l'exactitude et la stabilité des méthodes numériques implémentées dans `numerical_methods.py`. En suivant systématiquement ces étapes, nous pouvons garantir que:

1. Les algorithmes sont fidèles aux formulations théoriques
2. Les propriétés fondamentales (conservation, stabilité) sont respectées
3. Le comportement des schémas est correct dans tous les régimes de fonctionnement
4. Les conditions aux limites sont gérées de manière cohérente

L'application de ce plan permettra d'identifier d'éventuelles erreurs d'implémentation et d'optimiser les méthodes numériques pour améliorer la précision et l'efficacité des simulations de trafic.

