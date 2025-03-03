# Pretty LaTeX Enhancements for Traffic Modeling Document

This guide presents recommendations for creating a visually appealing LaTeX document using XeLaTeX, with specific focus on traffic modeling content.

## Typography and Font Selection

```latex
% Elegant Typography with XeLaTeX
\usepackage{fontspec}

% Option 1: Classic Academic Look
\setmainfont{Libertinus Serif}[
  Numbers=OldStyle,
  Ligatures=TeX
]
\setsansfont{Libertinus Sans}[Scale=0.95]
\setmonofont{Inconsolata}[Scale=0.9]
\setmathfont{Libertinus Math}

% Option 2: Modern Clean Look
\setmainfont{TeX Gyre Pagella}[
  Numbers=OldStyle,
  Ligatures=TeX
]
\setsansfont{TeX Gyre Heros}[Scale=0.9]
\setmonofont{Fira Mono}[Scale=0.85]
\setmathfont{TeX Gyre Pagella Math}

% Line spacing for better readability
\usepackage{setspace}
\setstretch{1.15} % Slightly more than single spacing
```

## Beautiful Chapter and Section Styling

```latex
\usepackage{titlesec}

% Elegant chapter style
\titleformat{\chapter}[display]
  {\normalfont\huge\bfseries\color{darkblue}}
  {\flushright\normalsize\color{midgray}CHAPITRE\\\Huge\thechapter}
  {20pt}
  {\titlerule[0.5pt]\vspace{6pt}\huge}
  [\vspace{.5ex}\titlerule[0.5pt]]

% Clean section style
\titleformat{\section}
  {\normalfont\Large\bfseries\color{darkblue}}
  {\thesection}
  {0.75em}
  {}

% Elegant subsection style  
\titleformat{\subsection}
  {\normalfont\large\bfseries\color{midblue}}
  {\thesubsection}
  {0.75em}
  {}
```

## Traffic-themed Color Scheme

```latex
\usepackage{xcolor}

% Traffic-related Color Scheme
\definecolor{roadgray}{RGB}{80,80,80}  % Asphalt color
\definecolor{darkblue}{RGB}{0,43,112}  % Professional blue
\definecolor{midblue}{RGB}{0,90,170}   % Medium blue
\definecolor{lightblue}{RGB}{135,206,250} % Light blue
\definecolor{trafficred}{RGB}{200,30,15} % Traffic light red
\definecolor{trafficyellow}{RGB}{240,200,0} % Traffic light yellow
\definecolor{trafficgreen}{RGB}{0,128,0}  % Traffic light green
\definecolor{midgray}{RGB}{120,120,120}  % Gray for secondary text
\definecolor{pagebackground}{RGB}{252,252,250} % Slight off-white for pages

% Set page background color
\pagecolor{pagebackground}
```

## Header and Footer Design

```latex
\usepackage{fancyhdr}
\usepackage{lastpage}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

\fancyhead[LE,RO]{\thepage}
\fancyhead[RE]{\textit{\leftmark}}
\fancyhead[LO]{\textit{\rightmark}}
\fancyfoot[C]{\small Modélisation du Trafic Routier au Bénin}

% Add decorative traffic-inspired element to header
\fancyheadoffset{0.5cm}
\setlength{\headheight}{15pt}
```

## Beautiful Cover Page

```latex
% In titlepage.tex
\begin{titlepage}
\thispagestyle{empty}
\pagecolor{white} % Ensure white background for cover
\begin{center}

% University logo or emblem
\includegraphics[width=4cm]{images/logo-university.png}\\[1cm]

\textsc{\LARGE Université d'Abomey-Calavi}\\[0.5cm]
\textsc{\Large Institut de Mathématiques et de Sciences Physiques}\\[2cm]

% Title with decorative rules
{\color{darkblue}\rule{\textwidth}{1.5pt}}\\[0.45cm]
{\huge\bfseries Modélisation du Trafic Routier au Bénin:\\
\Large Approche Macroscopique et Extension du Modèle LWR}\\[0.45cm]
{\color{darkblue}\rule{\textwidth}{1.5pt}}\\[1.5cm]

% Optional: Traffic-related decorative graphic
\includegraphics[width=10cm]{images/traffic-graphic.pdf}\\[1cm]

% Author information
\begin{flushright}
\large
\emph{Présenté par:}\\
Votre Nom\\[1cm]
\emph{Sous la direction de:}\\
Dr. Directeur de Thèse\\
\end{flushright}

\vfill
% Bottom date and place
{\large\bfseries Cotonou, \today}

\end{center}
\end{titlepage}
\pagecolor{pagebackground} % Reset to document background color
```

