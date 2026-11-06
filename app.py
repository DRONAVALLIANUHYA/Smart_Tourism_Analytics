
import streamlit as st
import os
import pandas as pd
import plotly.express as px
from datetime import date, timedelta, datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

from src.business_analytics import (
    get_data,
    passenger_analytics,
    hotel_analytics,
    sales_analytics
)

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Fuji Analytics | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0B1220;
    color: #E5EDF8;
}

[data-testid="stHeader"] {
    background: #0B1220;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080F1C 0%, #14243B 100%);
}

[data-testid="stSidebar"] * {
    color: #E5EDF8 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 8px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #263B58;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3, h4, [data-testid="stMarkdownContainer"] p {
    color: #E5EDF8;
}

[data-testid="stCaptionContainer"] {
    color: #9AABC1;
}

/* Dark date-range picker: style the Base Web input wrapper and its nested elements */
[data-testid="stDateInput"] label,
[data-testid="stDateInput"] p {
    color: #D7E3F3 !important;
}

/* Streamlit date_input renders a nested Base Web input wrapper.
   Style the wrapper itself, not only the HTML input element. */
[data-testid="stDateInput"] [data-baseweb="input"],
[data-testid="stDateInput"] [data-baseweb="input"] > div,
[data-testid="stDateInput"] [data-baseweb="input"] > div > div {
    background: #172338 !important;
    background-color: #172338 !important;
    border-color: #45617F !important;
    box-shadow: none !important;
}

[data-testid="stDateInput"] input,
[data-testid="stDateInput"] [data-baseweb="input"] input {
    background: transparent !important;
    background-color: transparent !important;
    color: #F1F5F9 !important;
    -webkit-text-fill-color: #F1F5F9 !important;
    border: 0 !important;
    caret-color: #38BDF8 !important;
}

[data-testid="stDateInput"] input::placeholder {
    color: #9AABC1 !important;
    -webkit-text-fill-color: #9AABC1 !important;
}

[data-testid="stDateInput"] [data-baseweb="input"] {
    border: 1px solid #45617F !important;
    border-radius: 9px !important;
    overflow: hidden !important;
}

[data-testid="stDateInput"] button {
    color: #38BDF8 !important;
    background: transparent !important;
}

[data-testid="stDateInput"] svg {
    fill: #38BDF8 !important;
    color: #38BDF8 !important;
}

[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] [role="dialog"],
[data-baseweb="calendar"] {
    background: #172338 !important;
    background-color: #172338 !important;
    color: #E5EDF8 !important;
}

[data-baseweb="calendar"] button,
[data-baseweb="calendar"] [role="gridcell"] {
    color: #E5EDF8 !important;
}

[data-testid="stTooltipContent"] {
    background: #172338 !important;
    color: #E5EDF8 !important;
    border: 1px solid #45617F !important;
}

.js-plotly-plot .gtitle,
.js-plotly-plot .legendtext {
    fill: #E5EDF8 !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172338, #1B2C45);
    border: 1px solid #30435E;
    padding: 22px 20px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.18);
}

[data-testid="stMetricLabel"] {
    color: #A9B8CC !important;
    font-size: 14px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
    font-weight: 800;
}

[data-testid="stPlotlyChart"] {
    background: #172338;
    border: 1px solid #30435E;
    border-radius: 16px;
    padding: 10px;
}

.section-title {
    color: #F1F5F9;
    font-size: 23px;
    font-weight: 750;
    margin-top: 22px;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #9AABC1;
    font-size: 13px;
    margin-bottom: 18px;
}

