import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Global Literacy Rate Dashboard")
st.write("This dashboard shows how literacy rates change over time across selected countries using World Bank data.")

# Load data
df = pd.read_csv("literacy_cleaned.csv")
df = df[~df["Country Name"].str.contains("income|states|IDA|IBRD|classification|Africa|Europe|Asia", case=False, na=False)]



# Sidebar filters
st.sidebar.header("Filters")

countries = st.sidebar.multiselect(
    "Select Countries",
    df["Country Name"].unique(),
    default=df["Country Name"].unique()[:5]
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (2000, 2022)
)

# Filter data
filtered_df = df[
    (df["Country Name"].isin(countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# Line chart
st.subheader("Literacy Rate Over Time")

line_data = filtered_df.pivot(index="Year", columns="Country Name", values="Literacy Rate")

st.line_chart(line_data)

# Bar chart (top countries)
st.subheader("Top Countries")

latest_year = filtered_df["Year"].max()
top_df = filtered_df[filtered_df["Year"] == latest_year]

top_df = top_df.sort_values(by="Literacy Rate", ascending=False).head(10)

st.bar_chart(top_df.set_index("Country Name")["Literacy Rate"])

# Map
st.subheader("World Literacy Map")

# Get latest year
latest_year = filtered_df["Year"].max()

map_df = filtered_df[filtered_df["Year"] == latest_year]

# Create map
fig = px.choropleth(
    map_df,
    locations="Country Name",
    locationmode="country names",
    color="Literacy Rate",
    title="Literacy Rates by Country"
)

st.plotly_chart(fig)



