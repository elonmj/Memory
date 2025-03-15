# Plan de Vérification des Visualisations

Ce document présente une méthodologie structurée pour vérifier l'implémentation des visualisations dans le projet de simulation de trafic, en se concentrant sur les modèles LWR et LWR multi-classes.

## 1. Objectifs de la Vérification

- Garantir que les visualisations représentent fidèlement les résultats des simulations
- Vérifier la cohérence des options de configuration et de personnalisation
- Assurer la clarté et la lisibilité des visualisations produites
- Valider la compatibilité avec différents scénarios de simulation
- Confirmer la structure appropriée des chemins de sortie pour l'organisation des résultats

## 2. Composants à Vérifier

### 2.1. `simulation_plotter.py`

Module principal de visualisation pour les simulations standard, responsable des graphiques d'évolution de densité, vitesse, flux et des profils spatiaux.

### 2.2. `multiclass_plotter.py`

Extension du plotter principal avec des visualisations spécifiques aux simulations multi-classes.

### 2.3. `fundamental_plotter.py`

Module dédié à la visualisation des diagrammes fondamentaux et des relations densité-vitesse-flux.

### 2.4. `density_profile_plotter.py`

Module spécialisé pour les profils de densité détaillés.

### 2.5. `animator.py`

Module pour la création d'animations des résultats de simulation.

## 3. Procédure de Vérification pour `simulation_plotter.py`

### 3.1. Vérification Structurelle

- [ ] Vérifier la présence de toutes les méthodes essentielles de tracé:
  - `plot_density_evolution`
  - `plot_velocity_evolution`
  - `plot_flow_evolution`
  - `plot_space_profiles`
  - `create_interactive_visualization`
  - `plot_combined_evolution` (méthode mentionnée dans `main.py`)

- [ ] Confirmer que la classe initialise correctement:
  - Le nom du modèle
  - Le répertoire de sortie
  - La création du répertoire si nécessaire

### 3.2. Vérification Fonctionnelle de `plot_density_evolution`

- [ ] Entrée de données:
  - Vérifier que la méthode accepte une matrice 2D `density[temps, espace]`
  - Vérifier le traitement correct des grilles spatiales (`grid_x`) et temporelles (`grid_t`)
  - S'assurer que les paramètres optionnels (`title`, `show`, `save`) fonctionnent correctement

- [ ] Logique de tracé:
  - Vérifier la création correcte du meshgrid pour `pcolormesh`
  - Confirmer l'utilisation de la colormap 'viridis' pour la densité
  - Vérifier l'échelle de couleurs et la barre de couleurs

- [ ] Labels et titres:
  - Vérifier les labels des axes (Position (km), Temps (h))
  - Vérifier l'étiquette de la barre de couleurs (Densité (véh/km))
  - Confirmer que le titre utilise soit le paramètre fourni, soit une valeur par défaut appropriée

- [ ] Chemin de sortie:
  - Vérifier que le fichier est correctement enregistré dans le répertoire de sortie
  - Confirmer que le nom du fichier est dérivé du titre ou utilise une valeur par défaut

### 3.3. Vérification Fonctionnelle de `plot_velocity_evolution`

- [ ] Entrée de données:
  - Vérifier que la méthode accepte une matrice 2D `velocity[temps, espace]`
  - Vérifier le traitement correct des grilles spatiales et temporelles

- [ ] Logique de tracé:
  - Confirmer l'utilisation de la colormap 'coolwarm' pour la vitesse
  - Vérifier que l'échelle de couleurs est appropriée pour les vitesses

- [ ] Labels et titres:
  - Vérifier les labels des axes
  - Vérifier l'étiquette de la barre de couleurs (Vitesse (km/h))

- [ ] Chemin de sortie:
  - Vérifier l'enregistrement correct du fichier

### 3.4. Vérification Fonctionnelle de `plot_flow_evolution`

- [ ] Entrée de données:
  - Vérifier que la méthode accepte une matrice 2D `flow[temps, espace]`

- [ ] Logique de tracé:
  - Confirmer l'utilisation de la colormap 'plasma' pour le flux
  - Vérifier que l'échelle de couleurs est appropriée pour les flux

- [ ] Labels et titres:
  - Vérifier l'étiquette de la barre de couleurs (Flux (véh/h))

