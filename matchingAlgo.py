import networkx as nx
from networkx.algorithms import bipartite
from datetime import datetime, time, timedelta

def parse_time(time_input):
    """Ensures time is converted correctly, handling overnight cases."""
    if isinstance(time_input, time):
        return time_input
    elif isinstance(time_input, str):
        return datetime.strptime(time_input, "%H:%M").time()
    else:
        raise ValueError(f"Unsupported time format: {time_input}")

def construct_bipartite_graph(recruiters, candidates):
    """
    Constructs a bipartite graph while correctly handling overnight availability.
    Supports multiple time slots per recruiter/candidate.
    """
    G = nx.Graph()
    recruiters_dict, candidates_dict = {}, {}

    for rec_email, start, end in recruiters:
        start, end = parse_time(start), parse_time(end)
        if end < start:  # Handle overnight case
            end = (datetime.combine(datetime.today(), end) + timedelta(days=1)).time()
        recruiters_dict.setdefault(rec_email, []).append((start, end))
        G.add_node(rec_email, bipartite=0)

    for cand_email, start, end in candidates:
        start, end = parse_time(start), parse_time(end)
        if end < start:  # Handle overnight case
            end = (datetime.combine(datetime.today(), end) + timedelta(days=1)).time()
        candidates_dict.setdefault(cand_email, []).append((start, end))
        G.add_node(cand_email, bipartite=1)

    for rec_email, rec_slots in recruiters_dict.items():
        for cand_email, cand_slots in candidates_dict.items():
            for rec_start, rec_end in rec_slots:
                for cand_start, cand_end in cand_slots:
                    # Allow overlap considering overnight cases
                    rec_start_dt = datetime.combine(datetime.today(), rec_start)
                    rec_end_dt = datetime.combine(datetime.today(), rec_end)
                    cand_start_dt = datetime.combine(datetime.today(), cand_start)
                    cand_end_dt = datetime.combine(datetime.today(), cand_end)

                    if rec_end_dt < rec_start_dt:
                        rec_end_dt += timedelta(days=1)  # Overnight fix
                    if cand_end_dt < cand_start_dt:
                        cand_end_dt += timedelta(days=1)  # Overnight fix

                    if rec_start_dt <= cand_end_dt and cand_start_dt <= rec_end_dt:
                        G.add_edge(rec_email, cand_email, weight=1)  # Keep track of connections

    return G, recruiters_dict, candidates_dict


def find_optimal_matching(G, recruiters_dict, candidates_dict):
    """
    Applies the Hopcroft-Karp algorithm to find the maximum bipartite matching.
    Ensures correct data structure usage.
    """
    matching = bipartite.maximum_matching(G)
    filtered_matching = {rec: cand for rec, cand in matching.items() if rec in recruiters_dict}
    return filtered_matching, recruiters_dict, candidates_dict


def greedy_time_slot_assignment(matching, recruiters_dict, candidates_dict):
    """
    Assigns candidates to the earliest available recruiter time slots using a greedy approach,
    while correctly handling schedules spanning midnight and multiple slots per person.
    """
    final_schedule = []

    for recruiter, candidate in matching.items():
        rec_slots = recruiters_dict[recruiter]
        cand_slots = candidates_dict[candidate]

        best_start = None
        best_end = None

        for rec_start, rec_end in rec_slots:
            for cand_start, cand_end in cand_slots:
                # Convert times to datetime for proper comparison
                rec_start_dt = datetime.combine(datetime.today(), rec_start)
                rec_end_dt = datetime.combine(datetime.today(), rec_end)
                cand_start_dt = datetime.combine(datetime.today(), cand_start)
                cand_end_dt = datetime.combine(datetime.today(), cand_end)

                # Handle overnight time
                if rec_end_dt < rec_start_dt:
                    rec_end_dt += timedelta(days=1)
                if cand_end_dt < cand_start_dt:
                    cand_end_dt += timedelta(days=1)

                # Find the overlap
                start_time = max(rec_start_dt, cand_start_dt)
                end_time = min(rec_end_dt, cand_end_dt)

                if start_time < end_time:  # Valid slot
                    if best_start is None or start_time < best_start:  # Pick earliest slot
                        best_start, best_end = start_time, end_time

        if best_start and best_end:
            final_schedule.append((recruiter, candidate, best_start.time(), best_end.time()))

    return final_schedule


def plot_bipartite_graph(G, recruiters_dict, candidates_dict, ax):
    """
    Plots the bipartite graph using Matplotlib on the provided ax.
    """
    if not G.edges:
        ax.text(0.5, 0.5, "No Matches Found", ha="center", va="center", fontsize=12, color="red")
        return

    pos = nx.bipartite_layout(G, list(recruiters_dict.keys()))
    node_colors = ["lightblue" if node in recruiters_dict else "lightgreen" for node in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray",
            node_size=3000, font_size=10, ax=ax)
