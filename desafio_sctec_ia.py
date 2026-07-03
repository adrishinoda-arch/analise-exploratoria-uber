#1. CONFIGURAÇÃO INICIAL
#Importação de bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print('Bibliotecas importadas com sucesso!')

# Carregar dataset
df_original = pd.read_csv('data/ncr_ride_bookings.csv')

#2. CONHECENDO O DATASET
print("=" * 60)
print("EXPLORANDO O DATASET")

#Dimensões do dataset
print(f"Dataset possui {df_original.shape[0]} registros e {df_original.shape[1]} colunas.")

#Informações gerais (incluindo tipos de dados)
df_original.info()

#Estatísticas descritivas
print(df_original.describe())

print("=" * 60)

#3.LIMPEZA E TRATAMENTO DO DATASET
#Criação de cópia de segurança onde serrão feitas as alterações
df = df_original.copy()

print("LIMPEZA E TRATAMENTO DO DATASET")
print("TRATAMENTO DE VALORES NULOS:")

#TRATAMENTO DE VALORES NULOS
#Verificação de valores nulos
nulos = df.isnull().sum()
nulos_percentual = (nulos / len(df)) * 100
print("\nValores nulos por coluna:")
print(pd.concat([nulos, nulos_percentual], axis=1, keys=['Contagem', '%']))

# Colunas com muitos nulos (>50%) - remover
colunas_remover = ['Cancelled Rides by Customer', 'Reason for cancelling by Customer', 'Cancelled Rides by Driver', 'Driver Cancellation Reason', 'Incomplete Rides', 'Incomplete Rides Reason']
df = df.drop(columns=[col for col in colunas_remover if col in df.columns])
print(f"\n✅ Colunas removidas")

nulos = df.isnull().sum()
nulos_percentual = (nulos / len(df)) * 100
print("\nValores nulos por coluna:")
print(pd.concat([nulos, nulos_percentual], axis=1, keys=['Contagem', '%']))

#Colunas com 38% nulos (preenchendo com mediana)
print("\nPreenchendo colunas com 38% de nulos...")

# Driver Ratings - avaliação do motorista
df['Driver Ratings'] = df['Driver Ratings'].fillna(df['Driver Ratings'].median())
print(f"  ✅ Driver Ratings: preenchido com mediana = {df['Driver Ratings'].median():.2f}")

# Customer Rating - avaliação do cliente
df['Customer Rating'] = df['Customer Rating'].fillna(df['Customer Rating'].median())
print(f"  ✅ Customer Rating: preenchido com mediana = {df['Customer Rating'].median():.2f}")

#Colunas com 32% nulos (preenchendo com mediana)
print("\nPreenchendo colunas com 32% de nulos...")
# Avg CTAT - tempo médio de viagem (preencher com mediana)
df['Avg CTAT'] = df['Avg CTAT'].fillna(df['Avg CTAT'].median())
print(f"  ✅ Avg CTAT: preenchido com mediana = {df['Avg CTAT'].median():.2f}")

# Booking Value - valor da corrida (preencher com mediana)
df['Booking Value'] = df['Booking Value'].fillna(df['Booking Value'].median())
print(f"  ✅ Booking Value: preenchido com mediana = {df['Booking Value'].median():.2f}")

# Ride Distance - distância (preencher com mediana)
df['Ride Distance'] = df['Ride Distance'].fillna(df['Ride Distance'].median())
print(f"  ✅ Ride Distance: preenchido com mediana = {df['Ride Distance'].median():.2f}")

# Payment Method - método de pagamento (preencher com moda - valor mais comum)
moda_pagamento = df['Payment Method'].mode()[0]
df['Payment Method'] = df['Payment Method'].fillna(moda_pagamento)
print(f"  ✅ Payment Method: preenchido com moda = {moda_pagamento}")

#Colunas com 7% nulos (preenchendo com mediana)
print("\nPreenchendo colunas com 7% de nulos...")
df['Avg VTAT'] = df['Avg VTAT'].fillna(df['Avg VTAT'].median())

