# TikZ Traffic Diagrams for Benin Traffic Modeling

This document provides TikZ code for creating visually appealing traffic modeling diagrams specific to your research on Benin's traffic with emphasis on motorcycle flow.

## 1. Fundamental Traffic Diagram (Multiclass)

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.95\textwidth,
    height=0.55\textwidth,
    xlabel={Densité $\dens$ (véh/km)},
    ylabel={Flux $\flow$ (véh/h)},
    domain=0:200,
    samples=100,
    smooth,
    grid=both,
    minor tick num=1,
    minor grid style={gray!10},
    major grid style={gray!25},
    axis lines=middle,
    legend style={at={(0.97,0.97)},anchor=north east,draw=gray!30,fill=white,font=\footnotesize},
    title style={font=\bfseries},
    title={Diagramme Fondamental Multiclasses},
    xmin=0, xmax=260,
    ymin=0, ymax=13000,
    xtick={0,50,100,150,200,250},
    ytick={0,2500,5000,7500,10000,12500},
]
% Cars flow-density curve
\addplot[color=blue, thick] {2000*(1-x/180)*x};
\addlegendentry{Voitures};

% Motorcycles flow-density curve
\addplot[color=red, thick, dashed] {3000*(1-x/240)*x};
\addlegendentry{Motos (Zémidjans)};

% Critical points
\addplot[only marks, mark=*, mark size=3pt, color=blue] coordinates {(90, 8100)};
\node[above left, blue] at (axis cs:90, 8100) {Point critique};

\addplot[only marks, mark=*, mark size=3pt, color=red] coordinates {(120, 10800)};
\node[below right, red] at (axis cs:120, 10800) {Point critique};

% Free flow and congestion regions
\draw[thick, ->, >=stealth, gray] (axis cs:30, 3000) -- (axis cs:80, 7500);
\node[gray, rotate=33] at (axis cs:50, 5000) {Régime fluide};

\draw[thick, ->, >=stealth, gray] (axis cs:140, 7000) -- (axis cs:170, 4000);
\node[gray, rotate=-35] at (axis cs:155, 5500) {Congestion};
\end{axis}
\end{tikzpicture}
\caption{Diagramme fondamental pour différentes classes de véhicules, montrant les relations flux-densité distinctes pour les voitures et les motos (Zémidjans).}
\label{fig:fundamental_diagram}
\end{figure}
```

## 2. Motorcycle Gap-Filling Behavior Visualization

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    scale=1.5,
    car/.style={rectangle, draw, minimum width=35pt, minimum height=18pt, fill=blue!30},
    moto/.style={ellipse, draw, minimum width=15pt, minimum height=8pt, fill=red!30},
    road/.style={very thick, gray!80},
    lane/.style={dashed, gray!60},
]
% Drawing the road
\draw[road] (0,0) -- (10,0);
\draw[road] (0,3) -- (10,3);
\draw[lane] (0,1.5) -- (10,1.5);

% Cars
\node[car] at (1.5,0.75) {Auto};
\node[car] at (4.5,0.75) {Auto};
\node[car] at (3,2.25) {Auto};
\node[car] at (7,2.25) {Auto};

% Motorcycles demonstrating gap-filling
\node[moto] at (2.5,0.75) {M};
\node[moto] at (6,2.25) {M};
\node[moto] at (8,1.5) {M}; % Between lanes
\node[moto] at (5.5,0.95) {M}; % Partial lane change

% Arrows showing movement pattern
\draw[->, very thick, red!70] (3.5,1.2) to[out=30,in=240] (5,1.8);
\draw[->, very thick, red!70] (6.5,0.6) to[out=30,in=210] (7.5,1.4);

% Labels
\node[align=center] at (5,3.5) {\large Gap-Filling et Interweaving des Motos};
\node[align=left] at (9,0.5) {$\eta_M = 0.4$\\$\mu_i = 0.3$};

% Legend
\node[car, scale=0.7, anchor=east] at (1,3.5) {};
\node[anchor=west] at (1.1,3.5) {Voiture};
\node[moto, scale=0.7, anchor=east] at (2.5,3.5) {};
\node[anchor=west] at (2.6,3.5) {Moto};
\end{tikzpicture}
\caption{Représentation du comportement gap-filling des motos (Zémidjans) dans le trafic. Les motos peuvent occuper des espaces entre les voitures et suivre des trajectoires impossibles pour les autres véhicules.}
\label{fig:gap_filling}
\end{figure}
```

