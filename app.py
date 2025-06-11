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

    # 1. Top 10 Cartas Mais Utilizadas nos Decks
    st.subheader("Top 10 Cartas Mais Utilizadas nos Decks")
    top_usadas = df.sort_values(by="Quantidade em Deck", ascending=False).head(10)
    fig_usadas = px.bar(top_usadas, x="Nome", y="Quantidade em Deck", text="Quantidade em Deck")
    st.plotly_chart(fig_usadas)

    # 2. Cartas com Maior Pontuação Total
    st.subheader("Top 10 Cartas com Maior Pontuação Total")
    top_pontuacao_total = df.sort_values(by="Pontuação Total", ascending=False).head(10)
    fig_total = px.bar(top_pontuacao_total, x="Nome", y="Pontuação Total", text="Pontuação Total")
    st.plotly_chart(fig_total)

    # 3. Cartas com Maior Pontuação Média
    st.subheader("Top 10 Cartas com Maior Pontuação Média")
    top_media = df[df["Quantidade em Deck"] > 1].copy()
    top_media["Pontuação Média"] = top_media["Pontuação Total"] / top_media["Quantidade em Deck"]
    top_media = top_media.sort_values(by="Pontuação Média", ascending=False).head(10)
    fig_media = px.bar(top_media, x="Nome", y="Pontuação Média", text="Pontuação Média")
    st.plotly_chart(fig_media)

    # 4. Distribuição por Identidade de Cor
    st.subheader("Distribuição por Identidade de Cor")
    cor_count = df["Identidade de Cor"].value_counts().reset_index()
    cor_count.columns = ["Identidade de Cor", "Quantidade"]
    fig_cor = px.pie(cor_count, names="Identidade de Cor", values="Quantidade", title="Distribuição de Cores")
    st.plotly_chart(fig_cor)

    # 5. CMC Médio dos Decks
    st.subheader("CMC Médio das Cartas nos Decks")
    cmc_deck = df[["CMC", "Quantidade em Deck"]].copy()
    cmc_medio_deck = (cmc_deck["CMC"] * cmc_deck["Quantidade em Deck"]).sum() / cmc_deck["Quantidade em Deck"].sum()
    st.metric("CMC Médio", round(cmc_medio_deck, 2))

    # 6. CMC Médio das Cartas Mais Pontuadas
    st.subheader("CMC Médio das Cartas Mais Pontuadas (Top 100)")
    top_100 = df.sort_values(by="Pontuação Total", ascending=False).head(100)
    cmc_top100 = top_100["CMC"].mean()
    st.metric("CMC Médio (Top 100)", round(cmc_top100, 2))

    # 7. Ranking (Tier) das Cartas
    st.subheader("Ranking (Tier) das Cartas por Pontuação Média")
    df["Pontuação Média"] = df["Pontuação Total"] / df["Quantidade em Deck"]
    df["Tier"] = pd.qcut(df["Pontuação Média"], 4, labels=["D", "C", "B", "A"])
    tier_count = df["Tier"].value_counts().sort_index()
    st.bar_chart(tier_count)

    # 8. Análise de Tipos de Terrenos
    st.subheader("Análise de Terrenos")
    df["É Terreno?"] = df["Tipo"].str.contains("Land", case=False, na=False)
    terreno_count = df["É Terreno?"].value_counts().rename({True: "Terrenos", False: "Outras Cartas"})
    st.bar_chart(terreno_count)

    # 9. Pontuação Média por Estirpe
    st.subheader("Pontuação Média por Estirpe")
    por_tribo = df.groupby("Estirpe (ou Tribo)")["Pontuação Média"].mean().reset_index()
    por_tribo = por_tribo.sort_values(by="Pontuação Média", ascending=False).head(10)
    fig_tribo = px.bar(por_tribo, x="Estirpe (ou Tribo)", y="Pontuação Média", text="Pontuação Média")
    st.plotly_chart(fig_tribo)

    # 10. Eficiência (Pontuação Média por Custo de Mana)
    st.subheader("Eficiência por Custo de Mana (Pontuação Média / CMC)")
    df_eff = df[df["CMC"] > 0].copy()
    df_eff["Eficiência"] = df_eff["Pontuação Média"] / df_eff["CMC"]
    top_eff = df_eff.sort_values(by="Eficiência", ascending=False).head(10)
    fig_eff = px.bar(top_eff, x="Nome", y="Eficiência", text="Eficiência")
    st.plotly_chart(fig_eff)

    # 11. Tier do Deck (pontuação média geral)
    st.subheader("Tier Geral do Deck (Pontuação Média das Cartas)")
    media_deck = df["Pontuação Média"].mean()
    if media_deck >= 8:
        tier_deck = "S"
    elif media_deck >= 6:
        tier_deck = "A"
    elif media_deck >= 4:
        tier_deck = "B"
    elif media_deck >= 2:
        tier_deck = "C"
    else:
        tier_deck = "D"
    st.metric("Tier do Deck", tier_deck)

else:
    st.info("Envie um arquivo .csv para começar.")
