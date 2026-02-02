import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

from eda_utils import (
    dataset_overview,
    missing_analysis,
    statistical_summary,
    get_numeric_columns,
    correlation_matrix
)

from insight_generator import generate_insights


st.set_page_config(page_title="Auto EDA Generator", layout="wide")

st.title("Auto EDA Report Generator")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.success("Dataset Loaded Successfully!")

    # ---------------- Dataset Preview ----------------
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------- Overview ----------------
    overview = dataset_overview(df)

    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", overview["rows"])
    col2.metric("Columns", overview["columns"])
    col3.metric("Missing Values", overview["missing"])

    # ---------------- Column Types ----------------
    st.subheader("Column Types")
    st.write(df.dtypes)

    # ---------------- Missing Values ----------------
    st.subheader("Missing Value Analysis")
    miss_df = missing_analysis(df)
    st.dataframe(miss_df)

    # ---------------- Summary Stats ----------------
    st.subheader("Statistical Summary")
    st.dataframe(statistical_summary(df))

    # ---------------- Correlation ----------------
    st.subheader("Correlation Heatmap")

    corr = correlation_matrix(df)

    if corr is not None:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Not enough numeric columns.")

    # ---------------- Distribution ----------------
    numeric_df = get_numeric_columns(df)

    if not numeric_df.empty:

        st.subheader("Distribution Plot")

        selected_col = st.selectbox(
            "Select numeric column",
            numeric_df.columns
        )

        fig = px.histogram(df, x=selected_col)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Box Plot")

        fig2 = px.box(df, y=selected_col)
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- Insights ----------------
    st.subheader("Auto Generated Insights")

    insights = generate_insights(df, numeric_df)

    for ins in insights:
        st.write("•", ins)

    # ---------------- Download Report ----------------
    st.subheader("Download Report")

    buffer = StringIO()
    df.describe().to_csv(buffer)

    st.download_button(
        label="Download Statistical Report",
        data=buffer.getvalue(),
        file_name="eda_report.csv",
        mime="text/csv",
    )

else:
    st.info("Upload a CSV file to begin analysis.")