#Verificação final --> NULOS
print("\n" + "="*50)
print("VERIFICAÇÃO FINAL")
print("="*50)

nulos_final = df.isnull().sum()
nulos_restantes = nulos_final[nulos_final > 0]

if len(nulos_restantes) == 0:
    print("✅ NENHUM VALOR NULO RESTANTE! Tratamento concluído com sucesso.")
else:
    print("⚠️ Ainda existem valores nulos:")
    print(nulos_restantes)

print(f"\n📊 Dataset após tratamento: {df.shape[0]} registros e {df.shape[1]} colunas")

print("=" * 60)
print("TRATAMENTO DE OUTLIERS")

# Verificar se df existe
try:
    print(f"✅ DataFrame carregado com {len(df)} registros")
except NameError:
    print("❌ ERRO: DataFrame 'df' não encontrado!")
    print("   Execute o tratamento de nulos primeiro.")
    exit()

# Lista de colunas para verificar
colunas_numericas = [
    'Avg VTAT',
    'Avg CTAT', 
    'Booking Value',
    'Ride Distance',
    'Driver Ratings',
    'Customer Rating'
]

# Verificar quais colunas existem
colunas_existentes = []
print("\nVerificando colunas:")
for col in colunas_numericas:
    if col in df.columns:
        colunas_existentes.append(col)
        print(f"✅ Coluna encontrada: {col}")
    else:
        print(f"⚠️ Coluna NÃO encontrada: {col}")

print(f"\n📊 Colunas existentes para análise: {colunas_existentes}")

# Detecção de outliers
print("\n" + "="*60)
print("DETECTANDO OUTLIERS")
print("="*60)

for col in colunas_existentes:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < limite_inferior) | (df[col] > limite_superior)]
    
    if len(outliers) > 0:
        print(f"\n📊 {col}:")
        print(f"  - Outliers detectados: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
        print(f"  - Limites: [{limite_inferior:.2f}, {limite_superior:.2f}]")
    else:
        print(f"\n✅ {col}: Nenhum outlier detectado")

print("\n" + "="*60)
print("INICIANDO TRATAMENTO DE OUTLIERS")
print("="*60)

# Tratamento de outliers
# Avg VTAT
if 'Avg VTAT' in df.columns:
    negativos = len(df[df['Avg VTAT'] < 0])
    df.loc[df['Avg VTAT'] < 0, 'Avg VTAT'] = 0
    altos = len(df[df['Avg VTAT'] > 60])
    df.loc[df['Avg VTAT'] > 60, 'Avg VTAT'] = 60
    print(f"\n✅ Avg VTAT:")
    print(f"   - {negativos} valores negativos ajustados para 0")
    print(f"   - {altos} valores acima de 60min ajustados para 60")

# Avg CTAT
if 'Avg CTAT' in df.columns:
    altos = len(df[df['Avg CTAT'] > 120])
    df.loc[df['Avg CTAT'] > 120, 'Avg CTAT'] = 120
    print(f"\n✅ Avg CTAT:")
    print(f"   - {altos} valores acima de 120min ajustados para 120")

# Booking Value
if 'Booking Value' in df.columns:
    altos = len(df[df['Booking Value'] > 1000])
    df.loc[df['Booking Value'] > 1000, 'Booking Value'] = 1000
    print(f"\n✅ Booking Value:")
    print(f"   - {altos} valores acima de R$1000 ajustados para 1000")

# Driver Ratings
if 'Driver Ratings' in df.columns:
    baixos = len(df[df['Driver Ratings'] < 1])
    altos = len(df[df['Driver Ratings'] > 5])
    df.loc[df['Driver Ratings'] < 1, 'Driver Ratings'] = 1
    df.loc[df['Driver Ratings'] > 5, 'Driver Ratings'] = 5
    print(f"\n✅ Driver Ratings:")
    print(f"   - {baixos} valores abaixo de 1 ajustados para 1")
    print(f"   - {altos} valores acima de 5 ajustados para 5")

# Customer Rating
if 'Customer Rating' in df.columns:
    baixos = len(df[df['Customer Rating'] < 1])
    altos = len(df[df['Customer Rating'] > 5])
    df.loc[df['Customer Rating'] < 1, 'Customer Rating'] = 1
    df.loc[df['Customer Rating'] > 5, 'Customer Rating'] = 5
    print(f"\n✅ Customer Rating:")
    print(f"   - {baixos} valores abaixo de 1 ajustados para 1")
    print(f"   - {altos} valores acima de 5 ajustados para 5")

# Ride Distance
if 'Ride Distance' in df.columns:
    altos = len(df[df['Ride Distance'] > 100])
    df.loc[df['Ride Distance'] > 100, 'Ride Distance'] = 100
    print(f"\n✅ Ride Distance:")
    print(f"   - {altos} valores acima de 100km ajustados para 100")

print("\n" + "="*60)
print("✅ Tratamento concluído! Todos os valores foram ajustados dentro de limites considerados mais próximos da realidade.")
print(f"📊 Dataset mantém {len(df)} registros.")

print("\n" + "="*60)

#Tratamento de duplicatas
print("INICIANDO TRATAMENTO DE DUPLICATAS")
total_duplicatas = df.duplicated().sum() 
print(f"Total de registros duplicados: {total_duplicatas}")

#4. ANÁLISES
print("ANÁLISES SOBRE O DATASET")

#CANCELAMENTOS

#Distribuição do status das corridas
status_counts = df['Booking Status'].value_counts()
print("\nDistribuição por Status:")
print(status_counts)

# Gráfico de barras
plt.figure(figsize=(10, 5))
ax = status_counts.plot(kind='bar', color='#2CA942')
plt.title('Distribuição dos Status das Corridas')
plt.xlabel('Status')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
total = status_counts.sum()
for container in ax.containers:
    ax.bar_label(container, labels=[f'{v/total:.1%}' for v in container.datavalues], padding=3)

plt.tight_layout()
plt.show()

# Gráfico de pizza (proporção)
plt.figure(figsize=(8, 8))
status_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                   colors=['#2CA942', '#4ECDC4', '#45B7D1', '#96CEB4', "#B4F4A9"])
plt.title('Proporção por Status')
plt.ylabel('')
plt.show()

