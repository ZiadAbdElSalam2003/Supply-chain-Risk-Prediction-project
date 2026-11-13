import json
import os
import unicodedata
from datetime import date
import joblib
import pandas as pd
import streamlit as st
# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Supply Chain | Late Delivery Risk",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# =========================================================
# 2. CUSTOM CSS (PROFESSIONAL DARK THEME)
# =========================================================
st.markdown("""
<style>
    :root {
        --bg-primary: #0b1220;
        --bg-surface: #111a2e;
        --bg-card: #141f36;
        --bg-input: #0e1729;
        --primary: #4c9aff;
        --primary-soft: rgba(76, 154, 255, 0.14);
        --accent: #6aa9ff;
        --success: #34d399;
        --success-soft: rgba(52, 211, 153, 0.10);
        --danger: #f87171;
        --danger-soft: rgba(248, 113, 113, 0.10);
        --warning: #fbbf24;
        --text: #e6edf7;
        --text-strong: #ffffff;
        --muted: #8fa1bb;
        --line: #1f2d4a;
        --line-strong: #2a3d63;
    }
    /* ---------- App background ---------- */
    .stApp {
        background:
            radial-gradient(1200px 600px at 12% -10%, rgba(76,154,255,0.10), transparent 60%),
            radial-gradient(900px 500px at 100% 0%, rgba(99,102,241,0.08), transparent 55%),
            var(--bg-primary);
        color: var(--text);
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1280px;
    }
    /* ---------- Typography ---------- */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-strong) !important;
        letter-spacing: -0.01em;
    }
    p, li, label, span {
        color: var(--text);
    }
    [data-testid="stCaptionContainer"],
    .stCaption, small {
        color: var(--muted) !important;
    }
    hr {
        border-color: var(--line) !important;
    }
    /* ---------- Hero ---------- */
    .hero-card {
        background:
            linear-gradient(135deg, rgba(20,38,70,0.95), rgba(14,26,50,0.95));
        border-radius: 22px;
        padding: 28px 30px;
        color: white;
        box-shadow: 0 18px 44px rgba(0, 0, 0, 0.45);
        border: 1px solid var(--line-strong);
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .hero-card::before {
        content: "";
        position: absolute;
        top: -80px;
        right: -80px;
        width: 280px;
        height: 280px;
        background: radial-gradient(circle, rgba(76,154,255,0.28), transparent 70%);
        pointer-events: none;
    }
    .hero-badge {
        display: inline-block;
        background: var(--primary-soft);
        border: 1px solid rgba(76,154,255,0.35);
        color: var(--accent);
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 11px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .main-title {
        font-size: 40px;
        font-weight: 800;
        line-height: 1.15;
        margin: 0 0 10px 0;
        color: var(--text-strong);
    }
    .subtitle {
        font-size: 16px;
        color: var(--muted);
        margin: 0;
        max-width: 760px;
    }
    .stat-row {
        margin-top: 1.4rem;
        display: flex;
        gap: 14px;
        flex-wrap: wrap;
    }
    .stat-chip {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--line-strong);
        border-radius: 12px;
        padding: 10px 14px;
        min-width: 130px;
    }
    .stat-chip .label {
        display: block;
        font-size: 11px;
        color: var(--muted);
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .stat-chip .value {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-strong);
    }
    /* ---------- Section headings ---------- */
    .section-title {
        font-size: 21px;
        font-weight: 800;
        color: var(--text-strong);
        margin-top: 12px;
        margin-bottom: 12px;
    }
    .section-badge {
        display: inline-block;
        background: var(--primary-soft);
        color: var(--accent);
        border: 1px solid rgba(76,154,255,0.25);
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .info-card {
        background: var(--bg-card);
        padding: 22px 20px;
        border-radius: 16px;
        border: 1px solid var(--line);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.30);
        margin-bottom: 15px;
    }
    /* ---------- Risk result cards ---------- */
    .risk-card {
        padding: 28px 26px;
        border-radius: 18px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.40);
    }
    .high-risk {
        background: linear-gradient(180deg, rgba(248,113,113,0.14) 0%, rgba(248,113,113,0.06) 100%);
        border: 1px solid rgba(248,113,113,0.45);
    }
    .low-risk {
        background: linear-gradient(180deg, rgba(52,211,153,0.14) 0%, rgba(52,211,153,0.06) 100%);
        border: 1px solid rgba(52,211,153,0.45);
    }
    .risk-label {
        font-size: 12px;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .risk-value {
        font-size: 32px;
        font-weight: 800;
        line-height: 1.2;
    }
    .risk-description {
        font-size: 15px;
        margin-top: 10px;
        font-weight: 500;
    }
    /* ---------- Buttons ---------- */
    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #2f7ae5 0%, #4c9aff 100%);
        color: white;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.85rem 1.5rem;
        font-size: 16px;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 12px 24px rgba(47, 122, 229, 0.30);
        transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    }
    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #3d88f0 0%, #6aa9ff 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 14px 28px rgba(76, 154, 255, 0.40);
        transform: translateY(-1px);
    }
    div.stButton > button:active,
    div[data-testid="stFormSubmitButton"] > button:active {
        transform: translateY(0);
    }
    /* ---------- Form / bordered containers ---------- */
    [data-testid="stForm"] {
        background: var(--bg-surface);
        padding: 28px 24px 18px 24px;
        border-radius: 20px;
        border: 1px solid var(--line);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
    }
    [data-testid="stVerticalBlockBorderWrapper"]:not(:has([data-testid="stForm"])) {
        border-color: var(--line) !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    /* ---------- Inputs ---------- */
    .stSelectbox label, .stNumberInput label, .stDateInput label {
        font-size: 13px;
        font-weight: 700;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    .stDateInput div[data-baseweb="input"] > div {
        background-color: var(--bg-input) !important;
        border: 1px solid var(--line-strong) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
    }
    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover {
        border-color: var(--primary) !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(76,154,255,0.20) !important;
    }
    input {
        color: var(--text) !important;
        background-color: transparent !important;
    }
    div[data-baseweb="select"] svg,
    div[data-baseweb="input"] svg {
        fill: var(--muted) !important;
    }
    /* Auto-filled (disabled) fields */
    div[data-baseweb="select"][aria-disabled="true"] > div,
    .stSelectbox:has(input[disabled]) div[data-baseweb="select"] > div {
        background-color: rgba(76,154,255,0.06) !important;
        border-style: dashed !important;
        opacity: 1 !important;
    }
    .stSelectbox:has(input[disabled]) div[data-baseweb="select"] div,
    .stSelectbox:has(input[disabled]) div[data-baseweb="select"] span {
        color: var(--accent) !important;
        -webkit-text-fill-color: var(--accent) !important;
        opacity: 1 !important;
    }
    /* Number input +/- steppers */
    .stNumberInput button {
        background-color: var(--bg-input) !important;
        color: var(--text) !important;
        border-color: var(--line-strong) !important;
    }
    .stNumberInput button:hover {
        background-color: var(--primary-soft) !important;
        color: var(--accent) !important;
    }
    /* Dropdown / popover menus */
    div[data-baseweb="popover"] > div,
    ul[role="listbox"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--line-strong) !important;
        border-radius: 10px !important;
    }
    li[role="option"] {
        background-color: transparent !important;
        color: var(--text) !important;
    }
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: var(--primary-soft) !important;
    }
    /* Calendar */
    div[data-baseweb="calendar"] {
        background-color: var(--bg-card) !important;
        color: var(--text) !important;
    }
    /* ---------- Metrics ---------- */
    .stMetric,
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.30);
    }
    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: var(--text-strong) !important;
    }
    /* ---------- Alerts ---------- */
    [data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--line-strong);
        background-color: var(--bg-card);
    }
    /* ---------- Expander / dataframe ---------- */
    [data-testid="stExpander"] {
        background: var(--bg-surface);
        border: 1px solid var(--line) !important;
        border-radius: 14px;
    }
    [data-testid="stExpander"] summary {
        color: var(--text) !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }
    /* ---------- Progress bar ---------- */
    .stProgress > div > div {
        background-color: var(--line) !important;
        border-radius: 8px;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #34d399 0%, #fbbf24 55%, #f87171 100%);
        border-radius: 8px;
    }
    /* ---------- KPI card ---------- */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.30);
        height: 100%;
    }
    .kpi-card .label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 8px;
    }
    .kpi-card .value {
        font-size: 26px;
        font-weight: 800;
        color: var(--text-strong);
    }
    .kpi-card .hint {
        margin-top: 8px;
        font-size: 12px;
        color: var(--muted);
    }
    /* ---------- Scrollbar ---------- */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb {
        background: var(--line-strong);
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #3a5280; }
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)
# =========================================================
# 3. MODEL & DATA CONFIGURATION
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = "models/late_delivery_pipeline.pkl"
THRESHOLD_PATH = "models/decision_threshold.pkl"
OPTIONS_PATH = os.path.join(BASE_DIR, "dropdown_options.json")
# Replace this with your Supply Chain image path
IMAGE_PATH = r"C:\Users\tsarget\OneDrive\Desktop\nextgen project\images\supply.jpg"
DEFAULT_COUNTRY = "Egipto"
DEFAULT_DEPARTMENT = "Apparel"
@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    threshold = joblib.load(THRESHOLD_PATH)
    return model, threshold
@st.cache_data
def load_dropdown_options(path):
    """
    Build the lookups used by the dependent dropdowns.
    country_lookup:  country -> list of (market, region) pairs
    dept_categories: department -> list of categories
    """
    with open(path, "r", encoding="utf-8") as f:
        options = json.load(f)
    country_lookup = {}
    for market, regions in options["region_countries"].items():
        for region, countries in regions.items():
            for country in countries:
                country_lookup.setdefault(country, []).append((market, region))
    dept_categories = options["department_categories"]
    return country_lookup, dept_categories
def sort_key(text):
    """Sort Spanish names naturally (accents ignored)."""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn").lower()
# =========================================================
# 4. STATIC FEATURE OPTIONS
# =========================================================
TYPE_OPTIONS = [
    "CASH",
    "DEBIT",
    "PAYMENT",
    "TRANSFER"
]
CUSTOMER_SEGMENT_OPTIONS = [
    "Consumer",
    "Corporate",
    "Home Office"
]
SHIPPING_OPTIONS = [
    "First Class",
    "Same Day",
    "Second Class",
    "Standard Class"
]
# =========================================================
# 5. HEADER
# =========================================================
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">Supply Chain Intelligence</div>
    <div class="main-title">Late Delivery Risk Prediction</div>
    <div class="subtitle">Operational forecasting engine for identifying at-risk orders before shipment delays impact service levels.</div>
    <div class="stat-row">
        <div class="stat-chip">
            <span class="label">Model</span>
            <span class="value">Live</span>
        </div>
        <div class="stat-chip">
            <span class="label">Threshold</span>
            <span class="value">Risk-based</span>
        </div>
        <div class="stat-chip">
            <span class="label">Use case</span>
            <span class="value">Logistics</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
header_left, header_right = st.columns([1.6, 0.9])
with header_left:
    st.markdown('<div class="section-badge">Assessment Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title" style="margin-top: 0;">Evaluate order risk before it becomes a delivery issue.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        "This application predicts the likelihood of an order being delivered later than its scheduled delivery date, based on order characteristics, shipping context, and commercial variables."
    )
with header_right:
    if IMAGE_PATH != "YOUR_IMAGE_PATH_HERE" and os.path.exists(IMAGE_PATH):
        st.image(IMAGE_PATH, use_container_width=True)
    else:
        st.markdown("""
        <div style="
            height: 190px;
            background: linear-gradient(135deg, #141f36 0%, #0e1729 100%);
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8fa1bb;
            font-size: 17px;
            font-weight: 700;
            border: 1px dashed #2a3d63;
        ">
            Supply Chain Image Placeholder
        </div>
        """, unsafe_allow_html=True)
st.divider()
# =========================================================
# 6. LOAD MODEL & DROPDOWN DATA
# =========================================================
try:
    model, threshold = load_model()
except FileNotFoundError:
    st.error(
        "Model files were not found. Please check the models folder "
        "and make sure both saved files exist."
    )
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()
try:
    country_lookup, dept_categories = load_dropdown_options(OPTIONS_PATH)
except FileNotFoundError:
    st.error(
        "dropdown_options.json was not found. Place it in the same folder "
        "as this app file."
    )
    st.stop()
except Exception as e:
    st.error(f"Error loading dropdown options: {e}")
    st.stop()
COUNTRY_OPTIONS = sorted(country_lookup.keys(), key=sort_key)
DEPARTMENT_OPTIONS = sorted(dept_categories.keys(), key=sort_key)
# =========================================================
# 7. INPUT SECTIONS
# =========================================================
st.markdown('<div class="section-badge">Order Information</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-title" style="margin-top: 0;">Input order parameters</div>',
    unsafe_allow_html=True
)
st.caption(
    "Enter the details below to evaluate the probability of delayed delivery. "
    "Market and region are filled automatically from the selected country, "
    "and categories are filtered by the selected department."
)
# ---------------------------------------------------------
# SECTION 1: GENERAL ORDER DETAILS
# Kept OUTSIDE the form so the dependent dropdowns
# (country -> market/region, department -> category)
# update instantly when the user changes a selection.
# ---------------------------------------------------------
with st.container(border=True):
    st.markdown("### 1. General Order Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        order_type = st.selectbox(
            "Payment Type",
            TYPE_OPTIONS,
            index=0
        )
        customer_segment = st.selectbox(
            "Customer Segment",
            CUSTOMER_SEGMENT_OPTIONS,
            index=0
        )
        order_date = st.date_input(
            "Order Date",
            value=date.today(),
            min_value=date(2000, 1, 1),
            max_value=date.today()
        )
    with col2:
        department = st.selectbox(
            "Department Name",
            DEPARTMENT_OPTIONS,
            index=DEPARTMENT_OPTIONS.index(DEFAULT_DEPARTMENT)
            if DEFAULT_DEPARTMENT in DEPARTMENT_OPTIONS else 0
        )
        # Categories filtered by the selected department.
        # The key includes the department so the selection resets
        # whenever the department changes.
        category_options = sorted(dept_categories[department], key=sort_key)
        category = st.selectbox(
            "Category Name",
            category_options,
            key=f"category_{department}",
            help="Only categories that belong to the selected department are listed."
        )
        shipping_mode = st.selectbox(
            "Shipping Mode",
            SHIPPING_OPTIONS,
            index=3
        )
    with col3:
        country = st.selectbox(
            "Order Country",
            COUNTRY_OPTIONS,
            index=COUNTRY_OPTIONS.index(DEFAULT_COUNTRY)
            if DEFAULT_COUNTRY in COUNTRY_OPTIONS else 0
        )
        # Market and region are derived from the country.
        # Locked (greyed) when there is only one possible value;
        # selectable when the country maps to several regions
        # (e.g. Estados Unidos -> East / West / South / Center).
        geo_entries = country_lookup[country]
        market_options = sorted({m for m, _ in geo_entries}, key=sort_key)
        market = st.selectbox(
            "Market",
            market_options,
            key=f"market_{country}",
            disabled=len(market_options) == 1,
            help="Set automatically from the selected country."
        )
        region_options = sorted(
            {r for m, r in geo_entries if m == market},
            key=sort_key
        )
        region = st.selectbox(
            "Order Region",
            region_options,
            key=f"region_{country}_{market}",
            disabled=len(region_options) == 1,
            help=(
                "Set automatically from the selected country."
                if len(region_options) == 1
                else "This country spans several regions. Choose one."
            )
        )
# ---------------------------------------------------------
# SECTIONS 2 & 3: SHIPPING AND FINANCIAL (inside the form)
# ---------------------------------------------------------
with st.container(border=True):
    # -----------------------------------------------------
    # SECTION 2: SHIPPING INFORMATION
    # -----------------------------------------------------
    st.markdown("### 2. Shipping Information")
    col1, col2 = st.columns(2)
    with col1:
        scheduled_days = st.number_input(
            "Days for Shipment (Scheduled)",
            min_value=0,
            value=3,
            step=1
        )
    with col2:
        quantity = st.number_input(
            "Order Item Quantity",
            min_value=1,
            value=1,
            step=1
        )
    st.divider()
    # -----------------------------------------------------
    # SECTION 3: FINANCIAL INFORMATION
    # -----------------------------------------------------
    st.markdown("### 3. Financial Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        product_price = st.number_input(
            "Order Item Product Price",
            min_value=0.0,
            value=100.0,
            step=1.0,
            format="%.2f"
        )
    with col2:
        discount_rate_percent = st.number_input(
            "Order Item Discount Rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0,
            format="%.2f",
            help="Enter the discount rate as a percentage (e.g. 10 = 10%)."
        )
    with col3:
        profit_ratio_percent = st.number_input(
            "Order Item Profit Ratio (%)",
            value=10.0,
            step=1.0,
            format="%.2f",
            help="Enter the profit ratio as a percentage (e.g. 10 = 10%)."
        )


    # Convert percentage inputs to decimals for the model.
    discount_rate = discount_rate_percent / 100
    profit_ratio = profit_ratio_percent / 100

    # Calculate the remaining financial features automatically.
    gross_amount = product_price * quantity
    discount = gross_amount * discount_rate
    item_total = gross_amount - discount
    benefit = item_total * profit_ratio

    st.caption("The following values are calculated automatically:")
    result_col1, result_col2, result_col3 = st.columns(3)
    with result_col1:
        st.metric("Order Item Discount", f"{discount:.2f}")
    with result_col2:
        st.metric("Order Item Total", f"{item_total:.2f}")
    with result_col3:
        st.metric("Benefit per Order", f"{benefit:.2f}")

    st.divider()
    # -----------------------------------------------------
    # SUBMIT
    # -----------------------------------------------------
    submitted = st.button(
        "Predict Delivery Risk"
    )
# =========================================================
# 8. PREDICTION
# =========================================================
if submitted:
    # Extract date components automatically
    order_month = order_date.month
    order_day = order_date.day
    order_year = order_date.year
    # Create input DataFrame
    input_data = pd.DataFrame([{
        "Type": order_type,
        "Days for shipment (scheduled)": scheduled_days,
        "Benefit per order": benefit,
        "Category Name": category,
        "Customer Segment": customer_segment,
        "Department Name": department,
        "Market": market,
        "Order Country": country,
        "Order Item Discount": discount,
        "Order Item Discount Rate": discount_rate,
        "Order Item Product Price": product_price,
        "Order Item Profit Ratio": profit_ratio,
        "Order Item Quantity": quantity,
        "Order Item Total": item_total,
        "Order Region": region,
        "Shipping Mode": shipping_mode,
        "order_month": order_month,
        "order_day": order_day,
        "order_year": order_year
    }])
    # Ensure the exact training feature order
    feature_order = [
        "Type",
        "Days for shipment (scheduled)",
        "Benefit per order",
        "Category Name",
        "Customer Segment",
        "Department Name",
        "Market",
        "Order Country",
        "Order Item Discount",
        "Order Item Discount Rate",
        "Order Item Product Price",
        "Order Item Profit Ratio",
        "Order Item Quantity",
        "Order Item Total",
        "Order Region",
        "Shipping Mode",
        "order_month",
        "order_day",
        "order_year"
    ]
    input_data = input_data[feature_order]
    # Predict probability
    probability = model.predict_proba(input_data)[0][1]
    # Apply selected threshold
    prediction = int(probability >= threshold)
    st.divider()
    st.markdown('<div class="section-badge">Prediction Results</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-title" style="margin-top: 0;">Operational risk review</div>',
        unsafe_allow_html=True
    )
    result_col1, result_col2 = st.columns(2)
    with result_col1:
        st.metric(
            label="Late Delivery Probability",
            value=f"{probability:.2%}"
        )
    with result_col2:
        st.metric(
            label="Decision Threshold",
            value=f"{threshold:.0%}"
        )
    # Risk result
    if prediction == 1:
        st.markdown(f"""
        <div class="risk-card high-risk">
            <div class="risk-label" style="color:#fca5a5;">
                DELIVERY RISK STATUS
            </div>
            <div class="risk-value" style="color:#f87171;">
                HIGH RISK
            </div>
            <div class="risk-description" style="color:#fecaca;">
                This order is predicted to be delivered late.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.warning(
            "Consider reviewing the shipping arrangements "
            "and taking preventive actions."
        )
    else:
        st.markdown(f"""
        <div class="risk-card low-risk">
            <div class="risk-label" style="color:#6ee7b7;">
                DELIVERY RISK STATUS
            </div>
            <div class="risk-value" style="color:#34d399;">
                LOW RISK
            </div>
            <div class="risk-description" style="color:#a7f3d0;">
                This order is predicted to arrive on time.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.success(
            "The order is currently classified as low risk."
        )
    # Probability progress bar
    st.markdown("#### Late Delivery Probability")
    st.progress(float(probability))
    st.caption(
        "The probability represents the model's estimated likelihood "
        "of late delivery. The final classification uses the selected "
        "decision threshold."
    )
    # Display submitted order information
    with st.expander("View Submitted Order Information"):
        st.dataframe(
            input_data.T.rename(columns={0: "Selected Value"}),
            use_container_width=True
        )
# =========================================================
# 9. FOOTER
# =========================================================
st.divider()
st.markdown("""
<div style="
    text-align: center;
    color: #5f7186;
    font-size: 13px;
    padding: 10px;
">
    Supply Chain Late Delivery Risk Prediction |
    Machine Learning Project
</div>
""", unsafe_allow_html=True)
