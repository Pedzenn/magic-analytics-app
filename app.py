import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Magic Analytics", layout="wide")
st.title("Magic: The Gathering - Dashboard Analítico de Cartas")

# Carrega automaticamente o arquivo CSV
df = pd.read_csv("Relatorio_Resumo_Cartas final.csv")
st.dataframe(df)

# Filtro para cartas não-terrenos
base_sem_terrenos = df[df['Tipo Terreno?'] == 'Não'].copy()

# Cria a coluna 'Tier' automaticamente com base na Pontuação Média da Carta
def get_tier(p):
    if p >= 11.12:
        return 'Tier S'
    elif p >= 8.94:
        return 'Tier A'
    elif p >= 6.88:
        return 'Tier B'
    else:
        return 'Tier C'

base_sem_terrenos['Tier'] = base_sem_terrenos['Pontuação Média da Carta'].apply(get_tier)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs([
    "Tabela Geral",
    "Identidade de Cor",
    "Tier das Cartas",
    "Top 10 Mais Usadas",
    "CMC Médio por Comandante",
    "Top 20 Pontuação Média",
    "CMC das + Pontuadas",
    "Pontuação Média por Estirpe",
    "CMC Médio por Estirpe",
    "Eficiência",
    "Quartis por Deck",
    "Composição de Tipos por Deck",
    "Deck Perfeito"
])

with tab1:
    st.subheader("Tabela Geral com Filtro")
    st.dataframe(df)

with tab2:
    st.subheader("Distribuição de Cartas por Identidade de Cores (Sem Terrenos)")
    dist_cores = base_sem_terrenos['Identidade de Cor'].value_counts().reset_index()
    dist_cores.columns = ['Identidade de Cor', 'Quantidade']
    fig = px.bar(dist_cores, x='Identidade de Cor', y='Quantidade')
    st.plotly_chart(fig)

with tab3:
    st.subheader("Distribuição das Cartas por Tier (Barras e Pizza)")
    tier_counts = base_sem_terrenos['Tier'].value_counts().reindex(['Tier S','Tier A','Tier B','Tier C'], fill_value=0)
    fig_tier = px.bar(tier_counts, x=tier_counts.index, y=tier_counts.values, labels={"x": "Tier", "y": "Quantidade"})
    st.plotly_chart(fig_tier)
    fig_pie = px.pie(values=tier_counts.values, names=tier_counts.index, title="Proporção de Cartas por Tier")
    st.plotly_chart(fig_pie)
    # Boxplot por Tier
    st.write("Resumo Estatístico da Pontuação Média por Tier:")
    fig_box, ax = plt.subplots(figsize=(8,5))
    sns.boxplot(data=base_sem_terrenos, x='Tier', y='Pontuação Média da Carta', order=['Tier S','Tier A','Tier B','Tier C'], palette='Set2', ax=ax)
    st.pyplot(fig_box)

with tab4:
    st.subheader("Top 10 Cartas Mais Utilizadas (Sem Terrenos)")
    mais_usadas = base_sem_terrenos.groupby('Nome da Carta')['Quantidade'].sum().reset_index()
    mais_usadas = mais_usadas.sort_values('Quantidade', ascending=False).head(10)
    fig_mais = px.bar(mais_usadas, y='Nome da Carta', x='Quantidade', orientation='h', title="Top 10 Cartas Mais Usadas")
    st.plotly_chart(fig_mais)

with tab5:
    st.subheader("Custo Médio de Mana por Comandante (por Jogador)")
    comand = df[df['Commander'] == 'Sim'][['Nome Completo', 'Nome da Carta']]
    cmc_deck = base_sem_terrenos.groupby('Nome Completo')['cmc'].mean().reset_index()
    resultado = pd.merge(comand, cmc_deck, on='Nome Completo')
    resultado = resultado.rename(columns={'Nome da Carta': 'Comandante', 'cmc': 'CMC Médio'})
    resultado['Comandante_Jogador'] = resultado['Comandante'] + " — " + resultado['Nome Completo']
    resultado = resultado.sort_values('CMC Médio', ascending=False)
    fig_cmc = px.bar(resultado, x='Comandante_Jogador', y='CMC Médio', hover_data=['Nome Completo'])
    fig_cmc.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_cmc)

with tab6:
    st.subheader("Top 20 Cartas com Maior Pontuação Média")
    top_media = base_sem_terrenos.groupby('Nome da Carta')['Pontuação Média da Carta'].mean().reset_index()
    top_media = top_media.sort_values('Pontuação Média da Carta', ascending=False).head(20)
    fig_top_media = px.bar(top_media, y='Nome da Carta', x='Pontuação Média da Carta', orientation='h')
    st.plotly_chart(fig_top_media)