## 3. Road Surface Quality Effects on Traffic Flow

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    scale=1.2,
    car/.style={rectangle, draw, minimum width=35pt, minimum height=18pt, fill=blue!30},
    moto/.style={ellipse, draw, minimum width=15pt, minimum height=8pt, fill=red!30},
]
% Define coordinates for the three road segments
\coordinate (start) at (0,0);
\coordinate (mid1) at (4,0);
\coordinate (mid2) at (8,0);
\coordinate (end) at (12,0);

% Draw the three road segments with different textures
% Paved road
\fill[gray!80] (start) rectangle (mid1,0.5);
\node[below] at (2,0) {Route bitumée};
\node[above] at (2,0.5) {$\lambda_{\text{mat},i}=1.0$};

% Dirt road
\fill[brown!60] (mid1) rectangle (mid2,0.5);
\node[below] at (6,0) {Route en terre};
\node[above] at (6,0.5) {$\lambda_{\text{mat},i}=0.7$};

% Paved with potholes (simulated with small circles)
\fill[gray!70] (mid2) rectangle (end,0.5);
\foreach \x in {8.2,8.6,9,9.4,9.8,10.2,10.6,11,11.4,11.8} {
    \foreach \y in {0.1,0.3} {
        \fill[black!80, opacity=0.7] (\x,\y) circle (0.08);
    }
}
\node[below] at (10,0) {Route pavée dégradée};
\node[above] at (10,0.5) {$\lambda_{\text{mat},i}=0.5$};

% Draw border around each segment
\draw[very thick] (start) -- (mid1) -- (mid2) -- (end);
\draw[very thick] (start) -- (start |- 0,0.5) -- (end |- 0,0.5) -- (end) -- cycle;
\draw[very thick] (mid1) -- (mid1 |- 0,0.5);
\draw[very thick] (mid2) -- (mid2 |- 0,0.5);

% Show vehicle speed with arrows
% Paved road
\node[car] at (1,1.5) {Auto};
\draw[->, very thick] (1,1.2) -- (1,0.7);
\draw[->, very thick, blue] (1.3,1.5) -- (2.3,1.5);

\node[moto] at (3,1.5) {M};
\draw[->, very thick] (3,1.2) -- (3,0.7);
\draw[->, very thick, red] (3.3,1.5) -- (4.5,1.5);

% Dirt road
\node[car] at (5,1.5) {Auto};
\draw[->, very thick] (5,1.2) -- (5,0.7);
\draw[->, very thick, blue] (5.3,1.5) -- (5.9,1.5); % Shorter arrow

\node[moto] at (7,1.5) {M};
\draw[->, very thick] (7,1.2) -- (7,0.7);
\draw[->, very thick, red] (7.3,1.5) -- (8.1,1.5); % Moto less affected

% Damaged road
\node[car] at (9,1.5) {Auto};
\draw[->, very thick] (9,1.2) -- (9,0.7);
\draw[->, very thick, blue] (9.3,1.5) -- (9.6,1.5); % Very short arrow

\node[moto] at (11,1.5) {M};
\draw[->, very thick] (11,1.2) -- (11,0.7);
\draw[->, very thick, red] (11.3,1.5) -- (11.9,1.5); % Still mobile

