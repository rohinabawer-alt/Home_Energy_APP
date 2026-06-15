# Home_Energy_APP
The Home Energy Analyzer is a Python desktop app that visualizes household electricity usage, cost, CO₂ impact, and appliance consumption using Tkinter and Matplotlib. It uses simulated data and simple statistical calculations to generate trends and predictions, helping users understand and manage energy use efficiently.
"""
╔══════════════════════════════════════════════════════════════╗
         HOME ENERGY ANALYZER - Python Desktop App           
         Color: Purple theme  |  Accents: Green              
         Libraries: tkinter, matplotlib                       
╚══════════════════════════════════════════════════════════════╝

HOW TO RUN:
    pip install matplotlib
    python home_energy_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import datetime
import os
import sys

# ─────────────────────────────────────────────────────────────
#  APP SETTINGS
# ─────────────────────────────────────────────────────────────
APP_TITLE    = "🔋 Battery NEXT power"
APP_SUBTITLE = "Smart Energy Management Dashboard"
LOGO_TEXT    = "🔋 EV PowerShare"
WINDOW_WIDTH  = 1200
WINDOW_HEIGHT = 780

# ─────────────────────────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────────────────────────
C_BG_DARK   = "#1A0A2E"
C_BG_MID    = "#2D1B5E"
C_BG_LIGHT  = "#3D2578"
C_ACCENT1   = "#7B2FBE"
C_ACCENT2   = "#9D4EDD"
C_GREEN     = "#00C853"
C_GREEN_D   = "#00953D"
C_WHITE     = "#F0E6FF"
C_GREY      = "#B0A0CC"
C_YELLOW    = "#FFD600"
C_RED       = "#FF4B4B"
C_CHART_BG  = "#150826"

# ─────────────────────────────────────────────────────────────
#  ELECTRICITY TYPES & PRICES (per kWh €)
# ─────────────────────────────────────────────────────────────
ELECTRICITY_TYPES = {
    "Solar (Own Panels)": {"price": 0.20, "color": "#FFD600", "icon": "☀️"},
    "EV batteries":       {"price": 0.20, "color": "#00C8FF", "icon": "💨"},
    "Green Certified":    {"price": 0.32, "color": "#00C853", "icon": "🌿"},
    "Night Rate":         {"price": 0.15, "color": "#A0A0FF", "icon": "🌙"},
    "Peak Rate":          {"price": 0.45, "color": "#FF4B4B", "icon": "⚡"},
}

# ─────────────────────────────────────────────────────────────
#  PAYMENT METHODS
# ─────────────────────────────────────────────────────────────
PAYMENT_METHODS = [
    "💳 Credit / Debit Card",
    "🏦 Bank Transfer (SEPA)",
    "📱 PayPal",
    "📲 Apple Pay / Google Pay",
    "🔄 Direct Debit (Monthly)",
    "₿ Cryptocurrency",
]

# ─────────────────────────────────────────────────────────────
#  HOME APPLIANCES (default kWh/day)
# ─────────────────────────────────────────────────────────────
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

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION CLASS
# ══════════════════════════════════════════════════════════════
class HomeEnergyApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg=C_BG_DARK)
        self.resizable(True, True)
        self.minsize(900, 620)

        # State variables
        self.elec_type  = tk.StringVar(value=list(ELECTRICITY_TYPES.keys())[0])
        self.pay_method = tk.StringVar(value=PAYMENT_METHODS[0])
        self.period     = tk.StringVar(value="Monthly")
        self.appliance_vars = {k: tk.DoubleVar(value=v) for k, v in APPLIANCES.items()}

        # Monthly usage data
        self.monthly_usage = [round(random.uniform(200, 450), 1) for _ in range(12)]

        self._configure_styles()
        self._build_ui()
        self._refresh_all()

    # ──────────────────────────────────────────────────────────
    #  TTK STYLES
    # ──────────────────────────────────────────────────────────
    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame",       background=C_BG_DARK)
        style.configure("Card.TFrame",  background=C_BG_MID)
        style.configure("Inner.TFrame", background=C_BG_LIGHT)

        style.configure("TLabel",
                        background=C_BG_DARK, foreground=C_WHITE,
                        font=("Helvetica", 10))
        style.configure("Card.TLabel",
                        background=C_BG_MID, foreground=C_WHITE,
                        font=("Helvetica", 10))
        style.configure("Title.TLabel",
                        background=C_BG_DARK, foreground=C_WHITE,
                        font=("Helvetica", 18, "bold"))
        style.configure("Sub.TLabel",
                        background=C_BG_DARK, foreground=C_GREY,
                        font=("Helvetica", 10))
        style.configure("KPI.TLabel",
                        background=C_BG_MID, foreground=C_GREEN,
                        font=("Helvetica", 22, "bold"))
        style.configure("KPIsub.TLabel",
                        background=C_BG_MID, foreground=C_GREY,
                        font=("Helvetica", 9))

        style.configure("Green.TButton",
                        background=C_GREEN, foreground="#000000",
                        font=("Helvetica", 10, "bold"),
                        borderwidth=0, relief="flat", padding=8)
        style.map("Green.TButton",
                  background=[("active", C_GREEN_D), ("pressed", C_GREEN_D)])

        style.configure("Purple.TButton",
                        background=C_ACCENT1, foreground=C_WHITE,
                        font=("Helvetica", 10, "bold"),
                        borderwidth=0, relief="flat", padding=8)
        style.map("Purple.TButton",
                  background=[("active", C_ACCENT2), ("pressed", C_BG_LIGHT)])

        style.configure("TCombobox",
                        fieldbackground=C_BG_LIGHT, background=C_BG_LIGHT,
                        foreground=C_WHITE, selectbackground=C_ACCENT1,
                        selectforeground=C_WHITE, arrowcolor=C_GREEN)
        style.map("TCombobox",
                  fieldbackground=[("readonly", C_BG_LIGHT)],
                  foreground=[("readonly", C_WHITE)])

        style.configure("TScale",
                        background=C_BG_MID, troughcolor=C_BG_DARK,
                        sliderlength=14, sliderrelief="flat")

        style.configure("TNotebook",
                        background=C_BG_DARK, tabmargins=[0, 0, 0, 0])
        style.configure("TNotebook.Tab",
                        background=C_BG_MID, foreground=C_GREY,
                        padding=[14, 8], font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", C_ACCENT1)],
                  foreground=[("selected", C_WHITE)])

        style.configure("Horizontal.TProgressbar",
                        troughcolor=C_BG_DARK, background=C_GREEN,
                        thickness=8, borderwidth=0)

    # ──────────────────────────────────────────────────────────
    #  MAIN UI LAYOUT
    # ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Top bar
        topbar = tk.Frame(self, bg=C_BG_MID, height=60)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Label(topbar, text=LOGO_TEXT, bg=C_BG_MID,
                 fg=C_GREEN, font=("Helvetica", 18, "bold")
                 ).pack(side="left", padx=20, pady=10)

        tk.Label(topbar, text=APP_SUBTITLE, bg=C_BG_MID,
                 fg=C_GREY, font=("Helvetica", 11)
                 ).pack(side="left", padx=4, pady=10)

        self.clock_lbl = tk.Label(topbar, text="", bg=C_ACCENT1,
                                  fg=C_WHITE, font=("Helvetica", 9, "bold"),
                                  padx=12, pady=4)
        self.clock_lbl.pack(side="right", padx=20, pady=14)
        self._tick_clock()

        # Main body
        body = tk.Frame(self, bg=C_BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=C_BG_MID, width=270)
        self.sidebar.pack(side="left", fill="y", padx=(0, 8))
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        # Content
        content = tk.Frame(body, bg=C_BG_DARK)
        content.pack(side="left", fill="both", expand=True)
        self._build_content(content)

    # ──────────────────────────────────────────────────────────
    #  SIDEBAR
    # ──────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb  = self.sidebar
        pad = {"padx": 14, "pady": 4}

        self._section_header(sb, "⚡  Electricity Type")
        elec_cb = ttk.Combobox(sb, textvariable=self.elec_type,
                               values=list(ELECTRICITY_TYPES.keys()),
                               state="readonly", width=28)
        elec_cb.pack(**pad, fill="x")
        elec_cb.bind("<<ComboboxSelected>>", lambda e: self._refresh_all())

        self.price_badge = tk.Label(sb, text="", bg=C_BG_LIGHT,
                                    fg=C_YELLOW, font=("Helvetica", 10, "bold"),
                                    pady=4)
        self.price_badge.pack(**pad, fill="x")

        tk.Frame(sb, bg=C_ACCENT1, height=1).pack(fill="x", padx=14, pady=8)

        self._section_header(sb, "📅  Analysis Period")
        period_cb = ttk.Combobox(sb, textvariable=self.period,
                                 values=["Daily", "Weekly", "Monthly", "Yearly"],
                                 state="readonly", width=28)
        period_cb.pack(**pad, fill="x")
        period_cb.bind("<<ComboboxSelected>>", lambda e: self._refresh_all())

        tk.Frame(sb, bg=C_ACCENT1, height=1).pack(fill="x", padx=14, pady=8)

        self._section_header(sb, "💰  Payment Method")
        pay_cb = ttk.Combobox(sb, textvariable=self.pay_method,
                              values=PAYMENT_METHODS,
                              state="readonly", width=28)
        pay_cb.pack(**pad, fill="x")
        pay_cb.bind("<<ComboboxSelected>>", lambda e: self._refresh_all())

        tk.Frame(sb, bg=C_ACCENT1, height=1).pack(fill="x", padx=14, pady=8)

        self._section_header(sb, "📊  Summary")
        kpi_frame = tk.Frame(sb, bg=C_BG_MID)
        kpi_frame.pack(fill="x", padx=14)

        self.kpi_usage         = self._kpi_card(kpi_frame, "Total Usage",     "— kWh")
        self.kpi_cost          = self._kpi_card(kpi_frame, "Total Cost",      "—  €")
        self.kpi_avg           = self._kpi_card(kpi_frame, "Avg / Month",     "— kWh")
        self.kpi_co2           = self._kpi_card(kpi_frame, "CO2 Saved",       "—  kg")
        self.kpi_ai_prediction = self._kpi_card(kpi_frame, "AI Prediction",   "— Years")

        tk.Frame(sb, bg=C_ACCENT1, height=1).pack(fill="x", padx=14, pady=8)

        ttk.Button(sb, text="🔄  Refresh Analysis", style="Green.TButton",
                   command=self._refresh_all).pack(padx=14, fill="x", pady=3)
        ttk.Button(sb, text="📄  Export Report", style="Purple.TButton",
                   command=self._export_report).pack(padx=14, fill="x", pady=3)
        ttk.Button(sb, text="🎲  Randomize Data", style="Purple.TButton",
                   command=self._randomize_data).pack(padx=14, fill="x", pady=3)

    def _section_header(self, parent, text):
        tk.Label(parent, text=text, bg=C_BG_MID, fg=C_GREEN,
                 font=("Helvetica", 10, "bold"), anchor="w"
                 ).pack(fill="x", padx=14, pady=(10, 2))

    def _kpi_card(self, parent, label, value):
        f = tk.Frame(parent, bg=C_BG_LIGHT, pady=6)
        f.pack(fill="x", pady=3)
        tk.Label(f, text=label, bg=C_BG_LIGHT, fg=C_GREY,
                 font=("Helvetica", 8)).pack()
        val_lbl = tk.Label(f, text=value, bg=C_BG_LIGHT,
                           fg=C_GREEN, font=("Helvetica", 14, "bold"))
        val_lbl.pack()
        return val_lbl

    # ──────────────────────────────────────────────────────────
    #  CONTENT TABS
    # ──────────────────────────────────────────────────────────
    def _build_content(self, parent):
        nb = ttk.Notebook(parent)
        nb.pack(fill="both", expand=True)

        self.tab_dash = tk.Frame(nb, bg=C_BG_DARK)
        nb.add(self.tab_dash, text="  📊 Dashboard  ")
        self._build_dashboard(self.tab_dash)

        self.tab_chart = tk.Frame(nb, bg=C_BG_DARK)
        nb.add(self.tab_chart, text="  📈 Usage Chart  ")
        self._build_usage_chart(self.tab_chart)

        self.tab_cost = tk.Frame(nb, bg=C_BG_DARK)
        nb.add(self.tab_cost, text="  💶 Cost Analysis  ")
        self._build_cost_tab(self.tab_cost)

        self.tab_appl = tk.Frame(nb, bg=C_BG_DARK)
        nb.add(self.tab_appl, text="  🏠 Appliances  ")
        self._build_appliances_tab(self.tab_appl)

    # ──────────────────────────────────────────────────────────
    #  TAB 1 – DASHBOARD (bar + pie)
    # ──────────────────────────────────────────────────────────
    def _build_dashboard(self, parent):
        self.fig_dash = Figure(figsize=(8.5, 4.8), facecolor=C_CHART_BG)
        self.fig_dash.subplots_adjust(left=0.07, right=0.97,
                                      top=0.88, bottom=0.12, wspace=0.35)
        self.ax_bar = self.fig_dash.add_subplot(1, 2, 1)
        self.ax_pie = self.fig_dash.add_subplot(1, 2, 2)

        canvas = FigureCanvasTkAgg(self.fig_dash, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas_dash = canvas

    def _draw_dashboard(self):
        ax_b = self.ax_bar
        ax_p = self.ax_pie
        ax_b.clear()
        ax_p.clear()
        ax_b.set_facecolor(C_CHART_BG)
        ax_p.set_facecolor(C_CHART_BG)

        colors = [C_GREEN if v < 300 else C_YELLOW if v < 380 else C_RED
                  for v in self.monthly_usage]
        bars = ax_b.bar(MONTHS, self.monthly_usage, color=colors,
                        width=0.65, zorder=3)
        ax_b.set_title("Monthly Consumption (kWh)",
                       color=C_WHITE, fontsize=11, pad=10)
        ax_b.set_ylabel("kWh", color=C_GREY, fontsize=9)
        ax_b.tick_params(colors=C_GREY, labelsize=8)
        for spine in ax_b.spines.values():
            spine.set_edgecolor(C_BG_LIGHT)
        ax_b.yaxis.grid(True, color=C_BG_LIGHT, linestyle="--", linewidth=0.5)
        ax_b.set_axisbelow(True)

        for bar, val in zip(bars, self.monthly_usage):
            ax_b.text(bar.get_x() + bar.get_width() / 2,
                      bar.get_height() + 4,
                      f"{val:.0f}", ha="center", va="bottom",
                      color=C_WHITE, fontsize=7)

        ap_vals = [v.get() for v in self.appliance_vars.values()]
        ap_keys = list(self.appliance_vars.keys())
        pie_colors = ["#7B2FBE","#00C853","#FFD600","#00C8FF","#FF4B4B",
                      "#9D4EDD","#FF8C00","#00BCD4","#E91E63","#8BC34A"]
        wedges, texts, autotexts = ax_p.pie(
            ap_vals, labels=None, autopct="%1.0f%%",
            colors=pie_colors[:len(ap_vals)],
            startangle=140, pctdistance=0.75,
            wedgeprops=dict(linewidth=1.5, edgecolor=C_BG_MID)
        )
        for at in autotexts:
            at.set(color=C_WHITE, fontsize=7, fontweight="bold")
        ax_p.set_title("Appliance Share (%)",
                       color=C_WHITE, fontsize=11, pad=10)
        ax_p.legend(ap_keys, loc="lower center", bbox_to_anchor=(0.5, -0.22),
                    ncol=2, fontsize=7, frameon=False, labelcolor=C_GREY)

        self.fig_dash.patch.set_facecolor(C_CHART_BG)
        self.canvas_dash.draw()

    # ──────────────────────────────────────────────────────────
    #  TAB 2 – USAGE CHART (line)
    # ──────────────────────────────────────────────────────────
    def _build_usage_chart(self, parent):
        self.fig_line = Figure(figsize=(8.5, 4.8), facecolor=C_CHART_BG)
        self.fig_line.subplots_adjust(left=0.08, right=0.97,
                                      top=0.88, bottom=0.1)
        self.ax_line = self.fig_line.add_subplot(1, 1, 1)

        canvas = FigureCanvasTkAgg(self.fig_line, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas_line = canvas

    def _draw_usage_chart(self):
        ax = self.ax_line
        ax.clear()
        ax.set_facecolor(C_CHART_BG)

        x     = list(range(12))
        usage = self.monthly_usage

        ax.fill_between(x, usage, alpha=0.18, color=C_ACCENT2)
        ax.plot(x, usage, color=C_GREEN, linewidth=2.5,
                marker="o", markersize=7, markerfacecolor=C_YELLOW,
                markeredgecolor=C_BG_DARK, markeredgewidth=1.5, zorder=5)

        window = 3
        avg = [sum(usage[max(0, i - window + 1):i + 1]) /
               len(usage[max(0, i - window + 1):i + 1]) for i in range(12)]
        ax.plot(x, avg, color=C_ACCENT2, linewidth=1.5,
                linestyle="--", label="3-month avg", zorder=4)

        ax.set_xticks(x)
        ax.set_xticklabels(MONTHS, color=C_GREY, fontsize=9)
        ax.tick_params(axis="y", colors=C_GREY, labelsize=9)
        ax.set_title("Annual Energy Usage — Line Chart",
                     color=C_WHITE, fontsize=12, pad=12)
        ax.set_ylabel("kWh", color=C_GREY, fontsize=10)
        ax.yaxis.grid(True, color=C_BG_LIGHT, linestyle="--", linewidth=0.5)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_edgecolor(C_BG_LIGHT)

        max_i = usage.index(max(usage))
        min_i = usage.index(min(usage))
        ax.annotate(f"Peak\n{usage[max_i]:.0f} kWh",
                    xy=(max_i, usage[max_i]),
                    xytext=(max_i + 0.6, usage[max_i] + 15),
                    color=C_RED, fontsize=8,
                    arrowprops=dict(arrowstyle="->", color=C_RED, lw=1))
        ax.annotate(f"Low\n{usage[min_i]:.0f} kWh",
                    xy=(min_i, usage[min_i]),
                    xytext=(min_i + 0.6, usage[min_i] - 35),
                    color=C_GREEN, fontsize=8,
                    arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1))

        ax.legend(fontsize=9, frameon=False, labelcolor=C_GREY)
        self.fig_line.patch.set_facecolor(C_CHART_BG)
        self.canvas_line.draw()

    # ──────────────────────────────────────────────────────────
    #  TAB 3 – COST ANALYSIS (stacked bar)
    # ──────────────────────────────────────────────────────────
    def _build_cost_tab(self, parent):
        self.fig_cost = Figure(figsize=(8.5, 4.8), facecolor=C_CHART_BG)
        self.fig_cost.subplots_adjust(left=0.09, right=0.97,
                                      top=0.88, bottom=0.1)
        self.ax_cost = self.fig_cost.add_subplot(1, 1, 1)

        canvas = FigureCanvasTkAgg(self.fig_cost, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas_cost = canvas

    def _draw_cost_chart(self):
        price = ELECTRICITY_TYPES[self.elec_type.get()]["price"]
        ax    = self.ax_cost
        ax.clear()
        ax.set_facecolor(C_CHART_BG)

        costs = [u * price for u in self.monthly_usage]
        tax   = [c * 0.22  for c in costs]
        base  = [c - t     for c, t in zip(costs, tax)]

        x = list(range(12))
        ax.bar(x, base, color=C_ACCENT2, label="Energy Cost", width=0.6, zorder=3)
        ax.bar(x, tax, bottom=base, color=C_YELLOW,
               label="VAT (22%)", width=0.6, zorder=3)

        ax.set_xticks(x)
        ax.set_xticklabels(MONTHS, color=C_GREY, fontsize=9)
        ax.tick_params(axis="y", colors=C_GREY, labelsize=9)
        ax.set_title(
            f"Monthly Cost Analysis  |  Rate: E{price:.2f}/kWh  |  "
            f"Payment: {self.pay_method.get().split()[1]}",
            color=C_WHITE, fontsize=10, pad=10)
        ax.set_ylabel("EUR Cost", color=C_GREY, fontsize=10)
        ax.yaxis.grid(True, color=C_BG_LIGHT, linestyle="--", linewidth=0.5)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_edgecolor(C_BG_LIGHT)
        ax.legend(fontsize=9, frameon=False, labelcolor=C_GREY, loc="upper right")

        for i, (b, t) in enumerate(zip(base, tax)):
            total = b + t
            ax.text(i, total + 0.5, f"E{total:.0f}",
                    ha="center", fontsize=7, color=C_WHITE)

        self.fig_cost.patch.set_facecolor(C_CHART_BG)
        self.canvas_cost.draw()

    # ──────────────────────────────────────────────────────────
    #  TAB 4 – APPLIANCES (sliders)
    # ──────────────────────────────────────────────────────────
    def _build_appliances_tab(self, parent):
        header = tk.Frame(parent, bg=C_BG_DARK)
        header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(header, text="Home  Daily Appliance Usage  (kWh/day)",
                 bg=C_BG_DARK, fg=C_GREEN,
                 font=("Helvetica", 12, "bold")).pack(side="left")
        ttk.Button(header, text="Recalculate",
                   style="Green.TButton",
                   command=self._refresh_all).pack(side="right")

        canvas_frame = tk.Frame(parent, bg=C_BG_DARK)
        canvas_frame.pack(fill="both", expand=True, padx=12, pady=4)

        cv = tk.Canvas(canvas_frame, bg=C_BG_DARK, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                  command=cv.yview)
        self.scroll_frame = tk.Frame(cv, bg=C_BG_DARK)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: cv.configure(scrollregion=cv.bbox("all"))
        )
        cv.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        cv.configure(yscrollcommand=scrollbar.set)
        cv.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.appl_val_labels = {}
        self.appl_progress   = {}

        for i, (name, var) in enumerate(self.appliance_vars.items()):
            row = tk.Frame(self.scroll_frame, bg=C_BG_MID, pady=6)
            row.pack(fill="x", pady=3)

            icon = APPLIANCE_ICONS[i]
            tk.Label(row, text=f"{icon}  {name}", bg=C_BG_MID,
                     fg=C_WHITE, font=("Helvetica", 10),
                     width=22, anchor="w").pack(side="left", padx=10)

            sl = ttk.Scale(row, from_=0, to=12, variable=var,
                           orient="horizontal", length=280,
                           command=lambda v, n=name: self._update_appl_label(n))
            sl.pack(side="left", padx=6)

            val_lbl = tk.Label(row, text=f"{var.get():.1f} kWh",
                               bg=C_BG_MID, fg=C_YELLOW,
                               font=("Helvetica", 10, "bold"), width=10)
            val_lbl.pack(side="left", padx=6)
            self.appl_val_labels[name] = val_lbl

            pb = ttk.Progressbar(row, orient="horizontal", length=100,
                                 mode="determinate",
                                 style="Horizontal.TProgressbar")
            pb.pack(side="left", padx=6)
            pb["value"] = (var.get() / 12) * 100
            self.appl_progress[name] = pb

    def _update_appl_label(self, name):
        val = self.appliance_vars[name].get()
        self.appl_val_labels[name].config(text=f"{val:.1f} kWh")
        if name in self.appl_progress:
            self.appl_progress[name]["value"] = (val / 12) * 100
        self._update_kpis()

    # ──────────────────────────────────────────────────────────
    #  KPI / REFRESH LOGIC  ← ALL 5 KPIs NOW UPDATED
    # ──────────────────────────────────────────────────────────
    def _refresh_all(self):
        self._update_price_badge()
        self._update_kpis()
        self._draw_dashboard()
        self._draw_usage_chart()
        self._draw_cost_chart()

    def _update_price_badge(self):
        et   = self.elec_type.get()
        info = ELECTRICITY_TYPES[et]
        self.price_badge.config(text=f"{info['icon']}  E{info['price']:.2f} / kWh")

    def _update_kpis(self):
        price  = ELECTRICITY_TYPES[self.elec_type.get()]["price"]
        period = self.period.get()
        total  = sum(self.monthly_usage)          # annual kWh
        cost   = total * price                    # annual cost EUR

        multiplier = {"Daily": 1/365, "Weekly": 1/52,
                      "Monthly": 1/12, "Yearly": 1}.get(period, 1/12)

        # ── KPI 1: Total Usage (period-adjusted) ──────────────
        self.kpi_usage.config(text=f"{total * multiplier:,.1f} kWh")

        # ── KPI 2: Total Cost (period-adjusted) ───────────────
        self.kpi_cost.config(text=f"E {cost * multiplier:,.1f}")

        # ── KPI 3: Average monthly usage ──────────────────────
        self.kpi_avg.config(text=f"{total / 12:,.1f} kWh")

        # ── KPI 4: CO2 saved vs grid average (0.233 kg/kWh) ───
        co2_saved = total * 0.233
        self.kpi_co2.config(text=f"{co2_saved:,.0f} kg")

        # ── KPI 5: AI Prediction — estimated years until       ─
        #    consumption rises 20% based on monthly variance    ─
        monthly_vals = self.monthly_usage
        avg_monthly  = total / 12
        # simple variance-based growth estimate
        variance     = sum((m - avg_monthly) ** 2 for m in monthly_vals) / 12
        growth_rate  = (variance ** 0.5) / avg_monthly  # coefficient of variation
        if growth_rate > 0:
            # years until 20% increase at this growth rate
            years_to_overload = round(0.20 / (growth_rate * 0.05), 1)
            years_to_overload = max(1.0, min(years_to_overload, 30.0))
        else:
            years_to_overload = 10.0
        self.kpi_ai_prediction.config(text=f"{years_to_overload:.1f} yrs")

    def _randomize_data(self):
        self.monthly_usage = [round(random.uniform(180, 480), 1)
                              for _ in range(12)]
        self._refresh_all()

    # ──────────────────────────────────────────────────────────
    #  EXPORT REPORT  ← FIXED: utf-8 encoding + open file after
    # ──────────────────────────────────────────────────────────
    def _export_report(self):
        price = ELECTRICITY_TYPES[self.elec_type.get()]["price"]
        total = sum(self.monthly_usage)
        cost  = total * price

        # AI prediction value (same logic as KPI)
        avg_monthly = total / 12
        variance    = sum((m - avg_monthly) ** 2 for m in self.monthly_usage) / 12
        growth_rate = (variance ** 0.5) / avg_monthly if avg_monthly else 0
        if growth_rate > 0:
            years_pred = round(0.20 / (growth_rate * 0.05), 1)
            years_pred = max(1.0, min(years_pred, 30.0))
        else:
            years_pred = 10.0

        lines = [
            "=" * 52,
            "        HOME ENERGY REPORT — EV PowerShare",
            "=" * 52,
            f"  Generated        : {datetime.datetime.now().strftime('%d %b %Y  %H:%M')}",
            f"  Electricity Type : {self.elec_type.get()}",
            f"  Price per kWh    : EUR {price:.2f}",
            f"  Payment Method   : {self.pay_method.get()}",
            f"  Period Selected  : {self.period.get()}",
            "-" * 52,
            "  MONTHLY USAGE (kWh):",
        ]
        for m, u in zip(MONTHS, self.monthly_usage):
            lines.append(f"    {m:>3}  ->  {u:6.1f} kWh  |  EUR {u * price:6.2f}")
        lines += [
            "-" * 52,
            f"  TOTAL ANNUAL USAGE  : {total:,.1f} kWh",
            f"  TOTAL ANNUAL COST   : EUR {cost:,.2f}",
            f"  AVG MONTHLY USAGE   : {total/12:,.1f} kWh",
            f"  AVG MONTHLY COST    : EUR {cost/12:,.2f}",
            f"  CO2 OFFSET EQUIV.   : {total * 0.233:,.0f} kg",
            f"  AI PREDICTION       : {years_pred:.1f} years",
            "=" * 52,
        ]
        report = "\n".join(lines)

        # Save next to the script so it's always findable
        script_dir  = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(script_dir, "energy_report.txt")

        try:
            # utf-8 encoding prevents Unicode errors on all platforms
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(report)

            # Auto-open the file after saving
            if sys.platform.startswith("win"):
                os.startfile(report_path)
            elif sys.platform == "darwin":
                os.system(f'open "{report_path}"')
            else:
                os.system(f'xdg-open "{report_path}"')

            messagebox.showinfo(
                "Report Saved",
                f"energy_report.txt saved to:\n{report_path}\n\nOpening file...")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    # ──────────────────────────────────────────────────────────
    #  CLOCK
    # ──────────────────────────────────────────────────────────
    def _tick_clock(self):
        now = datetime.datetime.now().strftime("  %d %b %Y  |  %H:%M:%S  ")
        self.clock_lbl.config(text=now)
        self.after(1000, self._tick_clock)


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = HomeEnergyApp()
    app.mainloop()


