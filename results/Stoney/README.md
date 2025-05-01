### Parameters 
activation model is not activated with these parameters. It would require gamma to be higher. This uses Stoney numpy convolution however different changes for different DTs
```math
\sigma = \begin{cases}
\text{ee: } & 150\\
\text{ie: } & 150\\
\text{ei: } & 150\\
\text{ii: } & 150
\end{cases} \\

W = \begin{cases}
\text{ee: } & 230\\
\text{ie: } & 150\\
\text{ei: } & 150\\
\text{ii: } & 25
\end{cases} \\

k = \begin{cases}
\text{exc: } & 1\\
\text{inh: } & 0.5
\end{cases} \\

\Theta = \Pi \\

\Delta T = 0.001 ms\\

\tau_s = 5 ms

```