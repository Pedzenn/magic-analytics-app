import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Magic Analytics", layout="wide")

st.title("Magic: The Gathering - Análise de Cartas")

uploaded_file = st.file_uploader("📂 Envie sua planilha de cartas (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    st.subheader("📊 Resumo das colunas numéricas")
    st.write(df.describe())

    # Gráfico 1: Top 10 cartas por quantidade em deck
    st.subheader("🏆 Top 10 Cartas Mais Utilizadas nos Decks")
    top_usadas = df.sort_values(by="Quantidade em Deck", ascending=False).head(10)
    fig1 = px.bar(top_usadas, x="Nome", y="Quantidade em Deck", text="Quantidade em Deck",
                  title="Top 10 Cartas Mais Presentes em Decks")
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Top 10 por pontuação total
    st.subheader("🔥 Top 10 Cartas por Pontuação Total")
    top_pont_total = df.sort_values(by="Pontuação Total da Carta", ascending=False).head(10)
    fig2 = px.bar(top_pont_total, x="Nome", y="Pontuação Total da Carta", text="Pontuação Total da Carta",
                  title="Cartas com Maior Pontuação Total")
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Top 10 por pontuação média
    st.subheader("⭐ Top 10 Cartas por Pontuação Média")
    top_pont_media = df.sort_values(by="Pontuação média da Carta", ascending=False).head(10)
    fig3 = px.bar(top_pont_media, x="Nome", y="Pontuação média da Carta", text="Pontuação média da Carta",
                  title="Cartas com Maior Pontuação Média")
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Distribuição por identidade de cor
    st.subheader("🌈 Distribuição por Identidade de Cor")
    cor_count = df['Identidade de Cor'].value_counts().reset_index()
    cor_count.columns = ['Identidade de Cor', 'Quantidade']
    fig4 = px.pie(cor_count, names='Identidade de Cor', values='Quantidade', hole=0.4)
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Distribuição da pontuação média
    st.subheader("📈 Distribuição da Pontuação Média das Cartas")
    fig5 = px.histogram(df, x="Pontuação média da Carta", nbins=30,
                        title="Distribuição da Pontuação Média")
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico 6: Quantidade de cartas por deck
    st.subheader("📦 Quantidade de Cartas por Deck")
    por_deck = df.groupby("Deck")["Nome"].count().reset_index(name="Quantidade de Cartas")
    fig6 = px.bar(por_deck, x="Deck", y="Quantidade de Cartas", title="Cartas por Deck")
    st.plotly_chart(fig6, use_container_width=True)

    # Gráfico 7: Proporção de Tipos de Cartas por Deck
    st.subheader("🔍 Proporção dos Tipos de Carta por Deck")
    tipo_por_deck = df.groupby(["Deck", "Tipo"]).size().reset_index(name="Quantidade")
    tipo_total = tipo_por_deck.groupby("Deck")["Quantidade"].transform("sum")
    tipo_por_deck["Proporção"] = tipo_por_deck["Quantidade"] / tipo_total

    fig7 = px.scatter(tipo_por_deck, x="Deck", y="Tipo", size="Proporção", color="Tipo",
                      title="Proporção de Tipos de Carta por Deck",
                      size_max=40)
    st.plotly_chart(fig7, use_container_width=True)

    # Gráfico 8: Custo médio de mana por deck
    st.subheader("💰 Custo Médio de Mana por Deck")
    cmc_por_deck = df.groupby("Deck")["Custo de Mana"].mean().reset_index()
    cmc_por_deck.columns = ["Deck", "CMC Médio"]
    fig8 = px.bar(cmc_por_deck, x="Deck", y="CMC Médio",
                  title="Custo Médio de Mana por Deck")
    st.plotly_chart(fig8, use_container_width=True)

else:
    st.info("👈 Envie um arquivo .csv para começar.")
