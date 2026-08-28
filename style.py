# style.py

import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        /* =========================================================
           FONTS
           ========================================================= */

        @import url(
            'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
        );


        /* =========================================================
           GLOBAL
           ========================================================= */

        html,
        body,
        [class*="css"] {
            font-family: "DM Sans", sans-serif;
        }

        .stApp {
            background:
                linear-gradient(
                    180deg,
                    #F8F6F0 0%,
                    #FFFFFF 32%,
                    #FFFFFF 100%
                ) !important;

            color: #17233C !important;
        }

        .stApp p,
        .stApp span,
        .stApp label,
        .stApp li,
        .stApp td,
        .stApp th {
            color: #17233C;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            color: #17233C !important;
        }


        /* =========================================================
           STREAMLIT CLEANUP
           ========================================================= */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        .block-container {
            max-width: 1080px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 4rem !important;
        }


        /* =========================================================
           LOGO
           ========================================================= */

        .stApp img {
            border-radius: 0 !important;
            box-shadow: none !important;
        }


        /* =========================================================
           HERO
           ========================================================= */

        .hero {
            text-align: center;
            padding: 10px 15px 30px 15px;
        }

        .hero-kicker {
            color: #B18A36 !important;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 12px;
        }

        .hero-title {
            font-family: "Playfair Display", serif !important;
            color: #17233C !important;
            font-size: 44px;
            font-weight: 700;
            line-height: 1.1;
            margin: 8px 0;
        }

        .hero-subtitle {
            color: #697589 !important;
            font-size: 16px;
            margin-top: 8px;
        }

        .gold-line {
            width: 70px;
            height: 4px;
            border-radius: 10px;
            background: linear-gradient(
                90deg,
                #A97D22,
                #D7B55B
            );
            margin: 18px auto 0 auto;
        }


        /* =========================================================
           INFO CARD
           ========================================================= */

        .info-card {
            background: #FFFFFF !important;
            border: 1px solid #E7E1D5 !important;
            border-radius: 18px;
            padding: 24px;
            margin: 5px 0 28px 0;
            text-align: center;

            box-shadow:
                0 8px 28px rgba(23, 35, 60, 0.06);
        }

        .info-icon {
            font-size: 30px;
            margin-bottom: 5px;
        }

        .info-title {
            color: #17233C !important;
            font-size: 19px;
            font-weight: 700;
        }

        .info-text {
            color: #697589 !important;
            font-size: 14px;
            line-height: 1.6;
            margin-top: 5px;
        }


        /* =========================================================
           SECTION TITLES
           ========================================================= */

        .section-title {
            font-family: "Playfair Display", serif !important;
            color: #17233C !important;
            font-size: 28px;
            font-weight: 700;
            margin-top: 12px;
            margin-bottom: 5px;
        }

        .section-description {
            color: #697589 !important;
            font-size: 14px;
            margin-bottom: 20px;
        }


        /* =========================================================
           FORM
           ========================================================= */

        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid #E3E6EB !important;
            border-radius: 20px !important;
            padding: 30px !important;

            box-shadow:
                0 12px 40px rgba(23, 35, 60, 0.07);
        }


        /* =========================================================
           TEXT INPUTS
           ========================================================= */

        .stTextInput label {
            color: #17233C !important;
            font-weight: 600 !important;
        }

        .stTextInput input {
            background-color: #FFFFFF !important;
            color: #17233C !important;
            caret-color: #17233C !important;

            border: 1px solid #CCD2DA !important;
            border-radius: 10px !important;

            min-height: 46px !important;
            font-size: 15px !important;
        }

        .stTextInput input:hover {
            border-color: #AEB6C2 !important;
        }

        .stTextInput input:focus {
            border-color: #B18A36 !important;

            box-shadow:
                0 0 0 2px rgba(177, 138, 54, 0.12) !important;
        }

        .stTextInput input::placeholder {
            color: #9099A8 !important;
            opacity: 1 !important;
        }


        /* =========================================================
           RADIO BUTTONS
           ========================================================= */

        .stRadio label {
            color: #17233C !important;
            font-weight: 600 !important;
        }

        .stRadio p {
            color: #17233C !important;
        }

        .stRadio [data-baseweb="radio"] {
            background: #FFFFFF !important;
            border: 1px solid #D9DEE5;
            border-radius: 10px;
            padding: 9px 13px;
        }


        /* =========================================================
           MULTISELECT
           ========================================================= */

        .stMultiSelect label {
            color: #17233C !important;
            font-weight: 600 !important;
        }

        .stMultiSelect [data-baseweb="select"] {
            background: #FFFFFF !important;
            border-radius: 10px !important;
        }

        .stMultiSelect input {
            color: #17233C !important;
        }

        .stMultiSelect [data-baseweb="tag"] {
            background: #17233C !important;
            border-radius: 7px !important;
        }

        .stMultiSelect [data-baseweb="tag"] span {
            color: #FFFFFF !important;
        }


        /* =========================================================
           SELECTBOX / DROPDOWN
           ========================================================= */

        .stSelectbox label {
            color: #17233C !important;
            font-weight: 600 !important;
        }

        .stSelectbox [data-baseweb="select"] {
            background: #FFFFFF !important;
            color: #17233C !important;
            border-radius: 10px !important;
        }


        /* =========================================================
           TABS
           ========================================================= */

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent !important;
            border-bottom: none !important;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab"] {
            background: #F0F2F5 !important;
            color: #17233C !important;

            border: 1px solid #DDE1E7 !important;
            border-radius: 10px !important;

            padding: 11px 16px !important;

            font-weight: 600 !important;
        }

        .stTabs [data-baseweb="tab"] * {
            color: #17233C !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: #17233C !important;
            color: #FFFFFF !important;

            border-color: #17233C !important;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] * {
            color: #FFFFFF !important;
        }


        /* =========================================================
           BUTTONS
           ========================================================= */

        .stButton > button {
            background:
                linear-gradient(
                    135deg,
                    #17233C,
                    #263A5D
                ) !important;

            color: #FFFFFF !important;

            border: none !important;
            border-radius: 11px !important;

            min-height: 50px !important;

            font-size: 15px !important;
            font-weight: 700 !important;

            transition: all 0.2s ease;
        }

        .stButton > button * {
            color: #FFFFFF !important;
        }

        .stButton > button:hover {
            background:
                linear-gradient(
                    135deg,
                    #243652,
                    #31486E
                ) !important;

            transform: translateY(-1px);

            box-shadow:
                0 8px 20px rgba(23, 35, 60, 0.20);
        }


        /* =========================================================
           SUBMIT BUTTON
           ========================================================= */

        .stFormSubmitButton > button {
            background:
                linear-gradient(
                    135deg,
                    #A97D22,
                    #D1AA50
                ) !important;

            color: #FFFFFF !important;

            border: none !important;
            border-radius: 12px !important;

            min-height: 56px !important;

            font-size: 17px !important;
            font-weight: 700 !important;

            margin-top: 15px;

            box-shadow:
                0 6px 18px rgba(169, 125, 34, 0.18);
        }

        .stFormSubmitButton > button * {
            color: #FFFFFF !important;
        }

        .stFormSubmitButton > button:hover {
            background:
                linear-gradient(
                    135deg,
                    #916B1D,
                    #BC943C
                ) !important;

            transform: translateY(-1px);

            box-shadow:
                0 9px 24px rgba(169, 125, 34, 0.25);
        }


        /* =========================================================
           DIVIDER
           ========================================================= */

        .soft-divider {
            height: 1px;
            background: #E7E3DA;
            margin: 28px 0;
        }


        /* =========================================================
           STATION HEADER
           ========================================================= */

        .station-header {
            background:
                linear-gradient(
                    135deg,
                    #F8F6F0,
                    #FFFFFF
                ) !important;

            border: 1px solid #E9E4DA;
            border-radius: 14px;

            padding: 14px 18px;
            margin-bottom: 16px;

            color: #17233C !important;
        }

        .station-header-title {
            color: #17233C !important;
            font-weight: 700;
            font-size: 18px;
        }

        .station-header-subtitle {
            color: #737D8D !important;
            font-size: 13px;
            margin-top: 3px;
        }


        /* =========================================================
           PUNCH CARD
           ========================================================= */

        .punch-card {
            background: #FFFFFF !important;

            border: 1px solid #E4E7EC;
            border-radius: 22px;

            padding: 40px 30px;

            text-align: center;

            box-shadow:
                0 12px 40px rgba(23, 35, 60, 0.08);

            margin: 15px 0 25px 0;
        }

        .punch-icon {
            font-size: 52px;
            margin-bottom: 10px;
        }

        .punch-title {
            font-family: "Playfair Display", serif !important;
            color: #17233C !important;
            font-size: 32px;
            font-weight: 700;
        }

        .punch-description {
            color: #697589 !important;
            font-size: 15px;
            margin-top: 7px;
            margin-bottom: 25px;
        }


        /* =========================================================
           ALERTS
           ========================================================= */

        [data-testid="stAlert"] {
            border-radius: 12px !important;
        }

        [data-testid="stAlert"] p {
            color: #17233C !important;
        }


        /* =========================================================
           EXPANDER
           ========================================================= */

        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E1E5EA !important;
            border-radius: 12px !important;
        }

        [data-testid="stExpander"] summary {
            color: #17233C !important;
        }

        [data-testid="stExpander"] summary * {
            color: #17233C !important;
        }


        /* =========================================================
           FOOTER
           ========================================================= */

        .footer {
            text-align: center;
            color: #7A8494 !important;
            font-size: 12px;
            padding: 35px 10px 5px 10px;
        }

        .footer-gold {
            color: #B18A36 !important;
        }


        /* =========================================================
           SUCCESS MESSAGE
           ========================================================= */

        .success-card {
            background:
                linear-gradient(
                    135deg,
                    #F0FFF5,
                    #FFFFFF
                );

            border: 1px solid #BFE5CB;
            border-radius: 16px;

            padding: 22px;

            text-align: center;

            margin-top: 20px;

            box-shadow:
                0 8px 24px rgba(40, 167, 69, 0.08);
        }

        .success-title {
            color: #176B35 !important;
            font-size: 20px;
            font-weight: 700;
        }

        .success-text {
            color: #4D6655 !important;
            font-size: 14px;
            margin-top: 5px;
        }


        /* =========================================================
           MOBILE
           ========================================================= */

        @media (max-width: 768px) {

            .block-container {
                padding:
                    0.8rem
                    0.8rem
                    3rem
                    0.8rem !important;
            }

            .hero {
                padding-top: 5px;
                padding-bottom: 20px;
            }

            .hero-title {
                font-size: 32px;
            }

            .hero-subtitle {
                font-size: 14px;
            }

            .info-card {
                padding: 20px 16px;
            }

            [data-testid="stForm"] {
                padding: 18px !important;
                border-radius: 16px !important;
            }

            .section-title {
                font-size: 24px;
            }

            .stTabs [data-baseweb="tab"] {
                padding: 9px 10px !important;
                font-size: 12px !important;
            }

            .punch-card {
                padding: 30px 18px;
            }

            .punch-title {
                font-size: 28px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )
