# Plan de Vérification d'Implémentation des Modèles LWR

## 1. Introduction

Ce document présente une méthodologie structurée pour vérifier l'implémentation des modèles de trafic LWR (Lighthill-Whitham-Richards) standard et LWR multi-classes. L'objectif est de s'assurer que le code implémenté correspond fidèlement aux fondements théoriques décrits dans les chapitres du mémoire et possède les propriétés mathématiques attendues.

## 2. Méthodologie Générale

La vérification suivra une approche systématique en quatre étapes principales :
1. Lecture analytique du code
2. Vérification spécifique de la fonction de flux
3. Examen approfondi du schéma numérique
4. Analyse des spécificités multi-classes (pour le modèle étendu)

Pour chaque fichier de code, nous compléterons une fiche de vérification documentant les résultats de chaque étape et les éventuelles non-conformités détectées.

## 3. Fichiers à Vérifier

Les fichiers principaux à examiner sont :
- `base_model.py`: Interface commune pour tous les modèles
- `lwr_model.py`: Implémentation du modèle LWR standard
- `multiclass_lwr.py`: Extension du modèle LWR pour le trafic multi-classes
- `vc_modulations.py`: Fonctions de modulation pour les interactions entre classes
- `fundamental_diagram.py`: Implémentation des relations fondamentales
- `numerical_methods.py`: Implémentation des schémas numériques

## 4. Étapes de Vérification Détaillées

### 4.1 Lecture Analytique du Code

#### Objectif
Vérifier la correspondance entre l'implémentation et les formulations théoriques présentées dans les chapitres du mémoire.

#### Points à vérifier
- **Correspondance avec les équations théoriques**
  - Équation de conservation: ∂ρ/∂t + ∂(ρv)/∂x = 0
  - Relation vitesse-densité (Greenshields): v(ρ) = v_max(1 - ρ/ρ_max)
  - Relations étendues pour le modèle multi-classes

- **Structure et organisation du code**
  - Respect des principes de programmation orientée objet
  - Cohérence de l'héritage (base_model → lwr_model → multiclass_lwr)
  - Documentation du code (docstrings, commentaires explicatifs)

- **Documentation des divergences**
  - Identifier les différences entre l'implémentation et les équations théoriques
  - Noter les simplifications ou optimisations adoptées et leur justification

#### Liste de contrôle
- [ ] Les équations de base sont correctement implémentées
- [ ] Les relations constitutives (vitesse-densité, flux-densité) sont conformes à la théorie
- [ ] La structure de classes respecte l'architecture décrite dans STRUCTURE.md
- [ ] Les divergences ou simplifications sont documentées et justifiées

### 4.2 Vérification Spécifique de la Fonction de Flux

#### Objectif
S'assurer que la fonction de flux q = ρ·v(ρ) est correctement implémentée et possède les propriétés mathématiques attendues.

#### Points à vérifier
- **Forme mathématique**
  - Pour Greenshields: q(ρ) = v_max·ρ·(1 - ρ/ρ_max)
  - Pour le modèle multi-classes: q_i(ρ) = λ_i(x)·v_i,0·ρ_i·(1 - ρ/ρ_max)·f_i(ρ_M)

- **Propriétés mathématiques**
  - Concavité de la fonction de flux
  - Existence et valeur du flux maximal (à ρ_c = ρ_max/2 pour Greenshields)
  - Comportement aux limites: q(0) = q(ρ_max) = 0

- **Unités et dimensions**
  - Cohérence des unités: ρ [véh/km], v [km/h], q [véh/h]
  - Paramètres physiques correctement dimensionnés

#### Tests à effectuer
1. **Test de forme**: Générer la courbe q(ρ) et vérifier sa forme parabolique (Greenshields)
2. **Test de flux maximal**: Identifier le point de flux maximal et vérifier qu'il correspond à ρ_c = ρ_max/2
3. **Tests aux limites**: Vérifier que q(0) = 0 et q(ρ_max) = 0

#### Liste de contrôle
- [ ] La fonction de flux est correctement implémentée
- [ ] Les propriétés de concavité sont respectées
- [ ] Le flux maximal est atteint à la densité critique théorique
- [ ] Les unités physiques sont cohérentes

### 4.3 Examen Approfondi du Schéma Numérique

#### Objectif
Vérifier que le schéma numérique utilisé est correctement implémenté et stable.

#### Points à vérifier
- **Identification du schéma**
  - Type de schéma utilisé (Godunov, Lax-Friedrichs, etc.)
  - Ordre de précision (1er ordre, 2ème ordre)

- **Implémentation des équations de mise à jour**
  - Pour Godunov: ρ_i^(n+1) = ρ_i^n - (Δt/Δx)·(F_{i+1/2}^n - F_{i-1/2}^n)
  - Calcul des flux numériques aux interfaces F_{i+1/2}

- **Condition de stabilité CFL**
  - Vérification de la condition: Δt ≤ Δx/max|λ|, où λ est la vitesse caractéristique
  - Implémentation du calcul dynamique du pas de temps

- **Traitement des conditions aux limites**
  - Conditions aux limites entrantes/sortantes
  - Gestion des discontinuités

#### Tests à effectuer
1. **Test de stabilité**: Vérifier qu'avec différents pas de temps/espace, la solution reste stable
2. **Test de conservation**: Vérifier que la masse totale est conservée au cours de la simulation
3. **Test de convergence**: Vérifier que l'erreur diminue avec le raffinement du maillage
4. **Test sur cas de référence**: Comparer avec des solutions analytiques connues (onde de choc, raréfaction)

