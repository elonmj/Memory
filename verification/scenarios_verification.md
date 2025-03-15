# Plan de Vérification de l'Implémentation des Scénarios de Simulation de Trafic

Ce document présente une méthodologie structurée pour vérifier l'implémentation des différents scénarios de trafic dans le cadre du projet de simulation de trafic, avec un accent particulier sur les modèles LWR standard et multi-classes.

## Objectifs de la Vérification

- Valider la cohérence des conditions initiales dans chaque scénario
- Vérifier la correcte configuration des paramètres spécifiques à chaque scénario
- S'assurer que les scénarios produisent les comportements de trafic attendus
- Vérifier l'intégration des paramètres multi-classes dans les scénarios spécialisés

## Méthodologie Générale

Pour chaque scénario, nous appliquons la démarche de vérification suivante :

1. **Analyse statique du code**
   - Vérifier l'héritage depuis `BaseScenario`
   - Analyser les paramètres par défaut définis dans `__init__`
   - Examiner la méthode `get_initial_density()` et sa cohérence avec le scénario

2. **Vérification des conditions initiales**
   - Tracer les profils de densité initiale pour différentes configurations
   - Vérifier la conformité avec les comportements théoriques attendus
   - S'assurer que les discontinuités (le cas échéant) sont correctement positionnées

3. **Vérification des paramètres et de leur influence**
   - Tester différentes valeurs pour les paramètres clés
   - Valider que les changements de paramètres produisent les effets attendus
   - Vérifier les valeurs par défaut et leur pertinence

4. **Tests de simulation**
   - Exécuter le scénario avec différentes configurations
   - Analyser les résultats (densité, vitesse, flux) au cours du temps
   - Comparer avec les comportements théoriques attendus

5. **Vérification des cas limites**
   - Tester avec des valeurs extrêmes des paramètres
   - Vérifier le comportement avec des densités proches de zéro ou maximales
   - S'assurer de l'absence d'erreurs numériques ou de comportements non physiques

## Vérification des Scénarios Spécifiques

### 1. Scénario d'Onde de Raréfaction (`rarefaction_wave.py`)

#### 1.1 Vérification de la structure

```python
# Exemple de vérification de la structure de base
def verify_structure():
    from scenarios.rarefaction_wave import RarefactionWaveScenario
    from scenarios.base_scenario import BaseScenario
    
    # Vérifier l'héritage
    assert issubclass(RarefactionWaveScenario, BaseScenario)
    
    # Instancier avec un modèle factice
    model = object()  # Simulacre de modèle pour le test
    scenario = RarefactionWaveScenario(model)
    
    # Vérifier les paramètres par défaut
    assert 'upstream_density' in scenario.default_params
    assert 'downstream_density' in scenario.default_params
    assert 'transition_point' in scenario.default_params
    
    # Vérifier la présence des méthodes requises
    assert hasattr(scenario, 'get_initial_density')
```

#### 1.2 Vérification des conditions initiales

- **Test de profil** : L'onde de raréfaction doit présenter une transition continue (non abrupte) entre une zone de haute densité et une zone de basse densité
- **Paramètres critiques** : 
  - `upstream_density` : doit être > `downstream_density`
  - `transition_point` : doit être dans l'intervalle [0, domain_length]
  - `buffer_length` : doit être > 0 pour assurer une transition lisse

```python
# Exemple de validation du profil de densité initial
def verify_initial_density_profile():
    import numpy as np
    import matplotlib.pyplot as plt
    from scenarios.rarefaction_wave import RarefactionWaveScenario
    from src.models.lwr_model import LWRModel
    
    # Créer un modèle LWR simple pour le test
    model = LWRModel(v_max=100, rho_max=180)
    
    # Créer un scénario avec des paramètres contrôlés
    scenario = RarefactionWaveScenario(model)
    test_params = {
        'domain_length': 10.0,
        'upstream_density': 0.7,  # 70% de rho_max
        'downstream_density': 0.2,  # 20% de rho_max
        'transition_point': 5.0,  # milieu du domaine
        'buffer_length': 2.0  # largeur de la zone de transition
    }
    
    # Générer la grille spatiale pour le test
    x = np.linspace(0, test_params['domain_length'], 100)
    
    # Calculer le profil de densité initial
    density = [scenario.get_initial_density(xi) for xi in x]
    
    # Vérifier que:
    # 1. La densité à gauche correspond à upstream_density
    assert np.isclose(density[0], test_params['upstream_density'] * model.rho_max)
    
    # 2. La densité à droite correspond à downstream_density
    assert np.isclose(density[-1], test_params['downstream_density'] * model.rho_max)
    
    # 3. La densité est décroissante (caractéristique d'une raréfaction)
    assert all(density[i] >= density[i+1] for i in range(len(density)-1))
    
    # 4. La transition est progressive (non discontinue)
    # Calculer le gradient de densité et vérifier qu'il n'est pas trop élevé
    gradient = np.diff(density)
    assert abs(min(gradient)) < 0.5 * model.rho_max  # Pas de chute brutale
```

