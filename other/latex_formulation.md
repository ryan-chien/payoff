## Latex Formulation
$$
\[min\sum_{i=0}^{N}\sum_{t=0}^{Z}D_i,_t + M_i,_t\]
\[P_i,_0 = P^*\]
\[P_i,_Z=0 \forall i\]
\[P_i,_t = (1+\frac{1}{12}R_i)P_i,_{t-1} - D_i,_{t-1} \medskip \forall \medskip i,t\]
\[\sum_{i=0}^{N}D_i,_t \medskip \leq B \medskip \forall t\]
\[M_i,_t \geq \frac{P_i,_t}{P_i,_0} \medskip \forall \medskip i,t\]
\[D_i,_t \geq F_iM_i,_t \medskip \forall \medskip i,t\]
$$