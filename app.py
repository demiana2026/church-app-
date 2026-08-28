
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

# New Jersey / Eastern Time
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

    # Check Streamlit secrets
    if "gcp_service_account" not in st.secrets:
        raise Exception(
            "The gcp_service_account section was not found "
            "in Streamlit secrets."
        )

    # Read service account from secrets
    service_account_info = dict(
        st.secrets["gcp_service_account"]
    )

    # Create credentials
    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=scope
    )

    # Connect to Google Sheets
    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    # Check Registration worksheet
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
# GOOGLE SHEETS CONNECTION MESSAGE
# ============================================================

if not SHEETS_ENABLED:

    st.error(
        "Google Sheets is not connected. "
        "Your registration cannot be saved."
    )

    with st.expander(
        "Show Google Sheets error"
    ):

        st.code(
            sheets_error
            or "Unknown Google Sheets error."
        )


# ============================================================
# THANK YOU MESSAGE
# ============================================================

st.info(
    "🙏 Thank You for Volunteering\n\n"
    "Complete the form below to register and "
    "choose where you would like to serve."
)


# ============================================================
# REGISTRATION TITLE
# ============================================================

st.header(
    "Volunteer Registration"
)

st.write(
    "Please complete all required fields and "
    "select one station and your available times."
)


# ============================================================
# STATION INFORMATION
# ============================================================

STATIONS = [
    "Station 1 - Prizes/Kids Games",
    "Station 2 - Cosmetology",
    "Station 3 - Inflatables",
    "Station 4 - Basketball",
    "Station 5 - Snacking"
]


STATION_OPTIONS = {
    "Station 1 - Prizes/Kids Games": {
        "Friday": [
            "4:30 pm - 7:30 pm (Set up)",
            "7:15 pm - 10:15 pm (Clean up)"
        ],
        "Saturday": [
            "10:45 am - 1:45 pm (Set up)",
            "1:30 pm - 4:30 pm",
            "4:15 pm - 7:15 pm",
            "7:00 pm - 10:00 pm"
        ],
        "Sunday": [
            "11:45 am - 2:45 pm (Set up)",
            "2:30 pm - 5:30 pm (Clean up)"
        ]
    },

    "Station 2 - Cosmetology": {
        "Friday": [
            "4:30 pm - 7:30 pm (Set up)",
            "7:15 pm - 10:15 pm (Clean up)"
        ],
        "Saturday": [
            "10:45 am - 1:45 pm (Set up)",
            "1:30 pm - 4:30 pm",
            "4:15 pm - 7:15 pm",
            "7:00 pm - 10:00 pm"
        ],
        "Sunday": [
            "11:45 am - 2:45 pm (Set up)",
            "2:30 pm - 5:30 pm (Clean up)"
        ]
    },

    "Station 3 - Inflatables": {
        "Friday": [
            "4:30 pm - 7:30 pm (Set up)",
            "7:15 pm - 10:15 pm (Clean up)"
        ],
        "Saturday": [
            "10:45 am - 1:45 pm (Set up)",
            "1:30 pm - 4:30 pm",
            "4:15 pm - 7:15 pm",
            "7:00 pm - 10:00 pm"
        ],
        "Sunday": [
            "11:45 am - 2:45 pm (Set up)",
            "2:30 pm - 5:30 pm (Clean up)"
        ]
    },

    "Station 4 - Basketball": {
        "Friday": [
            "4:30 pm - 7:30 pm (Set up)",
            "7:15 pm - 10:15 pm (Clean up)"
        ],
        "Saturday": [
            "10:45 am - 1:45 pm (Set up)",
            "1:30 pm - 4:30 pm",
            "4:15 pm - 7:15 pm",
            "7:00 pm - 10:00 pm"
        ],
        "Sunday": [
            "11:45 am - 2:45 pm (Set up)",
            "2:30 pm - 5:30 pm (Clean up)"
        ]
    },

    "Station 5 - Snacking": {
        "Friday": [
            "4:30 pm - 7:30 pm (Set up)",
            "7:15 pm - 10:15 pm (Clean up)"
        ],
        "Saturday": [
            "10:45 am - 1:45 pm (Set up)",
            "1:30 pm - 4:30 pm",
            "4:15 pm - 7:15 pm",
            "7:00 pm - 10:00 pm"
        ],
        "Sunday": [
            "11:45 am - 2:45 pm (Set up)",
            "2:30 pm - 5:30 pm (Clean up)"
        ]
    }
}


# ============================================================
# REGISTRATION FORM
# ============================================================

