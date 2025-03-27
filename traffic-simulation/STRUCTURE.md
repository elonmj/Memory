# Structure du Projet Traffic Simulation

## Description des Composants

### Models
- **base_model.py**: Classe de base abstraite définissant l'interface commune pour tous les modèles de trafic
- **lwr_model.py**: Implémentation standard du modèle LWR (Lighthill-Whitham-Richards) avec relation fondamentale de Greenshields
- **multiclass_lwr.py** et **vc_modulations.py**: Extension du modèle LWR pour le trafic multi-classes, spécifiquement adapté au contexte béninois avec:
  - Support des différentes classes de véhicules (motos, voitures, bus, etc.)
  - Modélisation du comportement gap-filling des motos (vc_modulations.py)
  - Coefficient de ralentissement selon le type de revêtement
  - Modulation des interactions entre classes de véhicules
- **fundamental_diagram.py**: Relations fondamentales entre densité, vitesse et flux incluant:
  - Modèle de Greenshields standard
  - Relations étendues pour le trafic multi-classes
  - Fonctions de modulation pour l'interaction entre classes

### Scenarios
- **base_scenario.py**: Classe de base abstraite pour tous les scénarios
- **multiclass_scenarios.py**: Implémentation des scénarios spécifiques au contexte béninois:
  - Interaction motos-voitures
  - Impact du revêtement routier
  - Comportement aux intersections
- **red_light.py**: Simulation d'un feu rouge (arrêt et redémarrage)
- **shock_wave.py**: Simulation d'une onde de choc (transition brusque de densité)
- **rarefaction_wave.py**: Simulation d'une onde de raréfaction (transition progressive)
- **traffic_jam.py**: Simulation d'embouteillages

### Analysis
- **flow_capacity_analyzer.py**: Analyse de la capacité et du flux:
  - Évaluation des impacts des différentes classes
  - Analyse des effets du revêtement
  - Calcul des seuils de congestion

### Visualization
- **plotter.py**: Création des graphiques de base pour densité, vitesse et flux
- **simulation_plotter.py**: Visualisation générale des résultats de simulation
- **density_profile_plotter.py**: Visualisation détaillée des profils de densité
- **multiclass_plotter.py**: Visualisations spécifiques pour le modèle multi-classes:
  - Distribution des classes de véhicules
  - Interactions entre classes
  - Impact du revêtement routier
- **fundamental_plotter.py**: Visualisation des diagrammes fondamentaux:
  - Relations standard densité-vitesse-flux
  - Relations étendues pour chaque classe
  - Effets de modulation inter-classes
- **animator.py**: Animation des résultats de simulation

### Configuration
- **simulation_config.py**: Configuration centralisée des paramètres:
  - Paramètres de simulation
  - Configuration des classes de véhicules
  - Paramètres d'analyse et de visualisation

### Examples
- **motorcycle_impact_analysis.py**: Analyse de l'impact des motos
- **multiclass_comparison.py**: Comparaison des différentes classes

### Utils
- **numerical_methods.py**: Implémentation des méthodes numériques:
  - Schéma de Godunov pour la résolution
  - Traitement des ondes de choc
  - Conditions aux limites
  - Gestion des discontinuités

### Simulations
Organisation des résultats dans simulations/ :

#### LWR/
Résultats pour le modèle LWR standard:
- **density/**: Évolution spatio-temporelle de la densité
  - Feu Rouge_density.png
  - Onde de Choc_density.png
  - Onde de Raréfaction_density.png
  
- **velocity/**: Évolution spatio-temporelle de la vitesse
  - Feu Rouge_velocity.png
  - Onde de Choc_velocity.png
  - Onde de Raréfaction_velocity.png
  
- **flow/**: Évolution spatio-temporelle du flux
  - Feu Rouge_flow.png
  - Onde de Choc_flow.png
  - Onde de Raréfaction_flow.png
  
- **diagrams/**: Diagrammes fondamentaux
  - diagramme_fondamental.png

#### MultiClass/
Résultats pour le modèle multi-classes:
- **density/**: Densités par classe de véhicule
- **velocity/**: Vitesses spécifiques à chaque classe
- **flow/**: Flux par type de véhicule
- **diagrams/**: Diagrammes fondamentaux étendus

Pour chaque simulation, trois types d'analyses sont générées:
1. **Densité**: Distribution spatiale des véhicules (globale et par classe)
2. **Vitesse**: Variations de vitesse selon le type de véhicule et le revêtement
3. **Flux**: Débit de circulation tenant compte des interactions entre classes

Les diagrammes fondamentaux illustrent les relations théoriques entre ces variables, mettant en évidence les spécificités du trafic béninois comme l'impact des motos et de l'état des routes.

## Correspondance avec le Cadre Théorique

Le code implémente les concepts théoriques développés dans la documentation LaTeX:

- Le modèle LWR standard (`lwr_model.py`) correspond au Chapitre 2 (Fondements Théoriques)
- L'extension multi-classes (`multiclass_lwr.py`) implémente les développements du Chapitre 3 (Extension du Modèle)
- Les scénarios et visualisations reflètent les cas d'étude et validations des Chapitres 4 et 5
- Les méthodes numériques (`numerical_methods.py`) suivent les schémas détaillés dans l'Annexe A
