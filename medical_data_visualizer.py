import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
bmi = df["weight"] / ((df["height"] / 100) ** 2)
df["overweight"] = (bmi > 25).astype(int)

# Normalize data
df["gluc"] = (df["gluc"] > 1).astype(int)
df["cholesterol"] = (df["cholesterol"] > 1).astype(int)

# Draw Categorical Plot
def draw_cat_plot():
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["active", "alco", "cholesterol", "gluc", "overweight", "smoke"])

    # Group and reformat the data to split by cardio
    df_cat = pd.DataFrame(df_cat.groupby(["cardio", "variable", "value"])["value"].count()).rename(columns={"value": "total"}).reset_index()

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x="variable", y="total", hue="value", col="cardio", data=df_cat, kind="bar")

    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df["ap_lo"] <= df["ap_hi"]) & (df["height"] >= df["height"].quantile(0.025)) & (df["height"] <= df["height"].quantile(0.975)) & (df["weight"] >= df["weight"].quantile(0.025)) & (df["weight"] <= df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt=".1f", mask=mask, vmax=0.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
