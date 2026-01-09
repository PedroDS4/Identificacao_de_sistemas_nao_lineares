##**Identificação de Sistemas Não Lineares**
Os sistemas lineares estão presentes em muitos campos de estudo, e muitas vezes eles são assumidos mesmo em modelos não lineares, para simplificação e aplicação de alguns tipos de modelagem, como a modelagem de Laplace ou de fourier.

Os sisteams lineares são caracterizados desse jeito, porque a equação diferencial que rege a dinâmica do sistema tem coeficientes constantes, e assim a saída do sistema pode ser modelada como a convolução da entrada com a resposta ao impulso do mesmo.


Porém, nem sempre a assunção de um sistema ser linear é verdadeira, assim, as vezes é preciso capturar a não linearidade e suas características para que uma precisão seja alcançada para determinada aplicação.


Nesse contexto, a identificação de sistemas não lineares entra, e com ela, é possível, utilizando aprendizado de máquina, capturar a dinâmica não linear de um sistema.


Considere um sistema dada pela equação

$$
\ddot{y}(t) = a_1 \dot{y}(t) + a_0 y(t) + x(t)  
$$

ou ainda em forma de equação de diferenças, temos

$$
y[k+2] = a_1 y[k+1] + a_0 y[k] + x[k]
$$

se os coeficientes $a_1$ e $a_0$ são constantes, o sistema é linear, porém, uma regra geral pra sistemas não lineares pode ser da forma

$$
y[k] = f(y[k-1],y[k-2],x[k],x[k-1])
$$

aqui consideramos causalidade e também que dependem de poucos atrasos no tempo.

Nomeando ainda, todas as variáveis dependentes como uma só, na forma matricial dada por

$$
\mathbf{U}[k] = (y[k-1],y[k-2],x[k],x[k-1])
$$

então o modelo se torna

$$
y[k] = f(\mathbf{U}[k])
$$

Então utilizaremos uma abordagem com funções de base radial, para estimar a não linearidade do sistema, temos então que a saída em função do tempo se torna

$$
y[k] = \sum_{i = 0}^{N_c}  w_i \Phi({ \frac{-||\mathbf{U}[k] - \mathbf{Z}_i||_2^2}{2 \sigma_i^2} })
$$

onde $N_c$ representa o número de funções de base, $\mathbf{Z}$ representa o vetor de centros, $\sigma_i^2$ representa a variância de cada componente da base.


Podemos então fazer um treinamento supervisionado com alguns dados para o sistema, e fazê-lo aprender a dinâmica do sistema utilizando algum algoritmo de otimização para ajustar os pesos $\alpha_j$, e então validar com outra entrada e saída.

A forma vetorial da equação de ajuste é dada por

$$
\mathbf{y} = \mathbf{\Phi} \mathbf{w}
$$

onde $\mathbf{w}$ é o vetor de pesos da rede, e a lei de formação da matriz $\mathbf{\Phi}$ é:

$$
{\Phi}[k,i] = \Phi({ \frac{-||\mathbf{U}[k] - \mathbf{Z}_i||_2^2}{2 \sigma_i^2} })
$$

o vetor de pesos ótimo para pode ser encontrado pela solução de mínimos quadrados, então podemos usá-la para fazer o treinamento, assim definimos a função de custo

$$
J(\mathbf{w}) = \frac{1}{2N}||\mathbf{y} - \mathbf{\Phi} \mathbf{w}||_2^2
$$

o ponto de mínimo dessa função é

$$
\mathbf{w} = ( \mathbf{\Phi}^T  \mathbf{\Phi})^{-1}  \mathbf{\Phi}^T \mathbf{y}
$$

assim podemos reconstruir finalmente a saída do sistema como

$$
\mathbf{y}_{est} = \mathbf{\Phi}(\mathbf{U}) \mathbf{w}_{otm}
$$