with tab7:
    st.subheader("CMC das 20 Cartas com Maior Pontuação Média")
    top_cmc = base_sem_terrenos.groupby('Nome da Carta').agg({
        'Pontuação Média da Carta': 'mean', 'cmc': 'mean'}).reset_index()
    top_cmc = top_cmc.sort_values('Pontuação Média da Carta', ascending=False).head(20)
    fig_top_cmc = px.bar(top_cmc, x='cmc', y='Nome da Carta', orientation='h', color='Pontuação Média da Carta',
                         title='CMC das 20 Cartas com Maior Pontuação Média',
                         labels={'cmc': 'CMC Médio', 'Nome da Carta': 'Carta'})
    st.plotly_chart(fig_top_cmc)

with tab8:
    st.subheader("Pontuação Média por Estirpe")
    media_estirpe = base_sem_terrenos.groupby('ESTIRPE')['Pontuação Média da Carta'].mean().reset_index()
    media_estirpe = media_estirpe.sort_values('Pontuação Média da Carta', ascending=False)
    fig_estirpe = px.bar(media_estirpe, x='ESTIRPE', y='Pontuação Média da Carta')
    st.plotly_chart(fig_estirpe)

with tab9:
    st.subheader("CMC Médio por Estirpe")
    cmc_estirpe = base_sem_terrenos.groupby('ESTIRPE')['cmc'].mean().reset_index()
    cmc_estirpe = cmc_estirpe.sort_values('cmc', ascending=False)
    fig_cmc_estirpe = px.bar(cmc_estirpe, x='ESTIRPE', y='cmc')
    st.plotly_chart(fig_cmc_estirpe)

with tab10:
    st.subheader("Eficiência das Cartas: Pontuação Média vs. Quantidade de Decks")
    eficiencia = base_sem_terrenos.copy()
    eficiencia = eficiencia.groupby('Nome da Carta').agg({
        'Pontuação Média da Carta':'mean',
        'Carta Aparece em Quantos Decks':'max'
    }).reset_index()
    fig_ef = px.scatter(eficiencia, x='Carta Aparece em Quantos Decks', y='Pontuação Média da Carta',
                        size='Pontuação Média da Carta', hover_name='Nome da Carta')
    st.plotly_chart(fig_ef)

with tab11:
    st.subheader("Distribuição da Pontuação Média dos Decks por Quartil")
    if "Quartil" in df.columns:
        deck_scores = df[df["Tipo Terreno?"] == "Não"]
        fig_quartil, axq = plt.subplots(figsize=(10,6))
        sns.boxplot(data=deck_scores, x='Quartil', y='Pontuação Média da Carta',
                    order=['Q1','Q2','Q3','Q4'], palette='viridis', ax=axq)
        st.pyplot(fig_quartil)
    else:
        st.info("A coluna 'Quartil' não foi encontrada na base. Calcule os quartis antes de enviar o arquivo.")

with tab12:
    st.subheader("Composição Percentual dos Tipos de Carta por Deck")
    nomes_decks = df['Nome Completo'].unique().tolist()
    escolha_deck = st.selectbox("Selecione o deck (Nome do Jogador)", nomes_decks)
    if escolha_deck:
        deck_atual = df[(df['Nome Completo'] == escolha_deck) & (df['Tipo Terreno?'] == 'Não')]
        tipo_counts = deck_atual['Tipo'].value_counts(normalize=True).reset_index()
        tipo_counts.columns = ['Tipo', 'Percentual']
        fig = px.bar(tipo_counts, x='Tipo', y='Percentual',
                     title=f"Composição Percentual de Tipos — {escolha_deck}",
                     labels={'Percentual': '% no Deck', 'Tipo': 'Tipo de Carta'})
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig)

with tab13:
    st.subheader("Deck Perfeito — Composição Recomendada de Tipos de Carta")
    composicao_perfeita = pd.DataFrame({
        'Tipo': ['Criatura', 'Terreno', 'Artefato', 'Encantamento', 'Feitiço', 'Instantâneo', 'Planeswalker'],
        'Quantidade': [40, 36, 8, 5, 5, 3, 2]
    })
    fig_dp_pie = px.pie(composicao_perfeita, names='Tipo', values='Quantidade', hole=0.3)
    fig_dp_bar = px.bar(composicao_perfeita, x='Tipo', y='Quantidade')
    st.write("Composição do Deck Perfeito (Exemplo Sugerido para 99 cartas)")
    st.plotly_chart(fig_dp_pie)
    st.write("Composição do Deck Perfeito (Barras)")
    st.plotly_chart(fig_dp_bar)

