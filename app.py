import streamlit as st
import pandas as pd
import plotly.express as px
import random
import gdown
import io
from pathlib import Path

GOOGLE_DRIVE_FOLDER_ID = st.secrets["google_drive_folder_id"]


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="OSIRIS Audit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# FILE LOCATION
# =========================================================

BASE_DIR = Path(__file__).parent


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* =====================================================
       GENERAL PAGE
       ===================================================== */

    .stApp {
        background-color: #eaf3ff;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #5d7898;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Sidebar title */

    .sidebar-title {
            background: linear-gradient(
            180deg,
            #737d8d 0%,
            #343d4d 100%
        );

        color: white;

        padding: 18px 10px;

        text-align: center;

        font-size: 20px;
        font-weight: 700;

        margin: -16px -20px 20px -20px;
    }


    /* Navigation buttons */

    section[data-testid="stSidebar"] .stButton > button {

        background-color: transparent;

        border: none;

        color: white;

        text-align: center;

        font-size: 16px;

        font-weight: 500;

        width: 100%;

        padding: 8px 12px;

        border-radius: 7px;

        margin-bottom: 3px;

    }


    section[data-testid="stSidebar"] .stButton > button:hover {

        background-color: rgba(255,255,255,0.15);

        color: white;

        border: none;

    }


    /* Selected navigation button */

    section[data-testid="stSidebar"] .selected-nav button {

        background-color: rgba(0, 188, 212, 0.20);

        color: #00bcd4;

        font-weight: 700;

    }


    /* Sidebar section heading */

    .sidebar-section {

        color: white;

        font-size: 17px;

        font-weight: 500;

        margin-top: 28px;

        margin-bottom: 10px;

        text-align: center;

    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    .main-title {

        text-align: center;

        color: #26344a;

        font-size: 36px;

        font-weight: 700;

        margin-bottom: 3px;

    }


    .main-subtitle {

        text-align: center;

        color: #667085;

        font-size: 16px;

        margin-bottom: 25px;

    }


    /* =====================================================
       CHART TITLES
       ===================================================== */

    .chart-title {

        color: #26344a;

        font-size: 18px;

        font-weight: 600;

        text-align: center;

        margin-top: 8px;

        margin-bottom: 0px;

    }


    /* =====================================================
       WHITE CONTENT AREA
       ===================================================== */

    .content-card {

        background-color: white;

        border-radius: 8px;

        padding: 18px;

        margin-bottom: 20px;

    }


    /* =====================================================
       WORK PACKAGE TITLE
       ===================================================== */

    .wp-title {

        color: #26344a;

        font-size: 30px;

        font-weight: 700;

        margin-bottom: 5px;

    }


    /* =====================================================
       DOWNLOAD BUTTON
       ===================================================== */

    div.stDownloadButton > button {

        background-color: #10a957;

        color: white;

        border: none;

        border-radius: 20px;

        font-weight: 600;

        padding: 8px 18px;

    }


    div.stDownloadButton > button:hover {

        background-color: #0d914a;

        color: white;

    }


    /* =====================================================
       HIDE STREAMLIT BRANDING
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA FROM GOOGLE DRIVE
# =========================================================

@st.cache_data
def load_drive_folder():

    output_dir = "google_drive_data"

    gdown.download_folder(
        id=GOOGLE_DRIVE_FOLDER_ID,
        output=output_dir,
        quiet=True,
        use_cookies=False
    )

    return Path(output_dir)


# =========================================================
# LOAD SUMMARY
# =========================================================

@st.cache_data
def load_summary():

    folder = load_drive_folder()

    file_path = folder / "OSIRIS_Audit_Summary.xlsx"

    return pd.read_excel(
        file_path,
        sheet_name="summary"
    )


# =========================================================
# LOAD WORK PACKAGE
# =========================================================

@st.cache_data
def load_work_package(
    file_name,
    sheet_name
):

    folder = load_drive_folder()

    file_path = folder / file_name

    return pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "Summary"


def change_page(page_name):

    st.session_state.page = page_name


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        '<div class="sidebar-title">DASHBOARD</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # MAIN NAVIGATION
    # -----------------------------------------------------

    # HOME

    if st.session_state.page == "Summary":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "📊  Summary",
            key="summary_selected",
            use_container_width=True
        ):
            change_page("Summary")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "📊  Summary",
            key="summary",
            use_container_width=True
        ):
            change_page("Summary")


    # METHODOLOGY

    if st.session_state.page == "Methodology":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "🔬  Methodology",
            key="methodology_selected",
            use_container_width=True
        ):
            change_page("Methodology")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "🔬  Methodology",
            key="methodology",
            use_container_width=True
        ):
            change_page("Methodology")


    # ABOUT

    if st.session_state.page == "About":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "ℹ️  About",
            key="help_selected",
            use_container_width=True
        ):
            change_page("About")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "ℹ️  About",
            key="about",
            use_container_width=True
        ):
            change_page("About")


    # -----------------------------------------------------
    # DETAILED MILESTONES
    # -----------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">'
        'Detailed milestones'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # WORK PACKAGE 2
    # -----------------------------------------------------

    if st.session_state.page == "Work package 2":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "📋  Work package 2",
            key="wp2_selected",
            use_container_width=True
        ):
            change_page("Work package 2")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "📋  Work package 2",
            key="wp2",
            use_container_width=True
        ):
            change_page("Work package 2")


    # -----------------------------------------------------
    # WORK PACKAGE 3
    # -----------------------------------------------------

    if st.session_state.page == "Work package 3":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "📋  Work package 3",
            key="wp3_selected",
            use_container_width=True
        ):
            change_page("Work package 3")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "📋  Work package 3",
            key="wp3",
            use_container_width=True
        ):
            change_page("Work package 3")


    # -----------------------------------------------------
    # WORK PACKAGE 4
    # -----------------------------------------------------

    if st.session_state.page == "Work package 4":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "📋  Work package 4",
            key="wp4_selected",
            use_container_width=True
        ):
            change_page("Work package 4")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "📋  Work package 4",
            key="wp4",
            use_container_width=True
        ):
            change_page("Work package 4")


    # -----------------------------------------------------
    # WORK PACKAGE 5
    # -----------------------------------------------------

    if st.session_state.page == "Work package 5":

        st.markdown(
            '<div class="selected-nav">',
            unsafe_allow_html=True
        )

        if st.button(
            "📋  Work package 5",
            key="wp5_selected",
            use_container_width=True
        ):
            change_page("Work package 5")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        if st.button(
            "📋  Work package 5",
            key="wp5",
            use_container_width=True
        ):
            change_page("Work package 5")


# =========================================================
# CURRENT PAGE
# =========================================================

page = st.session_state.page


# =========================================================
# SUMMARY
# =========================================================

if page == "Summary":

    df = load_summary()


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        '<div class="main-title">'
        'OSIRIS Audit Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Overview of OSIRIS audit milestones'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2, col3 = st.columns(3)

    # -----------------------------------------------------
    # PREREGISTRATION
    # -----------------------------------------------------

    with col1:

        st.markdown(
            '<div class="chart-title">'
            'Preregistration'
            '</div>',
            unsafe_allow_html=True
        )

        temp = df.copy()

        # Keep only records with a preregistration year
        temp = temp[
            temp["year_preregistration"].notna()
        ].copy()

        # Convert year to numeric
        temp["year"] = pd.to_numeric(
            temp["year_preregistration"],
            errors="coerce"
        )

        # Remove anything that could not be interpreted as a year
        temp = temp[
            temp["year"].notna()
        ].copy()

        temp["year"] = temp["year"].astype(int)

        # Count preregistrations by year and WP
        chart_data = (
            temp
            .groupby(["year", "wp"])
            .size()
            .reset_index(name="count")
            .sort_values("year")
        )

        # Stacked area chart
        fig = px.area(
            chart_data,
            x="year",
            y="count",
            color="wp",
            color_discrete_map={
             "WP 2": "#1565C0",
             "WP 3": "#64B5F6",
             "WP 4": "#7E57C2",
             "WP 5": "#F2C94C"
    }
        )

        fig.update_layout(
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend_title="",
            xaxis=dict(
                title="",
                dtick=1
            ),
            yaxis=dict(
                title="Count",
                rangemode="tozero"
            ),
            font=dict(size=10),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )
    # -----------------------------------------------------
    # PROTOCOL
    # -----------------------------------------------------

    with col2:

        st.markdown(
            '<div class="chart-title">'
            'Availability of protocol'
            '</div>',
            unsafe_allow_html=True
        )

        temp = df.copy()

        temp["status"] = (
            temp["protocol_11"]
            .fillna("Not recorded")
            .astype(str)
            .str.title()
        )

        chart_data = (
            temp
            .groupby(["status"])
            .size()
            .reset_index(name="count")
        )

        fig = px.pie(
            chart_data,
            names="status",
            values="count",
            hole=0.55,
            color="status",
            color_discrete_map={
            "Yes": "#1565C0",
            "No": "#EB7F91D0"
    }
        )

        fig.update_layout(
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="white",
            font=dict(size=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


    # -----------------------------------------------------
    # DATA AND CODE
    # -----------------------------------------------------

    with col3:

        st.markdown(
            '<div class="chart-title">'
            'Data & code sharing'
            '</div>',
            unsafe_allow_html=True
        )

        # Clean values
        data_status = (
            df["data_18"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        code_status = (
            df["code_7"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # Statuses from the Summary Excel
        statuses = [
            "yes",
            "partially",
            "planned",
            "no"
        ]

        # Count each status
        chart_data = pd.DataFrame({
            "status": statuses,

            "Data sharing": [
                (data_status == status).sum()
                for status in statuses
            ],

            "Code sharing": [
                (code_status == status).sum()
                for status in statuses
            ]
        })

        # Bar chart
        fig = px.bar(
            chart_data,
            x="status",
            y=[
                "Data sharing",
                "Code sharing"
            ],
            barmode="group"
        )

        fig.update_layout(
            height=280,

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),

            plot_bgcolor="white",
            paper_bgcolor="white",

            legend_title="",

            xaxis=dict(
                title=""
            ),

            yaxis=dict(
                title="Count",
                rangemode="tozero"
            ),

            font=dict(size=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # =====================================================
    # ROW 2
    # =====================================================

    col4, col5, col6 = st.columns(3)


    # -----------------------------------------------------
    # REPORTING TRANSPARENCY
    # -----------------------------------------------------

    with col4:

        st.markdown(
            '<div class="chart-title">'
            'Reporting guidelines'
            '</div>',
            unsafe_allow_html=True
        )

        chart_data = (
            df["reporting guideline_16"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        chart_data.columns = [
            "guideline",
            "count"
        ]

        fig = px.pie(
            chart_data,
            names="guideline",
            values="count"
        )

        fig.update_layout(
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="white",
            font=dict(size=9)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


    # -----------------------------------------------------
    # PREPRINT
    # -----------------------------------------------------

    with col5:

        st.markdown(
            '<div class="chart-title">'
            'Preprint'
            '</div>',
            unsafe_allow_html=True
        )

        temp = df.copy()

        temp["status"] = (
            temp["preprint_21"]
            .fillna("Not recorded")
            .astype(str)
            .str.title()
        )

        temp["wp"] = pd.Categorical(
    temp["wp"],
    categories=["WP 2", "WP 3", "WP 4", "WP 5"],
    ordered=True
)

        chart_data = (
            temp
            .groupby(["wp", "status"])
            .size()
            .reset_index(name="count")
        )

        fig = px.bar(
            chart_data,
            x="wp",
            y="count",
            color="status",
                labels={
        "wp": "Work package",
        "count": "Count",
        "status": "Status"
    },
            barmode="stack",
                color_discrete_map={
        "No": "#DA7F9D",
        "Yes": "#1A84DC",
        "Planned": "#F2C94C"
    }
        )

        fig.update_layout(
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            legend_title="",
            font=dict(size=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )


    # -----------------------------------------------------
    # OPEN ACCESS JOURNAL
    # -----------------------------------------------------

    with col6:

        st.markdown(
            '<div class="chart-title">'
            'Open access journal'
            '</div>',
            unsafe_allow_html=True
        )

        chart_data = (
            df["Open access"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        chart_data.columns = [
            "journal",
            "count"
        ]

        journals = chart_data["journal"].tolist()

        random.seed(42)

        positions = []

        for i in range(len(journals)):

            col = i % 3
            row = i // 3

            x = -1.2 + (col * 1.2) + random.uniform(-0.2, 0.2)
            y = 2.0 - (row * 1.0) + random.uniform(-0.15, 0.15)

            positions.append((x, y))

        bubble_data = pd.DataFrame({
            "journal": journals,
            "x": [
                p[0]
                for p in positions[:len(journals)]
            ],
            "y": [
                p[1]
                for p in positions[:len(journals)]
            ]
        })

        fig = px.scatter(
            bubble_data,
            x="x",
            y="y",
            text="journal",
            color="journal"
        )

        fig.update_traces(
            mode="markers+text",
            marker=dict(
                size=85,
                line=dict(
                    width=2,
                    color="white"
                )
            ),
            textposition="middle center",
            textfont=dict(
                size=12,
                color="black")
        )

        fig.update_layout(
            height=280,
            margin=dict(
                l=5,
                r=5,
                t=5,
                b=5
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            xaxis=dict(
                visible=False,
                range=[-2, 2]
            ),
            yaxis=dict(
                visible=False,
                range=[-0.6, 2.6],
                scaleanchor="x",
                scaleratio=1
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

# =========================================================
# METHODOLOGY
# =========================================================

elif page == "Methodology":

    st.markdown(
        '<div class="main-title">Methodology</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'OSIRIS Audit Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        In OSIRIS we are developing a procedure for auditing open science and reproducibility practices for research projects. 
        
        #### The aim of this audit is twofold:  
        1. **Audit ourselves** to see how open and reproducible our own practices and outputs are, and which challenges we encounter
        2. **Create an audit protocol** that is usable for other projects.

        After a first round of audits in 2025, we have revised this audit form. The information submitted last year is still included in this file.
        
        For detail, see **Detailed milestones** page.


"""
    )

# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.markdown(
        '<div class="main-title">About</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'OSIRIS Audit Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        ### OSF project proposal

        The project proposal and related information can be accessed through the OSF project page:
        [OSF project proposal](https://doi.org/10.17605/OSF.IO/8NYKE).

        ### OSIRIS

        For more information about the OSIRIS project, visit the official OSIRIS website: 
        [OSIRIS website](https://osiris4r.eu/).

        ### Dashboard

        Technical problem or error with this dahsboard?
        Contact us by [email](mailto:a.p.m.dewi@amsterdamumc.nl).
        """
    )

    st.markdown(
        '<br>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.link_button(
            "📄  View OSF project",
            "https://osf.io/8nyke/overview",
            use_container_width=True
        )

    with col2:

        st.link_button(
            "🌐  Visit OSIRIS website",
            "https://osiris4r.eu/",
            use_container_width=True
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# WORK PACKAGE PAGES
# =========================================================

elif page.startswith("Work package"):

    wp_number = page.split()[-1]


    # -----------------------------------------------------
    # FILE MAPPING
    # -----------------------------------------------------

    wp_files = {

        "2": {
            "file": "OSIRIS_Audit_WP2_2026.xlsx",
            "sheet": "WP2"
        },

        "3": {
            "file": "OSIRIS_Audit_WP3_2026.xlsx",
            "sheet": "WP3"
        },

        "4": {
            "file": "OSIRIS_Audit_WP4_2026.xlsx",
            "sheet": "WP4"
        },

        "5": {
            "file": "OSIRIS_Audit_WP5_2026.xlsx",
            "sheet": "WP5"
        }

    }


    selected = wp_files[wp_number]


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    st.markdown(
        f'<div class="wp-title">'
        f'Work package {wp_number}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subtitle">'
        'Audit data'
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # LOAD EXCEL
    # -----------------------------------------------------

    try:

        wp_df = load_work_package(
        selected["file"],
        selected["sheet"]
    )

    except Exception as e:

        st.error(
        f"Could not load Work Package {wp_number}."
    )

        st.code(str(e))

        st.stop()


    # -----------------------------------------------------
    # SEARCH + DOWNLOAD
    # -----------------------------------------------------

    search_col, spacer, download_col = st.columns(
    [4, 1, 1]
)


    with search_col:

        search = st.text_input(
        "🔍 Search",
        placeholder="Search the table...",
        label_visibility="collapsed"
    )


    with download_col:

        xlsx_data = io.BytesIO()

    with pd.ExcelWriter(xlsx_data, engine="openpyxl") as writer:
        wp_df.to_excel(
            writer,
            index=False,
            sheet_name="Data"
        )

    xlsx_data.seek(0)

    st.download_button(
        "⬇ Download Excel",
        data=xlsx_data,
        file_name=f"OSIRIS_WP{wp_number}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search.strip():

        search_text = search.strip()

        mask = (
            wp_df
            .astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search_text,
                    case=False,
                    na=False,
                    regex=False
                ).any(),
                axis=1
            )
        )

        display_df = wp_df.loc[mask].copy()

    else:

        display_df = wp_df.copy()


    # -----------------------------------------------------
    # COLUMN CONFIGURATION
    #
    # "auto" lets Streamlit size columns according
    # to their content where possible.
    # -----------------------------------------------------

    column_config = {}

    for column in display_df.columns:

        column_config[column] = st.column_config.Column(
            width="auto"
        )


    # -----------------------------------------------------
    # DISPLAY TABLE
    # -----------------------------------------------------

    st.dataframe(
        display_df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        height=650
    )


    # -----------------------------------------------------
    # RECORD COUNT
    # -----------------------------------------------------

    st.caption(
        f"Showing {len(display_df):,} of "
        f"{len(wp_df):,} records"
    )