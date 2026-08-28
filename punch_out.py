

"""
St. Anthony Coptic Orthodox Church
Volunteer Punch Out App
QR Code Punch Out System
"""

import logging
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

from style import apply_styles


# ============================================================
# GOOGLE SHEETS SETTINGS
# ============================================================

SPREADSHEET_ID = "1hCAZ77PfCl-OoC6nra_HJTG_m8tAirrDpb9lrt3ueE0"
PUNCH_OUT_SHEET = "Punch Out"

# New Jersey time
TIME_ZONE = ZoneInfo("America/New_York")


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="St. Anthony Volunteer - Punch Out",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# STYLE
# ============================================================

apply_styles()


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# VERSES
# ============================================================

volunteer_verses = [
    (
        "Each of you should use whatever gift you have received "
        "to serve others, as faithful stewards of God's grace. "
        "— 1 Peter 4:10"
    ),
    (
        "Whatever you do, work at it with all your heart, "
        "as working for the Lord, not for human masters. "
        "— Colossians 3:23"
    ),
    (
        "Serve wholeheartedly, as if you were serving the Lord, "
        "not people. — Ephesians 6:7"
    ),
    (
        "The greatest among you will be your servant. "
        "— Matthew 23:11"
    ),
    (
        "Carry each other's burdens, and in this way you will "
        "fulfill the law of Christ. — Galatians 6:2"
    )
]


# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================

SHEETS_ENABLED = False
punch_out_sheet = None
sheets_error = None

try:

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    if "gcp_service_account" not in st.secrets:

        raise Exception(
            "The gcp_service_account section was not found "
            "in Streamlit secrets."
        )

    service_account_info = dict(
        st.secrets["gcp_service_account"]
    )

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=scope
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet_names = [
        worksheet.title
        for worksheet in spreadsheet.worksheets()
    ]

    if PUNCH_OUT_SHEET not in sheet_names:

        raise Exception(
            f"The sheet '{PUNCH_OUT_SHEET}' was not found. "
            f"Available sheets: {sheet_names}"
        )

    punch_out_sheet = spreadsheet.worksheet(
        PUNCH_OUT_SHEET
    )

    SHEETS_ENABLED = True

except Exception as e:

    SHEETS_ENABLED = False
    sheets_error = str(e)

    logger.error(
        "Google Sheets connection failed: %s",
        e
    )


# ============================================================
# HEADER
# ============================================================

try:

    st.image(
        "stanthonylogo.png",
        width=120
    )

except Exception:

    st.write("⛪")


st.markdown(
    "### St. Anthony Coptic Orthodox Church"
)

st.title(
    "Volunteer Community"
)

st.write(
    "Serve with joy. Connect with community."
)


# ============================================================
# PUNCH OUT
# ============================================================

st.divider()

st.subheader(
    "🔴 Volunteer Punch Out"
)

st.write(
    "Enter your full name and phone number "
    "to complete your volunteer service."
)


name = st.text_input(
    "Full Name*",
    placeholder="Enter your full name",
    key="punch_out_name"
)


phone = st.text_input(
    "Cell Phone*",
    placeholder="Enter your cell phone number",
    key="punch_out_phone"
)


# ============================================================
# BUTTON
# ============================================================

if st.button(
    "🔴 Punch Out Now",
    key="punch_out_button",
    use_container_width=True
):

    if not name.strip():

        st.warning(
            "Please enter your full name."
        )

    elif not phone.strip():

        st.warning(
            "Please enter your cell phone number."
        )

    elif not SHEETS_ENABLED:

        st.error(
            "Your punch out could not be saved right now. "
            "Please contact the volunteer coordinator."
        )

        with st.expander(
            "Show Google Sheets error"
        ):

            st.code(
                sheets_error or "Unknown Google Sheets error."
            )

    else:

        clean_name = name.strip()
        clean_phone = phone.strip()

        timestamp = datetime.now(
            TIME_ZONE
        ).strftime(
            "%Y-%m-%d %I:%M %p"
        )

        try:

            punch_out_sheet.append_row(
                [
                    clean_name,
                    clean_phone,
                    "Out",
                    timestamp
                ],
                value_input_option="USER_ENTERED"
            )

            logger.info(
                "Punch OUT saved: %s - %s - %s",
                clean_name,
                clean_phone,
                timestamp
            )

            st.success(
                f"🎉 Great job, {clean_name}! "
                "You've successfully punched out."
            )

            st.info(
                f"🕐 Punch Out Time: {timestamp}"
            )

            st.info(
                "📖 " +
                random.choice(volunteer_verses)
            )

            st.subheader(
                "🌟 Thank You for Your Service!"
            )

            st.write(
                "Your dedication and time have made "
                "a real difference today. May God bless "
                "you for your generous heart and "
                "willing spirit."
            )

            st.subheader(
                "📋 Shift Complete"
            )

            st.write(
                "Your volunteer punch has been recorded. "
                "Thank you for being part of the "
                "St. Anthony community!"
            )

        except Exception as e:

            logger.error(
                "Punch OUT failed: %s",
                e
            )

            st.error(
                "Your punch out could not be saved right now. "
                "Please contact the volunteer coordinator."
            )

            with st.expander(
                "Show Google Sheets error"
            ):

                st.code(str(e))


# ============================================================
# INSTRUCTIONS
# ============================================================

st.divider()

st.subheader(
    "📱 How to Use"
)

st.write(
    "1. Enter your full name."
)

st.write(
    "2. Enter your cell phone number."
)

st.write(
    "3. Click Punch Out Now to complete your shift."
)

st.write(
    "4. Your punch-out time will be recorded "
    "in Google Sheets."
)


# ============================================================
# WHAT'S NEXT
# ============================================================

st.subheader(
    "🔗 What's Next?"
)

col1, col2 = st.columns(2)

with col1:

    st.info(
        "🟢 **Volunteer Again?**\n\n"
        "Use the Punch In QR code when "
        "you begin your next volunteer shift."
    )

with col2:

    st.success(
        "🙏 **Thank You!**\n\n"
        "Thank you for serving our community "
        "with love and dedication."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.write(
    "🏛️ St. Anthony Coptic Orthodox Church "
    "Volunteer System"
)

st.caption(
    "Thank you for serving with love and dedication ☦️"
)

st.caption(
    '"Whatever you do, work at it with all your heart, '
    'as working for the Lord." — Colossians 3:23'
)

