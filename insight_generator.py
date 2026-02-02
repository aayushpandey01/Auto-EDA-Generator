def generate_insights(df, numeric_df):
    insights = []

    for col in df.columns:
        null_percent = df[col].isnull().mean() * 100
        if null_percent > 30:
            insights.append(
                f"Column '{col}' has high missing values ({null_percent:.1f}%)."
            )

    for col in numeric_df.columns:
        skew_val = numeric_df[col].skew()

        if skew_val > 1:
            insights.append(f"'{col}' is highly right skewed.")
        elif skew_val < -1:
            insights.append(f"'{col}' is highly left skewed.")

    if not insights:
        insights.append("Dataset appears relatively clean and balanced.")

    return insights