#### 1.3 Vérification comportementale

- Exécuter une simulation complète et vérifier que :
  - La zone de transition s'élargit avec le temps (caractéristique d'une onde de raréfaction)
  - Les véhicules accélèrent progressivement en traversant la zone de transition
  - La conservation de la masse est maintenue

### 2. Scénario d'Onde de Choc (`shock_wave.py`)

#### 2.1 Vérification des conditions initiales

- **Test de profil** : Vérifier la présence d'une discontinuité nette entre la zone de faible densité et la zone de haute densité
- **Paramètres critiques** :
  - `upstream_density` : doit être < `downstream_density` (condition nécessaire pour une onde de choc)
  - `transition_point` : position de la discontinuité

```python
# Exemple de vérification des conditions pour une onde de choc
def verify_shock_wave_conditions():
    from scenarios.shock_wave import ShockWaveScenario
    
    # Vérifier que le scénario utilise bien des densités qui produiront un choc
    # (densité upstream inférieure à downstream)
    model = object()  # Simulacre de modèle
    scenario = ShockWaveScenario(model)
    
    assert scenario.default_params.get('upstream_density', 0) < scenario.default_params.get('downstream_density', 1)
```

#### 2.2 Vérification du choc résultant

- Exécuter une simulation et vérifier que :
  - Une onde de choc distincte se forme et se propage vers l'amont (vitesse négative)
  - La vitesse de propagation du choc correspond à la formule théorique :
    ```
    σ = (q2 - q1)/(ρ2 - ρ1)
    ```
    où q1, q2 sont les flux et ρ1, ρ2 les densités de part et d'autre du choc

### 3. Scénario de Feu Rouge (`red_light.py`)

#### 3.1 Vérification des paramètres spécifiques

- **Paramètres critiques** :
  - `light_position` : position du feu sur la route
  - `background_density` : densité du trafic fluide
  - `jam_density` : densité du trafic congestionné au feu
  - `jam_length` : longueur de l'embouteillage initial
  - `green_time` : moment où le feu passe au vert

```python
# Exemple de vérification des paramètres du feu rouge
def verify_red_light_parameters():
    from scenarios.red_light import RedLightScenario
    
    model = object()  # Simulacre de modèle
    scenario = RedLightScenario(model)
    
    # Vérifier la présence et cohérence des paramètres
    params = scenario.default_params
    assert 0 < params['light_position'] < params['domain_length']
    assert 0 < params['background_density'] < 1
    assert params['background_density'] < params['jam_density'] <= 1
    assert params['jam_length'] > 0
    assert params['green_time'] > 0
```

#### 3.2 Vérification du profil initial de densité

- Au temps t=0, vérifier que :
  - La densité est élevée (≈ jam_density) sur une longueur `jam_length` en amont du feu
  - La densité est faible (≈ background_density) ailleurs

#### 3.3 Vérification de la dynamique du feu