% Title
\node[align=center, font=\large\bfseries] at (6,2.5) {Impact du Type de Revêtement sur la Vitesse};
\end{tikzpicture}
\caption{Illustration de l'effet du revêtement routier sur la vitesse des véhicules au Bénin, modélisé par le coefficient $\lambda_{\text{mat},i}$. Les motos sont moins affectées par la dégradation du revêtement que les voitures.}
\label{fig:road_surface}
\end{figure}
```

## 4. Multiclass Traffic Wave Propagation

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.9\textwidth,
    height=0.55\textwidth,
    view={30}{30},
    xlabel={Position $x$ (km)},
    ylabel={Temps $t$ (min)},
    zlabel={Densité $\dens$ (véh/km)},
    colormap name=viridis,
    grid=both,
    minor grid style={gray!10},
    major grid style={gray!25},
    title style={font=\bfseries},
    title={Propagation d'Onde de Choc dans un Traffic Multiclasses},
    legend pos=outer north east
]

% Generate data point for shockwave
\addplot3[
    surf,
    shader=interp,
    domain=0:10,
    domain y=0:10,
    samples=20,
    samples y=20,
    opacity=0.8
] {
    80*exp(-(x-5-0.3*y)^2/(2*0.8^2))
    + 20
};
\addlegendentry{Voitures};

% Overlay with motorcycle density
\addplot3[
    surf,
    shader=interp,
    domain=0:10,
    domain y=0:10,
    samples=20,
    samples y=20,
    opacity=0.6,
    colormap name=hot
] {
    100*exp(-(x-4-0.5*y)^2/(2*1.2^2))
    + 30
};
\addlegendentry{Motos};

% Add a line showing the shock wave propagation
\addplot3[
    very thick, 
    red!70,
    quiver={u=1, v=0.3, w=0, scale arrows=0.2},
    samples=10
] ({x},{0.3*x},{0});

\node at (axis cs:7,5,20) {\rotatebox{45}{Propagation de l'onde}};

\end{axis}
\end{tikzpicture}
\caption{Propagation d'ondes de choc dans un trafic multiclasses. Les motos (Zémidjans) et les voitures ont des vitesses de propagation d'ondes différentes, créant des interactions complexes dans l'écoulement du trafic.}
\label{fig:shock_waves}
\end{figure}
```



## 5. Intersection Traffic Flow Modeling (Complete)

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    scale=1.2,
    road/.style={line width=12pt, gray!80},
    lane divider/.style={line width=1pt, white, dashed},
    car/.style={rectangle, draw, minimum width=15pt, minimum height=8pt, fill=blue!30},
    moto/.style={circle, draw, minimum size=6pt, fill=red!30},
    traffic light/.style={circle, draw, minimum size=8pt},
    intersection fill/.style={fill=gray!60}
]
% Roads
\draw[road] (-4,0) -- (4,0);
\draw[road] (0,-4) -- (0,4);

% Intersection
\fill[intersection fill] (-0.6,-0.6) rectangle (0.6,0.6);

% Lane dividers
\draw[lane divider] (-4,0) -- (-0.6,0);
\draw[lane divider] (0.6,0) -- (4,0);
\draw[lane divider] (0,-4) -- (0,-0.6);
\draw[lane divider] (0,0.6) -- (0,4);

% Traffic lights
\node[traffic light, fill=green] at (0.8,0.8) {};
\node[traffic light, fill=red] at (-0.8,-0.8) {};
\node[traffic light, fill=red] at (0.8,-0.8) {};
\node[traffic light, fill=red] at (-0.8,0.8) {};

% Vehicles
\node[car] at (-1.5,0.3) {};
\node[car] at (-2.5,0.3) {};
\node[car] at (-3.5,0.3) {};
\node[moto] at (-1.8,-0.3) {};
\node[moto] at (-2.2,-0.3) {};
\node[moto] at (-2.8,-0.3) {};
\node[moto] at (-1.2,0.3) {};

