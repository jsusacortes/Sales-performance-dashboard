import sys
from pathlib import Path

import plotly.express as px
import plotly.io as pio
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from src.load import load_data
from src.metrics import country_summary, monthly_revenue, mom_growth, product_summary, rep_summary

# ── Global Plotly template ────────────────────────────────────────────────────
_CARD_BG = "#1a1a2e"
_PAGE_BG = "#0f0f1a"

pio.templates["choc"] = pio.templates["plotly_dark"]
pio.templates["choc"].layout.update(
    paper_bgcolor=_CARD_BG,
    plot_bgcolor=_CARD_BG,
    font_color="#e2e8f0",
    hoverlabel=dict(bgcolor=_CARD_BG, font_size=13),
    margin=dict(t=40, b=20, l=10, r=10),
    coloraxis_colorbar=dict(tickfont_color="#e2e8f0", title_font_color="#e2e8f0"),
)
pio.templates.default = "choc"

st.set_page_config(page_title="Chocolate Sales Dashboard", layout="wide")

# ── Animations & Styling ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Easing tokens */
:root {
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-expo:  cubic-bezier(0.16, 1, 0.3, 1);
}

/* Page fade-in */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0);    }
}

/* Title entrance */
h1 {
  animation: fadeUp 500ms var(--ease-out-expo) both;
}

/* KPI cards — staggered slide-up */
[data-testid="stMetric"] {
  background: #1a1a2e;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  animation: fadeUp 500ms var(--ease-out-expo) both;
  transition: transform 200ms var(--ease-out-quart),
              box-shadow 200ms var(--ease-out-quart),
              border-color 200ms ease;
}
[data-testid="stMetric"]:nth-child(1) { animation-delay: 80ms;  }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 160ms; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 240ms; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 320ms; }

[data-testid="stMetric"]:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.35);
  border-color: rgba(255,255,255,0.18);
}

/* Metric value — accent color */
[data-testid="stMetricValue"] {
  color: #7dd3fc !important;
  font-weight: 700;
}

/* Chart containers — entrance */
[data-testid="stPlotlyChart"] {
  animation: fadeUp 600ms var(--ease-out-expo) 400ms both;
  border-radius: 10px;
  overflow: hidden;
}

/* Sidebar inputs — focus glow */
[data-testid="stSidebar"] input:focus,
[data-testid="stSidebar"] [data-baseweb="select"]:focus-within {
  box-shadow: 0 0 0 2px rgba(125, 211, 252, 0.4);
  transition: box-shadow 200ms var(--ease-out-quart);
}

/* Divider fade-in */
hr {
  animation: fadeUp 400ms var(--ease-out-quart) 300ms both;
}
</style>
""", unsafe_allow_html=True)

st.title("Chocolate Sales Performance Dashboard")
st.caption("Tracking rep performance, regional trends, and product mix across the portfolio.")


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()


df = get_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filters")

    # Date range
    date_min, date_max = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input("Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

    st.divider()

    # Country accordion
    with st.expander("Country", expanded=True):
        all_countries = sorted(df["Country"].unique())
        countries = [c for c in all_countries if st.checkbox(c, value=True, key=f"c_{c}")]

    # Sales Person accordion
    with st.expander("Sales Person", expanded=False):
        all_reps = sorted(df["Sales Person"].unique())
        reps = [r for r in all_reps if st.checkbox(r, value=True, key=f"r_{r}")]

    # Product accordion
    with st.expander("Product", expanded=False):
        all_products = sorted(df["Product"].unique())
        products = [p for p in all_products if st.checkbox(p, value=True, key=f"p_{p}")]

    st.divider()

    # Revenue range slider
    rev_min = int(df["Amount"].min())
    rev_max = int(df["Amount"].max())
    rev_range = st.slider("Revenue per transaction ($)", min_value=rev_min, max_value=rev_max, value=(rev_min, rev_max))

# ── Apply Filters ─────────────────────────────────────────────────────────────
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_min, date_max

# Fall back to all values if every checkbox is unchecked
active_countries = countries or all_countries
active_reps      = reps      or all_reps
active_products  = products  or all_products

filtered = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
    & (df["Country"].isin(active_countries))
    & (df["Sales Person"].isin(active_reps))
    & (df["Product"].isin(active_products))
    & (df["Amount"] >= rev_range[0])
    & (df["Amount"] <= rev_range[1])
]

with st.sidebar:
    st.caption(f"Showing **{len(filtered):,}** of {len(df):,} rows")

if filtered.empty:
    st.warning("No data matches your filters.")
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
total_revenue = filtered["Amount"].sum()
total_boxes = filtered["Boxes Shipped"].sum()
avg_rev_per_box = total_revenue / total_boxes if total_boxes > 0 else 0
top_rep = rep_summary(filtered).iloc[0]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${total_revenue:,.0f}")
k2.metric("Total Boxes Shipped", f"{total_boxes:,.0f}")
k3.metric("Avg Revenue per Box", f"${avg_rev_per_box:,.2f}")
k4.metric("Top Sales Rep", top_rep["Sales Person"], f"${top_rep['Revenue']:,.0f}")

st.divider()

# ── Row 1: Revenue Trend + Rep Leaderboard ────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Revenue Over Time")
    monthly = mom_growth(monthly_revenue(filtered))
    fig = px.line(
        monthly,
        x="Month",
        y="Revenue",
        markers=True,
        labels={"Revenue": "Revenue ($)", "Month": ""},
        custom_data=["MoM Growth %"],
    )
    fig.update_traces(
        hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<br>MoM: %{customdata[0]:.1f}%<extra></extra>",
        line=dict(width=2.5),
    )
    fig.update_layout(
        transition={"duration": 400, "easing": "cubic-in-out"},
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=13),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Sales Rep Leaderboard")
    reps_df = rep_summary(filtered)
    fig = px.bar(
        reps_df,
        x="Revenue",
        y="Sales Person",
        orientation="h",
        color="Revenue per Box",
        color_continuous_scale="Teal",
        labels={"Revenue": "Total Revenue ($)", "Sales Person": "", "Revenue per Box": "$/Box"},
        text=reps_df["Revenue"].apply(lambda x: f"${x:,.0f}"),
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_colorbar_title="$/Box",
        transition={"duration": 400, "easing": "cubic-in-out"},
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=13),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Country Bar + Product Treemap ──────────────────────────────────────
col3, col4 = st.columns([2, 3])

with col3:
    st.subheader("Revenue by Country")
    country_df = country_summary(filtered)
    fig = px.bar(
        country_df,
        x="Country",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Blues",
        labels={"Revenue": "Total Revenue ($)"},
        text=country_df["Revenue"].apply(lambda x: f"${x:,.0f}"),
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        coloraxis_showscale=False,
        transition={"duration": 400, "easing": "cubic-in-out"},
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=13),
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Product Performance")
    product_df = product_summary(filtered)
    fig = px.treemap(
        product_df,
        path=["Product"],
        values="Revenue",
        color="Revenue per Box",
        color_continuous_scale="RdYlGn",
        labels={"Revenue per Box": "$/Box", "Revenue": "Revenue ($)"},
        hover_data={"Revenue": ":,.0f", "Revenue per Box": ":.2f"},
    )
    fig.update_layout(
        coloraxis_colorbar_title="$/Box",
        transition={"duration": 400, "easing": "cubic-in-out"},
        hoverlabel=dict(bgcolor="#1a1a2e", font_size=13),
    )
    st.plotly_chart(fig, use_container_width=True)
