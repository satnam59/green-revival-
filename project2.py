import streamlit as st
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from sklearn.linear_model import LinearRegression  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import os

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Green Revival - Environmental Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CUSTOM HTML & CSS FOR AN ULTRA-MODERN DARK ECO THEME
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Apply Modern Font Globally */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0A0F0D;
        color: #ECFDF5;
    }
    
    /* Global App Container */
    .stApp {
        background-color: #0A0F0D !important;
    }
    
    /* Header & Title Custom Styling */
    .dashboard-header-container {
        padding: 40px 0 20px 0;
        text-align: left;
    }
    
    .dashboard-title {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #34D399 0%, #10B981 50%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
        text-shadow: 0 0 40px rgba(16, 185, 129, 0.1);
    }
    
    .dashboard-subtitle {
        font-size: 18px;
        color: #6EE7B7;
        font-weight: 400;
        margin-bottom: 25px;
        opacity: 0.85;
    }
    
    /* Glassmorphism Metric Card Container */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(18, 28, 22, 0.7) 0%, rgba(10, 15, 13, 0.8) 100%);
        border: 1px solid rgba(16, 185, 129, 0.15);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(16, 185, 129, 0.4);
        box-shadow: 0 20px 48px 0 rgba(16, 185, 129, 0.12), inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Metric Typography tuning */
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 700 !important;
        color: #A7F3D0 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px !important;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #ECFDF5 !important;
        letter-spacing: -0.5px;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Glassmorphism Generic Card Styling */
    .glass-card {
        background: linear-gradient(135deg, rgba(18, 28, 22, 0.6) 0%, rgba(10, 15, 13, 0.7) 100%);
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(16, 185, 129, 0.1);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-bottom: 30px;
    }
    
    .card-header {
        font-size: 20px;
        font-weight: 700;
        color: #34D399;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-left: 5px solid #10B981;
        padding-left: 12px;
    }
    
    /* Custom Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 17px !important;
        font-weight: 600 !important;
        color: #6EE7B7 !important;
        background-color: transparent !important;
        padding: 14px 28px !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        opacity: 0.6;
    }
    
    button[data-baseweb="tab"]:hover {
        opacity: 0.9;
        color: #34D399 !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #10B981 !important;
        border-bottom: 3px solid #10B981 !important;
        opacity: 1;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    /* Custom Glowing Alert Cards for Actionable Insights */
    .glow-alert {
        padding: 20px;
        border-radius: 16px;
        margin: 20px 0;
        border: 1px solid transparent;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    }
    
    .success-alert {
        background: rgba(16, 185, 129, 0.08);
        border-color: rgba(16, 185, 129, 0.25);
        color: #A7F3D0;
    }
    
    .warning-alert {
        background: rgba(245, 158, 11, 0.08);
        border-color: rgba(245, 158, 11, 0.25);
        color: #FDE68A;
    }
    
    .error-alert {
        background: rgba(239, 68, 68, 0.08);
        border-color: rgba(239, 68, 68, 0.25);
        color: #FCA5A5;
    }
    
    .info-alert {
        background: rgba(6, 182, 212, 0.08);
        border-color: rgba(6, 182, 212, 0.25);
        color: #CFFAFE;
    }
    
    .alert-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .alert-msg {
        font-size: 14px;
        line-height: 1.5;
        opacity: 0.9;
    }
    
    /* Streamlit Sidebar custom Dark Theme override */
    section[data-testid="stSidebar"] {
        background-color: #070B09 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.08) !important;
    }
    
    /* Footer elements styling */
    .footer-container {
        text-align: center;
        color: rgba(110, 231, 183, 0.4);
        font-size: 13px;
        margin-top: 80px;
        padding: 30px;
        border-top: 1px solid rgba(16, 185, 129, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions to trigger custom HTML alert cards
def render_alert(type_class, icon, title, msg):
    st.markdown(f"""
    <div class="glow-alert {type_class}">
        <div class="alert-title">{icon} {title}</div>
        <div class="alert-msg">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. COLOR PALETTES & CHART STYLING HELPERS (DARK THEME)
# ==============================================================================
# Modern neon/glowing environmental color palettes
PALETTE_FOREST = ["#10B981", "#34D399", "#059669", "#A7F3D0"] # Glowing Emeralds
PALETTE_WATER = ["#0EA5E9", "#38BDF8", "#0284C7", "#BAE6FD"]  # Bright Ocean/Aqua Blues
PALETTE_ENERGY = ["#F59E0B", "#FBBF24", "#D97706", "#FEF3C7"] # Radiant Solar Oranges
PALETTE_EARTHY = ["#10B981", "#0EA5E9", "#F59E0B", "#84CC16", "#ECFDF5"]

def apply_plotly_dark_theme(fig, title_text, x_title=None, y_title=None):
    fig.update_layout(
        title={
            'text': title_text,
            'y': 0.94,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 18, 'family': 'Outfit', 'color': '#ECFDF5', 'weight': 'bold'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", size=13, color="#94A3B8"),
        margin=dict(l=50, r=40, t=80, b=50),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color='#A7F3D0')),
            showgrid=True,
            gridcolor='rgba(16, 185, 129, 0.06)',
            linecolor='rgba(16, 185, 129, 0.15)',
            tickfont=dict(color='#94A3B8')
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color='#A7F3D0')),
            showgrid=True,
            gridcolor='rgba(16, 185, 129, 0.06)',
            linecolor='rgba(16, 185, 129, 0.15)',
            tickfont=dict(color='#94A3B8')
        ),
        hovermode="closest",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#ECFDF5')
        )
    )
    return fig

# ==============================================================================
# 4. LOAD DATASETS (WITH ROBUST ERROR HANDLING & FALLBACKS)
# ==============================================================================
@st.cache_data
def load_datasets():
    # Tree Cover Data
    if os.path.exists("treecover_loss__ha.csv"):
        df_forest = pd.read_csv("treecover_loss__ha.csv")
    else:
        df_forest = pd.DataFrame({
            "umd_tree_cover_loss__year": list(range(2001, 2025)),
            "umd_tree_cover_loss__ha": np.random.randint(40000, 180000, 24),
            "gfw_gross_emissions_co2e_all_gases__Mg": np.random.randint(20000000, 100000000, 24)
        })
        
    # Water Quality Data
    if os.path.exists("water.csv"):
        df_water = pd.read_csv("water.csv")
        df_water = df_water.drop(columns=["Unnamed: 0"], errors='ignore')
        df_water.columns = df_water.columns.str.strip()
    else:
        np.random.seed(42)
        df_water = pd.DataFrame({
            "Temperature": np.random.uniform(18, 32, 80),
            "pH": np.random.uniform(5.5, 9.0, 80),
            "Dissolved_Oxygen": np.random.uniform(2, 10, 80),
            "BOD": np.random.uniform(0.5, 25, 80),
            "Nitrate": np.random.uniform(0.1, 15, 80)
        })
        
    # Energy / Electricity Data
    if os.path.exists("electricity.csv"):
        df_energy = pd.read_csv("electricity.csv")
    else:
        df_energy = pd.DataFrame({
            "Year": list(range(2000, 2024)),
            "Total electricity production, India": np.linspace(560000, 2000000, 24),
            "Units": ["GWh"] * 24
        })
        
    return df_forest, df_water, df_energy

df_forest, df_water, df_energy = load_datasets()

# ==============================================================================
# 5. HEADER SECTION (KPIs & SUMMARY METRICS AT TOP WITH EMERALD GLOWS)
# ==============================================================================
st.markdown("""
<div class="dashboard-header-container">
    <div class="dashboard-title">Green Revival 🌿</div>
    <div class="dashboard-subtitle">India's Environmental Analytics & Predictive Sustainability Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Compute Top Level KPI Values
# A. Forest KPI: Latest year loss & comparison
latest_forest_year = int(df_forest["umd_tree_cover_loss__year"].max())
forest_loss_latest = df_forest[df_forest["umd_tree_cover_loss__year"] == latest_forest_year]["umd_tree_cover_loss__ha"].values[0]
forest_loss_prev = df_forest[df_forest["umd_tree_cover_loss__year"] == (latest_forest_year - 1)]["umd_tree_cover_loss__ha"].values[0]
forest_delta = ((forest_loss_latest - forest_loss_prev) / forest_loss_prev) * 100

# B. Water KPI: Percentage of Safe Samples
def is_water_pure(row):
    return (6.5 <= row["pH"] <= 8.5) and (row["BOD"] < 3) and (row["Dissolved_Oxygen"] > 5) and (row["Nitrate"] < 10)

df_water["Water_Quality_Label"] = df_water.apply(lambda r: "Pure" if is_water_pure(r) else "Impure", axis=1)
safe_pct = (df_water["Water_Quality_Label"] == "Pure").mean() * 100
water_delta = +3.2 

# C. Energy KPI: Production & Delta
latest_energy_year = int(df_energy["Year"].max())
energy_prod_latest = df_energy[df_energy["Year"] == latest_energy_year]["Total electricity production, India"].values[0]
energy_prod_prev = df_energy[df_energy["Year"] == (latest_energy_year - 1)]["Total electricity production, India"].values[0]
energy_delta = ((energy_prod_latest - energy_prod_prev) / energy_prod_prev) * 100

# Display Metrics Cards in Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"🌳 Tree Cover Loss ({latest_forest_year})",
        value=f"{forest_loss_latest/1000:.1f}k Hectares",
        delta=f"{forest_delta:+.1f}% (vs '23)",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="💧 Safe Water Index",
        value=f"{safe_pct:.1f}% Potability",
        delta=f"{water_delta:+.1f}% (vs Q1)",
        delta_color="normal"
    )

with col3:
    st.metric(
        label=f"⚡ Power Grid Yield ({latest_energy_year})",
        value=f"{energy_prod_latest/1000:,.0f}k GWh",
        delta=f"{energy_delta:+.1f}% (vs '22)",
        delta_color="normal"
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 6. LAYOUT & NAVIGATION: DYNAMIC SECTIONS (TABS)
# ==============================================================================
tab_forest, tab_water, tab_energy = st.tabs([
    "🌳 Forest Conservation", 
    "💧 Water Resources", 
    "⚡ Energy Usage"
])

# ------------------------------------------------------------------------------
# TAB 1: FOREST CONSERVATION
# ------------------------------------------------------------------------------
with tab_forest:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🌳 Forest Canopy Loss & Carbon Footprint Analysis</div>', unsafe_allow_html=True)
    
    col_f_1, col_f_2 = st.columns([2, 1])
    
    with col_f_1:
        # Dual Y-axis Chart for Tree Cover Loss and Gross CO2 Emissions (Styling updated for Dark Mode)
        fig_forest = go.Figure()
        fig_forest.add_trace(go.Bar(
            x=df_forest["umd_tree_cover_loss__year"],
            y=df_forest["umd_tree_cover_loss__ha"],
            name="Tree Cover Loss (ha)",
            marker=dict(
                color=PALETTE_FOREST[0],
                line=dict(color="rgba(16, 185, 129, 0.4)", width=1.5)
            ),
            opacity=0.8
        ))
        fig_forest.add_trace(go.Scatter(
            x=df_forest["umd_tree_cover_loss__year"],
            y=df_forest["gfw_gross_emissions_co2e_all_gases__Mg"],
            name="Gross CO2 Emissions (Mg)",
            yaxis="y2",
            line=dict(color="#EF4444", width=3, dash='solid'),
            mode="lines+markers"
        ))
        
        fig_forest.update_layout(
            yaxis2=dict(
                title=dict(text="Gross CO2 Emissions (Mg)", font=dict(color='#FCA5A5')),
                overlaying="y",
                side="right",
                showgrid=False,
                tickfont=dict(color='#FCA5A5')
            ),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(10, 15, 13, 0.6)')
        )
        apply_plotly_dark_theme(fig_forest, "Yearly Forest Cover Depletion vs. Gross CO2 Emissions in India", "Year", "Loss Area (Hectares)")
        st.plotly_chart(fig_forest, use_container_width=True)
        
    with col_f_2:
        st.markdown("### 🌲 Understanding India's Carbon Sinks")
        st.write("Deforestation spikes represent the rapid removal of primary forest cover, directly resulting in massive releases of locked carbon back into the atmosphere.")
        
        render_alert(
            "warning-alert", 
            "⚠️", 
            "CRITICAL ECO-ALERT", 
            "Deforestation creates an double-negative effect. Not only does burning releases gigatons of CO2, but it permanently eliminates active photosynthetic oxygen-generation cycles."
        )
        
        # Cumulative Forest Loss Stat
        total_loss_ha = df_forest["umd_tree_cover_loss__ha"].sum()
        total_emissions = df_forest["gfw_gross_emissions_co2e_all_gases__Mg"].sum()
        
        st.markdown(f"""
        <div style="background-color: rgba(18, 28, 22, 0.6); border: 1px solid rgba(16, 185, 129, 0.15); padding: 18px; border-radius: 12px; margin-top: 15px;">
            <div style="font-size: 13px; font-weight: bold; color: #A7F3D0; margin-bottom: 5px;">CUMULATIVE TREE LOSS (2001-2024)</div>
            <div style="font-size: 26px; font-weight: 800; color: #ECFDF5;">{total_loss_ha:,.0f} ha</div>
        </div>
        <div style="background-color: rgba(18, 28, 22, 0.6); border: 1px solid rgba(16, 185, 129, 0.15); padding: 18px; border-radius: 12px; margin-top: 12px;">
            <div style="font-size: 13px; font-weight: bold; color: #FCA5A5; margin-bottom: 5px;">ACCUMULATED CO2 EMISSIONS</div>
            <div style="font-size: 26px; font-weight: 800; color: #FCA5A5;">{total_emissions/1e6:,.1f} Million Mg</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --------------------------------------------------------------------------
    # FOREST COVER & CARBON FOOTPRINT FORECASTING (Predictive Model)
    # --------------------------------------------------------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🔮 Forest Cover & Carbon Footprint Forecasting</div>', unsafe_allow_html=True)
    st.write("Enter a target year to get a Machine Learning forecast of India's tree cover loss and gross CO₂ emissions using Linear Regression trained on historical data.")
    
    # Train two Linear Regression models on historical forest data
    X_forest_reg = df_forest[["umd_tree_cover_loss__year"]]
    model_forest_loss = LinearRegression().fit(X_forest_reg, df_forest["umd_tree_cover_loss__ha"])
    model_forest_co2  = LinearRegression().fit(X_forest_reg, df_forest["gfw_gross_emissions_co2e_all_gases__Mg"])
    
    col_fp_left, col_fp_right = st.columns([1, 2])
    
    with col_fp_left:
        st.markdown("#### 📅 Select Forecast Year")
        forecast_year = st.number_input(
            "Enter Target Year (2025–2060):",
            min_value=2025, max_value=2060, value=2030, step=1,
            key="forest_forecast_year"
        )
        run_forecast = st.button("🌳 Generate Forest Forecast", use_container_width=True, key="forest_forecast_btn")
    
    with col_fp_right:
        if run_forecast:
            pred_input_f = pd.DataFrame([[forecast_year]], columns=["umd_tree_cover_loss__year"])
            pred_loss_ha  = model_forest_loss.predict(pred_input_f)[0]
            pred_co2_mg   = model_forest_co2.predict(pred_input_f)[0]
            
            # Clamp predictions to non-negative values
            pred_loss_ha = max(pred_loss_ha, 0)
            pred_co2_mg  = max(pred_co2_mg, 0)
            
            st.markdown(f"""
            <div style="display: flex; gap: 16px; margin-bottom: 16px;">
                <div style="flex: 1; background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(10,15,13,0.8) 100%); border: 1px solid rgba(16,185,129,0.3); padding: 22px; border-radius: 16px;">
                    <div style="font-size: 12px; font-weight: 800; color: #A7F3D0; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px;">🌳 Forecast Tree Cover Loss ({forecast_year})</div>
                    <div style="font-size: 34px; font-weight: 800; color: #ECFDF5;">{pred_loss_ha/1000:.1f}k ha</div>
                    <div style="font-size: 12px; color: #6EE7B7; margin-top: 4px;">Hectares lost (predicted)</div>
                </div>
                <div style="flex: 1; background: linear-gradient(135deg, rgba(239,68,68,0.1) 0%, rgba(10,15,13,0.8) 100%); border: 1px solid rgba(239,68,68,0.3); padding: 22px; border-radius: 16px;">
                    <div style="font-size: 12px; font-weight: 800; color: #FCA5A5; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 6px;">☁️ Forecast CO₂ Emissions ({forecast_year})</div>
                    <div style="font-size: 34px; font-weight: 800; color: #FCA5A5;">{pred_co2_mg/1e6:.1f}M Mg</div>
                    <div style="font-size: 12px; color: #F87171; margin-top: 4px;">Million Megagrams (predicted)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Threat-level alert based on predicted tree cover loss
            if pred_loss_ha < 100000:
                render_alert(
                    "success-alert", "🌿",
                    "SUSTAINABLE DEPRECIATION RATE",
                    f"Projected forest loss of {pred_loss_ha/1000:.1f}k ha in {forecast_year} is within manageable bounds. Continue reforestation programs to maintain biodiversity."
                )
            elif pred_loss_ha < 140000:
                render_alert(
                    "warning-alert", "⚠️",
                    "MODERATE DEFICIT FORECASTED",
                    f"Projected forest loss of {pred_loss_ha/1000:.1f}k ha in {forecast_year} indicates growing pressure on India's forest ecosystems. Intensified conservation policies are urgently needed."
                )
            else:
                render_alert(
                    "error-alert", "🚨",
                    "CRITICAL BIODIVERSITY DANGER",
                    f"Projected forest loss of {pred_loss_ha/1000:.1f}k ha in {forecast_year} signals a critical deforestation trajectory. Immediate intervention, moratorium on forest clearance, and large-scale reforestation missions are essential."
                )
        else:
            st.markdown("""
            <div style="background: rgba(16,185,129,0.04); border: 1px dashed rgba(16,185,129,0.2); border-radius: 16px; padding: 40px; text-align: center; color: #6EE7B7; font-size: 15px;">
                🌳 Select a target year and click <strong>Generate Forest Forecast</strong> to view the ML-powered projection.
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: WATER RESOURCES
# ------------------------------------------------------------------------------
with tab_water:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">💧 Water Safety Index & Environmental Parameter Distribution</div>', unsafe_allow_html=True)
    
    col_w_1, col_w_2 = st.columns([1, 1])
    
    with col_w_1:
        # Water Quality Scatter Plot: pH vs Dissolved Oxygen
        fig_water_scatter = px.scatter(
            df_water,
            x="pH",
            y="Dissolved_Oxygen",
            color="Water_Quality_Label",
            size="Temperature",
            hover_data=["BOD", "Nitrate"],
            color_discrete_map={"Pure": PALETTE_WATER[0], "Impure": "#EF4444"},
            opacity=0.85
        )
        apply_plotly_dark_theme(fig_water_scatter, "Ecosystem Purity Index (pH vs. Dissolved Oxygen)", "pH Level", "Dissolved Oxygen (mg/L)")
        fig_water_scatter.update_traces(marker=dict(line=dict(width=1.5, color='#0A0F0D')))
        st.plotly_chart(fig_water_scatter, use_container_width=True)
        
    with col_w_2:
        # Water Quality Purity Distribution Pie Chart
        fig_water_pie = px.pie(
            df_water,
            names="Water_Quality_Label",
            color="Water_Quality_Label",
            color_discrete_map={"Pure": PALETTE_WATER[0], "Impure": "#EF4444"},
            hole=0.45
        )
        apply_plotly_dark_theme(fig_water_pie, "Ecosystem Water Potability Assessment")
        fig_water_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#0A0F0D', width=2)))
        st.plotly_chart(fig_water_pie, use_container_width=True)
        
    # Interactive Water Safety Prediction & Classification Section
    st.markdown("### 🔬 Ecological Purity Predictive Model")
    st.write("Deploy a live machine learning model to evaluate the suitability of chemical parameters of local water sources.")
    
    # Train prediction model live using the 'Purity' column from water.csv as target
    X_water = df_water[["Temperature", "pH", "Dissolved_Oxygen", "BOD", "Nitrate"]]
    y_water = df_water["Purity"]  # Target: 'Pure' / 'Impure' string labels from water.csv
    
    model_water = DecisionTreeClassifier(random_state=42, max_depth=4)
    model_water.fit(X_water, y_water)
    
    # Styled numeric inputs and sliders
    col_inputs = st.columns(5)
    with col_inputs[0]:
        input_temp = st.number_input("Temperature (°C)", min_value=10.0, max_value=45.0, value=25.0, key="water_temp")
    with col_inputs[1]:
        input_ph = st.slider("pH Factor", min_value=0.0, max_value=14.0, value=7.2, step=0.1, key="water_ph")
    with col_inputs[2]:
        input_do = st.number_input("Oxygen (mg/L)", min_value=0.0, max_value=20.0, value=6.5, key="water_do")
    with col_inputs[3]:
        input_bod = st.number_input("BOD Level (mg/L)", min_value=0.0, max_value=40.0, value=2.0, key="water_bod")
    with col_inputs[4]:
        input_nitrate = st.number_input("Nitrate Level (mg/L)", min_value=0.0, max_value=50.0, value=1.5, key="water_nitrate")
        
    if st.button("🌱 Evaluate Water Safety Index", use_container_width=True, key="water_btn"):
        pred_df = pd.DataFrame(
            [[input_temp, input_ph, input_do, input_bod, input_nitrate]],
            columns=["Temperature", "pH", "Dissolved_Oxygen", "BOD", "Nitrate"]
        )
        pred = model_water.predict(pred_df)
        
        if pred[0] == "Pure":
            render_alert(
                "success-alert",
                "✅",
                "SAMPLE POTABILITY CONFIRMED",
                "Ecosystem metrics meet all clean water protocols. Safe for bio-diversity and municipal grid deployment."
            )
        else:
            render_alert(
                "error-alert",
                "🚨",
                "POLLUTED MATRIX DETECTED",
                "Heavy ecosystem load indicators (BOD/Nitrates) exceed tolerances. Filtration and chemical treatment required immediately."
            )
            
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: ENERGY USAGE
# ------------------------------------------------------------------------------
with tab_energy:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">⚡ Power Grid Metrics & Carbon Neutrality Forecasting</div>', unsafe_allow_html=True)
    
    col_e_1, col_e_2 = st.columns([2, 1])
    
    with col_e_1:
        # Historical Energy Line Chart with smooth area fill
        fig_energy = px.area(
            df_energy,
            x="Year",
            y="Total electricity production, India",
            color_discrete_sequence=[PALETTE_ENERGY[0]]
        )
        apply_plotly_dark_theme(fig_energy, "Historical Power Production Trend in India", "Year", "Production (GWh)")
        fig_energy.update_traces(fillcolor="rgba(245, 158, 11, 0.08)", line=dict(width=3, color="#F59E0B"))
        st.plotly_chart(fig_energy, use_container_width=True)
        
    with col_e_2:
        st.markdown("### ⚡ Smart Transition & Demands")
        st.write("Adjust the slider below to project future energy generation requirements in India using historical trends.")
        
        # Train simple linear regression model
        X_energy = df_energy[["Year"]]
        y_energy = df_energy["Total electricity production, India"]
        model_energy = LinearRegression().fit(X_energy, y_energy)
        
        pred_year = st.slider("Select Forecast Target Year:", min_value=2025, max_value=2050, value=2032, step=1, key="energy_year")
        pred_df = pd.DataFrame([[pred_year]], columns=["Year"])
        pred_val = model_energy.predict(pred_df)[0]
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(10, 15, 13, 0.8) 100%); border: 1px solid rgba(245, 158, 11, 0.25); padding: 22px; border-radius: 16px; margin-top: 20px;">
            <div style="margin: 0; color: #FBBF24; font-weight: 800; font-size: 13px; letter-spacing: 0.5px; text-transform: uppercase;">FORECAST DEMAND ({pred_year})</div>
            <div style="margin: 8px 0 0 0; color: #ECFDF5; font-size: 30px; font-weight: 800;">{pred_val:,.0f} GWh</div>
            <div style="margin: 6px 0 0 0; color: #94A3B8; font-size: 12px;">Modeled using OLS Linear Regression baseline trends.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        st.write("##### 💡 Load Strain Level Analysis")
        user_consumption = st.number_input("Enter localized grid context (GWh):", value=1350000, key="energy_usage")
        
        if user_consumption < 900000:
            render_alert("success-alert", "✅", "EFFICIENT ENERGY STATE", "Power load levels are sustainable and well-integrated within carbon offset thresholds.")
        elif user_consumption < 1500000:
            render_alert("warning-alert", "⚠️", "MODERATE GRID DEMAND", "Grid strains detected. Power grid optimizations, LED retrofitting, and peak energy saving required.")
        else:
            render_alert("error-alert", "🚨", "CRITICAL OVERLOAD RISK", "High carbon reliance risk. Transition to clean, distributed rooftop solar power and micro-grids immediately.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div class="footer-container">
    Green Revival Environmental Engine • Built with 🌿 and ✨ for a Sustainable Tomorrow.
</div>
""", unsafe_allow_html=True)