.hero {
    background: linear-gradient(115deg, #10243D, #0F766E);
    padding: 30px;
    border: 1px solid #28566A;
    border-radius: 18px;
    color: #FFFFFF;
    margin-bottom: 25px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 29px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #C8E8EA !important;
    font-size: 14px;
    margin-bottom: 0;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #30435E;
    border-radius: 12px;
}

.stButton button, .stDownloadButton button {
    background: #0F766E;
    color: #FFFFFF;
    border: 1px solid #14B8A6;
    border-radius: 9px;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #14B8A6;
    color: #FFFFFF;
}

hr {
    border-color: #304158;
}

/* Website-style landing page */
@keyframes riseIn {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}
.landing-hero, .feature-card, .about-panel {
    animation: riseIn .7s ease both;
}
.feature-card {
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}
.feature-card:hover {
    transform: translateY(-5px);
    border-color: #2DD4BF;
    box-shadow: 0 15px 32px rgba(20,184,166,.13);
}
.landing-hero {
    position: relative;
    overflow: hidden;
    padding: 58px 48px;
    border: 1px solid rgba(103, 232, 249, 0.25);
    border-radius: 24px;
    background: radial-gradient(circle at 85% 15%, rgba(56,189,248,.22), transparent 28%),
                radial-gradient(circle at 8% 100%, rgba(20,184,166,.22), transparent 32%),
                linear-gradient(125deg, #10243D 0%, #123B4A 52%, #0F766E 100%);
    box-shadow: 0 18px 50px rgba(0,0,0,.28);
    margin: 8px 0 28px 0;
}
.landing-eyebrow {
    color: #99F6E4 !important;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2.2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}
.landing-hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(32px, 4vw, 48px);
    line-height: 1.12;
    font-weight: 800;
    max-width: 780px;
    margin: 0 0 16px 0;
}
.landing-hero p {
    color: #D6EAF2 !important;
    font-size: 16px;
    line-height: 1.75;
    max-width: 760px;
    margin-bottom: 0;
}
.landing-section-heading {
    color: #F1F5F9;
    font-size: 24px;
    font-weight: 750;
    margin: 28px 0 7px 0;
}
.landing-section-copy {
    color: #9AABC1;
    font-size: 14px;
    margin-bottom: 18px;
}
.feature-card {
    min-height: 176px;
    height: 100%;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #30435E;
    background: linear-gradient(145deg, #172338, #1B2C45);
    box-shadow: 0 8px 24px rgba(0,0,0,.14);
}
.feature-icon {
    font-size: 27px;
    margin-bottom: 12px;
}
.feature-card h3 {
    color: #F1F5F9 !important;
    font-size: 17px;
    font-weight: 750;
    margin: 0 0 8px 0;
}
.feature-card p {
    color: #A9B8CC !important;
    font-size: 13px;
    line-height: 1.55;
    margin: 0;
}
.about-panel {
    background: #111F32;
    border: 1px solid #30435E;
    border-radius: 17px;
    padding: 24px;
    margin-top: 22px;
}
.about-panel h3 {
    color: #F1F5F9 !important;
    margin-top: 0;
}
.about-panel p {
    color: #B8C7D9 !important;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🗻 FUJI ANALYTICS")
    st.caption("BUSINESS INTELLIGENCE PLATFORM")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Home",
            "Overview",
            "Transportation",
            "Hospitality",
            "Sales Analytics",
            "AI Insights",
            "Data Explorer"
        ],
        key="page_selector"
    )

    st.divider()

    st.markdown("### Date Range")
    selected_dates = st.date_input(
        "Filter dashboard data",
        value=(date.today() - timedelta(days=365), date.today()),
    )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = selected_dates
        end_date = selected_dates

    st.caption(f"Showing: {start_date:%d %b %Y} to {end_date:%d %b %Y}")

    st.divider()

    st.markdown("### Project Information")
    st.caption("Smart Tourism & Transportation")
    st.caption("Analytics System")

    st.divider()

    st.markdown("🟢 Database: MySQL")
    st.markdown("🔵 Analytics: Python + SQL")
    st.markdown("🟣 Visualization: Plotly")

    st.divider()
    st.caption("Academic Portfolio Project")


# On the public-facing landing page, hide the app sidebar completely.
# It becomes available after the visitor enters an analytics section.
if page == "Home":
    st.markdown("""
    <style>
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stAppViewContainer"] > .main {
            margin-left: 0 !important;
        }
        [data-testid="stHeader"] {
            background: transparent !important;
        }
        .main .block-container {
            max-width: 1380px;
            padding-top: 1.1rem;
            padding-left: 3.5rem;
            padding-right: 3.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: block !important;
        }
    </style>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data(ttl=60)
def load_dashboard_data(start_date, end_date):

    # Dates originate from Streamlit date_input and are formatted as ISO dates.
    start_value = start_date.isoformat()
    end_value = end_date.isoformat()

    passenger_df = get_data(f"""
        SELECT
            route,
            COUNT(*) AS total_passengers,
            SUM(ticket_price) AS total_revenue
        FROM passengers
        WHERE travel_date BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY route
        ORDER BY total_passengers DESC
    """)

    hotel_df = get_data(f"""
        SELECT
            hotel_name,
            COUNT(*) AS total_bookings,
            SUM(
                CASE WHEN booking_status = 'Cancelled'
                THEN 1 ELSE 0 END
            ) AS cancelled_bookings
        FROM hotel_bookings
        WHERE check_in BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY hotel_name
        ORDER BY total_bookings DESC
    """)

    sales_df = get_data(f"""
        SELECT
            product,
            SUM(quantity) AS total_quantity,
            SUM(total_amount) AS total_revenue
        FROM sales
        WHERE sale_date BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY product
        ORDER BY total_revenue DESC
    """)

    passenger_kpi = get_data(f"""
        SELECT COUNT(*) AS total
        FROM passengers
        WHERE travel_date BETWEEN '{start_value}' AND '{end_value}'
    """)

    hotel_kpi = get_data(f"""
        SELECT COUNT(*) AS total
        FROM hotel_bookings
        WHERE check_in BETWEEN '{start_value}' AND '{end_value}'
    """)

    revenue_kpi = get_data(f"""
        SELECT SUM(total_amount) AS total
        FROM sales
        WHERE sale_date BETWEEN '{start_value}' AND '{end_value}'
    """)

    passenger_trend = get_data(f"""
        SELECT
            DATE_FORMAT(travel_date, '%Y-%m') AS month,
            COUNT(*) AS passengers
        FROM passengers
        WHERE travel_date BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY month
        ORDER BY month
    """)

    sales_trend = get_data(f"""
        SELECT
            DATE_FORMAT(sale_date, '%Y-%m') AS month,
            SUM(total_amount) AS revenue
        FROM sales
        WHERE sale_date BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY month
        ORDER BY month
    """)

    booking_status = get_data(f"""
        SELECT
            booking_status,
            COUNT(*) AS total
        FROM hotel_bookings
        WHERE check_in BETWEEN '{start_value}' AND '{end_value}'
        GROUP BY booking_status
    """)

    return (
        passenger_df,
        hotel_df,
        sales_df,
        passenger_kpi,
        hotel_kpi,
        revenue_kpi,
        passenger_trend,
        sales_trend,
        booking_status
    )

try:

    (
        passenger_df,
        hotel_df,
        sales_df,
        passenger_kpi,
        hotel_kpi,
        revenue_kpi,
        passenger_trend,
        sales_trend,
        booking_status
    ) = load_dashboard_data(start_date, end_date)

except Exception as error:

    st.error(f"Unable to load dashboard data: {error}")
    st.stop()


# --------------------------------------------------
# KPI VALUES
# --------------------------------------------------

total_passengers = int(passenger_kpi.iloc[0, 0])
total_bookings = int(hotel_kpi.iloc[0, 0])

total_revenue = revenue_kpi.iloc[0, 0]

if pd.isna(total_revenue):
    total_revenue = 0

total_revenue = float(total_revenue)


# --------------------------------------------------
# PDF BUSINESS REPORT GENERATOR
# --------------------------------------------------

def create_pdf_report(
    start_date,
    end_date,
    total_passengers,
    total_bookings,
    total_revenue,
    passenger_df,
    hotel_df,
    sales_df
):
    """Create a downloadable PDF report for the selected dashboard period."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=24,
        textColor=colors.HexColor("#12304A"),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#526579"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#263445"),
        spaceAfter=5
    )

    story = []

    story.append(Paragraph("FUJI ANALYTICS", title_style))
    story.append(Paragraph(
        "Smart Tourism &amp; Transportation Business Report",
        subtitle_style
    ))
    story.append(Paragraph(
        f"Reporting period: {start_date:%d %B %Y} to {end_date:%d %B %Y}",
        subtitle_style
    ))
    story.append(Paragraph(
        f"Generated on: {datetime.now():%d %B %Y, %H:%M}",
        subtitle_style
    ))
    story.append(Spacer(1, 8))

    # KPI summary
    story.append(Paragraph("1. Executive Summary", section_style))

    kpi_data = [
        ["Performance Indicator", "Result"],
        ["Total passengers", f"{total_passengers:,}"],
        ["Total hotel bookings", f"{total_bookings:,}"],
        ["Total sales revenue", f"JPY {total_revenue:,.0f}"]
    ]

    kpi_table = Table(kpi_data, colWidths=[105 * mm, 55 * mm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12304A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#EEF4F8")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#263445")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5E0E8")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))
    story.append(kpi_table)

    def add_dataframe_table(title, dataframe, columns, headers):
        story.append(Paragraph(title, section_style))

        if dataframe.empty:
            story.append(Paragraph(
                "No records were found for the selected date range.",
                body_style
            ))
            return

        table_data = [headers]

        for _, row in dataframe[columns].iterrows():
            formatted_row = []
            for value in row.tolist():
                if pd.isna(value):
                    formatted_row.append("0")
                elif isinstance(value, (int, float)):
                    if isinstance(value, float):
                        formatted_row.append(f"{value:,.2f}")
                    else:
                        formatted_row.append(f"{value:,}")
                else:
                    formatted_row.append(str(value))
            table_data.append(formatted_row)

        widths = [160 * mm / len(headers)] * len(headers)
        report_table = Table(
            table_data,
            colWidths=widths,
            repeatRows=1,
            hAlign="LEFT"
        )
        report_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12304A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F4F7FA")),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#263445")),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5E0E8")),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ]))
        story.append(report_table)

    add_dataframe_table(
        "2. Transportation Performance",
        passenger_df,
        ["route", "total_passengers", "total_revenue"],
        ["Route", "Passengers", "Ticket revenue (JPY)"]
    )

    add_dataframe_table(
        "3. Hotel Booking Performance",
        hotel_df,
        ["hotel_name", "total_bookings", "cancelled_bookings"],
        ["Hotel", "Bookings", "Cancelled"]
    )

    add_dataframe_table(
        "4. Product Sales Performance",
        sales_df,
        ["product", "total_quantity", "total_revenue"],
        ["Product", "Quantity sold", "Revenue (JPY)"]
    )

    # Data-driven observations
    story.append(Paragraph("5. Business Observations", section_style))

    observations = []

    if not passenger_df.empty:
        top_route = passenger_df.loc[
            passenger_df["total_passengers"].idxmax()
        ]
        observations.append(
            f"The busiest route in the selected period is "
            f"<b>{top_route['route']}</b>, with "
            f"{int(top_route['total_passengers']):,} passenger records."
        )

    if not hotel_df.empty:
        top_hotel = hotel_df.loc[
            hotel_df["total_bookings"].idxmax()
        ]
        observations.append(
            f"<b>{top_hotel['hotel_name']}</b> recorded the highest "
            f"number of bookings among the hotels shown, with "
            f"{int(top_hotel['total_bookings']):,} bookings."
        )

        total_report_bookings = int(hotel_df["total_bookings"].sum())
        cancelled_report_bookings = int(hotel_df["cancelled_bookings"].sum())

        if total_report_bookings:
            cancellation_rate = (
                cancelled_report_bookings / total_report_bookings
            ) * 100
            observations.append(
                f"The booking cancellation rate for the selected period "
                f"is {cancellation_rate:.2f}%."
            )

    if not sales_df.empty:
        top_product = sales_df.loc[
            sales_df["total_revenue"].idxmax()
        ]
        observations.append(
            f"<b>{top_product['product']}</b> generated the highest "
            f"product revenue, at JPY {float(top_product['total_revenue']):,.0f}."
        )

    if observations:
        for item in observations:
            story.append(Paragraph(f"• {item}", body_style))
    else:
        story.append(Paragraph(
            "There is not enough data in this period to generate observations.",
            body_style
        ))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Data note: This academic portfolio dashboard uses synthetic sample "
        "data. The figures are for demonstration and are not actual Fuji "
        "Kyuko business records.",
        body_style
    ))

    document.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# --------------------------------------------------
