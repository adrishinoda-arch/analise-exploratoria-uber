# Uber Data Analytics: Análise Exploratória de Dados (AED)

<div align="center">
  <img src="./assets/banner.png" alt="Banner Análise Exploratória de Dados - Sobreviventes" width="100%">
</div>

## 📖 Introdução
Este projeto apresenta uma Análise Exploratória de Dados (AED) detalhada sobre o serviço de corridas da Uber. O objetivo é compreender o comportamento operacional e financeiro do serviço através de uma base de dados robusta, identificando padrões de utilização, fatores que influenciam o valor das corridas e oportunidades estratégicas para a otimização do serviço.

A análise é fundamental para empresas de mobilidade urbana, pois permite transformar grandes volumes de dados brutos em decisões que podem melhorar a experiência do usuário e a eficiência dos motoristas.

---

## 🎯 Pergunta de Negócio
**"Quais são os principais fatores que influenciam a taxa de conclusão de corridas e o valor médio das viagens, e como podemos otimizar a oferta de veículos com base nos padrões temporais de demanda?"**

Esta pergunta é crucial para o negócio, pois a taxa de conclusão (atualmente em 62%) e a gestão eficiente dos horários de pico impactam diretamente a receita e a satisfação tanto dos clientes quanto dos motoristas parceiros.

---

## 📊 Fonte dos Dados
O dataset utilizado é o **Uber Data Analytics Dashboard**, denominado “uber-ride-analytics-dashboard”, disponível no
endereço eletrônico:
https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard/data

*   **Volume de dados:** 150.000 registros.
*   **Complexidade:** 21 colunas contendo variáveis operacionais, financeiras e avaliativas.
*   **Contexto:** Dados históricos de corridas, incluindo informações sobre tipos de veículos, métodos de pagamento, tempos de espera, tempos de viagem e avaliações.

---

## 🛠 Tecnologias Utilizadas
Para este projeto, foram utilizadas as seguintes ferramentas:

-   **Linguagem:** Python 3.14.3;
-   **Manipulação de Dados:** Pandas e Numpy (lógica de limpeza, agrupamento e cálculos);
-   **Visualização:** Matplotlib (criação de matrizes de afinidade e histogramas).
-   **Ambiente:** Venv (ambiente virtual para isolamento de dependências);
-   **Editor:** VS Code.
*   **Git/GitHub:** Controle de versão e hospedagem do repositório.


Para acessar o stack tecnológico detalhado, [clique aqui](requirements.txt).

---
## 🗃️Estrutura de pastas e organização do código
---

Abaixo, o mapa de como o projeto está organizado e estruturado:

```text
projeto-uber-analytics/
├── assets/                 # Imagens, banners e gráficos exportados para o README
├── data/                   # Arquivos de dados brutos e processados
│   ├── ncr_ride_bookings.csv
│   └── ncr_ride_bookings_tratado.csv
├── venv/                   # Ambiente virtual do Python (não versionar no Git)
├── desafio_sctec_ia.py     # Script principal contendo o código da análise
├── Documentacao_SCTEC_ia.pdf # Relatório técnico do projeto
├── README-uber.md          # Documentação do projeto para o GitHub
└── requirements.txt        # Dependências do projeto (pandas, numpy, etc)
```
---
## 🧹 Limpeza e Preparação dos Dados
A etapa de preparação garantiu a integridade das análises. Os procedimentos realizados incluíram:

| Tipo de Tratamento | Onde | Motivo / Ação |
| :--- | :--- | :--- |
| **Valores Nulos (> 50%)** | Colunas de Cancelamento e Incompleto | Removidas, pois a alta taxa de vacância (82%-94%) inviabilizaria análises precisas. |
| **Valores Nulos (38%)** | Ratings e Métricas (Avg CTAT, etc) | Preenchimento com a **mediana** para manter o registro e evitar perda de dados. |
| **Outliers (Avg VTAT)** | Tempo de espera | Ajuste de valores negativos para "0". |
| **Outliers (Avg CTAT)** | Tempo de viagem | Limite de 120 minutos, considerando viagens superiores como exceções raras. |
| **Outliers (Booking Value)** | Valor da corrida | Limite de R$ 1.000,00 para estabilizar a amostra financeira. |

> Ao final do tratamento, mantivemos os 150.000 registros originais, garantindo que o dataset estivesse totalmente limpo e pronto para a exploração.

---

## 📈 Análise Exploratória
A análise foi segmentada para responder aos objetivos do projeto:

*   **Análise de Cancelamentos:** Avaliamos a taxa de conclusão (62%) versus cancelamentos (25%).
*   **Distribuição de Veículos:** Identificamos o "Auto" como o tipo mais utilizado (37.419 corridas).
*   **Padrões Temporais:** Observamos picos de demanda às 18h e maior volume de corridas concentrado às segundas-feiras.
*   **Análise Financeira:** Identificamos que o "Go Sedan" possui o ticket médio mais elevado (R$ 454,65).
*   **Avaliações:** As avaliações de passageiros (4.44) estão ligeiramente acima das dos motoristas (4.26).

---

## 💡 Insights
1.  **Otimização de Frota:** O modelo "Auto" é o carro-chefe. Estratégias de incentivo devem ser focadas neste segmento.
2.  **Gestão de Pagamentos:** O método UPI é o mais popular (93.909 corridas), indicando uma preferência clara dos usuários por pagamentos digitais instantâneos.
3.  **Atenção ao horário de pico:** O pico às 18h exige um sistema dinâmico de incentivos para garantir oferta de veículos.

---

## 🔗 Conexão com a Pergunta de Negócio
A análise responde à pergunta inicial ao demonstrar que a taxa de cancelamento (25%) é um ponto de atenção crítica. Identificamos que o valor médio das corridas e a preferência pelo "Auto" fornecem a base necessária para que a gestão possa ajustar a oferta de veículos em horários específicos, visando reduzir o tempo de espera e elevar a taxa de conclusão.

---

## 🏁 Conclusão
O projeto permitiu uma visão clara do ecossistema Uber. Com 62% de corridas completadas, existe uma oportunidade clara de otimização operacional, especialmente no horário das 18h. As limitações da análise residem na natureza dos dados (snapshot histórico), sugerindo como trabalho futuro a integração de dados climáticos ou de tráfego para entender melhor os motivos dos cancelamentos.

Nota: Para informações adicionais sobre a análise realizada, acesse o relatório técnico disponível [aqui](Relatório_técnico_análise.pdf).

---
## 🤝Contato

🔗 **LinkedIn:** [Adriana Shinoda](www.linkedin.com/in/adriana-shinoda-8577a651)

📧 **E-mail:** [adrishinoda@hotmail.com](mailto:adrishinoda@hotmail.com)

🐙 **GitHub:** [https://github.com/adrishinoda-arch](https://github.com/adrishinoda-arch)

**🏁 Fim da Documentação** Obrigada por visitar este projeto!  
Desenvolvido por **Adriana Shinoda** | Programa SCTEC | 2026