# Taxa de cancelamento
total = len(df)
cancelados = df[df['Booking Status'].str.contains('Cancelled', na=False)].shape[0]
completados = df[df['Booking Status'] == 'Completed'].shape[0]

print(f"\nTotal de corridas: {total}")
print(f"Corridas completadas: {completados} ({completados/total*100:.2f}%)")
print(f"Corridas canceladas: {cancelados} ({cancelados/total*100:.2f}%)")

#POR TIPO DE VEÍCULO
# Distribuição de corridas por tipo de veículo
veiculo_counts = df['Vehicle Type'].value_counts()
print("\nCorridas por tipo de veículo:")
print(veiculo_counts)

# Gráfico de barras da distribuição de corridas por tipo de veículo com percentuais
plt.figure(figsize=(10, 5))
ax = veiculo_counts.plot(kind='bar', color='#2CA942')
plt.title('Quantidade de Corridas por Tipo de Veículo')
plt.xlabel('Tipo de Veículo')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)

total = veiculo_counts.sum()
for container in ax.containers:
    ax.bar_label(container, 
                 labels=[f'{v/total:.1%}' for v in container.datavalues], 
                 padding=3,
                 fontweight='bold')

plt.tight_layout()
plt.show()

# Valor médio da corrida por tipo de veículo
valor_por_veiculo = df.groupby('Vehicle Type')['Booking Value'].mean().sort_values(ascending=False)
print("\nValor médio da corrida por tipo de veículo:")
print(valor_por_veiculo)

