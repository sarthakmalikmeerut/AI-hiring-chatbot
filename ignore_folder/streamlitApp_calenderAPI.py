import streamlit as st
import datetime
import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def fetch_calendar_events():
    creds = None
    try:
        if os.path.exists("../token.json"):
            creds = Credentials.from_authorized_user_file("../token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("../credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("../token.json", "w") as token:
                token.write(creds.to_json())

        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'

        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        event_details = []

        for event in events:
            start_time = event["start"].get("dateTime", "Unknown")
            end_time = event["end"].get("dateTime", "Unknown")
            summary = event.get("summary", "No Title")

            # Convert to readable format (hh:mm AM/PM)
            start_time_formatted = datetime.datetime.fromisoformat(start_time).strftime(
                "%I:%M %p") if start_time != "Unknown" else "Unknown"
            end_time_formatted = datetime.datetime.fromisoformat(end_time).strftime(
                "%I:%M %p") if end_time != "Unknown" else "Unknown"

            event_details.append({
                "Time": f"{start_time_formatted} - {end_time_formatted}",
                "Event": summary
            })

        return event_details
    except HttpError as error:
        st.error(f"An error occurred: {error}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return []


st.title("Recruiter & Candidate Email Collector")

# Initialize session state if not already done
if "recruiters" not in st.session_state:
    st.session_state["recruiters"] = []
if "candidates" not in st.session_state:
    st.session_state["candidates"] = []
if "recruiters_finished" not in st.session_state:
    st.session_state["recruiters_finished"] = False
if "candidates_finished" not in st.session_state:
    st.session_state["candidates_finished"] = False

col1, col2 = st.columns(2)


def add_recruiter():
    st.session_state.recruiters.append("")


def add_candidate():
    st.session_state.candidates.append("")


with col1:
    st.header("Recruiters")
    if st.button("Add Recruiter"):
        add_recruiter()

    for i, _ in enumerate(st.session_state.recruiters):
        st.session_state.recruiters[i] = st.text_input(f"Recruiter {i + 1} Email", value=st.session_state.recruiters[i],
                                                       key=f"rec_{i}")

    if st.button("Finish Recruiters"):
        st.session_state["recruiters_finished"] = True

with col2:
    st.header("Candidates")
    if st.button("Add Candidate"):
        add_candidate()

    for i, _ in enumerate(st.session_state.candidates):
        st.session_state.candidates[i] = st.text_input(f"Candidate {i + 1} Email", value=st.session_state.candidates[i],
                                                       key=f"cand_{i}")

    if st.button("Finish Candidates"):
        st.session_state["candidates_finished"] = True

if st.session_state.get("recruiters_finished") and st.session_state.get("candidates_finished"):
    st.header("Final Details")

    event_details = fetch_calendar_events()

    st.subheader("Recruiters")
    st.table(pd.DataFrame({"Emails": st.session_state["recruiters"]}))

    st.subheader("Candidates")
    st.table(pd.DataFrame({"Emails": st.session_state["candidates"]}))

    st.subheader("Today's Events")

    if event_details:
        # Generate combinations of recruiter-candidate for events
        event_rows = []
        for event in event_details:
            for recruiter in st.session_state["recruiters"]:
                for candidate in st.session_state["candidates"]:
                    event_rows.append({
                        "Recruiter Email": recruiter,
                        "Candidate Email": candidate,
                        "Event Time": event["Time"],
                        "Event Name": event["Event"]
                    })

        st.table(pd.DataFrame(event_rows))
    else:
        st.write("No events found.")
