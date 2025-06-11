import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Magic Analytics", layout="wide")

st.title("Magic: The Gathering - Análise de Cartas")

uploaded_file = st.file_uploader("Envie sua planilha de cartas (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    st.subheader("Resumo das colunas numéricas")
    st.write(df.describe())

    # Top 10 cartas mais usadas nos decks
    st.subheader("Top 10 Cartas Mais Utilizadas nos Decks")

    top_usadas = df.sort_values(by="Quantidade em Deck", ascending=False).head(10)
    fig_usadas = px.bar(top_usadas, x="Nome", y="Quantidade em Deck",
                        title="Top 10 Cartas com Maior Quantidade em Deck",
                        labels={"Quantidade em Deck": "Qtd em Deck"},
                        text="Quantidade em Deck")
    fig_usadas.update_traces(textposition='outside')
    st.plotly_chart(fig_usadas)

else:
    st.info("Envie um arquivo .csv para começar.")