#### Liste de contrôle
- [ ] Le schéma numérique est correctement implémenté
- [ ] La condition CFL est respectée
- [ ] La conservation de la masse est assurée
- [ ] Les conditions aux limites sont correctement traitées
- [ ] Le schéma converge vers la solution attendue pour des cas tests de référence

### 4.4 Analyse des Spécificités Multi-Classes

#### Objectif
Vérifier la correcte implémentation des extensions spécifiques au modèle multi-classes.

#### Points à vérifier
- **Structure de données multi-classes**
  - Représentation des différentes classes de véhicules
  - Gestion des tableaux de densités par classe
  - Calcul de la densité totale et des interactions

- **Paramètre de gap-filling**
  - Implémentation de la fonction f_M(ρ_M) = 1 + γ·ρ_M/ρ_M,max
  - Impact sur la vitesse des motos et le flux total

- **Coefficient de ralentissement (qualité de route)**
  - Implémentation du coefficient λ_i(x)
  - Variation spatiale et impact sur les vitesses par classe

- **Interactions entre classes**
  - Implémentation de la fonction f_i(ρ_M) = 1 - β_i·ρ_M/ρ_M,max pour i≠M
  - Effet des motos sur les autres classes de véhicules

#### Tests à effectuer
1. **Test du gap-filling**: Vérifier l'impact de différentes valeurs de γ sur le comportement des motos
2. **Test d'interaction**: Vérifier l'effet du paramètre β sur la vitesse des véhicules non-motos
3. **Test de revêtement**: Vérifier l'impact de variations de λ sur les vitesses et flux
4. **Test de proportion**: Analyser l'effet de différentes proportions de motos sur le flux total

#### Liste de contrôle
- [ ] Les structures de données multi-classes sont correctement implémentées
- [ ] Le paramètre de gap-filling fonctionne comme prévu théoriquement
- [ ] Les effets de la qualité de la route sont correctement modélisés
- [ ] Les interactions entre classes produisent les effets attendus

## 5. Comparaison avec les Résultats Théoriques

### 5.1 Modèle LWR Standard
- Comparer les diagrammes fondamentaux générés avec ceux présentés dans le chapitre "Fondements Théoriques"
- Vérifier les vitesses de propagation des ondes de choc et de raréfaction
- Analyser les résultats des scénarios classiques (feu rouge, onde de choc, raréfaction)

### 5.2 Modèle Multi-Classes
- Comparer les diagrammes fondamentaux multi-classes avec ceux du chapitre "Extension du Modèle"
- Vérifier que le comportement asymptotique correspond aux prédictions théoriques
- Analyser l'impact des paramètres spécifiques (γ, β, λ) sur les résultats

## 6. Documentation des Résultats

Les résultats de chaque étape de vérification seront documentés dans une fiche standardisée :

```
FICHE DE VÉRIFICATION

Fichier examiné : [nom_du_fichier.py]
Date de vérification : [date]
Vérificateur : [nom]

1. LECTURE ANALYTIQUE
   - Conformité aux équations : [Oui/Non/Partielle]
   - Divergences identifiées : [Liste]
   - Commentaires : [Texte]

2. FONCTION DE FLUX
   - Forme correcte : [Oui/Non]
   - Propriétés respectées : [Oui/Non]
   - Unités cohérentes : [Oui/Non]
   - Commentaires : [Texte]

3. SCHÉMA NUMÉRIQUE
   - Schéma identifié : [Type]
   - Implémentation correcte : [Oui/Non]
   - Condition CFL respectée : [Oui/Non]
   - Commentaires : [Texte]

4. SPÉCIFICITÉS MULTI-CLASSES (si applicable)
   - Structure de données adaptée : [Oui/Non]
   - Gap-filling correctement implémenté : [Oui/Non]
   - Coefficient de ralentissement correct : [Oui/Non]
   - Interactions entre classes correctes : [Oui/Non]
   - Commentaires : [Texte]

5. TESTS EFFECTUÉS
   [Liste des tests et résultats]

6. PROBLÈMES IDENTIFIÉS
   [Liste des problèmes et recommandations]

7. CONCLUSION
   [Synthèse de la vérification]
```

## 7. Planification et Suivi

### 7.1 Ordre de Vérification
1. `fundamental_diagram.py`
2. `numerical_methods.py`
3. `base_model.py`
4. `lwr_model.py` 
5. `vc_modulations.py`
6. `multiclass_lwr.py`

### 7.2 Tableau de Suivi

| Fichier | Lecture | Fonction | Schéma | Multi-classes | Statut |
|---------|---------|----------|--------|---------------|--------|
| fundamental_diagram.py | | | N/A | N/A | À faire |
| numerical_methods.py | | | | N/A | À faire |
| base_model.py | | | | N/A | À faire |
| lwr_model.py | | | | N/A | À faire |
| vc_modulations.py | | N/A | N/A | | À faire |
| multiclass_lwr.py | | | | | À faire |

## 8. Révision et Correction

Pour chaque problème identifié, des recommandations de correction seront formulées selon le format :

```
RECOMMANDATION DE CORRECTION

Fichier : [nom_du_fichier.py]
Ligne(s) : [numéros de ligne]
Problème : [Description du problème]
Impact : [Impact sur les résultats ou la stabilité]
Correction proposée : 
```

Un processus de révision itératif sera mis en place pour s'assurer que les corrections n'introduisent pas de nouveaux problèmes.
