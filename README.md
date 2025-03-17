
# **Interview Scheduler**

## **Overview**
The **Interview Scheduler** is a Streamlit-based web application that allows recruiters and candidates to input their availability, automatically finds optimal interview slots using a matching algorithm, and sends Google Calendar invites.

## **Features**
- ✅ **User-Friendly Interface:** Recruiters and candidates can easily enter their available time slots.
- 🔄 **Automated Scheduling:** Uses a bipartite graph matching algorithm to find the best interview slots.
- 📅 **Calendar Integration:** Generates Google Calendar event links and sends email invitations.
- 📊 **Graph Visualization:** Displays the scheduling process with a bipartite graph representation.

## **Installation & Setup**
### **Prerequisites**
- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- NetworkX
- Requests
- Pytz

### **Install Dependencies**
Run the following command in your terminal:
```bash
pip install streamlit pandas matplotlib networkx requests pytz
```

## **Usage**
### **Run the Application**
Start the Streamlit app with:
```bash
streamlit run main.py
```
This will open the web UI in your browser.

### **Workflow**
1. 📝 Candidates and recruiters enter their availability.
2. 🔗 The system constructs a bipartite graph to match the best possible slots.
3. 📆 The optimal interview schedule is displayed.
4. 📩 Google Calendar invites are sent via email.

## **Project Structure**
```
|-- main.py               # Streamlit-based UI for scheduling
|-- matchingAlgo.py       # Implements the bipartite matching algorithm
|-- calendarInvite.py     # Handles email invites and Google Calendar event creation
|-- requirements.txt      # List of dependencies (optional)
```

## **Run Command**
To start the application, use:
```bash
streamlit run main.py
```

## **Technology Stack**
- **Frontend:** Streamlit
- **Backend:** Python (Pandas, NetworkX, Matplotlib)
- **Email & Calendar Integration:** SMTP, Google Calendar links

## **Future Enhancements**
- 🌍 Add time zone support for international scheduling.
- 🔐 Implement OAuth for secure email sending.
- 🎨 Improve UI with more scheduling options.

---

🚀 **Happy Scheduling!** 🚀
