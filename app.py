
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Car Fuel Efficiency Explorer",
    layout="wide"
)

st.title("Car Fuel Efficiency Explorer")
st.write("IS445 HW6 - Interactive Data Visualization")


@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/vega/vega-datasets/main/data/cars.json"
    return pd.read_json(url)

df = load_data()

df["Year"] = pd.to_datetime(df["Year"], errors="coerce").dt.year

st.write(
    "This project explores the relationship between car horsepower, "
    "fuel efficiency, production year, and origin."
)

st.markdown(
    "[Data Source: Vega Cars Dataset]"
    "(https://github.com/vega/vega-datasets/blob/main/data/cars.json)"
)


col1, col2, col3 = st.columns(3)

col1.metric("Total Records", len(df))
col2.metric("Origins", df["Origin"].nunique())
col3.metric(
    "Average MPG",
    round(df["Miles_per_Gallon"].mean(), 2)
)

st.divider()


st.header("Plot 1: Horsepower vs. Fuel Efficiency")

scatter_data = df.dropna(
    subset=["Horsepower", "Miles_per_Gallon", "Origin"]
).copy()

origins = sorted(scatter_data["Origin"].unique().tolist())

selected_origin = st.selectbox(
    "Select car origin",
    ["All Origins"] + origins
)

if selected_origin != "All Origins":
    scatter_data = scatter_data[
        scatter_data["Origin"] == selected_origin
    ]

chart1 = (
    alt.Chart(scatter_data)
    .mark_circle(size=65, opacity=0.7)
    .encode(
        x=alt.X(
            "Horsepower:Q",
            title="Horsepower",
            scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "Miles_per_Gallon:Q",
            title="Miles per Gallon (MPG)",
            scale=alt.Scale(zero=False)
        ),
        color=alt.Color(
            "Origin:N",
            title="Origin",
            scale=alt.Scale(
                domain=["USA", "Europe", "Japan"],
                range=["#4C78A8", "#F58518", "#54A24B"]
            )
        ),
        tooltip=[
            alt.Tooltip("Name:N", title="Car"),
            alt.Tooltip("Horsepower:Q", title="Horsepower"),
            alt.Tooltip("Miles_per_Gallon:Q", title="MPG"),
            alt.Tooltip("Origin:N", title="Origin")
        ]
    )
    .properties(height=420)
)

st.altair_chart(chart1, use_container_width=True)

st.subheader("Plot 1 Analysis")

st.write(
    "This scatter plot highlights the relationship between horsepower "
    "and fuel efficiency. In general, cars with higher horsepower "
    "tend to have lower miles per gallon. I chose a scatter plot "
    "because both variables are quantitative, and individual points "
    "make it easy to identify patterns and unusual observations. "
    "Both axes use linear scales. I used blue, orange, and green to "
    "distinguish cars from the USA, Europe, and Japan. The points "
    "are partially transparent to reduce the problem of overlapping "
    "observations. I removed records with missing horsepower or "
    "fuel efficiency values before plotting. Users can select an "
    "origin to explore the relationship within a specific group. "
    "If I had more time, I would add regression lines and include "
    "car weight to better understand this relationship."
)

st.divider()


st.header("Plot 2: Average Fuel Efficiency by Year")

year_data = df.dropna(
    subset=["Year", "Miles_per_Gallon", "Origin"]
).copy()

year_data["Year"] = year_data["Year"].astype(int)

min_year = int(year_data["Year"].min())
max_year = int(year_data["Year"].max())

year_range = st.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

filtered_years = year_data[
    year_data["Year"].between(year_range[0], year_range[1])
]

yearly_avg = (
    filtered_years
    .groupby(["Year", "Origin"])["Miles_per_Gallon"]
    .mean()
    .reset_index()
)

chart2 = (
    alt.Chart(yearly_avg)
    .mark_line(point=True, strokeWidth=3)
    .encode(
        x=alt.X(
            "Year:Q",
            title="Year",
            axis=alt.Axis(format="d", tickMinStep=1),
            scale=alt.Scale(zero=False)
        ),
        y=alt.Y(
            "Miles_per_Gallon:Q",
            title="Average Miles per Gallon",
            scale=alt.Scale(zero=True)
        ),
        color=alt.Color(
            "Origin:N",
            title="Origin",
            scale=alt.Scale(
                domain=["USA", "Europe", "Japan"],
                range=["#4C78A8", "#F58518", "#54A24B"]
            )
        ),
        tooltip=[
            alt.Tooltip("Year:Q", title="Year", format="d"),
            alt.Tooltip("Origin:N", title="Origin"),
            alt.Tooltip(
                "Miles_per_Gallon:Q",
                title="Average MPG",
                format=".2f"
            )
        ]
    )
    .properties(height=420)
)

st.altair_chart(chart2, use_container_width=True)

st.subheader("Plot 2 Analysis")

st.write(
    "This line chart highlights changes in average fuel efficiency "
    "over time for cars from different origins. The overall pattern "
    "shows that fuel efficiency generally improved over the period "
    "covered by the dataset, although the trends differ across "
    "origins. I chose a line chart because it makes changes over "
    "time easier to follow. The x-axis represents years using a "
    "quantitative scale, and the y-axis represents average miles "
    "per gallon using a linear scale starting at zero. I used the "
    "same colors as the first plot to maintain consistency. "
    "Before plotting, I converted the date values into years, "
    "removed missing values, and calculated the mean MPG for "
    "each year and origin. The year range slider allows users "
    "to focus on a specific time period. If I had more time, "
    "I would add uncertainty intervals and show the number "
    "of observations behind each yearly average."
)

st.divider()

st.header("Interactivity")

st.write(
    "The first plot uses a dropdown menu to filter cars by origin. "
    "This helps users compare patterns within individual groups. "
    "The second plot uses a year range slider to explore changes "
    "during different time periods. Both visualizations also "
    "include tooltips that provide additional information. "
    "These interactive features allow users to explore the data "
    "without changing the Python code."
)

st.header("Comparison with Homework 5")

st.subheader("Plot 1 Comparison")

st.write(
    "There is no overlap in the dataset or visualization between "
    "this plot and Homework 5. Homework 5 used Bigfoot sighting "
    "reports and a bar chart to compare the number of reports "
    "across states. This plot uses a car dataset from Vega Datasets "
    "and a scatter plot to explore the relationship between "
    "horsepower and fuel efficiency."
)

st.subheader("Plot 2 Comparison")

st.write(
    "There is also no overlap in the dataset or visualization "
    "between this plot and Homework 5. Homework 5 compared Bigfoot "
    "sightings across seasons using a bar chart. This plot uses "
    "a line chart to compare average car fuel efficiency over "
    "time across different origins. Both the dataset and the "
    "variables are different from Homework 5."
)
