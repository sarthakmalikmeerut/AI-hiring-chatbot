import streamlit as st
import pandas as pd
import matchingAlgo
import matplotlib.pyplot as plt
import calendarInvite

def reset_session_state():
    """Resets all session state variables to restart the app."""
    st.session_state.candidate_availability = []
    st.session_state.recruiter_availability = []
    st.session_state.is_candidate_done = False
    st.session_state.is_recruiter_done = False
    st.session_state.candidate_email = ""
    st.session_state.candidate_start_time = None
    st.session_state.candidate_end_time = None
    st.session_state.recruiter_email = ""
    st.session_state.recruiter_start_time = None
    st.session_state.recruiter_end_time = None

def main():
    st.title("Interview Scheduler")

    if "candidate_availability" not in st.session_state:
        st.session_state.candidate_availability = []
    if "recruiter_availability" not in st.session_state:
        st.session_state.recruiter_availability = []
    if "is_candidate_done" not in st.session_state:
        st.session_state.is_candidate_done = False
    if "is_recruiter_done" not in st.session_state:
        st.session_state.is_recruiter_done = False

    if st.button("Reset All Data"):
        reset_session_state()
        st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.header("Candidate Availability")
        candidate_email = st.text_input("Candidate Email Address", key="candidate_email")
        start_col, end_col = st.columns(2)
        with start_col:
            candidate_start_time = st.time_input("Available From", key="candidate_start_time")
        with end_col:
            candidate_end_time = st.time_input("Available Until", key="candidate_end_time")

        if st.button("Add Candidate Availability", key="add_candidate"):
            if candidate_email and candidate_start_time and candidate_end_time:
                st.session_state.candidate_availability.append(
                    (candidate_email, candidate_start_time, candidate_end_time)
                )
                st.success("Candidate availability added!")

    with col2:
        st.header("Recruiter Availability")
        recruiter_email = st.text_input("Recruiter Email Address", key="recruiter_email")
        start_col, end_col = st.columns(2)
        with start_col:
            recruiter_start_time = st.time_input("Available From", key="recruiter_start_time")
        with end_col:
            recruiter_end_time = st.time_input("Available Until", key="recruiter_end_time")

        if st.button("Add Recruiter Availability", key="add_recruiter"):
            if recruiter_email and recruiter_start_time and recruiter_end_time:
                st.session_state.recruiter_availability.append(
                    (recruiter_email, recruiter_start_time, recruiter_end_time)
                )
                st.success("Recruiter availability added!")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Candidate Submission Complete", key="finalize_candidate"):
            st.session_state.is_candidate_done = True

    with col2:
        if st.button("Recruiter Submission Complete", key="finalize_recruiter"):
            st.session_state.is_recruiter_done = True

    if st.session_state.is_candidate_done and st.session_state.is_recruiter_done:
        schedule_data = [
            ["Candidate", email, start, end] for email, start, end in st.session_state.candidate_availability
        ] + [
            ["Recruiter", email, start, end] for email, start, end in st.session_state.recruiter_availability
        ]

        if schedule_data:
            df = pd.DataFrame(schedule_data, columns=["Role", "Email", "Available From", "Available Until"])
            st.write("### Scheduled Interview Availability")
            st.dataframe(df)

        G, recruiter_dict, candidate_dict = matchingAlgo.construct_bipartite_graph(
            st.session_state.recruiter_availability, st.session_state.candidate_availability
        )

        if G.number_of_edges() == 0:
            st.warning("No valid interview slots found.")
            return

        st.write("### Bipartite Graph Representation")
        fig, ax = plt.subplots()
        matchingAlgo.plot_bipartite_graph(G, recruiter_dict, candidate_dict, ax)
        st.pyplot(fig)

        matching, recruiter_dict, candidate_dict = matchingAlgo.find_optimal_matching(G, recruiter_dict, candidate_dict)

        final_schedule = matchingAlgo.greedy_time_slot_assignment(matching, recruiter_dict, candidate_dict)

        if final_schedule:
            st.write("### Final Interview Schedule")
            final_df = pd.DataFrame(final_schedule, columns=["Recruiter", "Candidate", "Interview Start", "Interview End"])
            st.dataframe(final_df)

            if st.button("Send Calendar Invitations"):
                calendarInvite.send_invites(final_schedule)
                st.success("Calendar invitations sent successfully!")
        else:
            st.warning("No valid interview slots found.")

main()
