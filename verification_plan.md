# Plan de Vérification des Simulations de Trafic

Ce plan détaille les étapes nécessaires pour vérifier le code de simulation de trafic, en se concentrant sur les sorties visuelles et les mesures quantitatives pour différents scénarios. L'objectif principal est de s'assurer que les simulations reproduisent fidèlement les phénomènes théoriques de la dynamique du trafic et que les résultats sont validés non seulement visuellement mais aussi par des métriques quantifiables.

**Tableau Récapitulatif des Scénarios et Métriques de Vérification**

| Scénario                     | Modèle      | Commande d'Exécution                                     | Chemin du Graphique                                                                 | Métriques Quantitatives Clés                                                                 |
| :--------------------------- | :---------- | :------------------------------------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| Onde de Raréfaction          | LWR         | `python traffic-simulation/main.py --model lwr --scenario rarefaction --plot basic` | `simulations/LWR/rarefaction/rarefactionwave_combined.png`                                  | Vitesse de l'onde de raréfaction                                                              |
| Onde de Choc               | LWR         | `python traffic-simulation/main.py --model lwr --scenario shock --plot basic`     | `simulations/LWR/shock/shockwave_combined.png`                                      | Vitesse de l'onde de choc                                                                   |
| Feu Rouge                    | LWR         | `python traffic-simulation/main.py --model lwr --scenario redlight --plot basic`  | `simulations/LWR/redlight/redlight_(light_turns_green_at_t=0.05h)_combined.png`            | Capacité de flux maximal après le feu vert                                                     |
| Embouteillage                | LWR         | `python traffic-simulation/main.py --model lwr --scenario trafficjam --plot basic`  | `simulations/LWR/trafficjam/trafficjam_combined.png`                                    | Plage de densité et de vitesse dans l'embouteillage                                             |
| Feu Rouge Multi-Classes      | Multi-Classes | `python traffic-simulation/main.py --model multiclass --scenario redlight --plot all` | `simulations/MULTICLASS/redlight/redlight_combined.png` <br> `simulations/MULTICLASS/redlight/redlight_-_class_0_density.png` <br> `simulations/MULTICLASS/redlight/redlight_-_class_1_density.png` | Comparaison des flux et densités par classe                                                     |
| Route Dégradée Multi-Classes | Multi-Classes | `python traffic-simulation/main.py --model multiclass --scenario degraded --plot all` | `simulations/MULTICLASS/degraded/degradedroad_combined.png` <br> `simulations/MULTICLASS/degraded/degradedroad_-_class_0_density.png` <br> `simulations/MULTICLASS/degraded/degradedroad_-_class_1_density.png` | Réduction de vitesse et augmentation de densité dans la zone dégradée par classe                 |
| "Gap Filling" Multi-Classes  | Multi-Classes | `python traffic-simulation/main.py --model multiclass --scenario gapfilling --plot all` | `simulations/MULTICLASS/gapfilling/gapfilling_combined.png` <br> `simulations/MULTICLASS/gapfilling/gapfilling_-_class_0_density.png` <br> `simulations/MULTICLASS/gapfilling/gapfilling_-_class_1_density.png` | Uniformité de la distribution spatiale des motos vs. voitures                                    |

## I. Scénarios Basiques LWR

### A. Onde de Raréfaction

**Contexte Théorique:** Une onde de raréfaction se produit lors de la transition d'une haute à une faible densité.

**Métriques Quantitatives:**
- Vitesse de l'onde de raréfaction (m/s)
- Gradient de densité maximal admissible
- Vitesse maximale atteinte

**Critères de Validation:**
- [x] **Conditions Nécessaires:**
    - [ ] Transitions douces et continues
    - [ ] Vitesse de l'onde ± 10% de la valeur théorique
    - [ ] Gradient de densité < 0.1 véh/m/m
- [x] **Conditions Suffisantes:**
    - [ ] Conservation de la masse vérifiée
    - [ ] Vitesses physiquement plausibles (0-120 km/h)

### B. Onde de Choc

**Métriques Quantitatives:**
- Vitesse de propagation de l'onde de choc
- Amplitude du saut de densité
- Ratio flux/densité avant/après le choc

**Critères de Validation:**
- [x] **Conditions Nécessaires:**
    - [ ] Discontinuité nette et propagation vers l'amont
    - [ ] Vitesse de l'onde conforme à Rankine-Hugoniot
    - [ ] Conservation du flux à travers le choc
- [x] **Conditions Suffisantes:**
    - [ ] Stabilité de la discontinuité
    - [ ] Pas d'oscillations numériques

### C. Feu Rouge

**Métriques Quantitatives:**
- Temps de formation de l'embouteillage
- Capacité de flux après passage au vert
- Vitesse de dissipation de la congestion

**Critères de Validation:**
- [x] **Phase Rouge:**
    - [ ] Densité maximale atteinte
    - [ ] Flux nul au feu
    - [ ] Propagation correcte de l'onde de congestion
- [x] **Phase Verte:**
    - [ ] Reprise du flux conforme au diagramme fondamental
    - [ ] Dissipation complète de l'embouteillage

### D. Embouteillage

**Métriques Quantitatives:**
- Densité dans l'embouteillage (proche de ρ_max)
- Vitesse résiduelle (proche de 0)
- Temps de persistance

**Critères de Validation:**
- [x] **Formation:**
    - [ ] Transition nette vers l'état congestionné
    - [ ] Densité > 80% de ρ_max
    - [ ] Vitesse < 5 km/h
- [x] **Evolution:**
    - [ ] Stabilité temporelle
    - [ ] Propagation physiquement cohérente

## II. Scénarios Multi-Classes

### A. Feu Rouge Multi-Classes

**Métriques Quantitatives:**
- Ratio des densités motos/voitures
- Différentiel de vitesse entre classes
- Capacité de flux par classe

**Critères de Validation:**
- [x] **Formation de l'Embouteillage:**
    - [ ] Densités différenciées par classe
    - [ ] Structure spatiale cohérente
- [x] **Dissipation:**
    - [ ] Reprise plus rapide des motos
    - [ ] Respect des ratios de flux

### B. Route Dégradée

**Métriques Quantitatives:**
- Réduction de vitesse par classe
- Augmentation de densité locale
- Impact sur le flux total

**Critères de Validation:**
- [x] **Impact sur les Voitures:**
    - [ ] Réduction significative de la vitesse
    - [ ] Augmentation notable de la densité
- [x] **Impact sur les Motos:**
    - [ ] Réduction modérée de la vitesse
    - [ ] Adaptation plus souple

### C. Gap Filling

**Métriques Quantitatives:**
- Écart-type de la distribution spatiale
- Taux d'occupation des espaces libres
- Efficacité de l'insertion

**Critères de Validation:**
- [x] **Distribution Spatiale:**
    - [ ] Plus grande uniformité des motos
    - [ ] Conservation des proportions globales
- [x] **Dynamique:**
    - [ ] Insertions fluides
    - [ ] Stabilité du flux mixte

## Conclusion

La vérification systématique de ces critères quantitatifs et qualitatifs permettra d'assurer la validité physique et numérique des simulations. Les métriques proposées fournissent des seuils objectifs pour l'évaluation des résultats, tout en maintenant une cohérence avec les phénomènes physiques modélisés.