import requests
import pandas as pd
import plotly.express as px
import streamlit as st

# Load geojson
geojson = requests.get(
    "https://raw.githubusercontent.com/plotly/datasets/master/india_states.geojson"
).json()

# Your data
df = pd.DataFrame({
    "state": ["Maharashtra", "Karnataka", "Tamil Nadu", "Delhi", "Punjab"],
    "value": [80, 65, 70, 50, 40]
})

# Map
fig = px.choropleth(
    df,
    geojson=geojson,
    locations="state",
    featureidkey="properties.ST_NM",  # IMPORTANT
    color="value",
    title="India State Map"
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig)