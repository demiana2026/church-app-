
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
# THANK YOU
# ============================================================

st.info(
    "🙏 Thank You for Volunteering\n\n"
    "Complete the form below to register "
    "and choose where you would like to serve."
)


# ============================================================
# REGISTRATION
# ============================================================

st.header(
    "Volunteer Registration"
)

st.write(
    "Please complete all required information "
    "and select your volunteer station and available times."
)


# ============================================================
# FORM
# ============================================================

with st.form(
    "registration_form"
):

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
    # STATIONS
    # ========================================================

    st.divider()

    st.header(
        "Choose Your Station"
    )

    st.write(
        "Select one station below and choose your "
        "available volunteer times."
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


    # ========================================================
    # STATION 1 - PRIZES
    # ========================================================

    with station_tabs[0]:

        st.subheader(
            "Station 1 - Prizes/Kids Games"
        )

        st.write(
            "Choose the times you are available."
        )

        prizes_friday = st.multiselect(
            "Friday Availability*",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key="prizes_friday"
        )

        prizes_saturday = st.multiselect(
            "Saturday Availability*",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key="prizes_saturday"
        )

        prizes_sunday = st.multiselect(
            "Sunday Availability*",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key="prizes_sunday"
        )


    # ========================================================
    # STATION 2 - COSMETOLOGY
    # ========================================================

    with station_tabs[1]:

        st.subheader(
            "Station 2 - Cosmetology"
        )

        st.write(
            "Choose the times you are available."
        )

        cosmetology_friday = st.multiselect(
            "Friday Availability*",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key="cosmetology_friday"
        )

        cosmetology_saturday = st.multiselect(
            "Saturday Availability*",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key="cosmetology_saturday"
        )

        cosmetology_sunday = st.multiselect(
            "Sunday Availability*",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key="cosmetology_sunday"
        )


    # ========================================================
    # STATION 3 - INFLATABLES
    # ========================================================

    with station_tabs[2]:

        st.subheader(
            "Station 3 - Inflatables"
        )

        st.write(
            "Choose the times you are available."
        )

        inflatables_friday = st.multiselect(
            "Friday Availability*",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key="inflatables_friday"
        )

        inflatables_saturday = st.multiselect(
            "Saturday Availability*",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key="inflatables_saturday"
        )

        inflatables_sunday = st.multiselect(
            "Sunday Availability*",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key="inflatables_sunday"
        )


    # ========================================================
    # STATION 4 - BASKETBALL
    # ========================================================

    with station_tabs[3]:

        st.subheader(
            "Station 4 - Basketball"
        )

        st.write(
            "Choose the times you are available."
        )

        basketball_friday = st.multiselect(
            "Friday Availability*",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key="basketball_friday"
        )

        basketball_saturday = st.multiselect(
            "Saturday Availability*",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key="basketball_saturday"
        )

        basketball_sunday = st.multiselect(
            "Sunday Availability*",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key="basketball_sunday"
        )


    # ========================================================
    # STATION 5 - SNACKING
    # ========================================================

    with station_tabs[4]:

        st.subheader(
            "Station 5 - Snacking"
        )

        st.write(
            "Choose the times you are available."
        )

        snacking_friday = st.multiselect(
            "Friday Availability*",
            [
                "4:30 pm - 7:30 pm (Set up)",
                "7:15 pm - 10:15 pm (Clean up)"
            ],
            key="snacking_friday"
        )

        snacking_saturday = st.multiselect(
            "Saturday Availability*",
            [
                "10:45 am - 1:45 pm (Set up)",
                "1:30 pm - 4:30 pm",
                "4:15 pm - 7:15 pm",
                "7:00 pm - 10:00 pm"
            ],
            key="snacking_saturday"
        )

        snacking_sunday = st.multiselect(
            "Sunday Availability*",
            [
                "11:45 am - 2:45 pm (Set up)",
                "2:30 pm - 5:30 pm (Clean up)"
            ],
            key="snacking_sunday"
        )


    # ========================================================
    # STATION SELECTION
    # ========================================================
    #
    # IMPORTANT:
    # Streamlit tabs do NOT tell Python which tab
    # the user clicked.
    #
    # Therefore, we use a required station selector
    # AFTER the tabs only to identify which tab's
    # times should be saved.
    #
    # If you want ONLY clickable tabs with no second
    # selector, Streamlit tabs cannot reliably determine
    # the active tab on form submission.
    #
    # To keep the user experience clean, we use a
    # dropdown here instead of repeating the old
    # "Confirm Your Station" section.
    # ========================================================

    st.divider()

    selected_station = st.selectbox(
        "Station*",
        [
            "Select a station",
            "Station 1 - Prizes/Kids Games",
            "Station 2 - Cosmetology",
            "Station 3 - Inflatables",
            "Station 4 - Basketball",
            "Station 5 - Snacking"
        ],
        index=0,
        key="selected_station"
    )


    # ========================================================
    # SUBMIT
    # ========================================================

    submitted = st.form_submit_button(
        "🙏 Submit Volunteer Registration",
        use_container_width=True
    )


# ============================================================
# SUBMISSION
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

    elif selected_station == "Select a station":

        st.error(
            "Please select a station."
        )

    else:

        # ====================================================
        # GET TIMES FOR SELECTED STATION
        # ====================================================

        if selected_station == "Station 1 - Prizes/Kids Games":

            friday = prizes_friday
            saturday = prizes_saturday
            sunday = prizes_sunday

        elif selected_station == "Station 2 - Cosmetology":

            friday = cosmetology_friday
            saturday = cosmetology_saturday
            sunday = cosmetology_sunday

        elif selected_station == "Station 3 - Inflatables":

            friday = inflatables_friday
            saturday = inflatables_saturday
            sunday = inflatables_sunday

        elif selected_station == "Station 4 - Basketball":

            friday = basketball_friday
            saturday = basketball_saturday
            sunday = basketball_sunday

        else:

            friday = snacking_friday
            saturday = snacking_saturday
            sunday = snacking_sunday


        # ====================================================
        # REQUIRED TIME
        # ====================================================

        if not friday and not saturday and not sunday:

            st.error(
                "Please select at least one available "
                "volunteer time for your selected station."
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

            # =================================================
            # NJ TIME
            # =================================================

            timestamp = datetime.now(
                TIME_ZONE
            ).strftime(
                "%Y-%m-%d %I:%M %p"
            )

            # =================================================
            # SAVE TO GOOGLE SHEETS
            # =================================================

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

                # =============================================
                # SUCCESS
                # =============================================

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

                verse_number = (
                    datetime.now(TIME_ZONE).day
                    % len(volunteer_verses)
                )

                st.info(
                    "📖 " +
                    volunteer_verses[verse_number]
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