# Gráfico de barras
plt.figure(figsize=(10, 5))
valor_por_veiculo.plot(kind='bar', color='#2CA942')
plt.title('Valor Médio da Corrida por Tipo de Veículo')
plt.xlabel('Tipo de Veículo')
plt.ylabel('Valor Médio')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Distância média por tipo de veículo
dist_por_veiculo = df.groupby('Vehicle Type')['Ride Distance'].mean().sort_values(ascending=False)
print("\nDistância média da corrida por tipo de veículo:")
print(dist_por_veiculo)

#ANÁLISE TEMPORAL
# Conversão colunas de data/hora
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

# Extração de data
df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
df['month'] = df['Date'].dt.month
df['day_of_week'] = df['Date'].dt.dayofweek  # 0=segunda, 6=domingo

# Corridas por hora do dia
corridas_por_hora = df.groupby('hour').size()
plt.figure(figsize=(12, 5))
plt.plot(corridas_por_hora.index, corridas_por_hora.values, marker='o', linestyle='-', color='#2CA942')
plt.title('Distribuição de Corridas por Hora do Dia')
plt.xlabel('Hora')
plt.ylabel('Quantidade de Corridas')
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.show()

# Corridas por dia da semana
dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
corridas_por_dia = df.groupby('day_of_week').size()
plt.figure(figsize=(10, 5))
plt.bar(dias, corridas_por_dia.values, color='#2CA942')
plt.title('Corridas por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade')
plt.show()

# Corridas por mês
corridas_por_mes = df.groupby('month').size()
plt.figure(figsize=(10, 5))
plt.bar(corridas_por_mes.index, corridas_por_mes.values, color='#2CA942')
plt.title('Corridas por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade')
plt.xticks(range(1, 13))
plt.show()