## Beautiful Tables

```latex
\usepackage{booktabs}
\usepackage{colortbl}
\usepackage{multirow}
\usepackage{array}

% Example of a well-formatted table
\begin{table}[htbp]
\centering
\caption{Paramètres du modèle par classe de véhicule}
\label{tab:parameters}
\begin{tabular}{>{\raggedright\arraybackslash}p{3cm}>{\centering\arraybackslash}p{2.5cm}>{\centering\arraybackslash}p{2.5cm}>{\centering\arraybackslash}p{2.5cm}}
\toprule
\rowcolor{lightblue!30} 
\textbf{Classe de véhicule} & \textbf{Vitesse libre (km/h)} & \textbf{Densité max. (véh/km)} & \textbf{Coef. d'interfaçage $\mu_i$} \\
\midrule
Voitures particulières & 70 & 180 & 0.3 \\
Motos (Zémidjans) & 60 & 240 & - \\
Taxis & 65 & 180 & 0.4 \\
Camions & 50 & 120 & 0.6 \\
\bottomrule
\end{tabular}
\end{table}
```

## Beautiful Mathematical Equations

```latex
% Enhanced math display
\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{thmtools}
\usepackage{empheq}

% Colorful equation boxes for important results
\newcommand{\highlight}[1]{%
\colorbox{lightblue!15}{$\displaystyle#1$}}

% Example of a highlighted equation
\begin{empheq}[box=\colorbox{lightblue!15}]{align}
\pd{\densi{i}}{t} + \pd{(\densi{i}\veli{i})}{x} = \interS
\end{empheq}

% Theorems with attractive styling
\declaretheoremstyle[
    headfont=\normalfont\bfseries\color{darkblue},
    notefont=\normalfont\bfseries\color{darkblue},
    bodyfont=\normalfont\itshape,
    headpunct={:},
    postheadspace=1em,
    spaceabove=12pt,
    spacebelow=12pt,
    mdframed={
        linewidth=1pt,
        linecolor=darkblue,
        backgroundcolor=lightblue!5,
        roundcorner=5pt
    }
]{prettytheorem}

\declaretheorem[style=prettytheorem,name=Théorème]{theorem}
\declaretheorem[style=prettytheorem,name=Proposition]{proposition}
\declaretheorem[style=prettytheorem,name=Lemme]{lemma}

% For less important definitions, use a simpler style
\declaretheoremstyle[
    headfont=\normalfont\bfseries,
    bodyfont=\normalfont,
    headpunct={:},
    postheadspace=1em,
    spaceabove=6pt,
    spacebelow=6pt,
]{simpledefinition}

\declaretheorem[style=simpledefinition,name=Définition]{definition}
```

## Beautiful Figures and Diagrams

```latex
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=newest}
\usetikzlibrary{arrows.meta,shapes,positioning,shadows,trees,decorations.pathmorphing}

% Example of a beautiful fundamental diagram
\begin{figure}[htbp]
\centering
\begin{tikzpicture}
\begin{axis}[
    width=0.8\textwidth,
    height=0.5\textwidth,
    xlabel={Densité $\dens$ (véh/km)},
    ylabel={Flux $\flow$ (véh/h)},
    domain=0:180,
    samples=100,
    smooth,
    grid=both,
    minor grid style={gray!10},
    major grid style={gray!25},
    axis lines=middle,
    legend style={at={(0.97,0.97)},anchor=north east,draw=gray!30,fill=white,font=\footnotesize},
    title style={font=\bfseries\color{darkblue}},
    title={Diagramme Fondamental du Trafic},
    xmin=0, xmax=200,
    ymin=0,
    enlarge x limits=0.05,
    enlarge y limits=0.05,
    every axis plot/.append style={thick},
    xlabel near ticks,
    ylabel near ticks
]
% Cars
\addplot[color=darkblue,thick] {1500*(1-x/180)*x};
\addlegendentry{Voitures};

% Motorcycles
\addplot[color=trafficred,thick,dashed] {2000*(1-x/240)*x};
\addlegendentry{Motos};

% Critical points
\addplot[color=darkblue,only marks,mark=*,mark size=3pt] coordinates {(90,67500)};
\addplot[color=trafficred,only marks,mark=*,mark size=3pt] coordinates {(120,120000)};
\end{axis}
\end{tikzpicture}
\caption{Diagramme fondamental pour différentes classes de véhicules avec points critiques}
\label{fig:diag_fond}
\end{figure}
```