- Vérifier que le feu est correctement modélisé :
  - Avant `green_time`, le feu est rouge (densité élevée maintenue à `light_position`)
  - Après `green_time`, le feu devient vert (l'embouteillage commence à se dissiper)
- S'assurer que la méthode `run()` ajoute correctement les informations sur le feu aux résultats

### 4. Scénario d'Embouteillage (`traffic_jam.py`)

#### 4.1 Vérification des paramètres et profil initial

- **Paramètres critiques** :
  - `left_density` et `right_density` : densités de part et d'autre du point de transition
  - `transition_point` : position de la transition
  - `transition_width` : largeur de la zone de transition
  - `smooth_transition` : type de transition (abrupte ou lisse)

```python
# Exemple de vérification du profil d'embouteillage
def verify_traffic_jam_profile():
    import numpy as np
    from scenarios.traffic_jam import TrafficJamScenario
    
    model = object()  # Simulacre de modèle
    scenario = TrafficJamScenario(model)
    
    # Paramètres de test
    test_params = {
        'domain_length': 10.0,
        'left_density': 0.7,
        'right_density': 0.1,
        'transition_point': 0.5,
        'transition_width': 1.0,
        'smooth_transition': True
    }
    
    # Générer la grille spatiale pour le test
    x = np.linspace(0, test_params['domain_length'], 100)
    
    # Tester avec transition lisse
    densities_smooth = [scenario.get_initial_density(xi) for xi in x]
    
    # Tester avec transition abrupte
    test_params['smooth_transition'] = False
    densities_sharp = [scenario.get_initial_density(xi) for xi in x]
    
    # Vérifier que les transitions sont différentes selon le paramètre
    transition_zone = np.where((x > test_params['domain_length']*0.4) & 
                             (x < test_params['domain_length']*0.6))[0]
    
    # La variance des gradients devrait être plus élevée pour une transition abrupte
    gradient_smooth = np.diff([densities_smooth[i] for i in transition_zone])
    gradient_sharp = np.diff([densities_sharp[i] for i in transition_zone])
    
    assert np.var(gradient_sharp) > np.var(gradient_smooth)
```

#### 4.2 Vérification du comportement de la congestion

- Exécuter une simulation et vérifier que :
  - Une onde de choc se forme à l'interface entre les régions de haute et basse densité
  - La vitesse de propagation de l'onde correspond aux prédictions théoriques
  - Le profil de congestion évolue comme attendu

### 5. Scénarios Multi-Classes (`multiclass_scenarios.py`)

#### 5.1 MulticlassRedLightScenario

- **Vérification structurelle** :
  - Comparer avec `RedLightScenario` standard pour s'assurer de l'extension correcte
  - Vérifier que le scénario exige un modèle multi-classes

- **Comportement des motos** :
  - Vérifier que les motos s'accumulent davantage à l'avant du feu
  - Confirmer que le paramètre de densité est correctement modulé pour les motos

```python
# Exemple de vérification du comportement spécifique aux motos
def verify_motorcycle_behavior():
    import numpy as np
    from scenarios.multiclass_scenarios import MulticlassRedLightScenario
    from src.models.multiclass_lwr_model import MulticlassLWRModel
    
    # Créer un modèle multi-classes simple pour le test
    model = MulticlassLWRModel(
        vehicle_classes=[
            {"name": "moto", "v_max": 90, "rho_max": 200},
            {"name": "car", "v_max": 100, "rho_max": 180}
        ],
        n_classes=2
    )
    
    scenario = MulticlassRedLightScenario(model)
    
    # Paramètres de test
    test_params = {
        'light_position': 3.0,
        'jam_length': 0.5
    }
    
    # Points spatiaux à vérifier
    x_near_light = test_params['light_position'] - 0.1  # Près du feu
    x_mid_jam = test_params['light_position'] - test_params['jam_length']/2  # Milieu de l'embouteillage
    x_far = 1.0  # Loin du feu
    
    # Obtenir les densités initiales
    densities_near = scenario.get_initial_density(x_near_light)
    densities_mid = scenario.get_initial_density(x_mid_jam)
    densities_far = scenario.get_initial_density(x_far)
    
    # Vérifier que les motos (indice 0) s'accumulent davantage près du feu
    moto_ratio_near = densities_near[0] / (densities_near[0] + densities_near[1])
    moto_ratio_mid = densities_mid[0] / (densities_mid[0] + densities_mid[1])
    
    assert moto_ratio_near > moto_ratio_mid, "Les motos devraient s'accumuler davantage à l'avant du feu"
    
    # Vérifier le comportement de fond loin du feu
    assert densities_far[0] < densities_near[0], "La densité de motos doit être plus faible loin du feu"
```

#### 5.2 DegradedRoadScenario

- **Paramètres de qualité de route** :
  - `degraded_start` et `degraded_end` : délimitent la section dégradée
  - `quality_good` et `quality_bad` : coefficients de qualité de route

- **Vérification de la fonction de qualité de route** :
  - S'assurer que `get_road_quality()` retourne une fonction qui donne les bonnes valeurs le long du domaine

```python
# Exemple de vérification de la fonction de qualité de route
def verify_road_quality_function():
    from scenarios.multiclass_scenarios import DegradedRoadScenario
    
    model = object()  # Simulacre de modèle multi-classes
    scenario = DegradedRoadScenario(model)
    
    # Obtenir la fonction de qualité de route
    road_quality_func = scenario.get_road_quality()
    
    # Vérifier les valeurs aux points clés
    quality_before = road_quality_func(scenario.default_params['degraded_start'] - 1)
    quality_in = road_quality_func((scenario.default_params['degraded_start'] + 
                                  scenario.default_params['degraded_end']) / 2)
    quality_after = road_quality_func(scenario.default_params['degraded_end'] + 1)
    
    assert abs(quality_before - scenario.default_params['quality_good']) < 1e-10
    assert abs(quality_in - scenario.default_params['quality_bad']) < 1e-10
    assert abs(quality_after - scenario.default_params['quality_good']) < 1e-10
```

#### 5.3 GapFillingScenario

- **Paramètres spécifiques** :
  - `moto_factor` et `car_factor` : facteurs de modulation pour les différentes classes
  - `upstream_density` et `downstream_density` : densités dans les différentes sections
  - `buffer_length` : largeur de la zone de transition
  - `transition_point` : position de la transition

- **Vérification du comportement gap-filling** :
  - S'assurer que les motos ont une densité relativement plus élevée que les autres véhicules
  - Vérifier que le modèle de densité des motos reflète leur capacité à s'infiltrer entre les véhicules plus grands

## Procédure de Vérification Consolidée

Pour une vérification approfondie et systématique de l'ensemble des scénarios, nous recommandons la démarche suivante :

### Étape 1 : Vérification Statique du Code

Parcourir chaque fichier de scénario pour vérifier :
- L'héritage correct depuis `BaseScenario`
- La définition complète des paramètres dans `__init__`
- La documentation adéquate des paramètres et méthodes

### Étape 2 : Validation des Conditions Initiales

Pour chaque scénario :
- Générer et tracer les profils de densité initiale pour différentes configurations de paramètres
- Vérifier que ces profils correspondent aux conditions théoriques attendues
- S'assurer que les transitions (continues ou discontinues selon le scénario) sont correctement implémentées

### Étape 3 : Tests de Simulation

Exécuter des simulations pour chaque scénario avec :
- Différentes configurations de paramètres
- Différents modèles (LWR standard et multi-classes le cas échéant)

Analyser les résultats pour vérifier que :
- Les phénomènes attendus se produisent (ondes de choc, raréfaction, etc.)
- Les comportements spécifiques aux classes de véhicules sont correctement modélisés
- La dynamique temporelle correspond aux prédictions théoriques

### Étape 4 : Analyse de Robustesse

Tester les scénarios dans des conditions limites :
- Valeurs extrêmes des paramètres
- Configurations susceptibles de générer des instabilités numériques
- Transitions très abruptes ou très graduelles

### Étape 5 : Comparaison Inter-Scénarios

Pour les scénarios qui modélisent des phénomènes similaires :
- Comparer les implémentations (standard vs multi-classes)
- Vérifier la cohérence des approches et des résultats

Par exemple, comparer `RedLightScenario` et `MulticlassRedLightScenario` pour s'assurer que le second est une extension cohérente du premier, tout en intégrant correctement les spécificités multi-classes.

## Conclusion

Cette méthodologie de vérification permet d'assurer que les scénarios de simulation de trafic sont correctement implémentés, tant pour le modèle LWR standard que pour son extension multi-classes. En suivant ces étapes, on peut garantir que les conditions initiales, les paramètres et les comportements dynamiques sont conformes aux prédictions théoriques, tout en vérifiant que les spécificités du contexte béninois sont correctement prises en compte dans les scénarios multi-classes.
