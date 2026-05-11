import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu

# ============================================================
# 1. PAGE CONFIG & PREMIUM THEME
# ============================================================
st.set_page_config(
    page_title="Smart Sales Monitoring & Optimization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* ---- Global Background ---- */
    .stApp {
        background: linear-gradient(135deg, #f0f2f5 0%, #e8ecf1 100%) !important;
    }
    
    /* ---- Glassmorphism Cards ---- */
    .glass-card {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07) !important;
        padding: 24px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.12) !important;
    }
    
    /* ---- Metric Cards (KPIs) ---- */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        padding: 20px 16px !important;
        text-align: center !important;
        transition: all 0.25s ease;
    }
    .metric-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08) !important;
        border-color: rgba(148, 163, 184, 0.5) !important;
    }
    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 4px !important;
    }
    .metric-label {
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #64748b !important;
        letter-spacing: 0.3px !important;
        text-transform: uppercase !important;
    }
    .metric-delta {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-top: 6px !important;
    }
    
    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] .sidebar-content {
        padding-top: 20px !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }
    
    /* ---- Typography ---- */
    h1 { font-weight: 800 !important; color: #0f172a !important; letter-spacing: -0.5px !important; }
    h2 { font-weight: 700 !important; color: #1e293b !important; letter-spacing: -0.3px !important; margin-top: 32px !important; }
    h3 { font-weight: 600 !important; color: #334155 !important; }
    
    /* ---- Tables & DataFrames ---- */
    .stDataFrame, div[data-testid="stTable"] {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03) !important;
    }
    
    /* ---- Custom Divider ---- */
    .custom-divider {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
        margin: 28px 0 !important;
    }
    
    /* ---- Info / Insight Boxes ---- */
    .insight-box {
        background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%) !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 18px 22px !important;
        color: #1e3a5f !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }
    .insight-box strong { color: #1d4ed8 !important; }
    
    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 12px !important;
        padding: 18px 22px !important;
        color: #14532d !important;
    }
    
    /* ---- Selectbox / Inputs ---- */
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #cbd5e1 !important;
    }
    
    /* ---- Animations ---- */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    /* ---- Causal Impact Badge ---- */
    .causal-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
    }
    .badge-positive { background: #dcfce7; color: #166534; }
    .badge-negative { background: #fee2e2; color: #991b1b; }
    .badge-neutral { background: #f1f5f9; color: #475569; }
    </style>
""", unsafe_allow_html=True)


# ============================================================
# 2. DATA LOADING
# ============================================================
@st.cache_data(ttl=3600)
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [str(c).strip().lower() for c in df.columns]
        if 'date' not in df.columns:
            df = pd.read_csv(file_path, header=1)
            df.columns = [str(c).strip().lower() for c in df.columns]
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df.dropna(subset=['date'])
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_full_sales():
    try:
        df = pd.read_csv('Sales_and_variables.csv')
        df['date'] = pd.to_datetime(df['date'], format='%m.%d.%Y')
        return df.sort_values('date').reset_index(drop=True)
    except Exception:
        return pd.DataFrame()

df_raw      = load_data('raw_data.csv')
df_fixed    = load_data('fixed.csv')
df_item     = load_data('item_data.csv')
df_smart    = pd.read_csv('Sales_Data_Phase2_Smart_Cleaned.csv') if __import__('os').path.exists('Sales_Data_Phase2_Smart_Cleaned.csv') else pd.DataFrame()
df_sales    = load_full_sales()

try:
    df_flavor = pd.read_csv('item_flavour.csv')
except Exception:
    df_flavor = pd.DataFrame()

@st.cache_data(ttl=3600)
def _load_csv_safe(path):
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()

THESIS = {
    'correlations':            _load_csv_safe('thesis_correlations.csv'),
    'lag_correlations':        _load_csv_safe('thesis_lag_correlations.csv'),
    'event_impacts':           _load_csv_safe('thesis_event_impacts.csv'),
    'salary_cycle':            _load_csv_safe('thesis_salary_cycle.csv'),
    'regression':              _load_csv_safe('thesis_regression_importance.csv'),
    'regression_no_ramadan':   _load_csv_safe('thesis_regression_importance_no_ramadan.csv'),
    'highview_lag':            _load_csv_safe('thesis_platform_highview_lag.csv'),
    'model_comparison':        _load_csv_safe('thesis_model_comparison.csv'),
    'model_predictions':       _load_csv_safe('thesis_model_predictions_test.csv'),
    'clean':                   _load_csv_safe('Sales_and_variables_CLEAN.csv'),
}

# ============================================================
# 3. SIDEBAR NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px 0;">
            <div style="font-size: 2.4rem; margin-bottom: 8px;">📊</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.3px;">
                Smart Sales Monitor
            </div>
            <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 4px;">
                Monitoring & Optimization System
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    selected = option_menu(
        menu_title=None,
        options=["About", "Overview", "Findings", "Conclusion"],
        icons=["info-circle", "grid-3x3-gap", "bar-chart-line", "check2-circle"],
        menu_icon="cast",
        default_index=1,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#94a3b8", "font-size": "16px"},
            "nav-link": {
                "font-size": "14px", "text-align": "left", "margin": "6px 8px",
                "color": "#cbd5e1", "border-radius": "10px", "padding": "10px 14px"
            },
            "nav-link-selected": {
                "background-color": "#3b82f6", "color": "#ffffff",
                "font-weight": "600", "box-shadow": "0 4px 14px rgba(59,130,246,0.35)"
            },
            "nav-link-hover": {"background-color": "rgba(255,255,255,0.08)"},
        }
    )
    
    st.divider()
    
    st.markdown("""
        <div style="padding: 0 8px;">
            <div style="font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;">
                Research Team
            </div>
            <div style="font-size: 0.82rem; color: #e2e8f0; line-height: 1.6;">
                Paywand Yousif<br>
                Amanj Salih<br>
                Shnyar Baram
            </div>
            <div style="margin-top: 12px; font-size: 0.7rem; color: #64748b;">
                Supervisor: Dr. Miran Taha
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.caption("Final Version — May 2026")


# ============================================================
# HELPER: KPI CARD
# ============================================================
def kpi_card(col, emoji, value, label, delta=None, delta_color="normal"):
    delta_html = ""
    if delta is not None:
        color = "#22c55e" if delta_color == "normal" and delta >= 0 else "#ef4444"
        sign = "+" if delta >= 0 else ""
        delta_html = f'<div class="metric-delta" style="color:{color};">{sign}{delta:.2f}</div>'
    col.markdown(f"""
        <div class="metric-card animate-in">
            <div style="font-size: 1.6rem; margin-bottom: 8px;">{emoji}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# SECTION 1: ABOUT
# ============================================================
if selected == "About":
    st.markdown("""
        <div style="text-align:center; padding: 40px 0 30px 0;">
            <div style="font-size: 3rem; margin-bottom: 16px;">🎯</div>
            <h1 style="font-size: 2.4rem; margin-bottom: 12px;">Smart Sales Monitoring & Optimization</h1>
            <p style="font-size: 1.1rem; color: #64748b; max-width: 600px; margin: 0 auto;">
                A graduation research project integrating internal sales metrics with 
                external digital and economic factors for predictive analytics.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="glass-card" style="height: 240px;">
                <div style="font-size: 2rem; margin-bottom: 12px;">🔒</div>
                <h3 style="margin-bottom: 10px;">Secure Data Storage</h3>
                <p style="color: #64748b; font-size: 0.92rem; line-height: 1.6;">
                    All raw operational data stored securely. Sales figures are indexed to maintain 
                    confidentiality while enabling full analytical depth.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="glass-card" style="height: 240px;">
                <div style="font-size: 2rem; margin-bottom: 12px;">🧠</div>
                <h3 style="margin-bottom: 10px;">Causal Inference Engine</h3>
                <p style="color: #64748b; font-size: 0.92rem; line-height: 1.6;">
                    Beyond correlation: Bayesian Structural Time Series (BSTS) models build 
                    counterfactual predictions to estimate true causal impact of interventions.
                </p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="glass-card" style="height: 240px;">
                <div style="font-size: 2rem; margin-bottom: 12px;">📈</div>
                <h3 style="margin-bottom: 10px;">Predictive Optimization</h3>
                <p style="color: #64748b; font-size: 0.92rem; line-height: 1.6;">
                    Identifies platform-specific lag patterns (TikTok instant, Instagram 3-day lag) 
                    and seasonal drivers to inform strategic budget allocation.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <h3 style="margin-bottom: 16px;">📋 System Capabilities</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 6px;">1. Contextual Intelligence</div>
                    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                        Differentiates weekdays vs weekends, school/university sessions, 
                        salary injection days, and public holidays.
                    </p>
                </div>
                <div>
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 6px;">2. Multi-Channel Attribution</div>
                    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                        Tracks Facebook, Instagram, and TikTok metrics with lag analysis 
                        to uncover each platform's unique conversion timeline.
                    </p>
                </div>
                <div>
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 6px;">3. Automated Exploration</div>
                    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                        Interactive data tables with date-range filtering, statistical 
                        summaries, and responsive metric cards.
                    </p>
                </div>
                <div>
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 6px;">4. Event Impact Quantification</div>
                    <p style="color: #64748b; font-size: 0.9rem; line-height: 1.5;">
                        BSTS CausalImpact analysis for Ramazan periods and influencer 
                        campaigns with validated placebo tests.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ============================================================
# SECTION 2: OVERVIEW
# ============================================================
elif selected == "Overview":
    st.markdown("""
        <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px;">
            <h1 style="margin: 0;">Business Intelligence Overview</h1>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500; background: #f1f5f9; padding: 3px 10px; border-radius: 20px;">
                raw_data.csv
            </span>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_raw.empty:
        # ---- KPI Row ----
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        kpi_card(kpi1, "📈", f"{df_raw['indexed sales'].mean():.2f}", "Avg Sales Index")
        kpi_card(kpi2, "🔥", f"{df_raw['tiktok view'].sum()/1e6:.2f}M", "TikTok Views")
        kpi_card(kpi3, "📸", f"{df_raw['instagram view'].sum()/1e6:.2f}M", "Instagram Views")
        kpi_card(kpi4, "📘", f"{df_raw['facebook view'].sum()/1e6:.2f}M", "Facebook Views")
        kpi_card(kpi5, "🏆", f"{df_raw['indexed sales'].max():.2f}", "Peak Daily Sales")
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # ---- Summary Table ----
        col_left, col_right = st.columns([5, 7])
        
        with col_left:
            st.markdown("""
                <div class="glass-card" style="padding: 20px !important; height: 100%;">
                    <h3 style="margin-bottom: 16px; font-size: 1.05rem;">Statistical Performance Summary</h3>
            """, unsafe_allow_html=True)
            
            rename_map = {
                'indexed sales': 'Indexed Sales', 'facebook view': 'Facebook Views',
                'facebook follow': 'Facebook Follows', 'instagram view': 'Instagram Views',
                'instagram followers': 'Instagram Followers', 'tiktok view': 'TikTok Views',
                'tiktok phone click': 'TikTok Phone Clicks'
            }
            avail = [c for c in rename_map if c in df_raw.columns]
            summary = df_raw[avail].describe().T[['mean', 'min', 'max']]
            summary.index = [rename_map.get(c, c) for c in summary.index]
            summary.columns = ['Average', 'Minimum', 'Maximum']
            
            st.table(summary.style.format("{:,.2f}").set_properties(**{
                'font-size': '0.88rem',
                'text-align': 'center'
            }).set_table_styles([
                {'selector': 'th', 'props': 'background-color: #f8fafc; color: #475569; font-weight: 600; padding: 10px; border-bottom: 2px solid #e2e8f0;'},
                {'selector': 'td', 'props': 'padding: 10px; border-bottom: 1px solid #f1f5f9;'},
                {'selector': 'tr:hover', 'props': 'background-color: #f8fafc !important;'}
            ]))
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown("""
                <div class="glass-card" style="padding: 20px !important; height: 100%;">
                    <h3 style="margin-bottom: 16px; font-size: 1.05rem;">Raw Data Explorer</h3>
            """, unsafe_allow_html=True)
            
            min_date = df_raw['date'].min().date()
            max_date = df_raw['date'].max().date()
            
            d1, d2 = st.columns(2)
            with d1:
                t_start = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
            with d2:
                t_end = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date, label_visibility="collapsed")
            
            filtered = df_raw.loc[(df_raw['date'].dt.date >= t_start) & (df_raw['date'].dt.date <= t_end)]
            display_df = filtered.copy()
            display_df.columns = [str(c).title() for c in display_df.columns]
            
            st.dataframe(display_df, use_container_width=True, height=320)
            st.markdown(f"""
                <div style="text-align: right; font-size: 0.78rem; color: #94a3b8; margin-top: 8px;">
                    Showing {len(filtered):,} rows
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # ---- Monthly Product Trend ----
        if not df_item.empty:
            st.subheader("Monthly Sales Performance: Top 3 Items")
            
            df_item['date'] = pd.to_datetime(df_item['date'], errors='coerce')
            df_item = df_item.dropna(subset=['date']).sort_values('date')
            df_item['month_name'] = df_item['date'].dt.strftime('%b %Y')
            
            def map_items(name):
                n = str(name).lower()
                if 'shklet special' in n: return 'Item 1'
                if 'dubai special' in n: return 'Item 2'
                if 'maqluba' in n: return 'Item 3'
                return 'Other'
            
            df_item['category'] = df_item['item'].apply(map_items)
            monthly = df_item[df_item['category'] != 'Other'].groupby(['month_name', 'category'], sort=False)['quantity_sold'].sum().reset_index()
            
            fig_items = px.line(
                monthly, x='month_name', y='quantity_sold', color='category', markers=True,
                text='quantity_sold',
                color_discrete_sequence=['#1e293b', '#ee1d52', '#64748b']
            )
            fig_items.update_traces(
                textposition="top center", texttemplate='%{text:.0f}', textfont_size=11,
                line=dict(width=3), marker=dict(size=9, line=dict(width=1, color='white'))
            )
            fig_items.update_layout(
                xaxis_title="", yaxis_title="Total Quantity Sold",
                legend_title="Product", template="plotly_white",
                margin=dict(t=30, b=10, l=10, r=10), hovermode="x unified",
                font=dict(family="Inter, sans-serif", size=12),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_items, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
        
        # ---- Sauce Split + Weekly Rhythm ----
        c_sauce, c_rhythm = st.columns([3, 7])
        
        with c_sauce:
            if not df_flavor.empty:
                st.subheader("Sauce Split")
                df_pie = df_flavor[df_flavor['Flavor'] != 'Total Sold'].copy()
                def map_sauce(f):
                    if f == 'Chocolate': return 'Sauce 1'
                    if f == 'Nutella': return 'Sauce 2'
                    return f
                df_pie['Sauce'] = df_pie['Flavor'].apply(map_sauce)
                
                fig_sauce = px.pie(
                    df_pie, names='Sauce', values='quantity_sold', hole=0.55,
                    color_discrete_map={'Sauce 1': '#D2B48C', 'Sauce 2': '#FFDAB9'}
                )
                fig_sauce.update_traces(
                    textposition='inside', textinfo='percent+label', textfont_size=12,
                    insidetextfont=dict(color='black'),
                    marker=dict(line=dict(color='#ffffff', width=3))
                )
                fig_sauce.update_layout(
                    showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=360,
                    font=dict(family="Inter, sans-serif"),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_sauce, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with c_rhythm:
            if not df_smart.empty and 'Indexed Sales' in df_smart.columns:
                st.subheader("Weekly Sales Rhythm")
                df_temp = df_smart.copy()
                df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce')
                df_temp['day_name'] = df_temp['date'].dt.day_name()
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                weekday_avg = df_temp.groupby('day_name')['Indexed Sales'].mean().reindex(day_order).reset_index()
                baseline = df_temp['Indexed Sales'].mean()
                
                fire_colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#10b981', '#3b82f6', '#8b5cf6']
                
                fig_bar = px.bar(
                    weekday_avg, x='day_name', y='Indexed Sales', text='Indexed Sales',
                    color='day_name', color_discrete_sequence=fire_colors
                )
                fig_bar.update_traces(
                    texttemplate='%{text:.2f}', textposition='outside',
                    marker=dict(line=dict(color='white', width=1.5)), opacity=0.9
                )
                fig_bar.add_hline(
                    y=baseline, line_dash="dash", line_color="#64748b", opacity=0.5,
                    annotation_text=f"Avg: {baseline:.2f}", annotation_position="top left"
                )
                fig_bar.update_layout(
                    xaxis_title=None, yaxis_title="Avg Indexed Sales",
                    showlegend=False, margin=dict(t=30, b=10, l=10, r=10), height=360,
                    font=dict(family="Inter, sans-serif", size=12),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)



# ============================================================
# SECTION 3: FINDINGS — interactive versions of the thesis figures
# ============================================================
elif selected == "Findings":
    st.markdown("""
        <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px;">
            <h1 style="margin: 0;">Findings</h1>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500; background: #f1f5f9; padding: 3px 10px; border-radius: 20px;">
                Interactive analysis
            </span>
        </div>
        <p style="color:#64748b; max-width:900px; margin-top:4px;">
            Eight numbered findings derived from 361 days of indexed sales data, ordered by effect size.
            Every chart is interactive — hover for exact values, zoom in on any region, and toggle
            traces in the legend.
        </p>
    """, unsafe_allow_html=True)

    df_clean = THESIS['clean']

    # ---------- Anchor / Jump-to bar ----------
    st.markdown("""
        <style>
        .findings-nav a {
            display:inline-block; padding:6px 12px; margin:4px 4px 4px 0;
            background:#ffffff; border:1px solid #e2e8f0; border-radius:20px;
            color:#475569; text-decoration:none; font-size:0.82rem; font-weight:500;
            transition: all 0.15s ease;
        }
        .findings-nav a:hover { background:#3b82f6; color:#ffffff; border-color:#3b82f6; }
        </style>
        <div class="findings-nav" style="margin: 8px 0 24px 0;">
            <a href="#f-desc">Descriptive</a>
            <a href="#f-1">1. Ramadan</a>
            <a href="#f-2">2. Clicks vs Views</a>
            <a href="#f-3">3. Platform Lag</a>
            <a href="#f-4">4. Payday V-shape</a>
            <a href="#f-5">5. Weekly Rhythm</a>
            <a href="#f-6">6. Events & Influencers</a>
            <a href="#f-7">7. Regression</a>
            <a href="#f-8">8. Predictive Models</a>
        </div>
    """, unsafe_allow_html=True)

    # =============================================================
    # DESCRIPTIVE STATISTICS
    # =============================================================
    st.markdown('<a id="f-desc"></a>', unsafe_allow_html=True)
    st.subheader("Descriptive Statistics")
    st.markdown(
        "Before any modelling, we summarise the target variable, **Indexed Sales**, across the "
        "full 361-day study period (5 Jan – 31 Dec 2025). A value of **1.00** means an average day; "
        "**2.00** means twice the average."
    )
    if not df_clean.empty and 'Indexed Sales' in df_clean.columns:
        y = df_clean['Indexed Sales'].dropna()
        d_stats = pd.DataFrame({
            'Statistic': ['Mean (μ)', 'Median', 'Std. dev (σ)', 'CV (σ/μ)', 'Min', 'Max', 'n'],
            'Value':     [f"{y.mean():.2f}", f"{y.median():.2f}", f"{y.std():.2f}",
                          f"{y.std()/y.mean()*100:.0f}%", f"{y.min():.2f}",
                          f"{y.max():.2f}", f"{len(y)}"]
        })
        c1, c2 = st.columns([1, 2])
        with c1:
            st.table(d_stats.set_index('Statistic'))
        with c2:
            fig_h = px.histogram(y, nbins=40, color_discrete_sequence=['#3b82f6'])
            fig_h.add_vline(x=y.mean(), line_dash='dash', line_color='#ef4444',
                            annotation_text=f"Mean {y.mean():.2f}")
            fig_h.update_layout(
                title="Distribution of daily Indexed Sales",
                xaxis_title="Indexed Sales", yaxis_title="Days",
                template="plotly_white", showlegend=False, height=330,
                margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_h, use_container_width=True)
    st.markdown(
        "<div class='insight-box'>The mean (1.19) exceeds the median (1.05), indicating a "
        "<strong>right-skewed distribution</strong> — a few exceptionally high days (mostly Ramadan) "
        "pull the average up. The coefficient of variation (~48%) places this business at the upper "
        "end of the normal range for sweets retail (30–50%).</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 1 — RAMADAN
    # =============================================================
    st.divider()
    st.markdown('<a id="f-1"></a>', unsafe_allow_html=True)
    st.subheader("Finding 1 — Ramadan dominates everything (+154%)")
    st.markdown(
        "The single largest sales driver in the entire dataset is **Ramadan**. Daily sales during "
        "Ramadan 2025 reached **2.5× the typical monthly baseline**, with peaks of 3.27 (more than "
        "three times the annual mean)."
    )
    if not df_clean.empty and 'Indexed Sales' in df_clean.columns and 'date' in df_clean.columns:
        df_t = df_clean.copy()
        df_t['date'] = pd.to_datetime(df_t['date'], errors='coerce')
        df_t = df_t.dropna(subset=['date']).sort_values('date')

        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(
            x=df_t['date'], y=df_t['Indexed Sales'], mode='lines',
            name='Daily Sales', line=dict(color='#0f172a', width=1.5)
        ))
        if 'Ramadan' in df_t.columns:
            r_mask = df_t['Ramadan'] == 1
            if r_mask.any():
                rmin, rmax = df_t.loc[r_mask, 'date'].min(), df_t.loc[r_mask, 'date'].max()
                fig_r.add_vrect(x0=rmin, x1=rmax, fillcolor='#f59e0b', opacity=0.20,
                                line_width=0, annotation_text="Ramadan",
                                annotation_position="top left")
        fig_r.add_hline(y=df_t['Indexed Sales'].mean(), line_dash='dash', line_color='#64748b',
                        annotation_text=f"Annual mean {df_t['Indexed Sales'].mean():.2f}")
        fig_r.update_layout(
            title="Daily Indexed Sales (Ramadan period highlighted)",
            xaxis_title=None, yaxis_title="Indexed Sales",
            template="plotly_white", height=420, hovermode="x unified",
            margin=dict(t=50, b=10, l=10, r=10),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_r, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Ramadan uplift", "+154.2%", "vs non-Ramadan")
    c2.metric("Peak day (Ramadan)", "3.27", "vs mean 1.19")
    c3.metric("Statistical significance", "p < 0.001", "Welch's t-test")

    st.markdown(
        "<div class='insight-box'>Since the majority of the population fasts during Ramadan, "
        "demand for sweets and beverages surges in the evening hours when families break their fast. "
        "This is the most consistent and predictable sales spike of the year — and it dominates any "
        "analysis that includes it.</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 2 — TIKTOK CLICKS vs VIEWS
    # =============================================================
    st.divider()
    st.markdown('<a id="f-2"></a>', unsafe_allow_html=True)
    st.subheader("Finding 2 — On TikTok, clicks beat views")
    st.markdown(
        "Despite TikTok views reaching up to **600,000 per day**, they have almost no relationship "
        "with daily sales (r ≈ +0.11). **Phone clicks** — which never exceed ~45 per day — show a "
        "much stronger positive trend (r = +0.44). In short: **20 phone clicks generate more "
        "measurable sales impact than 600,000 views**."
    )
    if not df_clean.empty and {'TikTok View', 'TikTok Phone Click', 'Indexed Sales'}.issubset(df_clean.columns):
        def _scatter_with_trend(df, x_col, y_col, color, title):
            sub = df[[x_col, y_col]].dropna()
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sub[x_col], y=sub[y_col], mode='markers',
                marker=dict(color=color, size=7, opacity=0.55,
                            line=dict(width=0.5, color='white')),
                name='Daily points'
            ))
            if len(sub) > 2 and sub[x_col].std() > 0:
                slope, intercept = np.polyfit(sub[x_col], sub[y_col], 1)
                xs = np.linspace(sub[x_col].min(), sub[x_col].max(), 50)
                ys = slope * xs + intercept
                fig.add_trace(go.Scatter(
                    x=xs, y=ys, mode='lines', name='OLS trend',
                    line=dict(color='#0f172a', width=2, dash='dash')
                ))
            fig.update_layout(
                title=title, xaxis_title=x_col, yaxis_title=y_col,
                template="plotly_white", height=380, showlegend=False,
                margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(
                _scatter_with_trend(df_clean, 'TikTok View', 'Indexed Sales',
                                    '#94a3b8', "TikTok Views vs Sales — flat trend (r=+0.11)"),
                use_container_width=True
            )
        with c2:
            st.plotly_chart(
                _scatter_with_trend(df_clean, 'TikTok Phone Click', 'Indexed Sales',
                                    '#ee1d52', "TikTok Clicks vs Sales — clear positive (r=+0.44)"),
                use_container_width=True
            )

    st.markdown(
        "<div class='insight-box'>The TikTok phone-click signal is strongest on the same day "
        "(r = +0.44) and decays steadily over the following three days. <strong>Views are vanity; "
        "clicks are revenue.</strong> Optimise content for the call-to-action, not raw reach.</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 3 — PLATFORM LAG EFFECTS
    # =============================================================
    st.divider()
    st.markdown('<a id="f-3"></a>', unsafe_allow_html=True)
    st.subheader("Finding 3 — Platform lag effects after high-view days")
    st.markdown(
        "When a platform has a **high-view day** (top 25% of its distribution), what happens to "
        "sales over the following 0–3 days? This reveals each platform's conversion timeline."
    )
    if not THESIS['highview_lag'].empty:
        hv = THESIS['highview_lag'].copy()
        hv['lag_label'] = hv['lag_days'].map({0: 'Day 0', 1: 'Day +1', 2: 'Day +2', 3: 'Day +3'})
        fig_hv = px.line(
            hv, x='lag_label', y='mean_on', color='platform', markers=True,
            color_discrete_map={'TikTok': '#ee1d52', 'Instagram': '#833ab4', 'Facebook': '#1877f2'}
        )
        fig_hv.update_traces(line=dict(width=3), marker=dict(size=11))
        fig_hv.update_layout(
            title="Mean Indexed Sales after high-view days, by platform",
            xaxis_title=None, yaxis_title="Mean Indexed Sales",
            template="plotly_white", height=420, hovermode="x unified",
            margin=dict(t=50, b=10, l=10, r=10),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_hv, use_container_width=True)

    st.markdown(
        "<div class='insight-box'>Instagram and Facebook function as <strong>direct-conversion "
        "channels</strong> — views translate to sales within the first 24 hours. TikTok views, by "
        "contrast, never show this same-day or short-lag boost; only TikTok <em>clicks</em> "
        "translate to sales (see Finding 2).</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 4 — PRIVATE SECTOR PAYDAY V-SHAPE
    # =============================================================
    st.divider()
    st.markdown('<a id="f-4"></a>', unsafe_allow_html=True)
    st.subheader("Finding 4 — Private sector payday produces a clear V-shape")
    st.markdown(
        "Most private-sector employees in Sulaymaniyah are paid on the **1st of each month**. "
        "Households defer spending in the days before payday and rebound sharply on the day itself — "
        "creating a recurring **V-shaped sales pattern**."
    )
    if not THESIS['salary_cycle'].empty:
        sc = THESIS['salary_cycle']
        sc_priv = sc[(sc['sector'] == 'Private Sector Salary') & (sc['scope'] == 'All days')]
        if not sc_priv.empty:
            sc_priv = sc_priv.sort_values('offset')
            colors = ['#e76f51' if v < 0 else '#2a9d8f' for v in sc_priv['uplift']]
            fig_sc = go.Figure()
            fig_sc.add_trace(go.Bar(
                x=[f"Day {int(o):+d}" if o != 0 else "Day 0 (payday)" for o in sc_priv['offset']],
                y=sc_priv['uplift'], marker_color=colors,
                text=[f"{v:+.1f}%" for v in sc_priv['uplift']],
                textposition='outside'
            ))
            fig_sc.add_hline(y=0, line_color='black', line_width=1)
            fig_sc.update_layout(
                title="Sales response around private sector payday (% vs baseline)",
                yaxis_title="Uplift vs baseline (%)", xaxis_title=None,
                template="plotly_white", showlegend=False, height=420,
                margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_sc, use_container_width=True)

    st.markdown(
        "<div class='insight-box'>Sales drop <strong>−17% to −22%</strong> two days before payday "
        "(the pre-payday slump), then rebound to <strong>+8%</strong> on payday itself — a swing of "
        "roughly +25 percentage points in a single day. The boost extends through the following "
        "week. <em>Counter-finding</em>: the public sector does not show this pattern, attributable "
        "to the well-documented irregularity of KRG public salary disbursement and the small sample "
        "(n = 11 paydays).</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 5 — WEEKLY SEASONALITY
    # =============================================================
    st.divider()
    st.markdown('<a id="f-5"></a>', unsafe_allow_html=True)
    st.subheader("Finding 5 — Weekly rhythm: Friday peaks, Monday troughs")
    st.markdown(
        "Sales rise progressively from Monday through Friday before declining over the weekend. "
        "The Friday-vs-Monday gap is approximately **28%** — a substantial intra-week swing that "
        "should drive staffing and stocking decisions."
    )
    if not df_clean.empty and 'Indexed Sales' in df_clean.columns and 'date' in df_clean.columns:
        df_w = df_clean.copy()
        df_w['date'] = pd.to_datetime(df_w['date'], errors='coerce')
        df_w = df_w.dropna(subset=['date'])
        df_w['day'] = df_w['date'].dt.day_name()
        order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly = df_w.groupby('day')['Indexed Sales'].mean().reindex(order).reset_index()
        baseline = df_w['Indexed Sales'].mean()
        fig_w = go.Figure()
        fig_w.add_trace(go.Bar(
            x=weekly['day'], y=weekly['Indexed Sales'],
            marker_color=['#94a3b8'] * 4 + ['#10b981'] + ['#94a3b8'] * 2,
            text=[f"{v:.2f}" for v in weekly['Indexed Sales']],
            textposition='outside'
        ))
        fig_w.add_hline(y=baseline, line_dash='dash', line_color='#64748b',
                        annotation_text=f"Overall mean {baseline:.2f}")
        fig_w.update_layout(
            title="Mean Indexed Sales by day of the week",
            yaxis_title="Mean Indexed Sales", xaxis_title=None, showlegend=False,
            template="plotly_white", height=420, margin=dict(t=50, b=10, l=10, r=10),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_w, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 6 — EVENTS & INFLUENCERS
    # =============================================================
    st.divider()
    st.markdown('<a id="f-6"></a>', unsafe_allow_html=True)
    st.subheader("Finding 6 — Events drive sales; influencer posts barely move the needle")
    st.markdown(
        "Event days produce a strong **+51.6% uplift** in mean sales (p < 0.001). Influencer posts "
        "show a smaller **+8.2%** directional uplift, but the effect is **not statistically "
        "significant** (p = 0.504) given the small sample (n = 16 posts)."
    )
    if not THESIS['event_impacts'].empty:
        ev = THESIS['event_impacts']
        row_event = ev[ev['condition'] == 'Had Event']
        row_infl  = ev[ev['condition'].str.contains('Influencer', case=False, na=False)]

        c1, c2 = st.columns(2)
        if not row_event.empty:
            r = row_event.iloc[0]
            with c1:
                fig_e = go.Figure()
                fig_e.add_trace(go.Bar(
                    x=['No Event', 'Event Day'], y=[r['mean_off'], r['mean_on']],
                    marker_color=['#264653', '#2a9d8f'], width=0.55,
                    text=[f"{r['mean_off']:.2f}", f"{r['mean_on']:.2f}"],
                    textposition='outside', textfont=dict(size=14)
                ))
                fig_e.add_annotation(x='Event Day', y=r['mean_on'] + 0.15,
                                     text=f"+{r['uplift_pct']:.1f}% uplift",
                                     showarrow=False, font=dict(color='#2a9d8f', size=13))
                fig_e.update_layout(
                    title="Event-Day Sales Uplift", yaxis_title="Mean Indexed Sales",
                    template="plotly_white", height=380, showlegend=False,
                    margin=dict(t=50, b=10, l=10, r=10),
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                )
                fig_e.update_yaxes(range=[0, r['mean_on'] * 1.4])
                st.plotly_chart(fig_e, use_container_width=True)
        # Influencer side — compute on the fly from clean data
        if not df_clean.empty and 'Influencer Post' in df_clean.columns and 'Indexed Sales' in df_clean.columns:
            ion  = df_clean.loc[df_clean['Influencer Post'] == 1, 'Indexed Sales']
            ioff = df_clean.loc[df_clean['Influencer Post'] == 0, 'Indexed Sales']
            if len(ion) > 0:
                uplift_i = (ion.mean() / ioff.mean() - 1) * 100
                with c2:
                    fig_i = go.Figure()
                    fig_i.add_trace(go.Bar(
                        x=['No Influencer Post', 'Influencer Post'], y=[ioff.mean(), ion.mean()],
                        marker_color=['#264653', '#e76f51'], width=0.55,
                        text=[f"{ioff.mean():.2f}", f"{ion.mean():.2f}"],
                        textposition='outside', textfont=dict(size=14)
                    ))
                    fig_i.add_annotation(x='Influencer Post', y=ion.mean() + 0.12,
                                         text=f"+{uplift_i:.1f}% (not significant)",
                                         showarrow=False, font=dict(color='#e76f51', size=12))
                    fig_i.update_layout(
                        title="Influencer Post Sales Impact", yaxis_title="Mean Indexed Sales",
                        template="plotly_white", height=380, showlegend=False,
                        margin=dict(t=50, b=10, l=10, r=10),
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
                    )
                    fig_i.update_yaxes(range=[0, ion.mean() * 1.5])
                    st.plotly_chart(fig_i, use_container_width=True)

    st.markdown(
        "<div class='insight-box'>Physical events deliver a reliable, statistically significant "
        "sales lift and should be prioritised. Influencer partnerships look promising directionally "
        "but cannot yet be defended on the data — more posts (and tracked campaigns) are needed "
        "before drawing conclusions.</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 7 — REGRESSION COEFFICIENTS
    # =============================================================
    st.divider()
    st.markdown('<a id="f-7"></a>', unsafe_allow_html=True)
    st.subheader("Finding 7 — Independent drivers from multivariate regression")
    st.markdown(
        "A standardised OLS regression with all 14 predictors entered simultaneously achieves "
        "**R² = 0.63**, explaining 63% of daily variation. The chart below shows the **positive "
        "independent contributors** — each variable's effect after controlling for all others."
    )
    if not THESIS['regression'].empty:
        reg = THESIS['regression']
        pos = reg[reg['std_beta'] > 0].sort_values('std_beta', ascending=True)
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(
            y=pos['variable'], x=pos['std_beta'], orientation='h',
            marker_color='#2a9d8f',
            text=[f"+{v:.2f}" for v in pos['std_beta']],
            textposition='outside', textfont=dict(size=12, color='#2a9d8f')
        ))
        fig_reg.update_layout(
            title="Positive standardised OLS coefficients (R² = 0.63)",
            xaxis_title="Std. β  (impact on sales, in σ units)", yaxis_title=None,
            template="plotly_white", height=460, showlegend=False,
            margin=dict(t=50, b=10, l=10, r=40),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    st.markdown(
        "<div class='insight-box'>Ramadan dwarfs every other variable (β = +0.81), confirming its "
        "dominance. Among non-Ramadan drivers, TikTok views, Facebook follows, Instagram views, "
        "and school terms emerge as the strongest independent contributors.</div>",
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # =============================================================
    # FINDING 8 — PREDICTIVE MODELS
    # =============================================================
    st.divider()
    st.markdown('<a id="f-8"></a>', unsafe_allow_html=True)
    st.subheader("Finding 8 — Sales are non-linear: tree models beat linear")
    st.markdown(
        "We trained three models on a chronological 80/20 split (first 290 days train, last 71 "
        "days test): **Ridge Regression** (linear), **Random Forest** (non-linear), and **Gradient "
        "Boosting** (non-linear). The linear model fails completely; both non-linear models succeed."
    )
    if not THESIS['model_comparison'].empty:
        mc = THESIS['model_comparison']
        c1, c2 = st.columns(2)
        with c1:
            order = mc.sort_values('R2', ascending=True)
            colors = ['#1f77b4' if 'Ridge' in m else '#2a9d8f' if 'Random' in m else '#e76f51'
                      for m in order['model']]
            fig_r2 = go.Figure()
            fig_r2.add_trace(go.Bar(
                y=order['model'], x=order['R2'], orientation='h',
                marker_color=colors,
                text=[f"{v:+.2f}" for v in order['R2']],
                textposition='outside', textfont=dict(size=14, color='#0f172a')
            ))
            fig_r2.add_vline(x=0, line_color='black', line_width=1)
            fig_r2.update_layout(
                title="Out-of-sample R² (Test Set)", xaxis_title="Test R²", yaxis_title=None,
                template="plotly_white", height=380, showlegend=False,
                margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_r2, use_container_width=True)
        with c2:
            fig_mp = go.Figure()
            fig_mp.add_trace(go.Bar(
                x=mc['model'], y=mc['MAPE_pct'], marker_color=['#1f77b4', '#2a9d8f', '#e76f51'],
                text=[f"{v:.1f}%" for v in mc['MAPE_pct']],
                textposition='outside', textfont=dict(size=13)
            ))
            fig_mp.update_layout(
                title="Mean Absolute Percentage Error (lower = better)",
                yaxis_title="MAPE (%)", template="plotly_white",
                showlegend=False, height=380, margin=dict(t=50, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_mp, use_container_width=True)

    if not THESIS['model_predictions'].empty:
        mp = THESIS['model_predictions'].copy()
        mp['date'] = pd.to_datetime(mp['date'], errors='coerce')
        st.markdown("##### Test set predictions — actual vs predicted, last 71 days")
        st.caption("Each model is shown on its own axis with the actual sales line in black for direct comparison.")
        model_specs = [
            ('Ridge',            'Ridge Regression (linear)',  '#1f77b4', '-0.55', '26.7%'),
            ('RandomForest',     'Random Forest (non-linear)', '#2a9d8f', '+0.30', '15.1%'),
            ('GradientBoosting', 'Gradient Boosting (non-linear)', '#e76f51', '+0.32', '14.7%'),
        ]
        for col, label, color, r2, mape in model_specs:
            if col not in mp.columns:
                continue
            fig_m = go.Figure()
            fig_m.add_trace(go.Scatter(
                x=mp['date'], y=mp['actual'], mode='lines',
                name='Actual', line=dict(color='#0f172a', width=2.5)
            ))
            fig_m.add_trace(go.Scatter(
                x=mp['date'], y=mp[col], mode='lines',
                name='Predicted', line=dict(color=color, width=2)
            ))
            fig_m.update_layout(
                title=f"{label}  —  Test R² = {r2}, MAPE = {mape}",
                yaxis_title="Indexed Sales", xaxis_title=None,
                template="plotly_white", height=330, hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=55, b=10, l=10, r=10),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_m, use_container_width=True)

    st.markdown(
        "<div class='insight-box'>Ridge scored <strong>R² = −0.55</strong> — worse than guessing "
        "the daily average. Random Forest (+0.30) and Gradient Boosting (+0.32) captured the "
        "complex interactions between religious calendar, digital marketing, and payday cycles. "
        "<strong>The sales system is fundamentally non-linear and interaction-driven.</strong> "
        "Accurate forecasting requires models that can capture how variables combine — not just "
        "add up.</div>",
        unsafe_allow_html=True
    )


# ============================================================
# SECTION 4: CONCLUSION
# ============================================================
elif selected == "Conclusion":
    st.markdown("""
        <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px;">
            <h1 style="margin: 0;">Conclusion</h1>
            <span style="font-size: 0.85rem; color: #94a3b8; font-weight: 500; background: #f1f5f9; padding: 3px 10px; border-radius: 20px;">
                What we learned & where we're going
            </span>
        </div>
    """, unsafe_allow_html=True)

    # ---------- Headline takeaway ----------
    st.markdown("""
        <div class="glass-card" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white;">
            <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                Headline takeaway
            </div>
            <h2 style="color: #ffffff; margin: 0 0 8px 0; font-size: 1.6rem; font-weight: 700;">
                Daily sales are not random — they are shaped by a measurable set of cultural,
                economic, and digital factors.
            </h2>
            <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
                Across 361 days of data, the same drivers appear again and again: religious calendar,
                paydays, weekly rhythm, and platform-specific engagement signals. Once you measure
                these properly, marketing decisions stop being guesswork.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # ---------- Numbered conclusions matching the 9 findings ----------
    st.subheader("What the data told us")
    summary_items = [
        ("🌙", "Ramadan is the dominant driver", "A +154% uplift that overshadows everything else. Plan inventory and staffing around it months in advance."),
        ("📱", "On TikTok, clicks beat views", "Phone clicks predict sales (r = +0.44); views do not (r = +0.11). Optimise content for action, not reach."),
        ("⏱", "Instagram and Facebook convert with a one-day lag", "When views spike on these platforms, sales follow within 24 hours. TikTok does not show this effect."),
        ("💰", "Private-sector payday creates a V-shape", "Sales dip −22% before payday and rebound +8% on the day. The boost lasts a full week."),
        ("📅", "Friday peaks, Monday troughs", "A 28% intra-week swing — meaningful for staffing and stocking."),
        ("🎉", "Events work; isolated influencer posts (yet) do not", "Event days lift sales by +51.6% (significant). Influencer posts show +8.2% directionally but not significantly given the small sample."),
        ("📐", "Multivariate regression confirms independence", "After controlling for everything, Ramadan, TikTok, Facebook, and weekly rhythm all hold up as independent drivers."),
        ("", "Sales are fundamentally non-linear", "Tree-based models (R² ≈ +0.31) decisively beat linear models (R² = −0.55). Variables interact — they don't just add."),
    ]
    for i in range(0, len(summary_items), 3):
        cols = st.columns(3)
        for col, (emoji, title, body) in zip(cols, summary_items[i:i+3]):
            col.markdown(f"""
                <div class="glass-card" style="height: 220px;">
                    <div style="font-size: 1.6rem; margin-bottom: 8px;">{emoji}</div>
                    <h4 style="margin: 0 0 8px 0; color: #0f172a; font-size: 0.98rem;">{title}</h4>
                    <p style="color: #64748b; font-size: 0.86rem; line-height: 1.55; margin: 0;">
                        {body}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # ---------- Actionable guidance ----------
    st.markdown("""
        <div class="success-box">
            <h3 style="margin-top:0; color:#14532d;">✅ Actionable guidance for the business</h3>
            <ul style="margin: 8px 0 0 0; padding-left: 22px; line-height: 1.85; color:#14532d;">
                <li><strong>Plan inventory for Ramadan</strong> — stock up to ~2.5× normal levels for the month.</li>
                <li><strong>Track TikTok phone clicks</strong>, not views, as the KPI for that platform.</li>
                <li><strong>Time Instagram & Facebook campaigns</strong> for one-day-out sales targets.</li>
                <li><strong>Brace for the pre-payday slump</strong> on the 28th–30th, then expect a rebound on the 1st.</li>
                <li><strong>Stock heavier for Fridays</strong>, lighter for Mondays.</li>
                <li><strong>Invest in physical events</strong> — they reliably move sales. Hold off on big influencer spend until ROI is measurable.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # ---------- Limitations ----------
    st.subheader("Limitations")
    st.markdown("""
        <div class="glass-card">
            <ul style="line-height: 1.85; color:#334155; margin:0; padding-left: 22px;">
                <li><strong>Single-business scope.</strong> All findings come from one SME in one city. Patterns may differ in other sectors or regions.</li>
                <li><strong>Correlation, not causation.</strong> Observational data cannot prove cause-and-effect; only controlled experiments can.</li>
                <li><strong>Public sector salary.</strong> The expected payday boost did not appear in the data, likely due to the well-documented irregularity of KRG public salary disbursement and a small sample (n = 11).</li>
                <li><strong>Small influencer sample.</strong> Only 16 influencer-post days were recorded — too few to reach statistical significance.</li>
                <li><strong>12-month window.</strong> One year cannot capture year-over-year trends or long-term seasonality shifts.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    # ---------- Future Directions ----------
    st.subheader("🚀 Future Directions")
    st.markdown("""
        <div class="glass-card" style="background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%); border-left: 4px solid #3b82f6;">
            <h3 style="margin-top:0; color:#1d4ed8;">Open this platform to every SME</h3>
            <p style="color:#1e3a5f; line-height:1.7; font-size:0.96rem;">
                The most exciting direction for this work is to <strong>make it public</strong>. The
                analytical pipeline developed in this project could be deployed as an online platform
                where any business owner uploads their own daily sales and marketing data. The system
                would run the same analysis presented here — correlation, lag, regression, and
                predictive modelling — and return a personalised report tailored to their business.
            </p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px;">
                <div style="background: rgba(255,255,255,0.7); padding: 16px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📈</div>
                    <strong style="color:#1e3a5f;">Marketing strategy</strong>
                    <p style="color:#475569; font-size:0.88rem; margin: 6px 0 0 0;">
                        Which platforms and metrics genuinely drive their sales, and which are just noise.
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 16px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">📦</div>
                    <strong style="color:#1e3a5f;">Logistics & stocking guidance</strong>
                    <p style="color:#475569; font-size:0.88rem; margin: 6px 0 0 0;">
                        When to stock up for seasonal peaks (Ramadan, paydays, weekends) and when to scale down.
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 16px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">🎤</div>
                    <strong style="color:#1e3a5f;">Event evaluation</strong>
                    <p style="color:#475569; font-size:0.88rem; margin: 6px 0 0 0;">
                        Whether attending physical events is actually profitable for that specific business.
                    </p>
                </div>
                <div style="background: rgba(255,255,255,0.7); padding: 16px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; margin-bottom: 6px;">💸</div>
                    <strong style="color:#1e3a5f;">Influencer ROI</strong>
                    <p style="color:#475569; font-size:0.88rem; margin: 6px 0 0 0;">
                        Whether influencer partnerships produce measurable sales lift or only vanity engagement.
                    </p>
                </div>
            </div>
            <p style="color:#1e3a5f; margin-top: 18px; margin-bottom: 0; font-style: italic;">
                In effect, the platform would democratise the same data-driven marketing-mix analysis
                that today is only accessible to large corporations with dedicated analytics teams.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card">
            <h4 style="margin-top:0;">Beyond the public platform</h4>
            <ul style="line-height:1.85; color:#334155; margin:0; padding-left: 22px;">
                <li><strong>Multi-year extension.</strong> Repeating the analysis over 2–3 years would confirm whether the patterns identified are stable or year-specific.</li>
                <li><strong>Multi-business comparison.</strong> Applying the same pipeline to other SMEs across retail categories (restaurants, clothing, electronics) would test the generalisability of the findings.</li>
                <li><strong>A/B testing.</strong> Introducing controlled experiments — for example, randomising when influencer posts are made — would move the analysis from correlation toward genuine causation.</li>
                <li><strong>Sentiment analysis.</strong> Adding text-based features from social media comments and reviews would complement the quantitative model with qualitative customer signals.</li>
                <li><strong>Real-time forecasting.</strong> Deploying the predictive models as a live dashboard that ingests daily data and produces next-day sales forecasts.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
