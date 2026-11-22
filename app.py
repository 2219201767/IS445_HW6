
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Bigfoot Sightings Explorer",
    layout="wide"
)

st.title("Bigfoot Sightings Explorer")
st.write("IS445 HW6 - Interactive Data Visualization")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/bfro_reports_fall2022.csv"
    return pd.read_csv(url)

df = load_data()

st.write(f"Total reports in dataset: {len(df):,}")

# Plot 1: Bigfoot sightings by year
st.header("Plot 1: Bigfoot Sightings Over Time")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year

year_data = df.dropna(subset=["year"]).copy()
year_data["year"] = year_data["year"].astype(int)

min_year = int(year_data["year"].min())
max_year = int(year_data["year"].max())

year_range = st.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_years = year_data[
    year_data["year"].between(year_range[0], year_range[1])
]

year_counts = (
    filtered_years.groupby("year")
    .size()
    .reset_index(name="count")
)

chart1 = (
    alt.Chart(year_counts)
    .mark_line(point=True)
    .encode(
        x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
        y=alt.Y("count:Q", title="Number of Reports"),
        tooltip=["year:Q", "count:Q"]
    )
    .properties(height=350)
)

st.altair_chart(chart1, use_container_width=True)

st.write(
    "This line chart shows how the number of reported Bigfoot sightings "
    "changes over time. I used a line chart to make yearly trends easier "
    "to compare. The x-axis represents years and the y-axis represents "
    "the number of reports. A single blue line keeps the design simple. "
    "Users can adjust the year range to focus on specific periods. "
    "If I had more time, I would investigate possible reasons for "
    "changes in reporting frequency."
)

# Plot 2: Bigfoot sightings by classification
st.header("Plot 2: Bigfoot Sightings by Classification")

states = sorted(df["state"].dropna().unique().tolist())
selected_state = st.selectbox(
    "Select a state",
    ["All States"] + states
)

if selected_state == "All States":
    classification_data = df.copy()
else:
    classification_data = df[df["state"] == selected_state].copy()

classification_counts = (
    classification_data.dropna(subset=["classification"])
    .groupby("classification")
    .size()
    .reset_index(name="count")
)

chart2 = (
    alt.Chart(classification_counts)
    .mark_bar()
    .encode(
        x=alt.X("classification:N", title="Classification"),
        y=alt.Y("count:Q", title="Number of Reports"),
        color=alt.Color("classification:N", title="Classification"),
        tooltip=["classification:N", "count:Q"]
    )
    .properties(height=350)
)

st.altair_chart(chart2, use_container_width=True)

st.write(
    "This bar chart compares the number of reports across different "
    "classification categories. I chose bars because they make it "
    "easy to compare category counts. The x-axis uses nominal "
    "encoding and the y-axis uses quantitative encoding. Different "
    "colors help distinguish the categories. Users can select a state "
    "to see how the classification distribution changes. If I had "
    "more time, I would explore whether these categories are related "
    "to location or season."
)

# Comparison with HW5
st.header("Comparison with Homework 5")

st.write(
    "This project uses the same Bigfoot dataset as Homework 5, "
    "but both visualizations are new. Homework 5 compared sightings "
    "across states and seasons. Homework 6 focuses on yearly trends "
    "and report classifications. The plots and written explanations "
    "were created for this homework and were not copied from Homework 5."
)
