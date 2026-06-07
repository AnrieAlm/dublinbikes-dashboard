import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DublinBikes Analytics", layout="wide")

df = pd.read_csv("station_summary.csv")

st.title("DublinBikes Station Utilisation Dashboard")
st.markdown("Open data from Smart Dublin / Dublinked")

col1, col2, col3 = st.columns(3)
col1.metric("Total Stations", df["STATION_ID"].nunique())
col2.metric("Avg Utilisation Rate", f"{df['avg_utilisation_rate'].mean():.1%}")
col3.metric("Total Bike Stands", int(df["BIKE_STANDS"].sum()))

st.subheader("Station Utilisation Map")
fig_map = px.scatter_mapbox(
    df, lat="LATITUDE", lon="LONGITUDE",
    size="avg_utilisation_rate", color="avg_utilisation_rate",
    color_continuous_scale="reds", hover_name="NAME",
    hover_data=["ADDRESS", "BIKE_STANDS"], zoom=12, height=500
)
fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map, use_container_width=True)

col_left, col_right = st.columns(2)

top_busy = df.nlargest(15, "avg_utilisation_rate")
fig_bar = px.bar(top_busy, x="avg_utilisation_rate", y="NAME",
                 orientation="h", color="avg_utilisation_rate",
                 color_continuous_scale="reds", title="Top 15 Busiest Stations")
col_left.plotly_chart(fig_bar, use_container_width=True)

top_capacity = df.nlargest(15, "BIKE_STANDS")
fig_cap = px.bar(top_capacity, x="BIKE_STANDS", y="NAME",
                 orientation="h", color="BIKE_STANDS",
                 color_continuous_scale="blues", title="Top 15 Largest Stations")
col_right.plotly_chart(fig_cap, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(df.sort_values("avg_utilisation_rate", ascending=False))
