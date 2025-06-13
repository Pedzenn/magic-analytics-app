import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Magic Analytics", layout="wide")
st.title("Magic: The Gathering - Análise de Cartas")

uploaded_file = st.file_uploader("Envie sua planilha de cartas (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Tabela com filtro")
    st.dataframe(df)

    # Top 20 cartas por pontuação total
    st.subheader("Top 20 Cartas por Pontuação Total")
    top_total = df.sort_values(by="Pontuação Total", ascending=False).head(20)
    fig_total = px.bar(top_total, x="Nome", y="Pontuação Total", text="Pontuação Total", title="Top 20 - Pontuação Total")
    fig_total.update_traces(textposition='outside')
    st.plotly_chart(fig_total)

    # Top 20 mais utilizadas nos decks
    st.subheader("Top 20 Cartas Mais Utilizadas nos Decks")
    top_usadas = df.sort_values(by="Quantidade em Deck", ascending=False).head(20)
    fig_usadas = px.bar(top_usadas, y="Nome", x="Quantidade em Deck", orientation='h', title="Top 20 - Cartas Mais Usadas")
    st.plotly_chart(fig_usadas)

    # Cartas com maior pontuação média
    st.subheader("Top 20 Cartas com Maior Pontuação Média")
    top_media = df[df["Quantidade em Deck"] >= 3].sort_values(by="Pontuação Média", ascending=False).head(20)
    fig_media = px.bar(top_media, y="Nome", x="Pontuação Média", orientation='h', title="Top 20 - Pontuação Média")
    st.plotly_chart(fig_media)

    # Distribuição da pontuação média
    st.subheader("Distribuição da Pontuação Média (Tabela)")
    st.dataframe(df[["Nome", "Pontuação Média"]].sort_values(by="Pontuação Média", ascending=False))

    # Distribuição das cartas por tier
    st.subheader("Distribuição das Cartas por Tier")
    tier_counts = df["Tier"].value_counts()
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(tier_counts)
    with col2:
        fig_pie = px.pie(values=tier_counts.values, names=tier_counts.index, title="Distribuição por Tier")
        st.plotly_chart(fig_pie)

    # Quantidade de cartas por deck
    st.subheader("Quantidade de Cartas por Deck")
    cartas_por_deck = df.groupby("Deck")["Nome"].count().reset_index(name="Quantidade de Cartas")
    st.dataframe(cartas_por_deck)

    # Distribuição por identidade de cor (sem terrenos)
    st.subheader("Distribuição por Identidade de Cor (sem Terrenos)")
    cores = df[~df["Tipo"].str.contains("Terreno", na=False)]
    identidade_counts = cores["Identidade"].value_counts().reset_index()
    identidade_counts.columns = ["Identidade", "Quantidade"]
    fig_identidade = px.bar(identidade_counts, x="Identidade", y="Quantidade", title="Distribuição por Identidade de Cor")
    st.plotly_chart(fig_identidade)

    # Pontuação média por identidade de cor
    st.subheader("Pontuação Média por Identidade de Cor")
    media_cor = cores.groupby("Identidade")["Pontuação Média"].mean().reset_index()
    fig_media_cor = px.bar(media_cor, x="Identidade", y="Pontuação Média", title="Pontuação Média por Identidade")
    st.plotly_chart(fig_media_cor)

    # Proporção dos tipos de cartas por deck (gráfico de bolhas)
    st.subheader("Proporção dos Tipos de Carta por Deck")
    tipos_por_deck = df.groupby(["Deck", "Tipo"]).size().reset_index(name="Quantidade")
    fig_bolhas = px.scatter(tipos_por_deck, x="Deck", y="Tipo", size="Quantidade", color="Tipo",
                            title="Proporção de Tipos por Deck", size_max=60)
    st.plotly_chart(fig_bolhas)

    # CMC médio por comandante
    st.subheader("CMC Médio por Deck")
    cmc_comandante = df.groupby("Deck")["CMC"].mean().reset_index()
    fig_cmc_deck = px.bar(cmc_comandante, x="Deck", y="CMC", title="CMC Médio por Deck")
    st.plotly_chart(fig_cmc_deck)

    # CMC médio das cartas com maior pontuação
    st.subheader("CMC Médio das Cartas Mais Pontuadas")
    top_cmc = top_total.groupby("Nome")["CMC"].mean().reset_index()
    fig_cmc_top = px.bar(top_cmc, y="Nome", x="CMC", orientation='h', title="CMC Médio - Cartas Mais Pontuadas")
    st.plotly_chart(fig_cmc_top)

    # Pontuação média por estirpe
    st.subheader("Pontuação Média por Estirpe")
    media_estirpe = df.groupby("Estirpe")["Pontuação Média"].mean().reset_index()
    fig_estirpe = px.bar(media_estirpe, x="Estirpe", y="Pontuação Média", title="Pontuação Média por Estirpe")
    st.plotly_chart(fig_estirpe)

    # CMC médio por estirpe
    st.subheader("CMC Médio por Estirpe")
    cmc_estirpe = df.groupby("Estirpe")["CMC"].mean().reset_index()
    fig_cmc_estirpe = px.bar(cmc_estirpe, x="Estirpe", y="CMC", title="CMC Médio por Estirpe")
    st.plotly_chart(fig_cmc_estirpe)

    # Eficiência das cartas: Pontuação Média vs. Quantidade em Deck
    st.subheader("Eficiência das Cartas (Pontuação Média x Qtd. em Deck)")
    fig_eficiencia = px.scatter(df, x="Quantidade em Deck", y="Pontuação Média", hover_name="Nome",
                                size="Pontuação Total", color="Tipo",
                                title="Eficiência das Cartas")
    st.plotly_chart(fig_eficiencia)

else:
    st.info("Envie um arquivo .csv para começar.")
