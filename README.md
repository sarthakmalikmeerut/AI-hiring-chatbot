# Interview Scheduler

This is a **Streamlit-based Interview Scheduler** that matches candidates and recruiters based on their available time slots and sends calendar invites for scheduled interviews.

## Features
- Add candidate and recruiter availability.
- Construct a **bipartite graph** to find optimal interview matches.
- Use the **Hopcroft-Karp algorithm** for efficient matching.
- Apply **greedy time slot assignment** for optimal scheduling.
- Visualize the **bipartite graph**.
- Send **Google Calendar invites** to confirmed interview participants.

---

## Prerequisites
Make sure you have the following installed:
- Python 3.7+
- pip

Install the required Python packages:
```sh
pip install -r requirements.txt
```

### Required Libraries
Ensure the following dependencies are included in `requirements.txt`:
```
streamlit
pandas
networkx
matplotlib
```

If you are using Google Calendar integration, also install:
```
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
```

---

## How to Run the Program
Execute the following command in the terminal:
```sh
streamlit run app.py
```

This will launch the Streamlit web application in your default browser.

---

## Usage
1. **Enter candidate details** (email and available time slots).
2. **Enter recruiter details** (email and available time slots).
3. Click **'Candidate Finish'** and **'Recruiter Finish'** to finalize inputs.
4. The system will:
   - Construct a **bipartite graph**.
   - Run the **matching algorithm**.
   - Display the **final interview schedule**.
   - Optionally, send **calendar invites**.

---

## Troubleshooting
- **No valid interview slots found?**
  - Ensure candidate and recruiter time slots **overlap**.
  - Adjust time slots if needed.
- **Error: networkx.exception.AmbiguousSolution?**
  - This happens when no valid edges exist in the bipartite graph.
  - Ensure time slots match properly.

---

## Author
Sarthak Malik