with st.form("registration_form"):

    # ========================================================
    # PERSONAL INFORMATION
    # ========================================================

    st.subheader(
        "Personal Information"
    )

    st.caption(
        "All fields are required."
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
            "Email*",
            placeholder="you@example.com"
        )

    age = st.radio(
        "Age*",
        [
            "14-18",
            "18+"
        ],
        horizontal=True,
        key="registration_age"
    )


    # ========================================================
    # SELECT STATION
    # ========================================================

    st.divider()

    st.header(
        "Choose Your Station"
    )

    st.write(
        "First select the station where you would "
        "like to volunteer."
    )

    chosen_station = st.radio(
        "Select one station*",
        STATIONS,
        index=None,
        key="registration_station"
    )


    # ========================================================
    # CHOOSE TIMES
    # ========================================================

    st.divider()

    st.header(
        "Choose Your Available Times"
    )

    if chosen_station is None:

        st.info(
            "Please select a station above to see "
            "the available volunteer times."
        )

        friday = []
        saturday = []
        sunday = []

    else:

        st.write(
            f"Available times for **{chosen_station}**:"
        )

        station_times = STATION_OPTIONS[
            chosen_station
        ]

        day_tabs = st.tabs(
            [
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

        # ----------------------------------------------------
        # FRIDAY
        # ----------------------------------------------------

        with day_tabs[0]:

            friday = st.multiselect(
                "Friday Availability*",
                station_times["Friday"],
                key="selected_friday"
            )

        # ----------------------------------------------------
        # SATURDAY
        # ----------------------------------------------------

        with day_tabs[1]:

            saturday = st.multiselect(
                "Saturday Availability*",
                station_times["Saturday"],
                key="selected_saturday"
            )

        # ----------------------------------------------------
        # SUNDAY
        # ----------------------------------------------------

        with day_tabs[2]:

            sunday = st.multiselect(
                "Sunday Availability*",
                station_times["Sunday"],
                key="selected_sunday"
            )


    # ========================================================
    # SUBMIT
    # ========================================================

    st.divider()

    submitted = st.form_submit_button(
        "🙏 Submit Volunteer Registration",
        use_container_width=True
    )


# ============================================================
# PROCESS SUBMISSION
# ============================================================

if submitted:

    # ========================================================
    # REQUIRED PERSONAL INFORMATION
    # ========================================================

    if not first_name.strip():

        st.error(
            "Please enter your First Name."
        )

    elif not last_name.strip():

        st.error(
            "Please enter your Last Name."
        )

    elif not cell_phone.strip():

        st.error(
            "Please enter your Cell Phone."
        )

    elif not email.strip():

        st.error(
            "Please enter your Email."
        )

    # ========================================================
    # REQUIRED STATION
    # ========================================================

    elif chosen_station is None:

        st.error(
            "Please select a station."
        )

    # ========================================================
    # REQUIRED TIME
    # ========================================================

    elif not friday and not saturday and not sunday:

        st.error(
            "Please select at least one available "
            "volunteer time."
        )

    # ========================================================
    # GOOGLE SHEETS
    # ========================================================

    elif not SHEETS_ENABLED:

        st.error(
            "Google Sheets is not connected. "
            "Your registration cannot be saved."
        )

        with st.expander(
            "Show Google Sheets error"
        ):

            st.code(
                sheets_error
                or "Unknown Google Sheets error."
            )

    # ========================================================
    # SAVE REGISTRATION
    # ========================================================

    else:

        clean_first_name = first_name.strip()
        clean_last_name = last_name.strip()
        clean_phone = cell_phone.strip()
        clean_email = email.strip()

        selected_station = chosen_station

        friday_text = (
            ", ".join(friday)
            if friday
            else "None"
        )

        saturday_text = (
            ", ".join(saturday)
            if saturday
            else "None"
        )

        sunday_text = (
            ", ".join(sunday)
            if sunday
            else "None"
        )

        # ====================================================
        # NEW JERSEY TIMESTAMP
        # ====================================================

        timestamp = datetime.now(
            TIME_ZONE
        ).strftime(
            "%Y-%m-%d %I:%M %p"
        )

        # ====================================================
        # SAVE TO GOOGLE SHEETS
        # ====================================================

        try:

            reg_sheet.append_row(
                [
                    clean_first_name,
                    clean_last_name,
                    clean_phone,
                    clean_email,
                    age,
                    selected_station,
                    friday_text,
                    saturday_text,
                    sunday_text,
                    timestamp
                ],
                value_input_option="USER_ENTERED"
            )

            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                f"🎉 Registration Complete! "
                f"Thank you, {clean_first_name}!"
            )

            st.info(
                f"📍 Station: {selected_station}"
            )

            st.info(
                f"🕐 Registration Time: {timestamp}"
            )

            st.info(
                "🙏 We appreciate your willingness "
                "to serve our community."
            )

            st.info(
                "📖 " + volunteer_verses[
                    datetime.now(TIME_ZONE).day
                    % len(volunteer_verses)
                ]
            )

        except Exception as e:

            st.error(
                "Your registration could not be saved "
                "right now. Please contact the volunteer "
                "coordinator."
            )

            with st.expander(
                "Show Google Sheets error"
            ):

                st.code(
                    str(e)
                )


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

st.caption(
    "Thank you for serving with love and dedication ☦️"
)
