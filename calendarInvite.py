import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote
import requests
from datetime import datetime, date
import pytz


def shorten_url(long_url):
    """
    Shortens a URL using TinyURL API.

    :param long_url: The original long URL
    :return: Shortened URL
    """
    try:
        response = requests.get(f"https://tinyurl.com/api-create.php?url={quote(long_url)}")
        if response.status_code == 200:
            return response.text
        else:
            return long_url  # Fallback to original URL if shortening fails
    except Exception as e:
        print(f"❌ Error shortening URL: {e}")
        return long_url


def generate_calendar_link(start_time, end_time, recruiter, candidate):
    """
    Generates a shortened Google Calendar invite link.

    :param start_time: Interview start time (IST, datetime object)
    :param end_time: Interview end time (IST, datetime object)
    :param recruiter: Recruiter's email
    :param candidate: Candidate's email
    :return: Shortened Google Calendar event link
    """
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"

    event_title = "Interview Scheduled"
    description = f"Interview between {recruiter} and {candidate}."
    location = "Google Meet"

    # Convert IST time to UTC
    ist = pytz.timezone("Asia/Kolkata")

    selected_date = date.today()  # You can modify this to take input from the user

    # Correctly combine date and time
    start_datetime = datetime.combine(selected_date, start_time).replace(tzinfo=ist)
    end_datetime = datetime.combine(selected_date, end_time).replace(tzinfo=ist)

    # Convert to UTC
    start_utc = start_datetime.astimezone(pytz.utc)
    end_utc = end_datetime.astimezone(pytz.utc)

    # Format times in Google Calendar format (UTC)
    start_str = start_utc.strftime('%Y%m%dT%H%M%SZ')
    end_str = end_utc.strftime('%Y%m%dT%H%M%SZ')

    # Construct full Google Calendar URL
    calendar_link = (f"{base_url}"
                     f"&text={quote(event_title)}"
                     f"&details={quote(description)}"
                     f"&location={quote(location)}"
                     f"&dates={start_str}/{end_str}")

    # Shorten the URL
    return shorten_url(calendar_link)


def send_invites(final_schedule):
    """
    Sends interview invitations via email with a Google Calendar event link.

    :param final_schedule: List of tuples (Recruiter Email, Candidate Email, Start Time, End Time)
    """
    sender_email = "sarthakmalikmeerut@gmail.com"
    sender_password = "gsqk cbvt dgnv kzmm"  # Use App Password if 2FA is enabled

    for recruiter, candidate, start_time, end_time in final_schedule:
        # Generate a shortened Google Calendar event link
        calendar_link = generate_calendar_link(start_time, end_time, recruiter, candidate)

        # Email body with Google Calendar invite link
        email_body = f"""
        Dear {recruiter} and {candidate},

        Your interview has been scheduled as follows:

        📅 **Date:** {start_time.strftime('%Y-%m-%d')}
        🕒 **Time:** {start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')} (IST)
        🌍 **Meeting Location:** Google Meet  
        📆 **Add to Calendar:** [Click here]({calendar_link})

        Please mark your calendar accordingly. If you have any questions, feel free to reach out.

        Best regards,  
        Interview Scheduling Team
        """

        # Construct email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recruiter  # Recruiter as primary recipient
        msg['Cc'] = candidate  # Candidate in CC
        msg['Subject'] = "Interview Scheduled Notification"

        msg.attach(MIMEText(email_body, 'plain'))  # Send as plain text

        recipients = [recruiter, candidate]  # Both recipients

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, msg.as_string())  # Send email
            server.quit()
            print(f"✅ Interview invite sent to {recruiter} and {candidate}")
        except Exception as e:
            print(f"❌ Error sending invite: {e}")
