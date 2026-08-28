
"""
St. Anthony Coptic Orthodox Church
Volunteer Registration System
"""

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
REGISTRATION_SHEET = "Registration"

# New Jersey uses America/New_York
TIME_ZONE = ZoneInfo("America/New_York")


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="St. Anthony Volunteer",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# STYLE
# ============================================================

apply_styles()


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
# GOOGLE SHEETS CONNECTION
# ============================================================

SHEETS_ENABLED = False
reg_sheet = None
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

    if REGISTRATION_SHEET not in sheet_names:

        raise Exception(
            f"'{REGISTRATION_SHEET}' was not found. "
            f"Available sheets: {sheet_names}"
        )

    reg_sheet = spreadsheet.worksheet(
        REGISTRATION_SHEET
    )

    SHEETS_ENABLED = True

except Exception as e:

    SHEETS_ENABLED = False
    sheets_error = str(e)


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
        "Your registration cannot be saved."
    )

    with st.expander("Show Google Sheets error"):

        st.code(
            sheets_error or "Unknown Google Sheets error."
        )


# ============================================================
# THANK YOU
# ============================================================

st.info(
    "🙏 Thank You for Volunteering\n\n"
    "Complete the form below to choose your "
    "volunteer station and preferred times."
)


# ============================================================
# REGISTRATION
# ============================================================

st.header(
    "Volunteer Registration"
)

st.write(
    "Please provide your information and select "
    "where you would like to serve."
)


# ============================================================
# STATIONS
# ============================================================

STATION_NAMES = [
    "Station 1 - Prizes/Kids Games",
    "Station 2 - Cosmetology",
    "Station 3 - Inflatables",
    "Station 4 - Basketball",
    "Station 5 - Snacking"
]


def create_station(number, station_name):

    st.subheader(station_name)

    st.caption(
        "Choose your available volunteer times."
    )

    day_tabs = st.tabs(
        [
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    with day_tabs[0]:

        friday = st.multiselect(
            "Friday Availability",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key=f"station_{number}_friday"
        )

    with day_tabs[1]:

        saturday = st.multiselect(
            "Saturday Availability",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key=f"station_{number}_saturday"
        )

    with day_tabs[2]:

        sunday = st.multiselect(
            "Sunday Availability",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key=f"station_{number}_sunday"
        )

    return {
        "friday": friday,
        "saturday": saturday,
        "sunday": sunday
    }


# ============================================================
# REGISTRATION FORM
# ============================================================

with st.form("registration_form"):

    st.subheader(
        "Personal Information"
    )

    st.caption(
        "First Name, Last Name, and Cell Phone are required."
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        first_name = st.text_input(
            "First Name*",
            max_chars=50,
            placeholder="First name"
        )

    with col2:

        last_name = st.text_input(
            "Last Name*",
            max_chars=50,
            placeholder="Last name"
        )

    col3, col4 = st.columns(
        2,
        gap="large"
    )

    with col3:

        cell_phone = st.text_input(
            "Cell Phone*",
            placeholder="(555) 555-5555"
        )

    with col4:

        email = st.text_input(
            "Email",
            placeholder="you@example.com"
        )

    age = st.radio(
        "Age",
        [
            "14-18",
            "18+"
        ],
        horizontal=True,
        key="age"
    )

    st.divider()

    st.header(
        "Choose Your Station"
    )

    st.write(
        "Select a station and choose the times "
        "that work for you. Station selection is optional."
    )

    station_tabs = st.tabs(
        [
            "🎁 Prizes",
            "💄 Cosmetology",
            "🎈 Inflatables",
            "🏀 Basketball",
            "🍿 Snacking"
        ]
    )

    station_data = {}

    with station_tabs[0]:

        station_data[
            STATION_NAMES[0]
        ] = create_station(
            1,
            STATION_NAMES[0]
        )

    with station_tabs[1]:

        station_data[
            STATION_NAMES[1]
        ] = create_station(
            2,
            STATION_NAMES[1]
        )

    with station_tabs[2]:

        station_data[
            STATION_NAMES[2]
        ] = create_station(
            3,
            STATION_NAMES[2]
        )

    with station_tabs[3]:

        station_data[
            STATION_NAMES[3]
        ] = create_station(
            4,
            STATION_NAMES[3]
        )

    with station_tabs[4]:

        station_data[
            STATION_NAMES[4]
        ] = create_station(
            5,
            STATION_NAMES[4]
        )

    st.divider()

    st.subheader(
        "Confirm Your Station"
    )

    st.caption(
        "Station selection is optional."
    )

    chosen_station = st.radio(
        "Which station are you signing up for?",
        STATION_NAMES,
        index=None,
        key="chosen_station"
    )

    submitted = st.form_submit_button(
        "🙏 Submit Volunteer Registration",
        use_container_width=True
    )


# ============================================================
# SAVE REGISTRATION
# ============================================================

if submitted:

    if (
        not first_name.strip()
        or not last_name.strip()
        or not cell_phone.strip()
    ):

        st.error(
            "Please complete First Name, Last Name, "
            "and Cell Phone."
        )

    elif not SHEETS_ENABLED:

        st.error(
            "Google Sheets is not connected. "
            "Your registration cannot be saved."
        )

        with st.expander(
            "Show Google Sheets error"
        ):

            st.code(
                sheets_error or "Unknown Google Sheets error."
            )

    else:

        clean_first_name = first_name.strip()
        clean_last_name = last_name.strip()
        clean_phone = cell_phone.strip()
        clean_email = email.strip()

        selected_station = (
            chosen_station
            if chosen_station
            else "Not Selected"
        )

        selected = station_data.get(
            chosen_station,
            {
                "friday": [],
                "saturday": [],
                "sunday": []
            }
        )

        friday = (
            ", ".join(selected["friday"])
            if selected["friday"]
            else "None"
        )

        saturday = (
            ", ".join(selected["saturday"])
            if selected["saturday"]
            else "None"
        )

        sunday = (
            ", ".join(selected["sunday"])
            if selected["sunday"]
            else "None"
        )

        timestamp = datetime.now(
            TIME_ZONE
        ).strftime(
            "%Y-%m-%d %I:%M %p"
        )

        try:

            reg_sheet.append_row(
                [
                    clean_first_name,
                    clean_last_name,
                    clean_phone,
                    clean_email,
                    age,
                    selected_station,
                    friday,
                    saturday,
                    sunday,
                    timestamp
                ],
                value_input_option="USER_ENTERED"
            )

            st.success(
                f"🎉 Registration Complete! "
                f"Thank you, {clean_first_name}!"
            )

            st.info(
                "🙏 We appreciate your willingness "
                "to serve our community."
            )

            st.info(
                f"🕐 Registration Time: {timestamp}"
            )

        except Exception as e:

            st.error(
                "Your registration could not be saved right now. "
                "Please contact the volunteer coordinator."
            )

            with st.expander(
                "Show Google Sheets error"
            ):

                st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "✦ Thank you for serving our community ✦"
)

st.caption(
    "St. Anthony Coptic Orthodox Church Volunteer System"
)