% Vehicles passing through the intersection with green light
\node[car] at (0.3,1.5) {};
\node[car] at (0.3,2.5) {};
\node[moto] at (-0.3,1.2) {};
\node[moto] at (-0.3,1.8) {};
\node[moto] at (-0.3,3.0) {};

% Flow indicators with arrows
\draw[->, thick, red] (-1.5,-0.3) .. controls (-0.8,-0.3) and (-0.3,-0.8) .. (-0.3,-1.5);
\draw[->, thick, blue] (-1.0,0.3) .. controls (-0.5,0.3) and (0.3,0.5) .. (0.3,1.0);

% Flow equations
\node[align=left, anchor=west] at (1.5,3) {
    $\Delta q(t) = \begin{cases}
    g(t) \cdot q_{\max} & \text{feu vert} \\
    0 & \text{feu rouge}
    \end{cases}$
};

% Title and annotations
\node[align=center, font=\large\bfseries] at (0,-4.5) {Modélisation d'une Intersection avec Feux};

% Legend
\draw[thick] (-4,-3) rectangle (-2,-2);
\node[car] at (-3.7,-2.5) {};
\node at (-3.0,-2.5) {Voiture};
\draw[thick] (-2,-3) rectangle (0,-2);
\node[moto] at (-1.7,-2.5) {};
\node at (-1.0,-2.5) {Moto};
\draw[thick] (0,-3) rectangle (2,-2);
\node[traffic light, fill=green] at (0.3,-2.5) {};
\node at (1.3,-2.5) {Feu vert};
\draw[thick] (2,-3) rectangle (4,-2);
\node[traffic light, fill=red] at (2.3,-2.5) {};
\node at (3.3,-2.5) {Feu rouge};

\end{tikzpicture}
\caption{Modélisation d'une intersection avec feux de circulation à Cotonou. L'approche multiclasses permet de représenter les interactions spécifiques entre motos et voitures, avec la source/puits modélisée par $\Delta q(t)$.}
\label{fig:intersection}
\end{figure}
```

## 6. Stochastic Aspects of Traffic Modelling

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    scale=1.2,
    car/.style={rectangle, draw, minimum width=20pt, minimum height=10pt, fill=blue!30},
    moto/.style={circle, draw, minimum size=8pt, fill=red!30},
]
% Set up the axis
\begin{axis}[
    width=0.95\textwidth,
    height=0.55\textwidth,
    xlabel={Densité $\dens$ (véh/km)},
    ylabel={Vitesse $\vel$ (km/h)},
    domain=0:180,
    samples=100,
    grid=both,
    minor tick num=1,
    minor grid style={gray!10},
    major grid style={gray!25},
    legend style={at={(0.03,0.03)},anchor=south west},
    title style={font=\bfseries},
    title={Aspects Stochastiques du Modèle Multiclasses},
    xmin=0, xmax=180,
    ymin=0, ymax=80,
]
% Deterministic velocity-density curve
\addplot[color=blue, thick] {70*(1-x/180)};
\addlegendentry{Relation déterministe (voitures)};

% Scatter plot to represent stochastic behavior
\pgfmathsetseed{1234}
\addplot[only marks, mark=*, blue, mark size=1pt, opacity=0.5] table[row sep=\\,y expr=70*(1-\thisrowno{0}/180)*(1+0.15*rand-0.075), x expr=\thisrowno{0}] {
data\\
0\\5\\10\\15\\20\\25\\30\\35\\40\\45\\50\\55\\60\\65\\70\\75\\80\\85\\90\\
95\\100\\105\\110\\115\\120\\125\\130\\135\\140\\145\\150\\155\\160\\165\\170\\175\\180\\
};

% Motorcycles velocity-density curve
\addplot[color=red, thick, dashed] {60*(1-x/240)};
\addlegendentry{Relation déterministe (motos)};

% Scatter plot for motorcycles
\pgfmathsetseed{5678}
\addplot[only marks, mark=*, red, mark size=1pt, opacity=0.5] table[row sep=\\,y expr=60*(1-\thisrowno{0}/240)*(1+0.25*rand-0.125), x expr=\thisrowno{0}] {
data\\
0\\5\\10\\15\\20\\25\\30\\35\\40\\45\\50\\55\\60\\65\\70\\75\\80\\85\\90\\
95\\100\\105\\110\\115\\120\\125\\130\\135\\140\\145\\150\\155\\160\\165\\170\\175\\180\\
};

% Confidence intervals
\addplot[blue!30, name path=upper_car] {70*(1-x/180)*1.15};
\addplot[blue!30, name path=lower_car] {70*(1-x/180)*0.85};
\addplot[blue!10] fill between[of=upper_car and lower_car];

\addplot[red!30, name path=upper_moto] {60*(1-x/240)*1.25};
\addplot[red!30, name path=lower_moto] {60*(1-x/240)*0.75};
\addplot[red!10] fill between[of=upper_moto and lower_moto];

% Annotations
\node[blue, align=left] at (axis cs:100,45) {$\var{v_{\text{voiture}}} \propto \rho$};
\node[red, align=left] at (axis cs:150,25) {$\var{v_{\text{moto}}} > \var{v_{\text{voiture}}}$};

\end{axis}

% Add vehicles illustrations
\node[car] at (9.5,6.5) {};
\node[moto] at (10.2,6.5) {};

\end{tikzpicture}
\caption{Représentation des aspects stochastiques du modèle montrant la variabilité dans les relations vitesse-densité pour les voitures et les motos. Les motos présentent une plus grande variabilité dans leurs comportements, représentée par des intervalles de confiance plus larges.}
\label{fig:stochastic_aspects}
\end{figure}
```

## 7. Calibration and Validation Process Diagram

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}[
    node distance=1.5cm and 2cm,
    process/.style={rectangle, draw, rounded corners, minimum width=3cm, minimum height=1cm, fill=lightblue!30},
    data/.style={trapezium, draw, trapezium left angle=70, trapezium right angle=110, minimum width=3cm, minimum height=1cm, fill=trafficyellow!30},
    decision/.style={diamond, draw, aspect=2, minimum width=3cm, minimum height=1cm, fill=trafficgreen!20},
    arrow/.style={thick, ->, >=stealth},
    note/.style={rectangle, draw=none, dashed, align=center, font=\small\itshape}
]

