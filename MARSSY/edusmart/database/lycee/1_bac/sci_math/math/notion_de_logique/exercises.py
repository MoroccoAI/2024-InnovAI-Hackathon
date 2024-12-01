exercises = [
    {
        "partie_name": "Proposition - fonction propositionnelle",
        "exos": [
            {
                "difficulty": "easy",
                "content": r"""\noindent\textbf{1.} La phrase : « Les nombres positifs sont des entiers naturels » est-elle une proposition ? Justifier. \\

\noindent\textbf{2.} Déterminer la valeur de vérité de chacune des propositions suivantes :
\begin{itemize}
    \item \textbf{P :} « $\frac{\pi}{2} \in \mathbb{Q}$ »
    \item \textbf{Q :} « $\left( \sqrt{\frac{3+\sqrt{5}}{2}} - \sqrt{\frac{3-\sqrt{5}}{2}} \right)^2 = 1$ »
    \item \textbf{R :} « $\cos \frac{\pi}{7} > 1$ »
    \item \textbf{S :} « Les solutions de l'équation $2018x^2 - 2017x - 1 = 0$ sont $1$ et $-\frac{1}{2018}$. »
\end{itemize}""",
            },
            {
                "difficulty": "medium",
                "content": r"""\noindent On considère la fonction propositionnelle : $P(x; y) : « (x; y) \in \mathbb{R}^2 ; 2x - 3y = 7 »$ \\

\noindent\textbf{1.} Déterminer l'ensemble des valeurs de la variable $(x; y)$ pour lesquelles $P(x; y)$ soit vraie. \\

\noindent\textbf{2.} Dans chacun des cas suivants, déterminer l'ensemble des nombres réels $S$, pour que chaque fonction propositionnelle soit une proposition vraie :

\begin{align*}
A(x) & : « x \in \mathbb{R} ; 3x^2 - 2x - 65 = 0 » \\
B(x) & : « x \in \mathbb{R} ; 5x^2 - 2\sqrt{15}x + 3 = 0 » \\
C(x) & : « x \in \mathbb{R} ; x^3 - 6x + 7 = 0 » \\
D(x) & : « x \in \mathbb{R} ; -x^2 + x + 6 \geq 0 » \\
P(x) & : « x \in \mathbb{R} ; (2 \sin x - 1) \cos x = 0 » \\
Q(x) & : « x \in [-\pi; \pi] ; \sin(x) \cos(x) \geq 0 »
\end{align*}""",
            },
        ],
    },
    {
        "partie_name": "Quantificateurs",
        "exos": [
            {
                "difficulty": "easy",
                "content": r"""\noindent\textbf{1.} Déterminer la valeur de vérité de chacune des propositions suivantes :

\begin{align*}
Q_1 & : « (\exists x \in \mathbb{R}) ; x^2 + x + 1 = 0 » \\
Q_2 & : « (\exists x \in \mathbb{R}) ; x^2 + x + 1 > 0 » \\
Q_3 & : « (\exists x \in \mathbb{N}) ; \sqrt{x^2 + 3} = 2x - 4 » \\
Q_4 & : « (\exists x \in \mathbb{R}) \; (\forall y \in \mathbb{R}) ; x \leq y » \\
Q_5 & : « (\exists x \in \mathbb{R}^*) \; (\forall y \in \mathbb{Z}^*) ; x^y = 1 » \\
Q_6 & : « (\forall x \in \mathbb{R}) \; (\exists y \in \mathbb{R}) ; x \leq y » \\
Q_7 & : « (\forall x \in \mathbb{R}) \; (\forall y \in \mathbb{R}) ; x^2y^2 > xy »
\end{align*}""",
            },
        ],
    },
    {
        "partie_name": "Opérations sur les propositions",
        "exos": [
            {
                "difficulty": "easy",
                "content": r"""\noindent\textbf{1.} Déterminer la valeur de vérité de chacune des propositions suivantes :

\begin{align*}
Q_1 & : « (\exists x \in \mathbb{R}) ; x^2 + x + 1 = 0 » \\
Q_2 & : « (\exists x \in \mathbb{R}) ; x^2 + x + 1 > 0 » \\
Q_3 & : « (\exists x \in \mathbb{N}) ; \sqrt{x^2 + 3} = 2x - 4 » \\
Q_4 & : « (\exists x \in \mathbb{R}) \; (\forall y \in \mathbb{R}) ; x \leq y » \\
Q_5 & : « (\exists x \in \mathbb{R}^*) \; (\forall y \in \mathbb{Z}^*) ; x^y = 1 » \\
Q_6 & : « (\forall x \in \mathbb{R}) \; (\exists y \in \mathbb{R}) ; x \leq y » \\
Q_7 & : « (\forall x \in \mathbb{R}) \; (\forall y \in \mathbb{R}) ; x^2y^2 > xy »
\end{align*}""",
            },
        ],
    },
    {
        "partie_name": "Opérations sur les propositions",
        "exos": [
            {
                "difficulty": "medium",
                "content": r"""\noindent\textbf{1.} En utilisant un raisonnement par contre-exemple, montrer que les propositions suivantes sont fausses :

\begin{align*}
P_1 & : « (\forall x \in \mathbb{R}^*) \; x + \sqrt{x} \geq 2 » \\
P_2 & : « (\forall x \in \mathbb{R}) \; (\forall y \in \mathbb{R}) \; 2x - 4y \neq 5 » \\
P_3 & : « (\forall x \in \mathbb{R}^*) \; x + \frac{1}{x} \geq 2 » \\
P_4 & : « (\forall x \in \mathbb{R}^+) \; (\forall y \in \mathbb{R}^+) \; x + y \geq \sqrt{x} + \sqrt{y} » \\
P_5 & : « (\forall x \in ]0; 1]) \; \frac{-2x}{x^2(1-x^2)} < 1 » \\
P_6 & : « (\forall \alpha \in ]0; 1]) \; (\forall \beta \in ]0; 1]) \; \frac{1}{\alpha} + \frac{1}{\beta} < 1 - \alpha \beta »
\end{align*}""",
            },
            {
                "difficulty": "medium",
                "content": r"""\noindent Soit $P$ une proposition.

\begin{enumerate}
    \item Montrer que la proposition $\overline{(P \text{ ou } P)}$ est fausse.
\end{enumerate}

\noindent Soit $a$ et $b$ deux réels de l'intervalle $]4; +\infty[$, et on considère les deux équations :
\[
(E) : x^2 + ax + b = 0 \quad \text{et} \quad (F) : x^2 + bx + a = 0
\]

\noindent Soit $\Delta_1$ le discriminant de $(E)$ et $\Delta_2$ celui de $(F)$, et les propositions :
\[
P_1 : « \Delta_1 \geq 0 » \quad \text{et} \quad P_2 : « \Delta_2 \geq 0 »
\]

\begin{enumerate}
    \setcounter{enumi}{1}
    \item Montrer que la proposition $(P_1 \text{ ou } P_2)$ est vraie.
\end{enumerate}""",
            },
            {
                "difficulty": "medium",
                "content": r"""\noindent Soit $P$ une proposition.

\begin{enumerate}
    \item Montrer que la proposition $\overline{(P \text{ et } P)}$ est vraie.

    \item Déterminer les réels $x$ et $y$ tels que : 
    \[
    (y = 3x - 1 \text{ et } x^2 - x = 0).
    \]

    \item En utilisant la distributivité de la conjonction logique par rapport à la disjonction logique, résoudre dans les systèmes suivants :
    \[
    (S_1) : 
    \begin{cases} 
    x^2 - y^2 = 0 \\
    2x^2 + y^2 = 3
    \end{cases}
    \]
    \[
    (S_2) : 
    \begin{cases} 
    xy - x + y = 1 \\
    2x^2 - xy - y = 0
    \end{cases}
    \]
    \[
    (S_3) : 
    \begin{cases} 
    4x^2 - y^2 = 0 \\
    (x - 2)(y - 6) = 0
    \end{cases}
    \]

    \item Soit $x$ et $y$ deux réels tels que $x \geq 1$ et $y \geq 1$. Montrer que :
    \[
    \sqrt{x - 1} + \sqrt{y - 1} \leq xy.
    \]

    \item Déterminer le domaine de définition de la fonction $f$ définie par :
    \[
    f(x) = \sqrt{x^2 - 1} + \frac{x}{2x - 3}.
    \]
\end{enumerate}""",
            },
        ],
    },
    {
        "partie_name": "Lois logiques et raisonnements",
        "exos": [
            {
                "difficulty": "easy",
                "content": r"""\noindent Soit $P$ et $Q$ deux propositions.

\begin{enumerate}
    \item Montrer que les propositions suivantes sont des lois logiques :
    \[
    P \Rightarrow (Q \Rightarrow P)
    \]
    \[
    P \Rightarrow (\overline{P} \Rightarrow Q)
    \]
    \[
    (\overline{Q} \text{ ou } P) \text{ ou } (Q \text{ ou } \overline{P})
    \]
    \[
    (P \Leftrightarrow Q) \Leftrightarrow \big[(P \text{ et } Q) \text{ ou } (\overline{P} \text{ et } \overline{Q})\big]
    \]
\end{enumerate}""",
            },
            {
                "difficulty": "medium",
                "content": r"""\noindent Soit $P$ et $Q$ deux propositions.

\begin{enumerate}
    \item Déterminer la négation des propositions suivantes :
    \[
    P : « (\exists x \in \mathbb{R}) \; 0 \leq x < 1 »
    \]
    \[
    Q : « (\forall x \in \mathbb{R}) \; (x^2 = 1 \Rightarrow x = 1) »
    \]
    \[
    R : « (\forall a \in \mathbb{R}) \; (|a + 1| \leq 2 \Rightarrow a \geq -3) »
    \]
    \[
    S : « (\forall x \in \mathbb{R}) \; (\forall y \in \mathbb{R}^+) \; (x^2 \leq y^2 \Leftrightarrow -y \leq x \leq y) »
    \]
\end{enumerate}""",
            },
        ],
    },
]
