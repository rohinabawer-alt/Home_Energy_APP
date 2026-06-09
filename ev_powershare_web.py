"""
EV PowerShare - Web Version (Streamlit)
HOW TO RUN:
    pip install streamlit matplotlib
    streamlit run ev_powershare_web.py
HOW TO GET FREE https:// LINK:
    1. github.com → create free account → new repo → upload this file
    2. share.streamlit.io → sign in with GitHub → New app → Deploy
    3. Get your https://yourname.streamlit.app link!
"""

import streamlit as st
import matplotlib.pyplot as plt
import random
import datetime

st.set_page_config(
    page_title="Battery NEXT power",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLORS ────────────────────────────────────────────────────
C_BG_DARK  = "#1A0A2E"
C_BG_MID   = "#2D1B5E"
C_BG_LIGHT = "#3D2578"
C_ACCENT1  = "#7B2FBE"
C_ACCENT2  = "#9D4EDD"
C_GREEN    = "#00C853"
C_WHITE    = "#F0E6FF"
C_GREY     = "#B0A0CC"
C_YELLOW   = "#FFD600"
C_RED      = "#FF4B4B"
C_CHART_BG = "#150826"

# ── CSS — matches desktop app exactly ────────────────────────
st.markdown(f"""
<style>
  html, body, [class*="css"] {{ font-family: Helvetica, sans-serif; }}
  .stApp {{ background-color: {C_BG_DARK}; }}
  section[data-testid="stSidebar"] {{
      background-color: {C_BG_MID} !important;
  }}
  section[data-testid="stSidebar"] * {{ color: {C_WHITE} !important; }}
  .stSelectbox > div > div {{
      background-color: {C_BG_LIGHT} !important;
      color: {C_WHITE} !important;
      border: 1px solid {C_ACCENT1} !important;
  }}
  .stSelectbox label {{ color: {C_GREEN} !important; font-weight: bold; font-size:13px; }}
  .stButton > button {{
      background-color: {C_ACCENT1} !important;
      color: {C_WHITE} !important;
      border: none !important;
      border-radius: 6px !important;
      font-weight: bold !important;
      width: 100%;
      padding: 8px !important;
  }}
  .stButton > button:hover {{ background-color: {C_ACCENT2} !important; }}
  .stTabs [data-baseweb="tab-list"] {{ background-color: {C_BG_MID}; border-radius: 8px; }}
  .stTabs [data-baseweb="tab"] {{
      color: {C_GREY} !important;
      font-weight: bold;
      background-color: {C_BG_MID};
      border-radius: 6px 6px 0 0;
  }}
  .stTabs [aria-selected="true"] {{
      background-color: {C_ACCENT1} !important;
      color: {C_WHITE} !important;
  }}
  .stSlider label {{ color: {C_GREEN} !important; font-weight: bold; font-size:12px; }}
  .stSlider [data-baseweb="slider"] {{ margin-top: -8px; }}
  div[data-testid="metric-container"] {{
      background-color: {C_BG_LIGHT};
      border: 1px solid {C_ACCENT1};
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 6px;
  }}
  div[data-testid="metric-container"] label {{
      color: {C_GREY} !important;
      font-size: 11px !important;
  }}
  div[data-testid="stMetricValue"] {{
      color: {C_GREEN} !important;
      font-size: 20px !important;
      font-weight: bold !important;
  }}
  h1, h2, h3, h4 {{ color: {C_WHITE} !important; }}
  p, li {{ color: {C_WHITE}; }}
  .topbar {{
      background-color: {C_BG_MID};
      padding: 14px 22px;
      border-radius: 10px;
      margin-bottom: 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
  }}
  .logo {{ color: {C_GREEN}; font-size: 22px; font-weight: bold; }}
  .subtitle {{ color: {C_GREY}; font-size: 13px; margin-left: 14px; }}
  .clock {{
      background-color: {C_ACCENT1};
      color: {C_WHITE};
      padding: 5px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: bold;
  }}
  .sec-header {{
      color: {C_GREEN};
      font-weight: bold;
      font-size: 13px;
      margin: 14px 0 4px 0;
      border-left: 3px solid {C_GREEN};
      padding-left: 8px;
  }}
  .price-badge {{
      background-color: {C_BG_LIGHT};
      color: {C_YELLOW};
      font-weight: bold;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 13px;
      margin: 4px 0 10px 0;
      display: inline-block;
  }}
  .appl-row {{
      background-color: {C_BG_MID};
      border-radius: 6px;
      padding: 6px 12px;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      justify-content: space-between;
  }}
  .appl-val {{
      color: {C_YELLOW};
      font-weight: bold;
      font-size: 13px;
      min-width: 70px;
      text-align: right;
  }}
  .report-box {{
      background-color: {C_BG_MID};
      border: 1px solid {C_ACCENT1};
      border-radius: 8px;
      padding: 18px;
      font-family: monospace;
      font-size: 12px;
      color: {C_WHITE};
      white-space: pre;
      overflow-x: auto;
  }}
  .divider {{
      border-top: 1px solid {C_ACCENT1};
      margin: 10px 0;
  }}
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────
ELECTRICITY_TYPES = {
    "Solar (Own Panels)": {"price": 0.20, "icon": "☀️"},
    "EV batteries":       {"price": 0.20, "icon": "🔋"},
    "Green Certified":    {"price": 0.32, "icon": "🌿"},
    "Night Rate":         {"price": 0.15, "icon": "🌙"},
    "Peak Rate":          {"price": 0.45, "icon": "⚡"},
}
PAYMENT_METHODS = [
    "💳 Credit / Debit Card",
    "🏦 Bank Transfer (SEPA)",
    "📱 PayPal",
    "📲 Apple Pay / Google Pay",
    "🔄 Direct Debit (Monthly)",
    "₿ Cryptocurrency",
]
APPLIANCES = {
    "Refrigerator":    1.5,
    "Washing Machine": 1.2,
    "Dishwasher":      1.0,
    "Air Conditioner": 3.5,
    "Heating System":  4.0,
    "TV / Screens":    0.8,
    "Lighting":        0.6,
    "Electric Oven":   2.0,
    "EV Charger":      7.5,
    "Other Devices":   1.0,
}
APPLIANCE_ICONS = ["🧊","🫧","🍽️","❄️","🔥","📺","💡","🍳","🚗","🔌"]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
PIE_COLORS = ["#7B2FBE","#00C853","#FFD600","#00C8FF","#FF4B4B",
              "#9D4EDD","#FF8C00","#00BCD4","#E91E63","#8BC34A"]

# ── SESSION STATE ─────────────────────────────────────────────
if "monthly_usage" not in st.session_state:
    st.session_state.monthly_usage = [round(random.uniform(200, 450), 1) for _ in range(12)]
if "appl_values" not in st.session_state:
    st.session_state.appl_values = dict(APPLIANCES)

# ── TOP BAR ───────────────────────────────────────────────────
now = datetime.datetime.now().strftime("%d %b %Y  |  %H:%M")
st.markdown(f"""
<div class="topbar">
  <div>
    <span class="logo">🔋 EV PowerShare</span>
    <span class="subtitle">Smart Energy Management Dashboard</span>
  </div>
  <div class="clock">🕐 {now}</div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo" style="font-size:18px;margin-bottom:12px;">🔋 EV PowerShare</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-header">⚡ Electricity Type</div>', unsafe_allow_html=True)
    elec_type = st.selectbox("elec", list(ELECTRICITY_TYPES.keys()), label_visibility="collapsed")
    info = ELECTRICITY_TYPES[elec_type]
    price = info["price"]
    st.markdown(f'<div class="price-badge">{info["icon"]}  €{price:.2f} / kWh</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">📅 Analysis Period</div>', unsafe_allow_html=True)
    period = st.selectbox("period", ["Daily", "Weekly", "Monthly", "Yearly"], index=2, label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-header">💰 Payment Method</div>', unsafe_allow_html=True)
    pay_method = st.selectbox("pay", PAYMENT_METHODS, label_visibility="collapsed")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── KPI CALCULATIONS ──────────────────────────────────────
    usage      = st.session_state.monthly_usage
    total      = sum(usage)
    cost       = total * price
    multiplier = {"Daily":1/365,"Weekly":1/52,"Monthly":1/12,"Yearly":1}.get(period, 1/12)
    avg_monthly = total / 12
    variance    = sum((m - avg_monthly)**2 for m in usage) / 12
    growth_rate = (variance**0.5) / avg_monthly if avg_monthly > 0 else 0
    price_factor = price / 0.28
    if growth_rate > 0:
        years_pred = round(0.20 / (growth_rate * 0.05 * price_factor), 1)
        years_pred = max(1.0, min(years_pred, 30.0))
    else:
        years_pred = 10.0

    st.markdown('<div class="sec-header">📊 Summary</div>', unsafe_allow_html=True)
    st.metric("Total Usage",   f"{total * multiplier:,.1f} kWh")
    st.metric("Total Cost",    f"€ {cost * multiplier:,.1f}")
    st.metric("Avg / Month",   f"{avg_monthly:,.1f} kWh")
    st.metric("CO₂ Saved",     f"{(total * 0.233) * multiplier:,.0f} kg")
    st.metric("AI Prediction", f"{years_pred:.1f} yrs")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col2:
        if st.button("🎲 Randomize"):
            st.session_state.monthly_usage = [round(random.uniform(180, 480), 1) for _ in range(12)]
            st.rerun()

# ── CHART HELPER ─────────────────────────────────────────────
def styled_fig(w=9, h=4.0):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(C_CHART_BG)
    ax.set_facecolor(C_CHART_BG)
    ax.tick_params(colors=C_GREY, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(C_BG_LIGHT)
    ax.yaxis.grid(True, color=C_BG_LIGHT, linestyle="--", linewidth=0.5)
    ax.set_axisbelow(True)
    return fig, ax

# ── TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊 Dashboard  ",
    "  📈 Usage Chart  ",
    "  💶 Cost Analysis  ",
    "  🏠 Appliances  ",
    "  📄 Export Report  ",
])

# ══ TAB 1: DASHBOARD ════════════════════════════════════════
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = styled_fig()
        colors = [C_GREEN if v < 300 else C_YELLOW if v < 380 else C_RED for v in usage]
        bars = ax.bar(MONTHS, usage, color=colors, width=0.65, zorder=3)
        ax.set_title("Monthly Consumption (kWh)", color=C_WHITE, fontsize=11, pad=10)
        ax.set_ylabel("kWh", color=C_GREY, fontsize=9)
        for bar, val in zip(bars, usage):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+4,
                    f"{val:.0f}", ha="center", va="bottom", color=C_WHITE, fontsize=7)
        st.pyplot(fig); plt.close(fig)

    with col2:
        ap_vals = [st.session_state.appl_values.get(n, v) for n, v in APPLIANCES.items()]
        ap_keys = list(APPLIANCES.keys())
        fig, ax = styled_fig()
        ax.set_facecolor(C_CHART_BG)
        fig.patch.set_facecolor(C_CHART_BG)
        wedges, texts, autotexts = ax.pie(
            ap_vals, labels=None, autopct="%1.0f%%",
            colors=PIE_COLORS[:len(ap_vals)], startangle=140, pctdistance=0.75,
            wedgeprops=dict(linewidth=1.5, edgecolor=C_BG_MID))
        for at in autotexts:
            at.set(color=C_WHITE, fontsize=7, fontweight="bold")
        ax.set_title("Appliance Share (%)", color=C_WHITE, fontsize=11, pad=10)
        ax.legend(ap_keys, loc="lower center", bbox_to_anchor=(0.5, -0.28),
                  ncol=2, fontsize=7, frameon=False, labelcolor=C_GREY)
        st.pyplot(fig); plt.close(fig)

# ══ TAB 2: USAGE CHART ══════════════════════════════════════
with tab2:
    fig, ax = styled_fig(11, 4.2)
    x = list(range(12))
    ax.fill_between(x, usage, alpha=0.18, color=C_ACCENT2)
    ax.plot(x, usage, color=C_GREEN, linewidth=2.5, marker="o", markersize=7,
            markerfacecolor=C_YELLOW, markeredgecolor=C_BG_DARK, markeredgewidth=1.5, zorder=5)
    window = 3
    avg_line = [sum(usage[max(0,i-window+1):i+1])/len(usage[max(0,i-window+1):i+1]) for i in range(12)]
    ax.plot(x, avg_line, color=C_ACCENT2, linewidth=1.5, linestyle="--", label="3-month avg", zorder=4)
    ax.set_xticks(x); ax.set_xticklabels(MONTHS, color=C_GREY, fontsize=9)
    ax.tick_params(axis="y", colors=C_GREY, labelsize=9)
    ax.set_title("Annual Energy Usage — Line Chart", color=C_WHITE, fontsize=12, pad=12)
    ax.set_ylabel("kWh", color=C_GREY, fontsize=10)
    max_i = usage.index(max(usage)); min_i = usage.index(min(usage))
    ax.annotate(f"Peak\n{usage[max_i]:.0f} kWh",
                xy=(max_i, usage[max_i]), xytext=(max_i+0.6, usage[max_i]+15),
                color=C_RED, fontsize=8, arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))
    ax.annotate(f"Low\n{usage[min_i]:.0f} kWh",
                xy=(min_i, usage[min_i]), xytext=(min_i+0.6, usage[min_i]-35),
                color=C_GREEN, fontsize=8, arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1))
    ax.legend(fontsize=9, frameon=False, labelcolor=C_GREY)
    st.pyplot(fig); plt.close(fig)