% Nodes
\node[data] (raw_data) {Données de terrain Bénin};
\node[process, below=of raw_data] (preprocessing) {Prétraitement};
\node[data, below=of preprocessing] (clean_data) {Données calibration/validation};
\node[process, right=of clean_data] (model) {Modèle LWR Étendu};
\node[process, above=of model] (parameters) {Paramètres initiaux};
\node[decision, below=of clean_data] (split) {Division};
\node[data, below left=of split] (cal_data) {Données calibration};
\node[data, below right=of split] (val_data) {Données validation};
\node[process, right=of cal_data] (cal_process) {Calibration};
\node[process, right=of val_data] (val_process) {Validation};
\node[data, below=of cal_process] (cal_params) {Paramètres calibrés};
\node[decision, below=of val_process] (decision) {Validation \\ réussie?};
\node[process, right=of decision] (refine) {Raffiner le modèle};
\node[process, below=of decision] (final) {Modèle final};

% Connections
\draw[arrow] (raw_data) -- (preprocessing);
\draw[arrow] (preprocessing) -- (clean_data);
\draw[arrow] (parameters) -- (model);
\draw[arrow] (clean_data) -- (split);
\draw[arrow] (split) -- (cal_data);
\draw[arrow] (split) -- (val_data);
\draw[arrow] (cal_data) -- (cal_process);
\draw[arrow] (val_data) -- (val_process);
\draw[arrow] (model) -- (cal_process);
\draw[arrow] (cal_process) -- (cal_params);
\draw[arrow] (cal_params) -- (val_process);
\draw[arrow] (val_process) -- (decision);
\draw[arrow] (decision) -- node[anchor=west] {Non} (refine);
\draw[arrow] (refine) to[out=90,in=0] (model);
\draw[arrow] (decision) -- node[anchor=west] {Oui} (final);

