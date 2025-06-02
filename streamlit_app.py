import streamlit as st
import pandas as pd
import math
import requests
import zipfile
import io

# -----------------------------------------------------------------------------
# Page config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GDP dashboard",
    page_icon=":earth_americas:",
)

# -----------------------------------------------------------------------------
# Utility functions
# -----------------------------------------------------------------------------
@st.cache_data(ttl=86400)
def fetch_and_prepare_gdp():
    """
    1. Download the latest World Bank GDP CSV (zipped) via their API.
    2. Extract the main CSV file (named “API_NY.GDP.MKTP.CD_…csv”).
    3. Read it into a DataFrame.
    4. Pivot “year” columns (e.g. “1960”, “1961”, …) into rows: [Year, GDP].
    
    The result is cached for 24 hours (86400 seconds) to avoid re-downloading on each rerun.
    """
    # 1. Download the zipped CSV from World Bank
    wb_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?downloadformat=csv"
    r = requests.get(wb_url, stream=True)
    r.raise_for_status()

    # 2. Unzip in-memory and find the CSV whose name starts with “API_NY.GDP.MKTP.CD”
    z = zipfile.ZipFile(io.BytesIO(r.content))
    csv_filename = None
    for name in z.namelist():
        # We're looking for the main data file, not the metadata file
        if name.startswith("API_NY.GDP.MKTP.CD") and name.endswith(".csv"):
            csv_filename = name
            break

    if csv_filename is None:
        raise ValueError("Could not find the expected CSV inside the World Bank ZIP")

    # 3. Read that CSV into a DataFrame
    raw = pd.read_csv(z.open(csv_filename), skiprows=4)  
    # skiprows=4 because the first 4 rows are header/info rows in the downloaded CSV.

    # 4. Identify all year-columns (e.g. “1960”, “1961”, …) dynamically
    year_cols = [col for col in raw.columns if col.isdigit()]
    years_int = sorted(int(col) for col in year_cols)

    # 5. Melt those year-columns into long form: [Country Code, Year, GDP]
    melted = raw.melt(
        id_vars=["Country Code"],
        value_vars=[str(y) for y in years_int],
        var_name="Year",
        value_name="GDP",
    )
    melted["Year"] = melted["Year"].astype(int)

    return melted

gdp_df = fetch_and_prepare_gdp()

# -----------------------------------------------------------------------------
# Main page layout
# -----------------------------------------------------------------------------
st.markdown("# :earth_americas: GDP dashboard")
st.markdown(
    """
Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) API.  
This app automatically fetches (and then caches) the latest available data; the cache is refreshed every 24 hours.
"""
)

st.write("")  # small spacer

# Determine full range of years in the dataset
min_year = int(gdp_df["Year"].min())
max_year = int(gdp_df["Year"].max())

from_year, to_year = st.slider(
    "Which years are you interested in?",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    format="%d",
)

# List of all country codes present
all_countries = sorted(gdp_df["Country Code"].unique())
if not all_countries:
    st.warning("No countries found in the dataset.")
    st.stop()

selected_countries = st.multiselect(
    "Which countries would you like to view?",
    options=all_countries,
    default=["DEU", "FRA", "GBR", "BRA", "MEX", "JPN"],
)

st.write("")  # spacer

# Filter based on selection
filtered = gdp_df[
    (gdp_df["Country Code"].isin(selected_countries))
    & (gdp_df["Year"] >= from_year)
    & (gdp_df["Year"] <= to_year)
]

st.header("GDP over time", anchor=None)
st.line_chart(
    data=filtered,
    x="Year",
    y="GDP",
    color="Country Code",
)

st.write("")  # spacer

# Show year-to-year metric comparisons for each selected country
st.header(f"GDP in {to_year}", anchor=None)

cols = st.columns(4)

first_slice = gdp_df[gdp_df["Year"] == from_year]
last_slice = gdp_df[gdp_df["Year"] == to_year]

for idx, country in enumerate(selected_countries):
    col = cols[idx % len(cols)]
    with col:
        # Safely fetch GDP for that country in the chosen years
        try:
            gdp_start = first_slice.loc[first_slice["Country Code"] == country, "GDP"].iat[0]
            gdp_end = last_slice.loc[last_slice["Country Code"] == country, "GDP"].iat[0]
        except IndexError:
            gdp_start = float("nan")
            gdp_end = float("nan")

        # Convert to billions for display
        if not math.isnan(gdp_end):
            gdp_end_b = gdp_end / 1_000_000_000
        else:
            gdp_end_b = float("nan")

        # Compute growth ratio if possible
        if math.isnan(gdp_start) or gdp_start == 0:
            growth_label = "n/a"
            delta_color = "off"
        else:
            ratio = gdp_end / gdp_start
            growth_label = f"{ratio:,.2f}×"
            delta_color = "normal"

        st.metric(
            label=f"{country} GDP",
            value=(f"{gdp_end_b:,.0f}B" if not math.isnan(gdp_end_b) else "n/a"),
            delta=growth_label,
            delta_color=delta_color,
        )