# ══ TAB 3: COST ANALYSIS ════════════════════════════════════
with tab3:
    costs = [u * price for u in usage]
    tax   = [c * 0.22  for c in costs]
    base  = [c - t     for c, t in zip(costs, tax)]
    fig, ax = styled_fig(11, 4.2)
    x = list(range(12))
    ax.bar(x, base, color=C_ACCENT2, label="Energy Cost", width=0.6, zorder=3)
    ax.bar(x, tax, bottom=base, color=C_YELLOW, label="VAT (22%)", width=0.6, zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(MONTHS, color=C_GREY, fontsize=9)
    ax.tick_params(axis="y", colors=C_GREY, labelsize=9)
    ax.set_title(
        f"Monthly Cost Analysis  |  Rate: €{price:.2f}/kWh  |  Payment: {pay_method.split()[1]}",
        color=C_WHITE, fontsize=10, pad=10)
    ax.set_ylabel("€ Cost", color=C_GREY, fontsize=10)
    ax.legend(fontsize=9, frameon=False, labelcolor=C_GREY, loc="upper right")
    for i, (b, t) in enumerate(zip(base, tax)):
        ax.text(i, b+t+0.5, f"€{b+t:.0f}", ha="center", fontsize=7, color=C_WHITE)
    st.pyplot(fig); plt.close(fig)

# ══ TAB 4: APPLIANCES ═══════════════════════════════════════
with tab4:
    st.markdown(f'<div style="color:{C_GREEN};font-weight:bold;font-size:16px;margin-bottom:12px;">🏠 Daily Appliance Usage (kWh/day)</div>', unsafe_allow_html=True)

    appl_values = {}
    col1, col2 = st.columns(2)
    items = list(APPLIANCES.items())
    half  = len(items) // 2

    for i, (name, default) in enumerate(items):
        col = col1 if i < half else col2
        icon = APPLIANCE_ICONS[i]
        with col:
            val = st.slider(
                f"{icon} {name}",
                min_value=0.0, max_value=12.0,
                value=float(st.session_state.appl_values.get(name, default)),
                step=0.1, format="%.1f kWh"
            )
            appl_values[name] = val

    # Save updated values
    st.session_state.appl_values = appl_values

    # Recalculate button — rebuilds monthly usage from slider values
    if st.button("↺  Recalculate Monthly Usage from Appliances"):
        daily_total = sum(appl_values.values())
        seasonal = [0.85,0.88,0.92,0.95,1.0,1.15,1.20,1.18,1.05,0.95,0.90,0.87]
        st.session_state.monthly_usage = [
            round(daily_total * 30 * seasonal[i] + random.uniform(-10, 10), 1)
            for i in range(12)
        ]
        st.success("✅ Monthly usage recalculated from your appliance settings!")
        st.rerun()

    # Live pie chart
    st.markdown(f'<div style="color:{C_GREEN};font-weight:bold;margin-top:16px;">Live Appliance Share</div>', unsafe_allow_html=True)
    fig, ax = styled_fig(6, 3.5)
    ax.set_facecolor(C_CHART_BG); fig.patch.set_facecolor(C_CHART_BG)
    vals = list(appl_values.values())
    keys = list(appl_values.keys())
    if sum(vals) > 0:
        wedges, texts, autotexts = ax.pie(
            vals, labels=None, autopct="%1.0f%%",
            colors=PIE_COLORS[:len(vals)], startangle=140, pctdistance=0.75,
            wedgeprops=dict(linewidth=1.5, edgecolor=C_BG_MID))
        for at in autotexts:
            at.set(color=C_WHITE, fontsize=7, fontweight="bold")
        ax.legend(keys, loc="lower center", bbox_to_anchor=(0.5, -0.3),
                  ncol=2, fontsize=7, frameon=False, labelcolor=C_GREY)
    st.pyplot(fig); plt.close(fig)

# ══ TAB 5: EXPORT REPORT ════════════════════════════════════
with tab5:
    st.markdown(f'<div style="color:{C_GREEN};font-weight:bold;font-size:16px;margin-bottom:12px;">📄 Energy Report</div>', unsafe_allow_html=True)

    lines = [
        "=" * 52,
        "        HOME ENERGY REPORT — EV PowerShare",
        "=" * 52,
        f"  Generated        : {datetime.datetime.now().strftime('%d %b %Y  %H:%M')}",
        f"  Electricity Type : {elec_type}",
        f"  Price per kWh    : EUR {price:.2f}",
        f"  Payment Method   : {pay_method}",
        f"  Period Selected  : {period}",
        "-" * 52,
        "  MONTHLY USAGE (kWh):",
    ]
    for m, u in zip(MONTHS, usage):
        lines.append(f"    {m:>3}  ->  {u:6.1f} kWh  |  EUR {u * price:6.2f}")
    lines += [
        "-" * 52,
        f"  TOTAL ANNUAL USAGE  : {total:,.1f} kWh",
        f"  TOTAL ANNUAL COST   : EUR {cost:,.2f}",
        f"  AVG MONTHLY USAGE   : {avg_monthly:,.1f} kWh",
        f"  AVG MONTHLY COST    : EUR {cost/12:,.2f}",
        f"  CO2 OFFSET EQUIV.   : {total * 0.233:,.0f} kg",
        f"  AI PREDICTION       : {years_pred:.1f} years",
        "=" * 52,
    ]
    report = "\n".join(lines)
    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
    st.download_button(
        label="⬇️  Download Report as .txt",
        data=report,
        file_name="energy_report.txt",
        mime="text/plain"
    )