## Enhanced Lists

```latex
\usepackage{enumitem}

\setlist[itemize]{leftmargin=*,label=\textcolor{darkblue}{$\blacktriangleright$}}
\setlist[enumerate]{leftmargin=*,label=\textcolor{darkblue}{\arabic*.},font=\color{darkblue}\bfseries}

% Example usage
\begin{itemize}
\item Caractéristique du modèle LWR original
\item Extension pour les multi-classes de véhicules
\item Adaptation au contexte béninois
\end{itemize}
```

## Document Layout Improvements

```latex
% Fine-tuning the margins for better readability
\usepackage[
  top=2.5cm,
  bottom=2.5cm,
  left=2.5cm,
  right=2.5cm,
  marginparwidth=1.8cm,
  marginparsep=0.3cm,
  headsep=0.7cm,
  footskip=1.2cm
]{geometry}

% Adjust paragraph spacing
\setlength{\parindent}{1.2em}
\setlength{\parskip}{0.8ex plus 0.2ex minus 0.1ex}

% Add spacing between paragraphs in specific environments
\usepackage{etoolbox}
\BeforeBeginEnvironment{theorem}{\vspace{1ex}}
\AfterEndEnvironment{theorem}{\vspace{1ex}}
```

## Algorithm Styling

```latex
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage{algorithmicx}
\algnewcommand{\LeftComment}[1]{\hfill\(\triangleright\) #1}

% Example usage
\begin{algorithm}
\caption{Calibrage du modèle multi-classes}
\begin{algorithmic}[1]
\State \textbf{Entrée:} Données de trafic $D$, Paramètres initiaux $\theta_0$
\State \textbf{Sortie:} Paramètres calibrés $\theta^*$
\State $\theta \gets \theta_0$ \LeftComment{Initialisation}
\For{$k = 1$ to $K$}
    \State Calculer $L(\theta, D)$ \LeftComment{Fonction de perte}
    \State $\nabla L \gets$ gradient de $L$ par rapport à $\theta$
    \State $\theta \gets \theta - \alpha \nabla L$ \LeftComment{Mise à jour des paramètres}
    \If{$\|\nabla L\| < \epsilon$}
        \State \textbf{break} \LeftComment{Convergence atteinte}
    \EndIf
\EndFor
\State \Return $\theta$
\end{algorithmic}
\end{algorithm}
```

## Side Notes and Margin Notes

```latex
\usepackage{sidenotes}
\usepackage{marginnote}

% Example usage
Ce phénomène est particulièrement observable sur les axes routiers de Cotonou\sidenote{Observations faites sur l'axe Cotonou-Porto-Novo entre 2020 et 2022.} où la densité des motos peut atteindre des valeurs extrêmes.
```

## Creating a Style File

Combine all these customizations into a single style file:

```latex
% benintraffic.sty - create this file in your styles/ directory
\ProvidesPackage{benintraffic}[2023/04/10 Beautiful style for Benin traffic document]

% Load required packages
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{booktabs}
\RequirePackage{thmtools}
\RequirePackage{pgfplots}
\RequirePackage{enumitem}
\RequirePackage{empheq}
\RequirePackage{sidenotes}

% Insert all the styling code from above here
% ...

\endinput
```

Then in your main document:

```latex
\documentclass[a4paper,12pt,twoside]{report}
\usepackage{benintraffic} % All your beautiful styling in one package
```

This approach keeps your main document clean while maintaining consistent styling throughout.