% Notes
\node[note, right=of preprocessing] {Filtrage, normalisation, \\ analyse des valeurs aberrantes};
\node[note, left=of cal_process] {Optimisation: \\ Algorithme génétique};
\node[note, left=of val_process] {Métriques: RMSE, GEH};
\node[note, right=of cal_params] {$v_{i,\max}^0$, $\rho_{i,\max}$, $\eta_M$, $\mu_i$, $\lambda_{\text{mat},i}$};

\end{tikzpicture}
\caption{Processus de calibration et validation du modèle LWR étendu pour le trafic béninois. Le processus itératif permet d'affiner les paramètres spécifiques aux différentes classes de véhicules et aux conditions routières locales.}
\label{fig:calibration_process}
\end{figure}
```

## 8. Material Coefficient Impact Visualization

```latex
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.95\textwidth,
    height=0.55\textwidth,
    view={30}{30},
    xlabel={Coefficient $\lambda_{\text{mat},i}$},
    ylabel={Densité $\dens$ (véh/km)},
    zlabel={Vitesse $\vel$ (km/h)},
    grid=both,
    minor grid style={gray!10},
    major grid style={gray!25},
    title style={font=\bfseries},
    title={Impact du Coefficient de Ralentissement sur la Vitesse},
    colormap name=viridis,
    legend pos=outer north east,
    xtick={0.5,0.6,0.7,0.8,0.9,1.0},
    ytick={0,50,100,150},
    ztick={0,20,40,60},
    ticklabel style={font=\footnotesize}
]

% Generate surface for cars
\addplot3[
    surf,
    shader=interp,
    domain=0.5:1,
    domain y=0:180,
    samples=20,
    samples y=20,
    opacity=0.7,
    colormap name=cool,
] {70*x*(1-y/180)};
\addlegendentry{Voitures};

% Generate surface for motorcycles
\addplot3[
    surf,
    shader=interp,
    domain=0.5:1,
    domain y=0:240,
    samples=20,
    samples y=20,
    opacity=0.7,
    colormap name=hot,
] {60*x*(1-y/240)};
\addlegendentry{Motos};

% Add points for different road surfaces
\coordinate (paved_car) at (axis cs:1.0,90,35);
\coordinate (dirt_car) at (axis cs:0.7,90,24.5);
\coordinate (damaged_car) at (axis cs:0.5,90,17.5);

\coordinate (paved_moto) at (axis cs:1.0,90,37.5);
\coordinate (dirt_moto) at (axis cs:0.7,90,26.25);
\coordinate (damaged_moto) at (axis cs:0.5,90,18.75);

\addplot3[only marks, mark=*, color=blue, mark size=3pt] coordinates {(1.0,90,35) (0.7,90,24.5) (0.5,90,17.5)};
\addplot3[only marks, mark=*, color=red, mark size=3pt] coordinates {(1.0,90,37.5) (0.7,90,26.25) (0.5,90,18.75)};

% Add labels for road surfaces
\node[anchor=south] at (paved_car) {Route bitumée};
\node[anchor=south] at (dirt_car) {Route en terre};
\node[anchor=south] at (damaged_car) {Route dégradée};

\end{axis}
\end{tikzpicture}
\caption{Visualisation 3D de l'impact du coefficient de ralentissement lié au revêtement ($\lambda_{\text{mat},i}$) sur la relation vitesse-densité pour les voitures et les motos. Les différents types de routes au Bénin (bitumée, en terre, dégradée) sont représentés par des points sur les surfaces.}
\label{fig:material_coefficient}
\end{figure}
```