### 3.5. Vérification Fonctionnelle de `plot_space_profiles`

- [ ] Entrée de données:
  - Vérifier le traitement correct des matrices de densité, vitesse, flux
  - Confirmer le fonctionnement du paramètre `time_indices`

- [ ] Logique de tracé:
  - Vérifier la création des sous-graphiques pour densité, vitesse et flux
  - Confirmer que les profils sont tracés pour les temps sélectionnés

- [ ] Labels et légendes:
  - Vérifier les labels des axes pour chaque sous-graphique
  - Confirmer que les légendes indiquent correctement les temps correspondants

### 3.6. Vérification Fonctionnelle de `create_interactive_visualization`

- [ ] Entrée de données:
  - Vérifier que la méthode accepte un dictionnaire de résultats contenant densité, vitesse, flux, grilles

- [ ] Logique d'animation:
  - Vérifier la création correcte des sous-graphiques
  - Confirmer que la fonction `update` met correctement à jour les données
  - Vérifier que l'annotation du temps est mise à jour

- [ ] Paramètres d'animation:
  - Vérifier le nombre d'images (`frames`)
  - Confirmer l'intervalle entre les images
  - Vérifier l'utilisation de `blit=True` pour l'efficacité

### 3.7. Vérification de `plot_combined_evolution` (mentionné dans main.py)

- [ ] Confirmer l'existence de cette méthode
- [ ] Vérifier qu'elle crée un graphique combiné avec densité, vitesse et flux

## 4. Procédure de Vérification pour `multiclass_plotter.py`

### 4.1. Vérification Structurelle

- [ ] Confirmer que la classe hérite correctement de `SimulationPlotter`
- [ ] Vérifier la présence des méthodes spécifiques multi-classes:
  - `plot_all`
  - `plot_class_comparison`
  - `plot_flow_density_relationship`
  - `create_multiclass_animation`
  - `plot_spacetime_class_comparison`
  - `create_dashboard` (mentionné dans `motorcycle_impact_analysis.py`)

- [ ] Vérifier l'initialisation des attributs spécifiques:
  - Couleurs par classe
  - Noms des classes

### 4.2. Vérification Fonctionnelle de `plot_all`

- [ ] Vérifier que la méthode génère l'ensemble complet des visualisations:
  - Densité totale, vitesse moyenne, flux total
  - Densités par classe
  - Comparaisons de classes à différents temps
  - Relation flux-densité

### 4.3. Vérification Fonctionnelle de `plot_class_comparison`

- [ ] Vérifier que la comparaison de classes à un temps donné utilise:
  - Les couleurs appropriées par classe
  - Les noms de classes corrects
  - Une légende claire

### 4.4. Vérification Fonctionnelle de `plot_flow_density_relationship`

- [ ] Confirmer que le graphique montre correctement:
  - Les points flux-densité pour chaque classe
  - Les points flux-densité pour le total
  - Une légende appropriée

### 4.5. Vérification Fonctionnelle de `create_multiclass_animation`

- [ ] Vérifier la création de l'animation avec:
  - Des lignes distinctes pour chaque classe
  - Une ligne pour la densité totale
  - Une annotation de temps mise à jour

## 5. Procédure de Vérification pour `fundamental_plotter.py`

### 5.1. Vérification des Méthodes Principales

- [ ] `plot_fundamental_diagrams`:
  - Vérifier le tracé correct du diagramme fondamental
  - Confirmer la présence des trois relations: flux-densité, vitesse-densité, flux-vitesse

- [ ] `compare_fundamental_diagrams`:
  - Vérifier la possibilité de comparer plusieurs modèles
  - Confirmer l'utilisation de couleurs/styles différents pour chaque modèle
  - Vérifier la présence d'une légende

- [ ] `plot_multiclass_fundamental_diagrams`:
  - Vérifier le tracé pour différentes proportions de classes de véhicules
  - Confirmer la présence d'une légende claire pour les proportions

## 6. Tests Pratiques

### 6.1. Test avec Données Synthétiques

- [ ] Créer des données de test simples pour chaque type de visualisation
- [ ] Exécuter chaque méthode de tracé avec ces données
- [ ] Vérifier visuellement les résultats pour la clarté et l'exactitude

### 6.2. Test avec Données de Simulation

