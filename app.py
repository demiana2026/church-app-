
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
# STATION SETTINGS
# ============================================================

STATIONS = {
    "🎁 Prizes": {
        "name": "Station 1 - Prizes/Kids Games",
        "number": 1
    },
    "💄 Cosmetology": {
        "name": "Station 2 - Cosmetology",
        "number": 2
    },
    "🎈 Inflatables": {
        "name": "Station 3 - Inflatables",
        "number": 3
    },
    "🏀 Basketball": {
        "name": "Station 4 - Basketball",
        "number": 4
    },
    "🍿 Snacking": {
        "name": "Station 5 - Snacking",
        "number": 5
    }
}


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

    # --------------------------------------------------------
    # CHECK STREAMLIT SECRETS
    # --------------------------------------------------------

    if "gcp_service_account" not in st.secrets:

        raise Exception(
            "The gcp_service_account section was not found "
            "in Streamlit secrets."
        )

    # --------------------------------------------------------
    # GET SERVICE ACCOUNT
    # --------------------------------------------------------

    service_account_info = dict(
        st.secrets["gcp_service_account"]
    )

    # --------------------------------------------------------
    # CREATE CREDENTIALS
    # --------------------------------------------------------

    credentials = Credentials.from_service_account_info(
        service_account_info,
        scopes=scope
    )

    # --------------------------------------------------------
    # CONNECT TO GOOGLE SHEETS
    # --------------------------------------------------------

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    # --------------------------------------------------------
    # CHECK REGISTRATION TAB
    # --------------------------------------------------------

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
# GOOGLE SHEETS ERROR
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
    "the station and times where you would like to serve."
)


# ============================================================
# FORM
# ============================================================

