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
