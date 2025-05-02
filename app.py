import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="County WAS Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("sanitation_data.xlsx", sheet_name="wash status")
    return df

df = load_data()

st.title("🧼 County Water and Sanitation (WAS) Dashboard")
st.markdown("Explore sanitation coverage by ward, sub-location, and village.")

ward = st.selectbox("Select Ward", sorted(df["Ward"].dropna().unique()))
filtered_df = df[df["Ward"] == ward]

for _, row in filtered_df.iterrows():
    st.subheader(f"📍 {row['Village']} - {row['Sub-Location']}, {row['Ward']} Ward")

    total = row["Number of households"]
    without = row["Number of Households without Sanitation Facilities"]
    basic = row["Number of Households with Basic  Sanitation Facilities"]
    improved = row["Number of Households with Improved Sanitation Facilities"]

    pct_without = (without / total) * 100
    pct_basic = (basic / total) * 100
    pct_improved = (improved / total) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Households", int(total))
    col2.metric("No Sanitation", f"{pct_without:.1f}%", delta=f"{int(without)} HHs")
    col3.metric("Basic Sanitation", f"{pct_basic:.1f}%", delta=f"{int(basic)} HHs")
    col4.metric("Improved Sanitation", f"{pct_improved:.1f}%", delta=f"{int(improved)} HHs")

    fig = px.pie(
        names=["Without Sanitation", "Basic Sanitation", "Improved Sanitation"],
        values=[without, basic, improved],
        title="Sanitation Distribution",
        color_discrete_sequence=["#EF553B", "#FFA15A", "#00CC96"]
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 View Raw Data"):
    st.dataframe(filtered_df)