#VALOR E DISTÂNCIA
# Distribuição do valor da corrida
plt.figure(figsize=(10, 5))
plt.hist(df['Booking Value'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='#2CA942')
plt.title('Distribuição do Valor das Corridas')
plt.xlabel('Valor da Corrida')
plt.ylabel('Frequência')
plt.show()

# Distribuição da distância percorrida
plt.figure(figsize=(10, 5))
plt.hist(df['Ride Distance'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='#2CA942')
plt.title('Distribuição da Distância Percorrida')
plt.xlabel('Distância (km)')
plt.ylabel('Frequência')
plt.show()

# Relação entre distância e valor (scatter plot)
plt.figure(figsize=(10, 6))
plt.scatter(df['Ride Distance'], df['Booking Value'], alpha=0.3, s=5, color='#2CA942')
plt.title('Relação entre Distância e Valor da Corrida')
plt.xlabel('Distância (km)')
plt.ylabel('Valor da Corrida')
plt.show()

#AVALIAÇÕES
# Distribuição das avaliações do motorista
plt.figure(figsize=(10, 5))
plt.hist(df['Driver Ratings'].dropna(), bins=20, edgecolor='black', alpha=0.7, color='#2CA942')
plt.title('Distribuição das Avaliações dos Motoristas')
plt.xlabel('Avaliação')
plt.ylabel('Frequência')
plt.show()

# Distribuição das avaliações dos clientes
plt.figure(figsize=(10, 5))
plt.hist(df['Customer Rating'].dropna(), bins=20, edgecolor='black', alpha=0.7, color='#2CA942')
plt.title('Distribuição das Avaliações dos Clientes')
plt.xlabel('Avaliação')
plt.ylabel('Frequência')
plt.show()

# Média de avaliações por tipo de veículo
avaliacoes_por_veiculo = df.groupby('Vehicle Type')[['Driver Ratings', 'Customer Rating']].mean()
print("\nMédia de avaliações por tipo de veículo:")
print(avaliacoes_por_veiculo)

#MÉTODOS DE PAGAMENTO
# Distribuição dos métodos de pagamento
pagamento_counts = df['Payment Method'].value_counts()
print("\nDistribuição por método de pagamento:")
print(pagamento_counts)

plt.figure(figsize=(8, 8))
cores = ['#2CA942', '#4ECDC4', '#45B7D1', '#96CEB4', "#B4F4A9"]
pagamento_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=cores)
plt.title('Distribuição por Método de Pagamento')
plt.ylabel('')
plt.show()

# Valor médio por método de pagamento
valor_por_pagamento = df.groupby('Payment Method')['Booking Value'].mean().sort_values(ascending=False)
print("\nValor médio da corrida por método de pagamento:")
print(valor_por_pagamento)

# Gráfico de barras básico
plt.figure(figsize=(10, 5))
ax = valor_por_pagamento.plot(kind='bar', color='#2CA942')
plt.title('Valor Médio da Corrida por Método de Pagamento')
plt.xlabel('Método de Pagamento')
plt.ylabel('Valor Médio (R$)')
plt.xticks(rotation=45)
for container in ax.containers:
    ax.bar_label(container, labels=[f'R$ {v:.2f}' for v in container.datavalues], 
                 padding=3, fontweight='bold')

plt.tight_layout()
plt.show()

#TEMPOS DE VIAGEM
# Distribuição do tempo de espera
plt.figure(figsize=(10, 5))
plt.hist(df['Avg VTAT'].dropna(), bins=30, edgecolor='black', alpha=0.7,color='#2CA942')
plt.title('Distribuição do Tempo de Espera (VTAT)')
plt.xlabel('Tempo de Espera (min)')
plt.ylabel('Frequência')
plt.show()

# Distribuição do tempo de viagem 
plt.figure(figsize=(10, 5))
plt.hist(df['Avg CTAT'].dropna(), bins=30, edgecolor='black', alpha=0.7, color='#2CA942')
plt.title('Distribuição do Tempo de Viagem (CTAT)')
plt.xlabel('Tempo de Viagem (min)')
plt.ylabel('Frequência')
plt.show()

# Relação entre tempo de espera e valor
plt.figure(figsize=(10, 6))
plt.scatter(df['Avg VTAT'], df['Booking Value'], alpha=0.3, s=5, color='#2CA942')
plt.title('Relação entre Tempo de Espera e Valor da Corrida')
plt.xlabel('Tempo de Espera (min)')
plt.ylabel('Valor da Corrida')
plt.show()

print("=" * 60)

#5. MATRIZ DE CORRELAÇÃO
# Selecionar apenas colunas numéricas
colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()

# Remover colunas binárias que podem distorcer (opcional)
colunas_numericas = [c for c in colunas_numericas if c not in 
                     ['Cancelled Rides by Customer', 'Cancelled Rides by Driver', 'Incomplete Rides']]

print("=" * 60)

#6.INSIGHTS
print("=" * 60)
print("PRINCIPAIS INSIGHTS DA ANÁLISE EXPLORATÓRIA")
print("=" * 60)

print(f"\n1. Volume de dados: {df.shape[0]} corridas registradas.")

print(f"\n2. Taxa de conclusão: {completados/total*100:.1f}% das corridas são completadas.")
print(f"   Taxa de cancelamento: {cancelados/total*100:.1f}%.")

print(f"\n3. Veículo mais utilizado: {veiculo_counts.index[0]} ({veiculo_counts.values[0]} corridas).")
print(f"   Veículo com maior valor médio: {valor_por_veiculo.index[0]} (R$ {valor_por_veiculo.values[0]:.2f}).")

print("\n4. Padrões temporais:")
print(f"   - Horário de pico: {corridas_por_hora.idxmax()}h com {corridas_por_hora.max()} corridas.")
print(f"   - Dia com mais corridas: {dias[corridas_por_dia.idxmax()]}.")

print(f"\n5. Método de pagamento mais utilizado: {pagamento_counts.index[0]} ({pagamento_counts.values[0]} corridas).")

print("\n6. Avaliações:")
print(f"   - Média das avaliações dos motoristas: {df['Driver Ratings'].mean():.2f}")
print(f"   - Média das avaliações dos clientes: {df['Customer Rating'].mean():.2f}")

#Exportação do dataset cópia tratado
df.to_csv('ncr_ride_bookings_tratado.csv', index=False)