- [ ] Exécuter des simulations pour les scénarios clés:
  - Onde de choc
  - Onde de raréfaction
  - Feu rouge
  - Embouteillage
- [ ] Pour chaque scénario, générer l'ensemble des visualisations
- [ ] Vérifier que les visualisations reflètent correctement les phénomènes de trafic attendus

### 6.3. Tests de Cas Limites

- [ ] Tester avec une grille très fine (nombreux points)
- [ ] Tester avec une grille très grossière (peu de points)
- [ ] Tester avec des simulations très longues/courtes
- [ ] Vérifier le comportement avec des données nulles ou constantes

### 6.4. Test des Chemins de Sortie

- [ ] Vérifier la génération de fichiers dans la structure de répertoires attendue
- [ ] Confirmer que les noms de fichiers sont cohérents et descriptifs
- [ ] S'assurer que les fichiers existants ne sont pas écrasés sans avertissement

## 7. Vérification Spécifique pour les Scénarios Multi-classes

### 7.1. Vérification des Visualisations Spécifiques aux Motos

- [ ] Confirmer que les visualisations permettent d'observer:
  - L'effet de gap-filling des motos
  - Les différences de comportement selon le revêtement routier
  - L'impact de la proportion de motos sur le flux global

### 7.2. Vérification des Comparaisons de Classes

- [ ] Vérifier que les comparaisons montrent clairement:
  - Les différences de densité entre classes
  - Les différences de vitesse entre classes
  - Les différences de flux entre classes
  - L'impact des paramètres spécifiques (eta, beta)

## 8. Critères de Réussite

Pour considérer que l'implémentation des visualisations est correcte, les critères suivants doivent être satisfaits:

### 8.1. Critères Techniques

- [ ] Toutes les méthodes de tracé fonctionnent sans erreur
- [ ] Les graphiques sont générés dans les formats attendus
- [ ] Les chemins de sortie sont correctement gérés
- [ ] Les options de personnalisation (titres, couleurs, etc.) fonctionnent correctement

### 8.2. Critères de Qualité Visuelle

- [ ] Les graphiques sont clairs et lisibles
- [ ] Les échelles sont appropriées pour les données visualisées
- [ ] Les couleurs sont significatives et distinctes
- [ ] Les labels et légendes sont informatifs et correctement positionnés

### 8.3. Critères de Pertinence Scientifique

- [ ] Les visualisations permettent d'identifier clairement les phénomènes de trafic attendus
- [ ] Les diagrammes fondamentaux représentent correctement les relations théoriques
- [ ] Les comparaisons entre classes de véhicules sont informatives
- [ ] Les animations montrent clairement l'évolution temporelle des variables

## 9. Plan de Correction

Si des problèmes sont identifiés lors de la vérification:

1. **Documenter précisément le problème**:
   - Description du comportement attendu vs observé
   - Contexte de reproduction (données, paramètres utilisés)
   - Capture d'écran si applicable

2. **Classer le problème par gravité**:
   - Critique: empêche l'utilisation correcte des visualisations
   - Majeur: affecte significativement la qualité ou l'interprétation
   - Mineur: problèmes cosmétiques ou d'optimisation

3. **Proposer une correction**:
   - Modification de code spécifique
   - Ajustement des paramètres par défaut
   - Ajout de nouvelles fonctionnalités si nécessaire

4. **Test de validation**:
   - Vérifier que la correction résout le problème
   - S'assurer qu'elle n'introduit pas de régression
   - Documenter le résultat de la correction

## 10. Annexe: Exemples de Visualisations Attendues

### 10.1. Diagramme Fondamental Attendu

Le diagramme fondamental devrait montrer:
- La relation parabolique flux-densité
- La relation linéaire décroissante vitesse-densité
- Le point critique à ρ = ρ_max/2

### 10.2. Evolution de Densité Attendue pour Onde de Choc

L'évolution de densité pour une onde de choc devrait montrer:
- Une discontinuité nette entre les régions de haute et basse densité
- Une propagation de l'onde vers l'amont avec vitesse constante
- Une conservation de la forme du front d'onde

### 10.3. Comparaison Multi-classes Attendue

La comparaison multi-classes devrait montrer:
- Des profils distincts pour chaque classe de véhicule
- L'effet de gap-filling pour les motos (densité plus élevée)
- L'impact du revêtement sur les différentes classes
