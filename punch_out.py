"""
St. Anthony Coptic Orthodox Church
Volunteer Punch Out App
QR Code Punch Out System
"""

import logging
import random
import re
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

PUNCH_IN_SHEET = "Punch In"
PUNCH_OUT_SHEET = "Punch Out"
HOURS_SHEET = "Volunteer Hours"

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
# VOLUNTEER VERSES
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
# HELPER FUNCTIONS
# ============================================================

def normalize_name(value):
    """
    Makes name matching case-insensitive
    and removes extra spaces.
    """

    if value is None:
        return ""

    value = str(value).strip().lower()

    # Replace multiple spaces with one
    value = re.sub(r"\s+", " ", value)

    return value


def normalize_phone(value):
    """
    Removes all phone formatting.

    Examples:

    (732) 555-1234
    732-555-1234
    732.555.1234
    732 555 1234

    All become:

    7325551234
    """

    if value is None:
        return ""

    return re.sub(
        r"\D",
        "",
        str(value)
    )


def get_record_value(record, possible_names):
    """
    Finds a value even if the Google Sheet
    column has slightly different capitalization
    or spacing.
    """

    normalized_columns = {}

    for key in record.keys():

        normalized_key = re.sub(
            r"[^a-z0-9]",
            "",
            str(key).lower()
        )

        normalized_columns[
            normalized_key
        ] = key

    for possible_name in possible_names:

        normalized_name = re.sub(
            r"[^a-z0-9]",
            "",
            possible_name.lower()
        )

        if normalized_name in normalized_columns:

            actual_key = normalized_columns[
                normalized_name
            ]

            return record.get(
                actual_key,
                ""
            )

    return ""


def parse_datetime(value):
    """
    Converts the Punch In timestamp into
    a timezone-aware datetime.
    """

    if not value:
        return None

    value = str(value).strip()

    formats = [

        "%Y-%m-%d %I:%M:%S %p",

        "%Y-%m-%d %I:%M %p",

        "%Y-%m-%d %H:%M:%S",

        "%Y-%m-%d %H:%M",

        "%m/%d/%Y %I:%M:%S %p",

        "%m/%d/%Y %I:%M %p",

        "%m/%d/%Y %H:%M:%S",

        "%m/%d/%Y %H:%M"
    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).replace(
                tzinfo=TIME_ZONE
            )

        except ValueError:

            continue

    return None


# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================

SHEETS_ENABLED = False

punch_in_sheet = None
punch_out_sheet = None
hours_sheet = None

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

    client = gspread.authorize(
        credentials
    )

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    sheet_names = [
        worksheet.title
        for worksheet in spreadsheet.worksheets()
    ]

    required_sheets = [
        PUNCH_IN_SHEET,
        PUNCH_OUT_SHEET,
        HOURS_SHEET
    ]

    missing_sheets = [
        sheet
        for sheet in required_sheets
        if sheet not in sheet_names
    ]

    if missing_sheets:

        raise Exception(
            "Missing Google Sheet tab(s): "
            + ", ".join(missing_sheets)
            + ". Available sheets: "
            + ", ".join(sheet_names)
        )

    punch_in_sheet = spreadsheet.worksheet(
        PUNCH_IN_SHEET
    )

    punch_out_sheet = spreadsheet.worksheet(
        PUNCH_OUT_SHEET
    )

    hours_sheet = spreadsheet.worksheet(
        HOURS_SHEET
    )

    SHEETS_ENABLED = True

    logger.info(
        "Google Sheets connected successfully."
    )


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
# CONNECTION ERROR
# ============================================================

if not SHEETS_ENABLED:

    st.error(
        "Google Sheets is not connected. "
        "Your punch out cannot be saved."
    )

    with st.expander(
        "Show Google Sheets error"
    ):

        st.code(
            sheets_error
            or "Unknown Google Sheets error."
        )


# ============================================================
# PUNCH OUT INTRODUCTION
# ============================================================

st.divider()

st.subheader(
    "🔴 Volunteer Punch Out"
)

st.write(
    "Enter your full name and phone number "
    "to complete your volunteer service."
)


# ============================================================
# NAME
# ============================================================

name = st.text_input(
    "Full Name",
    placeholder="Enter your full name",
    key="punch_out_name"
)


# ============================================================
# PHONE
# ============================================================

phone = st.text_input(
    "Cell Phone",
    placeholder="Enter your cell phone number",
    key="punch_out_phone"
)


# ============================================================
# PUNCH OUT BUTTON
# ============================================================

