import pandas as pd
import numpy as np


def dataset_overview(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": df.isnull().sum().sum()
    }


def missing_analysis(df):
    missing = df.isnull().sum()
    percent = (missing / len(df)) * 100

    return pd.DataFrame({
        "Missing Count": missing,
        "Missing %": percent
    })


def statistical_summary(df):
    return df.describe()


def get_numeric_columns(df):
    return df.select_dtypes(include=np.number)


def correlation_matrix(df):
    numeric_df = get_numeric_columns(df)
    if numeric_df.shape[1] > 1:
        return numeric_df.corr()
    return None