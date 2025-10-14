import pandas as pd
import altair as alt

# load data
df = pd.read_json('https://raw.githubusercontent.com/APWright/CSC477-Fall2025/refs/heads/main/Assignment-3/csforca-enrollment.json')

# get field names
print(df.columns)

# add column: total population of CS students
df["CS_students"] = df["AP CS"] + df["Non-AP CS"]
# add column: participation rate of CS students
df["participation_rate"] = df["CS_students"] / df["Overall Enrollment"]


# sketch 1 visualization
data_1 = (
    # combine all race categories for each gender in each county
    df.groupby(["county", "sex"], as_index=False)
    # sum total population of CS students for each race and
    # sum total population of students enrolled
    .agg({"CS_students": "sum", "Overall Enrollment": "sum"})
)

# recalculate participation rate for county gender pairs
data_1["participation_rate"] = data_1["CS_students"] / data_1["Overall Enrollment"]

chart_1 = (
    alt.Chart(data_1)  # load dataset
    .mark_bar()  # draw bars
    .encode(
        x=alt.X("county:N", title="County", sort="-y"),  # X (categorical): counties
        y=alt.Y("participation_rate:Q", title="CS Participation Rate", axis=alt.Axis(format="%")),  # Y (quantitative): participation rate
        color=alt.Color("sex:N", legend=alt.Legend(title="Gender")),  # add color and legend
        tooltip=["county", "sex", alt.Tooltip("participation_rate:Q", format=".1%")]  # display values
    )
    .properties(title="CS Participation Rate by Gender and County (2018-2019)")  # add title
)

chart_1.save("chart_1.html")


# sketch 2 visualization
data_2 = (
    # combine all race categories for each gender in each county
    df.groupby(["county", "sex"], as_index=False)
    # sum total population of CS students for each race
    .agg({"CS_students": "sum"})
)

# recalculate gender proportions of CS students
data_2["percentage_of_CS"] = data_2.groupby("county")["CS_students"].transform(lambda x: x /x.sum())

chart_2 = (
    alt.Chart(data_2)  # load dataset
    .mark_bar()  # draw bars
    .encode(
        x=alt.X("county:N", title="County"),  # X (categorical): counties
        y=alt.Y("percentage_of_CS:Q", title="Share of CS Students", axis=alt.Axis(format="%"), stack="normalize"),  # stacked bars that add up to 100%
        color=alt.Color("sex:N", legend=alt.Legend(title="Gender")),  # add color and legend
        tooltip=["county", "sex", alt.Tooltip("percentage_of_CS:Q", format=".1%")]  # display values
    )
    .properties(title="Gender Composition of CS Enrollment by County (2018-2019)")
)

chart_2.save("chart_2.html")