if st.button(
    "🔴 Punch Out Now",
    key="punch_out_button",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATE NAME
    # --------------------------------------------------------

    if not name.strip():

        st.warning(
            "Please enter your full name."
        )

    # --------------------------------------------------------
    # VALIDATE PHONE
    # --------------------------------------------------------

    elif not phone.strip():

        st.warning(
            "Please enter your cell phone number."
        )

    # --------------------------------------------------------
    # CHECK GOOGLE SHEETS
    # --------------------------------------------------------

    elif not SHEETS_ENABLED:

        st.error(
            "Your punch out could not be saved right now. "
            "Please contact the volunteer coordinator."
        )

        with st.expander(
            "Show Google Sheets error"
        ):

            st.code(
                sheets_error
                or "Unknown Google Sheets error."
            )

    else:

        clean_name = name.strip()
        clean_phone = phone.strip()

        normalized_user_name = normalize_name(
            clean_name
        )

        normalized_user_phone = normalize_phone(
            clean_phone
        )

        # ====================================================
        # CURRENT NEW JERSEY TIME
        # ====================================================

        punch_out_datetime = datetime.now(
            TIME_ZONE
        )

        punch_out_timestamp = punch_out_datetime.strftime(
            "%Y-%m-%d %I:%M:%S %p"
        )

        try:

            # =================================================
            # GET PUNCH IN RECORDS
            # =================================================

            punch_in_records = (
                punch_in_sheet.get_all_records()
            )

            matching_punch_ins = []

            # =================================================
            # FIND MATCH
            # =================================================

            for record in punch_in_records:

                # ---------------------------------------------
                # GET NAME
                # ---------------------------------------------

                record_name = get_record_value(
                    record,
                    [
                        "Name",
                        "Full Name",
                        "Volunteer Name"
                    ]
                )

                # ---------------------------------------------
                # GET PHONE
                # ---------------------------------------------

                record_phone = get_record_value(
                    record,
                    [
                        "Phone",
                        "Cell Phone",
                        "CellPhone",
                        "Phone Number"
                    ]
                )

                # ---------------------------------------------
                # GET STATUS
                # ---------------------------------------------

                record_status = get_record_value(
                    record,
                    [
                        "Status"
                    ]
                )

                # ---------------------------------------------
                # GET DATE/TIME
                # ---------------------------------------------

                record_datetime = get_record_value(
                    record,
                    [
                        "Date & Time",
                        "Date and Time",
                        "Timestamp",
                        "Time",
                        "Date/Time"
                    ]
                )

                # ---------------------------------------------
                # NORMALIZE
                # ---------------------------------------------

                normalized_record_name = normalize_name(
                    record_name
                )

                normalized_record_phone = normalize_phone(
                    record_phone
                )

                normalized_status = (
                    str(record_status)
                    .strip()
                    .lower()
                )

                # ---------------------------------------------
                # MATCH NAME + PHONE
                # ---------------------------------------------

                name_matches = (
                    normalized_record_name
                    == normalized_user_name
                )

                phone_matches = (
                    normalized_record_phone
                    == normalized_user_phone
                )

                status_matches = (
                    normalized_status == "in"
                )

                # ---------------------------------------------
                # SAVE MATCH
                # ---------------------------------------------

                if (
                    name_matches
                    and phone_matches
                    and status_matches
                    and record_datetime
                ):

                    parsed_time = parse_datetime(
                        record_datetime
                    )

                    if parsed_time:

                        matching_punch_ins.append(
                            (
                                parsed_time,
                                str(record_datetime)
                            )
                        )

            # =================================================
            # NO MATCH
            # =================================================

            if not matching_punch_ins:

                st.error(
                    "We could not find a matching Punch In "
                    "for this name and phone number."
                )

                st.info(
                    "Name matching is not case-sensitive, "
                    "and phone formatting does not matter."
                )

            else:

                # =================================================
                # FIND LATEST PUNCH IN
                # =================================================

                matching_punch_ins.sort(
                    key=lambda x: x[0]
                )

                punch_in_datetime = (
                    matching_punch_ins[-1][0]
                )

                # =================================================
                # CALCULATE DURATION
                # =================================================

                duration = (
                    punch_out_datetime
                    - punch_in_datetime
                )

                total_seconds = int(
                    duration.total_seconds()
                )

                # =================================================
                # INVALID DURATION
                # =================================================

                if total_seconds <= 0:

                    raise Exception(
                        "The Punch Out time is earlier than "
                        "the Punch In time."
                    )

                # =================================================
                # HOURS / MINUTES
                # =================================================

                total_hours = (
                    total_seconds // 3600
                )

                remaining_seconds = (
                    total_seconds % 3600
                )

                total_minutes = (
                    remaining_seconds // 60
                )

                decimal_hours = round(
                    total_seconds / 3600,
                    2
                )

                total_time = (
                    f"{total_hours}:"
                    f"{total_minutes:02d}"
                )

                # =================================================
                # SAVE PUNCH OUT
                # =================================================

                punch_out_sheet.append_row(
                    [
                        clean_name,
                        clean_phone,
                        "Out",
                        punch_out_timestamp
                    ],
                    value_input_option="USER_ENTERED"
                )

                # =================================================
                # SAVE VOLUNTEER HOURS
                # =================================================

                hours_sheet.append_row(
                    [
                        clean_name,
                        clean_phone,
                        punch_in_datetime.strftime(
                            "%Y-%m-%d %I:%M:%S %p"
                        ),
                        punch_out_timestamp,
                        total_time,
                        decimal_hours,
                        "Complete"
                    ],
                    value_input_option="USER_ENTERED"
                )

                logger.info(
                    "Punch OUT saved for %s",
                    clean_name
                )

                # =================================================
                # SUCCESS
                # =================================================

                st.success(
                    f"🎉 Great job, {clean_name}! "
                    "You've successfully punched out."
                )

                st.info(
                    f"🟢 Punch In: "
                    f"{punch_in_datetime.strftime('%I:%M %p')}"
                )

                st.info(
                    f"🔴 Punch Out: "
                    f"{punch_out_datetime.strftime('%I:%M %p')}"
                )

                st.success(
                    f"⏱️ Total Volunteer Time: "
                    f"{total_time}"
                )

                st.info(
                    f"📊 Total Hours: "
                    f"{decimal_hours:.2f}"
                )

                st.info(
                    "📖 "
                    + random.choice(
                        volunteer_verses
                    )
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

                st.code(
                    str(e)
                )


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
    "4. Your punch-out time and total hours "
    "will be recorded automatically."
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