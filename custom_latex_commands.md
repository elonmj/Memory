# Custom LaTeX Commands for Traffic Modeling

These custom commands are specifically designed for your traffic modeling document to ensure consistent notation throughout and make the equations more readable.

```latex
% --- Traffic Flow Variables ---
% Basic variables
\newcommand{\dens}{\rho}                  % Traffic density
\newcommand{\vel}{v}                      % Traffic velocity
\newcommand{\flow}{q}                     % Traffic flow

% Indexed variables (for multiclass model)
\newcommand{\densi}[1]{\rho_{#1}}         % Density of class i
\newcommand{\veli}[1]{v_{#1}}             % Velocity of class i
\newcommand{\flowi}[1]{q_{#1}}            % Flow of class i
\newcommand{\densM}{\rho_{\text{M}}}      % Motorcycle density
\newcommand{\velM}{v_{\text{M}}}          % Motorcycle velocity
\newcommand{\flowM}{q_{\text{M}}}         % Motorcycle flow

% Maximum values
\newcommand{\maxdens}{\rho_{\text{max}}}  % Maximum density
\newcommand{\maxvel}{v_{\text{max}}}      % Maximum velocity
\newcommand{\maxdensM}{\rho_{\text{M,max}}} % Maximum motorcycle density
\newcommand{\maxveli}[1]{v_{{#1},\text{max}}^0} % Free flow speed for class i

% Parameters
\newcommand{\matcoef}[1]{\lambda_{\text{mat},{#1}}} % Material coefficient for class i
\newcommand{\modM}[1]{f_{\text{M},{#1}}} % Motorcycle modulation function
\newcommand{\etaM}{\eta_{\text{M}}}      % Gap-filling coefficient
\newcommand{\mui}[1]{\mu_{#1}}           % Interweaving coefficient

% --- Calculus Operations ---
\newcommand{\pd}[2]{\frac{\partial #1}{\partial #2}} % Partial derivative
\newcommand{\pdd}[2]{\frac{\partial^2 #1}{\partial #2^2}} % Second partial derivative
\newcommand{\pdm}[3]{\frac{\partial^2 #1}{\partial #2 \partial #3}} % Mixed partial derivative

% --- Equation References ---
\newcommand{\eqref}[1]{(\ref{#1})}        % Reference to equation

% --- Special Functions and Sets ---
\newcommand{\RR}{\mathbb{R}}              % Real numbers
\newcommand{\real}{\mathbb{R}}            % Alternative for real numbers
\newcommand{\expect}[1]{\mathbb{E}\left[#1\right]} % Expected value
\newcommand{\var}[1]{\text{Var}\left(#1\right)} % Variance

% --- Optimization and Analysis ---
\newcommand{\argmin}{\text{arg\,min}}     % Argument minimum
\newcommand{\argmax}{\text{arg\,max}}     % Argument maximum
\newcommand{\minimize}{\text{minimize}}   % Minimize
\newcommand{\maximize}{\text{maximize}}   % Maximize
\newcommand{\rmse}{\text{RMSE}}           % Root Mean Square Error
\newcommand{\mae}{\text{MAE}}             % Mean Absolute Error

% --- Traffic-Specific Terms ---
\newcommand{\deltaQ}{\Delta q}            % Flow variation at intersections
\newcommand{\greenT}{g(t)}                % Green time function
\newcommand{\interS}{S_i(x,t)}            % Source/sink term for class i

% --- Document Organization ---
\newcommand{\eqnlabel}[1]{\label{eq:#1}}  % Label for equations
\newcommand{\figlabel}[1]{\label{fig:#1}} % Label for figures
\newcommand{\tablabel}[1]{\label{tab:#1}} % Label for tables
\newcommand{\secref}[1]{Section~\ref{sec:#1}} % Reference to section
```

## Example Usage in Your Document

Here's how you might use these commands in your traffic modeling document:

```latex
\begin{equation}
\pd{\densi{i}}{t} + \pd{(\densi{i} \veli{i})}{x} = \interS
\eqnlabel{conservation_i}
\end{equation}

The velocity of class $i$ vehicles is given by:

\begin{equation}
\veli{i} = \matcoef{i} \maxveli{i} \left(1 - \frac{\sum_{j=1}^{N} \densi{j}}{\maxdens}\right) \times \modM{i}(\densM)
\eqnlabel{velocity_i}
\end{equation}

Where $\modM{i}(\densM)$ represents the motorcycle modulation function:

\begin{equation}
\modM{M}(\densM) = 1 + \etaM \frac{\densM}{\maxdensM} \quad \text{(for motorcycles)}
\eqnlabel{mod_M}
\end{equation}

\begin{equation}
\modM{i}(\densM) = 1 - \mui{i} \frac{\densM}{\maxdensM} \quad \text{(for other vehicle classes)}
\eqnlabel{mod_others}
\end{equation}
```

Including these commands in a custom style file will ensure consistent notation throughout your document and make complex mathematical expressions more readable and maintainable.
