# Plan de Vérification des Scénarios de Simulation de Trafic

Ce document présente une méthodologie détaillée pour vérifier l'implémentation correcte des modèles LWR et LWR multi-classes dans les scénarios de simulation de trafic routier.

## Table des matières

1. [Introduction](#introduction)
2. [Procédure générale de vérification](#procédure-générale-de-vérification)
3. [Vérification des scénarios à classe unique](#vérification-des-scénarios-à-classe-unique)
   - [Scénario Onde de Choc (ShockWave)](#scénario-onde-de-choc-shockwave)
   - [Scénario Feu Rouge (RedLight)](#scénario-feu-rouge-redlight)
   - [Scénario Embouteillage (TrafficJam)](#scénario-embouteillage-trafficjam)
4. [Vérification des scénarios multi-classes](#vérification-des-scénarios-multi-classes)
   - [Scénario Feu Rouge Multi-classes](#scénario-feu-rouge-multi-classes)
   - [Scénario Route Dégradée](#scénario-route-dégradée)
   - [Scénario Remplissage des Espaces](#scénario-remplissage-des-espaces)
5. [Liste de contrôle finale](#liste-de-contrôle-finale)
6. [Annexes](#annexes)

## Introduction

Ce plan de vérification a pour objectif d'assurer que les scénarios implémentés correspondent fidèlement aux modèles théoriques LWR et LWR multi-classes. Le processus se concentre sur la validation des conditions initiales, des paramètres de simulation, et des comportements spécifiques à chaque type de scénario.

### Objectifs de la vérification

- Confirmer que les conditions initiales sont définies correctement pour chaque scénario
- Vérifier la cohérence physique des paramètres utilisés
- S'assurer que les comportements simulés correspondent aux phénomènes théoriques attendus
- Valider les fonctionnalités spécifiques aux modèles multi-classes

## Procédure générale de vérification

### 1. Lecture structurée du code

Pour chaque fichier de scénario:

1. **Analyse de la structure de classe**:
   - Examiner l'héritage depuis `BaseScenario`
   - Identifier les méthodes surchargées

2. **Examen de la méthode `__init__`**:
   - Identifier les paramètres spécifiques au scénario
   - Noter les valeurs par défaut et leur signification physique

3. **Analyse de la méthode `get_initial_density`**:
   - Comprendre comment les profils de densité sont définis
   - Identifier les équations ou fonctions utilisées pour générer les conditions initiales

4. **Vérification des méthodes supplémentaires**:
   - Examiner les fonctions spécifiques comme `get_road_quality` ou `run`
   - Noter les fonctionnalités particulières au scénario

### 2. Validation des conditions initiales

Pour chaque scénario:

1. **Vérification de la cohérence mathématique**:
   - Les profils de densité sont-ils définis par des fonctions appropriées?
   - Les transitions sont-elles cohérentes avec le type de scénario?

2. **Vérification de la cohérence physique**:
   - Les valeurs de densité sont-elles exprimées en proportion de la densité maximale?
   - Les plages de valeurs sont-elles réalistes (entre 0 et 1 pour les ratios)?

3. **Test de sensibilité**:
   - Comment les conditions initiales varient-elles en fonction des paramètres d'entrée?
   - Les cas limites (densité nulle, densité maximale) sont-ils gérés correctement?

### 3. Analyse des paramètres de scénario

Pour chaque scénario:

1. **Identification des paramètres clés**:
   - Lister les paramètres spécifiques au scénario
   - Comprendre le rôle de chaque paramètre dans la simulation

2. **Vérification des plages de valeurs**:
   - Les valeurs par défaut sont-elles réalistes?
   - Existe-t-il des limites implicites ou explicites pour ces paramètres?

3. **Tests de sensibilité paramétrique**:
   - Comment la simulation réagit-elle à des variations des paramètres?
   - Y a-t-il des valeurs critiques qui modifient qualitativement le comportement?

## Vérification des scénarios à classe unique

### Scénario Onde de Choc (ShockWave)

#### Description du scénario
Le scénario Onde de Choc simule la formation d'une onde de choc lorsque du trafic fluide (faible densité) rencontre du trafic congestionné (haute densité).

#### Paramètres spécifiques à vérifier

| Paramètre | Description | Valeur par défaut | Plage recommandée |
|-----------|-------------|-------------------|-------------------|
| `domain_length` | Longueur du domaine (km) | 20.0 | 5.0 - 50.0 |
| `simulation_time` | Durée de simulation (h) | 0.5 | 0.1 - 2.0 |
| `upstream_density` | Densité ratio en amont | 0.1 | 0.05 - 0.3 |
| `downstream_density` | Densité ratio en aval | 0.7 | 0.5 - 0.9 |
| `transition_point` | Position relative de la transition | 0.5 | 0.2 - 0.8 |

#### Vérification des conditions initiales

1. **Profil de densité initial**:
   - Vérifier que la fonction `get_initial_density` crée correctement une distribution avec une transition abrupte entre `upstream_density` et `downstream_density`
   - La transition doit être située à la position `transition_point * domain_length`

2. **Tests spécifiques**:
   - Vérifier si la transition est correctement positionnée
   - Confirmer que les densités sont correctement multipliées par `rho_max` du modèle

#### Résultats attendus

- Formation d'une onde de choc se propageant vers l'amont (direction négative en x)
- Vitesse de propagation du choc conforme à la théorie: σ = (q₂-q₁)/(ρ₂-ρ₁)
- Conservation de la masse totale des véhicules pendant la simulation

### Scénario Feu Rouge (RedLight)

#### Description du scénario
Le scénario Feu Rouge simule l'accumulation de véhicules à un feu rouge puis leur accélération lorsque le feu passe au vert.

#### Paramètres spécifiques à vérifier

| Paramètre | Description | Valeur par défaut | Plage recommandée |
|-----------|-------------|-------------------|-------------------|
| `domain_length` | Longueur du domaine (km) | 5.0 | 2.0 - 10.0 |
| `simulation_time` | Durée de simulation (h) | 0.25 | 0.1 - 0.5 |
| `light_position` | Position du feu rouge (km) | 3.0 | 1.0 - 4.0 |
| `background_density` | Densité ratio de fond | 0.2 | 0.1 - 0.4 |
| `jam_density` | Densité ratio du bouchon | 0.9 | 0.7 - 0.95 |
| `jam_length` | Longueur du bouchon (km) | 0.5 | 0.2 - 1.0 |
| `green_time` | Moment où le feu passe au vert (h) | 0.05 | 0.01 - 0.1 |

#### Vérification des conditions initiales

1. **Profil de densité initial**:
   - Vérifier que la densité est élevée (`jam_density`) dans la zone entre `light_position - jam_length` et `light_position`
   - Vérifier que la densité est égale à `background_density` ailleurs

2. **Tests spécifiques**:
   - Pour les modèles multi-classes: vérifier la distribution spécifique des motos (accumulées à l'avant)
   - Vérifier la gestion du feu rouge dans la méthode `run`

#### Résultats attendus

- Avant `green_time`: maintien du bouchon au niveau du feu rouge
- Après `green_time`: dissipation progressive du bouchon (onde de raréfaction)
- Pour les modèles multi-classes: démarrage plus rapide des motos que des autres véhicules

### Scénario Embouteillage (TrafficJam)

#### Description du scénario
Le scénario Embouteillage simule la formation et la propagation d'un embouteillage causé par des différences de densité sur différents segments de route.

#### Paramètres spécifiques à vérifier

| Paramètre | Description | Valeur par défaut | Plage recommandée |
|-----------|-------------|-------------------|-------------------|
| `domain_length` | Longueur du domaine (km) | 10.0 | 5.0 - 20.0 |
| `simulation_time` | Durée de simulation (h) | 0.5 | 0.1 - 1.0 |
| `left_density` | Densité ratio côté gauche | 0.7 | 0.5 - 0.9 |
| `right_density` | Densité ratio côté droit | 0.1 | 0.05 - 0.3 |
| `transition_width` | Largeur de la zone de transition (km) | 1.0 | 0.5 - 2.0 |
| `transition_point` | Position relative de la transition | 0.5 | 0.2 - 0.8 |
| `smooth_transition` | Transition progressive (booléen) | True | True/False |

#### Vérification des conditions initiales

1. **Profil de densité initial**:
   - Si `smooth_transition` est True: vérifier que la transition entre `left_density` et `right_density` est progressive (sur une largeur de `transition_width`)
   - Si `smooth_transition` est False: vérifier que la transition est abrupte
   - La transition doit être centrée à la position `transition_point * domain_length`

2. **Tests spécifiques**:
   - Vérifier l'impact du paramètre `smooth_transition` sur le profil initial
   - Tester différentes valeurs de `transition_width` pour confirmer son effet sur la largeur de la transition

#### Résultats attendus

- Formation d'ondes de choc ou de raréfaction selon les densités relatives
- Propagation des ondes à des vitesses conformes à la théorie
- Si `left_density` > `right_density` et l'ensemble des densités est supérieur à la densité critique: propagation d'une onde de choc vers l'amont

## Vérification des scénarios multi-classes

### Scénario Feu Rouge Multi-classes

#### Description du scénario
Extension du scénario Feu Rouge pour les modèles multi-classes, prenant en compte les comportements spécifiques des différentes classes de véhicules.

#### Paramètres spécifiques à vérifier

Les mêmes que pour le scénario Feu Rouge standard, plus:

| Paramètre | Description | Impact attendu |
|-----------|-------------|----------------|
| `vehicle_classes` | Classes de véhicules du modèle | Définit les comportements spécifiques |
| `n_classes` | Nombre de classes | Doit correspondre à la longueur de `vehicle_classes` |

#### Vérification des conditions initiales

1. **Distribution par classe**:
   - Vérifier que la méthode `get_initial_density` retourne bien un tableau de densités par classe
   - Confirmer que les motos (classe 0) ont une densité plus élevée près du feu rouge selon le paramètre `proximity_to_light`

2. **Tests spécifiques**:
   - Valider la formule de calcul de `proximity_to_light` = (x - (light_position - jam_length)) / jam_length
   - Vérifier que `density_factor` pour les motos augmente avec la proximité au feu

3. **Validation multi-classes**:
   - S'assurer que l'implémentation lève une exception si le modèle n'est pas multi-classes (`hasattr(self.model, 'n_classes')`)

#### Résultats attendus

- Distribution non uniforme des motos dans le bouchon (plus concentrées à l'avant)
- Dissipation du bouchon avec des dynamiques différentes selon les classes après le passage au vert
- Les motos devraient redémarrer plus rapidement que les autres véhicules

### Scénario Route Dégradée

#### Description du scénario
Ce scénario simule l'effet d'une section de route dégradée sur les différentes classes de véhicules.

#### Paramètres spécifiques à vérifier

| Paramètre | Description | Valeur par défaut | Plage recommandée |
|-----------|-------------|-------------------|-------------------|
| `domain_length` | Longueur du domaine (km) | 10.0 | 5.0 - 20.0 |
| `simulation_time` | Durée de simulation (h) | 0.2 | 0.1 - 0.5 |
| `density` | Densité ratio uniforme | 0.3 | 0.1 - 0.6 |
| `degraded_start` | Début de la section dégradée (km) | 3.0 | 2.0 - 5.0 |
| `degraded_end` | Fin de la section dégradée (km) | 7.0 | 5.0 - 8.0 |
| `quality_good` | Coefficient de qualité route bonne | 1.0 | 0.9 - 1.0 |
| `quality_bad` | Coefficient de qualité route dégradée | 0.6 | 0.4 - 0.7 |

#### Vérification des conditions initiales

1. **Profil de densité initial**:
   - Confirmer que `get_initial_density` génère une densité uniforme pour toutes les classes
   - Vérifier que la densité est bien multipliée par `rho_max` de chaque classe

2. **Fonction de qualité routière**:
   - Vérifier que `get_road_quality` retourne une fonction qui:
     - Retourne `quality_bad` pour x entre `degraded_start` et `degraded_end`
     - Retourne `quality_good` ailleurs

3. **Validation multi-classes**:
   - S'assurer que le scénario lève une exception si le modèle n'est pas multi-classes

#### Résultats attendus

- Ralentissement des véhicules dans la section dégradée
- Impact différentiel selon les classes (les motos devraient être moins affectées que les voitures)
- Formation possible de congestions à l'entrée de la section dégradée

### Scénario Remplissage des Espaces

#### Description du scénario
Ce scénario teste la capacité des motos à remplir les espaces entre les voitures (comportement de "gap-filling").

#### Paramètres spécifiques à vérifier

| Paramètre | Description | Valeur par défaut | Plage recommandée |
|-----------|-------------|-------------------|-------------------|
| `domain_length` | Longueur du domaine (km) | 20.0 | 10.0 - 30.0 |
| `simulation_time` | Durée de simulation (h) | 1.0 | 0.5 - 2.0 |
| `upstream_density` | Densité ratio en amont | 0.4 | 0.3 - 0.6 |
| `downstream_density` | Densité ratio en aval | 0.3 | 0.1 - 0.4 |
| `transition_point` | Position relative de la transition | 0.5 | 0.3 - 0.7 |
| `buffer_length` | Longueur de la zone tampon (km) | 2.0 | 1.0 - 3.0 |
| `car_factor` | Facteur de densité des voitures | 0.7 | 0.5 - 0.9 |
| `moto_factor` | Facteur de densité des motos | 1.2 | 1.0 - 1.5 |

#### Vérification des conditions initiales

1. **Distribution par classe**:
   - Vérifier que la méthode `get_initial_density` génère des densités différentes pour chaque classe
   - Confirmer que les densités des motos sont multipliées par `moto_factor` et celles des autres véhicules par `car_factor`

2. **Gestion des sections**:
   - Vérifier la transition à `transition_point * domain_length`
   - S'assurer que les densités amont/aval sont correctement appliquées

3. **Validations spécifiques**:
   - Vérifier la gestion des paramètres manquants dans les méthodes `get_initial_density` et `run`
   - Confirmer que les informations de segment sont correctement ajoutées aux résultats

#### Résultats attendus

- Les motos devraient montrer un comportement de "remplissage des espaces" entre les voitures
- La vitesse et le flux des motos devraient être moins impactés par l'augmentation de la densité que ceux des voitures
- La transition entre les sections devrait montrer des dynamiques différentes pour les motos et les autres véhicules

## Liste de contrôle finale

Utiliser cette liste pour une vérification complète de chaque scénario:

1. **Structure et héritage**:
   - [ ] La classe hérite correctement de BaseScenario
   - [ ] Les méthodes nécessaires sont correctement surchargées

2. **Conditions initiales**:
   - [ ] Le profil de densité initial correspond au type de scénario
   - [ ] Les transitions (abruptes ou progressives) sont correctement implémentées
   - [ ] Les densités sont exprimées en proportion de rho_max
   - [ ] Pour les scénarios multi-classes: les densités par classe sont correctes

3. **Paramètres**:
   - [ ] Les paramètres par défaut ont des valeurs réalistes
   - [ ] Les unités des paramètres sont cohérentes (km, h, etc.)
   - [ ] Les paramètres influencent correctement les conditions initiales et la simulation

4. **Fonctions auxiliaires**:
   - [ ] `get_road_quality` est implémentée si nécessaire
   - [ ] `run` ajoute correctement les métadonnées aux résultats

5. **Spécificités multi-classes**:
   - [ ] La vérification du type de modèle est effectuée
   - [ ] Les paramètres spécifiques aux multi-classes sont correctement utilisés
   - [ ] Les comportements de classe spécifiques sont correctement modélisés

## Annexes

### A. Procédures de test recommandées

1. **Tests unitaires**:
   - Tester individuellement les méthodes `get_initial_density`, `get_road_quality`, etc.
   - Vérifier les valeurs retournées pour différentes entrées

2. **Tests d'intégration**:
   - Exécuter les scénarios avec différents paramètres
   - Comparer les résultats avec les résultats théoriques attendus

3. **Tests de sensibilité paramétrique**:
   - Faire varier systématiquement chaque paramètre
   - Observer et documenter l'impact sur les résultats

### B. Équations théoriques de référence

1. **Vitesse de propagation des ondes de choc**:
   ```
   σ = (q₂-q₁)/(ρ₂-ρ₁)
   ```
   où q et ρ sont les flux et densités de part et d'autre du choc.

2. **Relation vitesse-densité de Greenshields**:
   ```
   v(ρ) = v_max * (1 - ρ/ρ_max)
   ```

3. **Flux en fonction de la densité**:
   ```
   q(ρ) = ρ * v(ρ) = v_max * ρ * (1 - ρ/ρ_max)
   ```

4. **Densité critique** (maximisant le flux):
   ```
   ρ_c = ρ_max/2
   ```

### C. Exemples de visualisations pour la vérification

1. **Profils de densité initiale**:
   - Tracer ρ(x,0) pour vérifier les conditions initiales

2. **Diagrammes espace-temps**:
   - Tracer ρ(x,t) avec une échelle de couleur pour visualiser la propagation des ondes

3. **Comparaisons multi-classes**:
   - Tracer les densités par classe sur le même graphique pour observer les comportements différentiels
