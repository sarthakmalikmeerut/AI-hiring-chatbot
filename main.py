import streamlit as st
import pandas as pd
import matchingAlgo  # Import the custom module
import matplotlib.pyplot as plt
import calendarInvite  # Import the new module

def clear_all():
    """Clears all session state variables to restart the app."""
    st.session_state.candidate_schedules = []
    st.session_state.recruiter_schedules = []
    st.session_state.cand_finished = False
    st.session_state.rec_finished = False
    st.session_state.cand_email = ""
    st.session_state.cand_start = None
    st.session_state.cand_end = None
    st.session_state.rec_email = ""
    st.session_state.rec_start = None
    st.session_state.rec_end = None

def main():
    st.title("Interview Scheduler")

    # Initialize session state variables if not set
    if "candidate_schedules" not in st.session_state:
        st.session_state.candidate_schedules = []
    if "recruiter_schedules" not in st.session_state:
        st.session_state.recruiter_schedules = []
    if "cand_finished" not in st.session_state:
        st.session_state.cand_finished = False
    if "rec_finished" not in st.session_state:
        st.session_state.rec_finished = False

    # Clear All Button
    if st.button("Clear All Data"):
        clear_all()
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.header("Candidate")
        candidate_email = st.text_input("Candidate Email", key="cand_email")
        start_col, end_col = st.columns(2)
        with start_col:
            candidate_start = st.time_input("Start Time", key="cand_start")
        with end_col:
            candidate_end = st.time_input("End Time", key="cand_end")

        if st.button("Add Candidate Schedule", key="cand_add"):
            if candidate_email and candidate_start and candidate_end:
                st.session_state.candidate_schedules.append((candidate_email, candidate_start, candidate_end))
                st.success("Candidate schedule added!")

    with col2:
        st.header("Recruiter")
        recruiter_email = st.text_input("Recruiter Email", key="rec_email")
        start_col, end_col = st.columns(2)
        with start_col:
            recruiter_start = st.time_input("Start Time", key="rec_start")
        with end_col:
            recruiter_end = st.time_input("End Time", key="rec_end")

        if st.button("Add Recruiter Schedule", key="rec_add"):
            if recruiter_email and recruiter_start and recruiter_end:
                st.session_state.recruiter_schedules.append((recruiter_email, recruiter_start, recruiter_end))
                st.success("Recruiter schedule added!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Candidate Finish", key="cand_finish"):
            st.session_state.cand_finished = True

    with col2:
        if st.button("Recruiter Finish", key="rec_finish"):
            st.session_state.rec_finished = True

    if st.session_state.cand_finished and st.session_state.rec_finished:
        schedule_data = []
        for email, start, end in st.session_state.candidate_schedules:
            schedule_data.append(["Candidate", email, start, end])
        for email, start, end in st.session_state.recruiter_schedules:
            schedule_data.append(["Recruiter", email, start, end])

        if schedule_data:
            df = pd.DataFrame(schedule_data, columns=["Role", "Email", "Start Time", "End Time"])
            st.write("### Scheduled Interview Details")
            st.dataframe(df)

        # 🔹 Construct Bipartite Graph (Ensure dicts are returned)
        G, recruiters_dict, candidates_dict = matchingAlgo.construct_bipartite_graph(
            st.session_state.recruiter_schedules,
            st.session_state.candidate_schedules
        )

        if G.number_of_edges() == 0:
            print("No valid matches found. Skipping matching algorithm.")
            st.warning("No valid interview slots found.")
            return

        st.write("### Bipartite Graph Representation")
        fig, ax = plt.subplots()
        matchingAlgo.plot_bipartite_graph(G, recruiters_dict, candidates_dict, ax)
        st.pyplot(fig)

        # 🔹 Apply Matching Algorithm (Hopcroft-Karp)
        matching, recruiters_dict, candidates_dict = matchingAlgo.find_optimal_matching(G, recruiters_dict, candidates_dict)

        # 🔹 Apply Greedy Scheduling
        final_schedule = matchingAlgo.greedy_time_slot_assignment(
            matching,
            recruiters_dict,  # ✅ Pass correct dict
            candidates_dict   # ✅ Pass correct dict
        )

        # 🔹 Display Final Interview Schedule
        if final_schedule:
            st.write("### Final Interview Schedule")
            final_df = pd.DataFrame(final_schedule, columns=["Recruiter", "Candidate", "Start Time", "End Time"])
            st.dataframe(final_df)

            # 🔹 Send Calendar Invites
            if st.button("Send Calendar Invites"):
                calendarInvite.send_invites(final_schedule)
                st.success("Calendar invites sent successfully!")
        else:
            st.warning("No valid interview slots found.")

main()
