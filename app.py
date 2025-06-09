import streamlit as st
import pandas as pd

st.set_page_config(page_title="Magic Analytics", layout="wide")

st.title("Magic: The Gathering - Análise de Cartas")

uploaded_file = st.file_uploader("Envie sua planilha de cartas (.csv)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    st.subheader("Resumo das colunas numéricas")
    st.write(df.describe())
else:
    st.info("Envie um arquivo .csv para começar.")