# REUSABLE CHART STYLE
# --------------------------------------------------

def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#172338",
        plot_bgcolor="#172338",
        font=dict(
            family="Inter",
            color="#E5EDF8",
            size=12
        ),
        title_font=dict(color="#F1F5F9", size=15),
        legend_font=dict(color="#CBD5E1", size=11),
        margin=dict(l=25, r=25, t=55, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(
        showgrid=False,
        color="#A9B8CC"
    )
    fig.update_yaxes(
        gridcolor="#304158",
        zeroline=False,
        color="#A9B8CC"
    )

    return fig


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

if page != "Home":
    st.markdown("""
    <div class="hero">
        <h1>Smart Tourism & Transportation Analytics</h1>
        <p>
            Business intelligence and operational performance
            insights for tourism, transportation and hospitality.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Analytics period: {start_date:%d %b %Y} – {end_date:%d %b %Y}"
    )


# --------------------------------------------------
# WEBSITE LANDING PAGE
# --------------------------------------------------

if page == "Home":

    nav_left, nav_space, nav_action = st.columns([2.2, 4.8, 1.5], vertical_alignment="center")
    with nav_left:
        st.markdown(
            '<div style="font-size:20px;font-weight:800;letter-spacing:.4px;color:#F1F5F9;">'
            '🗻 FUJI <span style="color:#5EEAD4;">ANALYTICS</span></div>'
            '<div style="font-size:10px;letter-spacing:2px;color:#94A3B8;">SMART DESTINATIONS PLATFORM</div>',
            unsafe_allow_html=True
        )
    with nav_action:
        st.button(
            "Enter Dashboard  →",
            key="landing_enter_dashboard",
            type="primary",
            use_container_width=True,
            on_click=lambda: st.session_state.update(page_selector="Overview")
        )

    st.markdown("""
    <div class="landing-hero">
        <div class="landing-eyebrow">SMART DESTINATIONS · CONNECTED MOBILITY · DATA INSIGHTS</div>
        <h1>Explore smarter tourism through data.</h1>
        <p>
            A unified analytics platform that brings transportation,
            hospitality and sales data together. Explore performance,
            understand business patterns and generate AI-assisted insights
            through one interactive workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="landing-section-heading">Welcome to the platform</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="landing-section-copy">Explore the key capabilities of the Smart Tourism & Transportation Analytics System.</div>',
        unsafe_allow_html=True
    )

    feature_columns = st.columns(3, gap="large")
    features = [
        ("🚆", "Transportation Analytics", "Understand passenger traffic, route performance and ticket revenue.", "Transportation"),
        ("🏨", "Hospitality Analytics", "Review hotel bookings, reservation status and cancellation patterns.", "Hospitality"),
        ("📈", "Sales Analytics", "Explore product performance, sales revenue and monthly trends.", "Sales Analytics"),
        ("✨", "AI Business Insights", "Generate management observations and practical recommendations from aggregated data.", "AI Insights"),
        ("🗂️", "Data Explorer", "View and download sample records stored in the MySQL database.", "Data Explorer"),
        ("📄", "Business Reports", "Create a downloadable PDF report for the selected reporting period.", "Overview")
    ]

    for idx, (icon, title, description, target) in enumerate(features):
        with feature_columns[idx % 3]:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{icon}</div>'
                f'<h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True
            )
            st.button(
                f"Open {title}",
                key=f"home_nav_{idx}",
                use_container_width=True,
                on_click=lambda destination=target: st.session_state.update(page_selector=destination)
            )

    st.markdown("""
    <div class="about-panel">
        <h3>About this project</h3>
        <p>
            This project demonstrates how data engineering, SQL analytics,
            interactive visualization and generative AI can support data-informed
            decisions across tourism-related business operations. It is designed
            as an academic portfolio project using synthetic sample datasets.
        </p>
        <p>
            <b>Technology:</b> Python · MySQL · Pandas · Plotly · Streamlit · Groq API
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        f"Sample dashboard period: {start_date:%d %b %Y} to {end_date:%d %b %Y}. "
        "The data shown are synthetic and are not actual Fuji Kyuko business records."
    )


# --------------------------------------------------
# OVERVIEW PAGE
# --------------------------------------------------

elif page == "Overview":

    st.markdown(
        '<div class="section-title">Business Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Key business performance indicators</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "👥 Total Passengers",
        f"{total_passengers:,}"
    )

    col2.metric(
        "🏨 Total Hotel Bookings",
        f"{total_bookings:,}"
    )

    col3.metric(
        "💴 Total Sales Revenue",
        f"¥{total_revenue:,.0f}"
    )

    st.divider()

    # Passenger charts
    st.markdown(
        '<div class="section-title">Transportation Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            passenger_df,
            x="route",
            y="total_passengers",
            color="route",
            title="Passenger Traffic by Route",
            labels={
                "route": "Transportation Route",
                "total_passengers": "Passengers"
            }
        )

        fig.update_layout(showlegend=False)
        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        fig = px.pie(
            passenger_df,
            names="route",
            values="total_revenue",
            hole=0.55,
            title="Revenue Distribution by Route"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    # Trends
    st.markdown(
        '<div class="section-title">Business Trends</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.line(
            passenger_trend,
            x="month",
            y="passengers",
            markers=True,
            title="Monthly Passenger Trends",
            labels={
                "month": "Month",
                "passengers": "Passengers"
            }
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        fig = px.line(
            sales_trend,
            x="month",
            y="revenue",
            markers=True,
            title="Monthly Sales Revenue",
            labels={
                "month": "Month",
                "revenue": "Revenue (JPY)"
            }
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    # Hotel booking status
    st.markdown(
        '<div class="section-title">Hospitality Performance</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns([1, 2])

    with c1:

        fig = px.pie(
            booking_status,
            names="booking_status",
            values="total",
            hole=0.55,
            title="Booking Status Distribution"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with c2:

        fig = px.bar(
            hotel_df,
            x="hotel_name",
            y="total_bookings",
            color="hotel_name",
            title="Hotel-wise Booking Performance"
        )

        fig.update_layout(showlegend=False)

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )


# --------------------------------------------------
# TRANSPORTATION PAGE
# --------------------------------------------------

elif page == "Transportation":

    st.markdown("## 🚆 Transportation Analytics")
    st.caption("Passenger traffic, route performance, revenue and operational observations.")

    st.metric("Total Passengers", f"{total_passengers:,}")

    if passenger_df.empty:
        st.info("No passenger records are available for the selected date range. Adjust the date filter to view transportation analytics.")
    else:
        transport_view = passenger_df.copy()
        transport_view["average_ticket_price"] = (
            transport_view["total_revenue"] /
            transport_view["total_passengers"].replace(0, pd.NA)
        ).fillna(0)

        top_route = transport_view.sort_values("total_passengers", ascending=False).iloc[0]
        low_route = transport_view.sort_values("total_passengers", ascending=True).iloc[0]
        total_route_revenue = float(transport_view["total_revenue"].sum())
        average_fare = (
            total_route_revenue / float(transport_view["total_passengers"].sum())
            if float(transport_view["total_passengers"].sum()) > 0 else 0
        )

        k1, k2, k3 = st.columns(3)
        k1.metric("Routes Analysed", f"{len(transport_view):,}")
        k2.metric("Top Route", str(top_route["route"]))
        k3.metric("Average Ticket Price", f"¥{average_fare:,.0f}")

        st.divider()
        c1, c2 = st.columns(2)

        with c1:
            fig = px.bar(
                transport_view.sort_values("total_passengers", ascending=False),
                x="route",
                y="total_passengers",
                color="total_passengers",
                color_continuous_scale=["#164E63", "#2DD4BF"],
                title="Route-wise Passenger Traffic",
                labels={"route": "Route", "total_passengers": "Passengers"}
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with c2:
            fig = px.bar(
                transport_view.sort_values("total_revenue", ascending=False),
                x="route",
                y="total_revenue",
                color="total_revenue",
                color_continuous_scale=["#1D4ED8", "#38BDF8"],
                title="Route-wise Ticket Revenue",
                labels={"route": "Route", "total_revenue": "Revenue (JPY)"}
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        if not passenger_trend.empty:
            fig = px.line(
                passenger_trend,
                x="month",
                y="passengers",
                markers=True,
                title="Monthly Passenger Trend",
                labels={"month": "Month", "passengers": "Passengers"}
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.markdown("### Business Observations & Recommendations")
        st.caption("Automatically calculated from the selected passenger records.")

        observation_col, recommendation_col = st.columns(2)
        with observation_col:
            st.markdown("**What the data shows**")
            st.markdown(
                f"- **{top_route['route']}** has the highest passenger volume "
                f"({int(top_route['total_passengers']):,} passengers)."
            )
            if str(low_route["route"]) != str(top_route["route"]):
                st.markdown(
                    f"- **{low_route['route']}** has the lowest passenger volume "
                    f"({int(low_route['total_passengers']):,} passengers)."
                )
            st.markdown(
                f"- The analysed routes generated **¥{total_route_revenue:,.0f}** "
                f"in ticket revenue."
            )

        with recommendation_col:
            st.markdown("**Suggested actions**")
            st.markdown(
                f"- Review capacity and service frequency on **{top_route['route']}**, "
                "especially during its busier travel periods."
            )
            if str(low_route["route"]) != str(top_route["route"]):
                st.markdown(
                    f"- Investigate demand patterns on **{low_route['route']}** "
                    "before changing its service frequency."
                )
            st.markdown(
                "- Compare passenger demand by day and time before making "
                "timetable or resource-allocation decisions."
            )

        st.caption(
            "These are data-based planning suggestions, not operational instructions. "
            "The project uses synthetic demonstration data."
        )

        st.markdown("### Route Performance Details")
        st.dataframe(
            transport_view.rename(columns={
                "route": "Route",
                "total_passengers": "Passengers",
                "total_revenue": "Ticket Revenue (JPY)",
                "average_ticket_price": "Average Ticket Price (JPY)"
            }),
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# HOSPITALITY PAGE
# --------------------------------------------------

elif page == "Hospitality":

    st.markdown("## 🏨 Hospitality Analytics")
    st.caption("Hotel booking performance, cancellation patterns and operational observations.")

    if hotel_df.empty:
        st.info("No hotel bookings are available for the selected date range. Adjust the date filter to view hospitality analytics.")
    else:
        hotel_view = hotel_df.copy()
        hotel_view["cancelled_bookings"] = hotel_view["cancelled_bookings"].fillna(0)
        hotel_view["active_bookings"] = (
            hotel_view["total_bookings"] - hotel_view["cancelled_bookings"]
        ).clip(lower=0)
        hotel_view["cancellation_rate"] = (
            hotel_view["cancelled_bookings"] /
            hotel_view["total_bookings"].replace(0, pd.NA) * 100
        ).fillna(0)

        cancelled_total = int(hotel_view["cancelled_bookings"].sum())
        active_total = int(hotel_view["active_bookings"].sum())
        cancellation_rate = (
            cancelled_total / int(hotel_view["total_bookings"].sum()) * 100
            if int(hotel_view["total_bookings"].sum()) else 0
        )
        top_hotel = hotel_view.sort_values("total_bookings", ascending=False).iloc[0]
        highest_cancel_hotel = hotel_view.sort_values("cancellation_rate", ascending=False).iloc[0]

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Bookings", f"{total_bookings:,}")
        k2.metric("Non-cancelled Bookings", f"{active_total:,}")
        k3.metric("Cancelled Bookings", f"{cancelled_total:,}")
        k4.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")

        st.divider()
        left_chart, right_chart = st.columns(2)

        with left_chart:
            fig = px.bar(
                hotel_view.sort_values("total_bookings", ascending=False),
                x="hotel_name",
                y="total_bookings",
                color="total_bookings",
                color_continuous_scale=["#164E63", "#2DD4BF"],
                title="Bookings by Hotel",
                labels={"hotel_name": "Hotel", "total_bookings": "Bookings"}
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right_chart:
            fig = px.pie(
                booking_status,
                names="booking_status",
                values="total",
                hole=0.58,
                title="Booking Status Distribution"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        fig = px.bar(
            hotel_view.sort_values("cancellation_rate", ascending=False),
            x="hotel_name",
            y="cancellation_rate",
            color="cancellation_rate",
            color_continuous_scale=["#0F766E", "#F59E0B"],
            title="Cancellation Rate by Hotel",
            labels={"hotel_name": "Hotel", "cancellation_rate": "Cancellation Rate (%)"}
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)

        st.markdown("### Business Observations & Recommendations")
        observation_col, recommendation_col = st.columns(2)

        with observation_col:
            st.markdown("**What the data shows**")
            st.markdown(
                f"- **{top_hotel['hotel_name']}** has the highest booking volume "
                f"({int(top_hotel['total_bookings']):,} bookings)."
            )
            st.markdown(
                f"- Overall cancellation rate for this period is **{cancellation_rate:.1f}%**."
            )
            if str(highest_cancel_hotel["hotel_name"]) != str(top_hotel["hotel_name"]):
                st.markdown(
                    f"- **{highest_cancel_hotel['hotel_name']}** has the highest "
                    f"cancellation rate ({float(highest_cancel_hotel['cancellation_rate']):.1f}%)."
                )

        with recommendation_col:
            st.markdown("**Suggested actions**")
            st.markdown(
                f"- Review booking capacity and guest services at **{top_hotel['hotel_name']}** "
                "to support its higher booking volume."
            )
            st.markdown(
                "- Review cancellation reasons and booking policies before making changes."
            )
            st.markdown(
                "- Compare cancellation patterns across reporting periods to identify "
                "whether the rate is improving or worsening."
            )

        st.caption(
            "Recommendations are planning suggestions based on the displayed sample data. "
            "The project uses synthetic demonstration records."
        )

        st.markdown("### Hotel Performance Details")
        st.dataframe(
            hotel_view.rename(columns={
                "hotel_name": "Hotel",
                "total_bookings": "Total Bookings",
                "cancelled_bookings": "Cancelled Bookings",
                "active_bookings": "Non-cancelled Bookings",
                "cancellation_rate": "Cancellation Rate (%)"
            }),
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# SALES PAGE
# --------------------------------------------------

elif page == "Sales Analytics":

    st.markdown("## 💴 Sales Analytics")
    st.caption("Product performance, sales volume, revenue trends and business observations.")

    if sales_df.empty:
        st.info("No sales records are available for the selected date range. Adjust the date filter to view sales analytics.")
    else:
        sales_view = sales_df.copy()
        sales_view["average_selling_price"] = (
            sales_view["total_revenue"] /
            sales_view["total_quantity"].replace(0, pd.NA)
        ).fillna(0)

        total_units = int(sales_view["total_quantity"].sum())
        top_revenue_product = sales_view.sort_values("total_revenue", ascending=False).iloc[0]
        top_volume_product = sales_view.sort_values("total_quantity", ascending=False).iloc[0]
        total_product_revenue = float(sales_view["total_revenue"].sum())
        average_revenue_per_unit = (
            total_product_revenue / total_units if total_units > 0 else 0
        )

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Sales Revenue", f"¥{total_revenue:,.0f}")
        k2.metric("Units Sold", f"{total_units:,}")
        k3.metric("Products Analysed", f"{len(sales_view):,}")
        k4.metric("Average Revenue per Unit", f"¥{average_revenue_per_unit:,.0f}")

        st.divider()
        left_chart, right_chart = st.columns(2)

        with left_chart:
            fig = px.bar(
                sales_view.sort_values("total_revenue", ascending=False),
                x="product",
                y="total_revenue",
                color="total_revenue",
                color_continuous_scale=["#164E63", "#2DD4BF"],
                title="Revenue by Product",
                labels={"product": "Product", "total_revenue": "Revenue (JPY)"}
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        with right_chart:
            fig = px.pie(
                sales_view,
                names="product",
                values="total_quantity",
                hole=0.58,
                title="Units Sold by Product"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        if not sales_trend.empty:
            fig = px.line(
                sales_trend,
                x="month",
                y="revenue",
                markers=True,
                title="Monthly Sales Revenue Trend",
                labels={"month": "Month", "revenue": "Revenue (JPY)"}
            )
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            st.plotly_chart(style_chart(fig), use_container_width=True)

        st.markdown("### Business Observations & Recommendations")
        observation_col, recommendation_col = st.columns(2)

        with observation_col:
            st.markdown("**What the data shows**")
            st.markdown(
                f"- **{top_revenue_product['product']}** generated the highest revenue "
                f"(¥{float(top_revenue_product['total_revenue']):,.0f})."
            )
            st.markdown(
                f"- **{top_volume_product['product']}** had the highest sales volume "
                f"({int(top_volume_product['total_quantity']):,} units)."
            )
            st.markdown(
                f"- Total quantity sold across the listed products was **{total_units:,} units**."
            )

        with recommendation_col:
            st.markdown("**Suggested actions**")
            st.markdown(
                f"- Review stock availability and product placement for **{top_revenue_product['product']}**, "
                "which contributes the most revenue in this period."
            )
            st.markdown(
                f"- Check demand and replenishment needs for **{top_volume_product['product']}**, "
                "which has the highest unit volume."
            )
            st.markdown(
                "- Compare monthly revenue trends before making pricing, promotion or inventory decisions."
            )

        st.caption(
            "Recommendations are planning suggestions based on the displayed sample data. "
            "The project uses synthetic demonstration records."
        )

        st.markdown("### Product Performance Details")
        st.dataframe(
            sales_view.rename(columns={
                "product": "Product",
                "total_quantity": "Units Sold",
                "total_revenue": "Revenue (JPY)",
                "average_selling_price": "Average Revenue per Unit (JPY)"
            }),
            use_container_width=True,
            hide_index=True
        )


# --------------------------------------------------
# AI BUSINESS INSIGHTS
# --------------------------------------------------

elif page == "AI Insights":

    st.markdown("## 🤖 AI-Powered Business Insights")
    st.caption(
        "Generate management observations from the filtered passenger, "
        "hotel and sales data."
    )

    st.info(
        f"Insights will use records from {start_date:%d %b %Y} "
        f"to {end_date:%d %b %Y}."
    )

    # Prepare only aggregated dashboard data for the language model.
    insight_data = {
        "reporting_period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "kpis": {
            "total_passengers": total_passengers,
            "total_hotel_bookings": total_bookings,
            "total_sales_revenue_jpy": total_revenue
        },
        "transportation_by_route": passenger_df.to_dict(orient="records"),
        "hotel_performance": hotel_df.to_dict(orient="records"),
        "sales_by_product": sales_df.to_dict(orient="records"),
        "monthly_passenger_trend": passenger_trend.to_dict(orient="records"),
        "monthly_sales_trend": sales_trend.to_dict(orient="records"),
        "booking_status": booking_status.to_dict(orient="records")
    }

    st.markdown("### Data summary")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Passengers", f"{total_passengers:,}")
    metric_col2.metric("Hotel bookings", f"{total_bookings:,}")
    metric_col3.metric("Sales revenue", f"¥{total_revenue:,.0f}")

    st.markdown("### Generate management insights")
    st.caption(
        "The AI receives aggregated results only. Customer names and "
        "individual booking records are not sent."
    )

    if st.button(
        "✨ Generate AI Business Insights",
        use_container_width=True,
        type="primary"
    ):
        # Read credentials from Streamlit secrets or environment variables.
        try:
            groq_api_key = st.secrets.get("GROQ_API_KEY", "")
            groq_model = st.secrets.get(
                "GROQ_MODEL",
                "llama-3.3-70b-versatile"
            )
        except Exception:
            groq_api_key = ""
            groq_model = "llama-3.3-70b-versatile"

        groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY", "")
        groq_model = os.getenv("GROQ_MODEL", groq_model)

        if not groq_api_key:
            st.warning(
                "Groq API key is not configured yet. Add GROQ_API_KEY "
                "to .streamlit/secrets.toml, then restart the application."
            )

            st.markdown("#### Data-based observations")
            if not passenger_df.empty:
                top_route = passenger_df.loc[
                    passenger_df["total_passengers"].idxmax()
                ]
                st.write(
                    f"- **Highest passenger traffic:** {top_route['route']} "
                    f"({int(top_route['total_passengers']):,} passengers)."
                )

            if not hotel_df.empty:
                top_hotel = hotel_df.loc[
                    hotel_df["cancelled_bookings"].idxmax()
                ]
                st.write(
                    f"- **Hotel with the most cancellations:** "
                    f"{top_hotel['hotel_name']} "
                    f"({int(top_hotel['cancelled_bookings']):,} cancellations)."
                )

            if not sales_df.empty:
                top_product = sales_df.loc[
                    sales_df["total_revenue"].idxmax()
                ]
                st.write(
                    f"- **Highest-revenue product:** {top_product['product']} "
                    f"(JPY {float(top_product['total_revenue']):,.0f})."
                )

            st.caption(
                "These are calculated observations, not LLM-generated advice."
            )

        else:
            try:
                from groq import Groq

                system_prompt = (
                    "You are a business intelligence analyst supporting a "
                    "transportation, tourism and hospitality company. "
                    "Use only the supplied aggregated data. Do not invent "
                    "figures, causes, trends or facts. Clearly distinguish "
                    "observed results from recommendations. If data is empty "
                    "or insufficient, say so. Provide: 1) key findings, "
                    "2) risks or operational issues, 3) practical management "
                    "recommendations, and 4) data limitations. Use concise "
                    "professional language. The dataset is synthetic sample "
                    "data for an academic portfolio project, not actual "
                    "Fuji Kyuko company data."
                )

                with st.spinner("Analysing the selected business data..."):
                    client = Groq(api_key=groq_api_key)
                    completion = client.chat.completions.create(
                        model=groq_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {
                                "role": "user",
                                "content": (
                                    "Analyse these aggregated dashboard results "
                                    "and produce management insights:\n"
                                    + pd.Series(insight_data).to_json(
                                        force_ascii=False,
                                        indent=2
                                    )
                                )
                            }
                        ],
                        temperature=0.2,
                        max_tokens=1200
                    )

                    ai_response = completion.choices[0].message.content

                st.markdown("### AI Analysis")
                st.markdown(ai_response)
                st.success(
                    f"Insights generated using Groq model: {groq_model}"
                )

            except ImportError:
                st.error(
                    "The Groq Python package is not installed. Run "
                    "`pip install groq` in your project virtual environment."
                )
            except Exception as error:
                st.error(f"AI insight generation failed: {error}")
                st.caption(
                    "Check your API key, model availability, internet "
                    "connection and Groq account limits."
                )

    st.divider()
    st.caption(
        "Decision support only. Validate findings against operational "
        "context before making business decisions."
    )


# --------------------------------------------------
# DATA EXPLORER
# --------------------------------------------------

elif page == "Data Explorer":

    st.markdown("## 📁 Data Explorer")

    st.caption("Explore records stored in the MySQL database.")

    tab1, tab2, tab3 = st.tabs([
        "Passengers",
        "Hotel Bookings",
        "Sales"
    ])

    with tab1:

        data = get_data("SELECT * FROM passengers LIMIT 1000")
        st.dataframe(data, use_container_width=True)

        st.download_button(
            "Download Passenger Data",
            data.to_csv(index=False),
            "passenger_data.csv",
            "text/csv"
        )

    with tab2:

        data = get_data("SELECT * FROM hotel_bookings LIMIT 500")
        st.dataframe(data, use_container_width=True)

        st.download_button(
            "Download Hotel Data",
            data.to_csv(index=False),
            "hotel_bookings.csv",
            "text/csv"
        )

    with tab3:

        data = get_data("SELECT * FROM sales LIMIT 1000")
        st.dataframe(data, use_container_width=True)

        st.download_button(
            "Download Sales Data",
            data.to_csv(index=False),
            "sales_data.csv",
            "text/csv"
        )


# --------------------------------------------------
# PDF BUSINESS REPORT
# --------------------------------------------------

st.divider()
st.markdown("## 📄 Download Business Report")
st.caption(
    "Generate a PDF summary using the currently selected date range "
    "and the filtered dashboard results."
)

try:
    pdf_report = create_pdf_report(
        start_date=start_date,
        end_date=end_date,
        total_passengers=total_passengers,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        passenger_df=passenger_df,
        hotel_df=hotel_df,
        sales_df=sales_df
    )

    st.download_button(
        label="⬇️ Download PDF Business Report",
        data=pdf_report,
        file_name=f"fuji_analytics_report_{start_date}_{end_date}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

except Exception as error:
    st.error(f"Unable to generate the PDF report: {error}")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#8492A6; padding:15px;">
        <b>FUJI ANALYTICS</b><br>
        Smart Tourism & Transportation Analytics System<br>
        Academic Portfolio Project | Synthetic Sample Data
    </div>
    """,
    unsafe_allow_html=True
)