with st.form("registration_form"):

    # ========================================================
    # PERSONAL INFORMATION
    # ========================================================

    st.subheader(
        "Personal Information"
    )

    st.caption(
        "All fields below are required."
    )

    col1, col2 = st.columns(
        2,
        gap="large"
    )

    with col1:

        first_name = st.text_input(
            "First Name *",
            max_chars=50,
            placeholder="First name"
        )

    with col2:

        last_name = st.text_input(
            "Last Name *",
            max_chars=50,
            placeholder="Last name"
        )

    col3, col4 = st.columns(
        2,
        gap="large"
    )

    with col3:

        cell_phone = st.text_input(
            "Cell Phone *",
            placeholder="(555) 555-5555"
        )

    with col4:

        email = st.text_input(
            "Email *",
            placeholder="you@example.com"
        )

    age = st.radio(
        "Age *",
        [
            "14-18",
            "18+"
        ],
        horizontal=True,
        key="age"
    )


    # ========================================================
    # STATION SELECTION
    # ========================================================

    st.divider()

    st.header(
        "Choose Your Station"
    )

    st.write(
        "Open a station tab and select the times "
        "you are available to volunteer."
    )


    # ========================================================
    # STATION TABS
    # ========================================================

    station_tabs = st.tabs(
        list(STATIONS.keys())
    )


    all_availability = {}


    # ========================================================
    # FUNCTION TO CREATE DAY AVAILABILITY
    # ========================================================

    def availability_selector(
        station_number,
        day,
        options
    ):

        selected = st.multiselect(
            f"{day} Availability",
            options,
            key=f"station_{station_number}_{day.lower()}_availability"
        )

        return selected


    # ========================================================
    # STATION 1 - PRIZES
    # ========================================================

    with station_tabs[0]:

        st.subheader(
            STATIONS["🎁 Prizes"]["name"]
        )

        st.caption(
            "Select the times you are available to volunteer."
        )

        friday = availability_selector(
            1,
            "Friday",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ]
        )

        saturday = availability_selector(
            1,
            "Saturday",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ]
        )

        sunday = availability_selector(
            1,
            "Sunday",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ]
        )

        all_availability[
            STATIONS["🎁 Prizes"]["name"]
        ] = {
            "Friday": friday,
            "Saturday": saturday,
            "Sunday": sunday
        }


    # ========================================================
    # STATION 2 - COSMETOLOGY
    # ========================================================

    with station_tabs[1]:

        st.subheader(
            STATIONS["💄 Cosmetology"]["name"]
        )

        st.caption(
            "Select the times you are available to volunteer."
        )

        friday = availability_selector(
            2,
            "Friday",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ]
        )

        saturday = availability_selector(
            2,
            "Saturday",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ]
        )

        sunday = availability_selector(
            2,
            "Sunday",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ]
        )

        all_availability[
            STATIONS["💄 Cosmetology"]["name"]
        ] = {
            "Friday": friday,
            "Saturday": saturday,
            "Sunday": sunday
        }


    # ========================================================
    # STATION 3 - INFLATABLES
    # ========================================================

    with station_tabs[2]:

        st.subheader(
            STATIONS["🎈 Inflatables"]["name"]
        )

        st.caption(
            "Select the times you are available to volunteer."
        )

        friday = availability_selector(
            3,
            "Friday",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ]
        )

        saturday = availability_selector(
            3,
            "Saturday",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ]
        )

        sunday = availability_selector(
            3,
            "Sunday",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ]
        )

        all_availability[
            STATIONS["🎈 Inflatables"]["name"]
        ] = {
            "Friday": friday,
            "Saturday": saturday,
            "Sunday": sunday
        }


    # ========================================================
    # STATION 4 - BASKETBALL
    # ========================================================

    with station_tabs[3]:

        st.subheader(
            STATIONS["🏀 Basketball"]["name"]
        )

        st.caption(
            "Select the times you are available to volunteer."
        )

        friday = availability_selector(
            4,
            "Friday",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ]
        )

        saturday = availability_selector(
            4,
            "Saturday",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ]
        )

        sunday = availability_selector(
            4,
            "Sunday",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ]
        )

        all_availability[
            STATIONS["🏀 Basketball"]["name"]
        ] = {
            "Friday": friday,
            "Saturday": saturday,
            "Sunday": sunday
        }


    # ========================================================
    # STATION 5 - SNACKING
    # ========================================================

    with station_tabs[4]:

        st.subheader(
            STATIONS["🍿 Snacking"]["name"]
        )

        st.caption(
            "Select the times you are available to volunteer."
        )

        friday = availability_selector(
            5,
            "Friday",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ]
        )

        saturday = availability_selector(
            5,
            "Saturday",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ]
        )

        sunday = availability_selector(
            5,
            "Sunday",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ]
        )

        all_availability[
            STATIONS["🍿 Snacking"]["name"]
        ] = {
            "Friday": friday,
            "Saturday": saturday,
            "Sunday": sunday
        }


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

    elif "@" not in email.strip():

        st.error(
            "Please enter a valid email address."
        )

    else:

        # ====================================================
        # FIND SELECTED STATIONS
        # ====================================================

        selected_station_data = []

        for station_name, days in all_availability.items():

            has_availability = False

            for day, times in days.items():

                if times:

                    has_availability = True
                    break

            if has_availability:

                selected_station_data.append(
                    (station_name, days)
                )


        # ====================================================
        # REQUIRE STATION + TIME
        # ====================================================

        if not selected_station_data:

            st.error(
                "Please choose a station and select "
                "at least one available volunteer time."
            )

        # ====================================================
        # GOOGLE SHEETS
        # ====================================================

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

        # ====================================================
        # SAVE
        # ====================================================

        else:

            clean_first_name = first_name.strip()
            clean_last_name = last_name.strip()
            clean_phone = cell_phone.strip()
            clean_email = email.strip()

            timestamp = datetime.now(
                TIME_ZONE
            ).strftime(
                "%Y-%m-%d %I:%M %p"
            )

            try:

                rows_saved = 0

                # --------------------------------------------
                # SAVE EACH SELECTED STATION
                # --------------------------------------------

                for station_name, days in selected_station_data:

                    friday = (
                        ", ".join(days["Friday"])
                        if days["Friday"]
                        else ""
                    )

                    saturday = (
                        ", ".join(days["Saturday"])
                        if days["Saturday"]
                        else ""
                    )

                    sunday = (
                        ", ".join(days["Sunday"])
                        if days["Sunday"]
                        else ""
                    )

                    reg_sheet.append_row(
                        [
                            clean_first_name,
                            clean_last_name,
                            clean_phone,
                            clean_email,
                            age,
                            station_name,
                            friday,
                            saturday,
                            sunday,
                            timestamp
                        ],
                        value_input_option="USER_ENTERED"
                    )

                    rows_saved += 1


                # --------------------------------------------
                # SUCCESS
                # --------------------------------------------

                st.success(
                    f"🎉 Registration Complete! "
                    f"Thank you, {clean_first_name}!"
                )

                st.info(
                    f"🙏 Your registration was saved for "
                    f"{rows_saved} station(s)."
                )

                st.info(
                    f"🕐 Registration Time: {timestamp}"
                )

                st.info(
                    "📖 " + volunteer_verses[
                        datetime.now(TIME_ZONE).day
                        % len(volunteer_verses)
                    ]
                )

                st.subheader(
                    "Thank You for Serving!"
                )

                st.write(
                    "Your willingness to serve makes a "
                    "difference in our community. "
                    "May God bless your service!"
                )


            except Exception as e:

                st.error(
                    "Your registration could not be saved "
                    "right now. Please contact the "
                    "volunteer coordinator."
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
