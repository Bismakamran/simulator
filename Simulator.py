import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from scipy import stats
from scipy.stats import chisquare
import os

# --- Streamlit Setup ---
st.set_page_config(page_title="Patient Queue Simulator", page_icon="🩺", layout="wide")
st.title("👩‍⚕️ Patient Queue Simulator (Time + Optional Cumulative Probability)")

st.markdown("""
Simulate patient arrivals and services using selected distributions.
Simulation runs for the specified **Simulation Time**.
Optionally, enable **Cumulative Probability (C.P.) check** to stop when CDF reaches 1.
""")

# --- About Section ---
with st.expander("About this app", expanded=False):
    st.write(
        """
        This interactive simulator models a single-queue service system with configurable
        arrival and service time distributions. It computes core performance metrics,
        visualizes timelines with a Gantt chart, and includes optional goodness-of-fit
        checks using the Chi-square test.
        """
    )

# --- Secrets / Auth (optional) ---
# Read token from Streamlit secrets or environment variable if provided
AUTH_TOKEN = st.secrets.get("REDY_AUTH", os.getenv("REDY_AUTH"))
DB_USERNAME = st.secrets.get("DB_USERNAME")
DB_TOKEN = st.secrets.get("DB_TOKEN")
SOME_SECTION_KEY = None
try:
    SOME_SECTION_KEY = st.secrets.get("some_section", {}).get("some_key")
except Exception:
    SOME_SECTION_KEY = None

with st.sidebar:
    if AUTH_TOKEN:
        st.info("Auth token detected and loaded from secrets.")
    if DB_USERNAME or DB_TOKEN:
        masked_user = (DB_USERNAME[:2] + "***") if DB_USERNAME else "(none)"
        masked_token = ("***" + DB_TOKEN[-3:]) if DB_TOKEN and len(DB_TOKEN) >= 3 else "(none)"
        st.success(f"DB creds loaded (user: {masked_user}, token: {masked_token})")
    if SOME_SECTION_KEY is not None:
        st.write("Additional config loaded (some_section.some_key)")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    simulation_time = st.number_input("⏱️ Total Simulation Time (minutes)", min_value=1, value=60)
    enable_cp = st.checkbox("✅ Enable Cumulative Probability Stop")

    st.subheader("📥 Arrival")
    mean_arrival = st.number_input("Mean Inter-arrival Time", min_value=0.1, value=5.0)
    arrival_dist = st.selectbox("Arrival Distribution", ["Exponential", "Poisson", "Uniform", "Normal"])

    st.subheader("🧾 Service")
    mean_service = st.number_input("Mean Service Time", min_value=0.1, value=3.0)
    service_dist = st.selectbox("Service Distribution", ["Exponential", "Poisson", "Uniform", "Normal"])

# --- Distribution Generator ---
def generate_time(dist, mean):
    if dist == "Exponential":
        return np.random.exponential(scale=mean)
    elif dist == "Poisson":
        return np.random.poisson(lam=mean)
    elif dist == "Uniform":
        return np.random.uniform(low=mean * 0.5, high=mean * 1.5)
    elif dist == "Normal":
        return max(0, np.random.normal(loc=mean, scale=mean * 0.3))
    return mean

# --- CDF Helper ---
def get_cdf(x, dist, mean):
    if dist == "Exponential":
        return stats.expon.cdf(x, scale=mean)
    elif dist == "Poisson":
        return stats.poisson.cdf(x, mu=mean)
    elif dist == "Uniform":
        return stats.uniform.cdf(x, loc=mean * 0.5, scale=mean)
    elif dist == "Normal":
        return stats.norm.cdf(x, loc=mean, scale=mean * 0.3)
    return 0

# --- Run Simulation ---
if st.button("▶️ Run Simulation"):
    arrival_times = []
    service_times = []
    arrival_cp = []
    service_cp = []

    current_time = 0
    total_cp_a = total_cp_s = 0

    while current_time < simulation_time:
        a = generate_time(arrival_dist, mean_arrival)
        s = generate_time(service_dist, mean_service)

        cp_a = get_cdf(a, arrival_dist, mean_arrival)
        cp_s = get_cdf(s, service_dist, mean_service)

        if enable_cp:
            if total_cp_a + cp_a > 1 and total_cp_s + cp_s > 1:
                break
            total_cp_a += cp_a
            total_cp_s += cp_s
            arrival_cp.append(round(total_cp_a, 4))
            service_cp.append(round(total_cp_s, 4))
        else:
            arrival_cp.append(None)
            service_cp.append(None)

        current_time += a
        if current_time > simulation_time:
            break

        arrival_times.append(round(current_time, 2))
        service_times.append(round(s, 2))

    # --- Queue Calculations ---
    n = len(arrival_times)
    start_time = []
    complete_time = []
    waiting_time = []
    turnaround_time = []
    response_time = []

    for i in range(n):
        start = arrival_times[i] if i == 0 else max(arrival_times[i], complete_time[i-1])
        end = start + service_times[i]
        wait = start - arrival_times[i]
        tat = end - arrival_times[i]

        start_time.append(round(start, 2))
        complete_time.append(round(end, 2))
        waiting_time.append(round(wait, 2))
        turnaround_time.append(round(tat, 2))
        response_time.append(round(wait, 2))

    # --- Summary Metrics ---
    df = pd.DataFrame({
        "Patient": range(1, n+1),
        "Arrival Time": arrival_times,
        "Service Time": service_times,
        "Start Time": start_time,
        "Completion Time": complete_time,
        "Waiting Time": waiting_time,
        "Turnaround Time": turnaround_time,
        "Response Time": response_time
    })

    if enable_cp:
        df["Arrival C.P."] = arrival_cp
        df["Service C.P."] = service_cp

    st.subheader("📋 Simulation Results")
    st.dataframe(df.style.format(precision=2), use_container_width=True)

    # --- Average Stats ---
    st.markdown("### 📊 Averages Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg. Arrival Time", f"{np.mean(arrival_times):.2f}")
        st.metric("Avg. Service Time", f"{np.mean(service_times):.2f}")
    with col2:
        st.metric("Avg. Turnaround Time", f"{np.mean(turnaround_time):.2f}")
        st.metric("Avg. Waiting Time", f"{np.mean(waiting_time):.2f}")
    with col3:
        st.metric("Avg. Response Time", f"{np.mean(response_time):.2f}")
        st.metric("Utilization", f"{(sum(service_times)/(complete_time[-1]-arrival_times[0])):.2f}")

    # --- Gantt Chart ---
    st.subheader("📅 Patient Timeline (Gantt Chart)")
    gantt_data = [{
        'Task': f'Patient {i+1}',
        'Start': arrival_times[i],
        'Finish': complete_time[i],
        'Resource': 'Service'
    } for i in range(n)]
    fig = ff.create_gantt(gantt_data, index_col='Resource', show_colorbar=True, group_tasks=True)
    st.plotly_chart(fig, use_container_width=True)
enable_playback = st.checkbox("🎥 Enable Real-Time Playback")

if enable_playback:
    import time  # ensure this is imported at the top if not already

    st.subheader("🕒 Real-Time Queue Simulation")
    playback = st.empty()
    for i in range(n):
        with playback.container():
            st.markdown(f"#### ▶️ Now Serving: Patient {i+1}")
            st.markdown(f"- Arrival: `{arrival_times[i]} min`\n- Service Start: `{start_time[i]} min`\n- Completion: `{complete_time[i]} min`")
            st.progress(min(int((service_times[i] / max(service_times)) * 100), 100))
        time.sleep(0.5)

    # --- Histograms ---
    st.subheader("📈 Distribution Histograms")
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots()
        sns.histplot(arrival_times, kde=True, ax=ax1, bins=10, color="skyblue")
        ax1.set_title("Arrival Time")
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots()
        sns.histplot(service_times, kde=True, ax=ax2, bins=10, color="salmon")
        ax2.set_title("Service Time")
        st.pyplot(fig2)

    # --- Chi-square Test ---
    st.subheader("🧪 Chi-Square Goodness-of-Fit")

    def chi_square_test(data, dist_name, mean):
        observed, bins = np.histogram(data, bins='auto')
        expected = []
        for i in range(len(bins)-1):
            low, high = bins[i], bins[i+1]
            if dist_name == "Exponential":
                prob = stats.expon.cdf(high, scale=mean) - stats.expon.cdf(low, scale=mean)
            elif dist_name == "Poisson":
                prob = stats.poisson.cdf(high, mu=mean) - stats.poisson.cdf(low, mu=mean)
            elif dist_name == "Uniform":
                prob = stats.uniform.cdf(high, loc=mean*0.5, scale=mean) - stats.uniform.cdf(low, loc=mean*0.5, scale=mean)
            elif dist_name == "Normal":
                prob = stats.norm.cdf(high, loc=mean, scale=mean*0.3) - stats.norm.cdf(low, loc=mean, scale=mean*0.3)
            else:
                prob = 0
            expected.append(prob)

        expected = np.array(expected) * sum(observed) / np.sum(expected)
        chi_stat, p = chisquare(observed, expected)
        return round(chi_stat, 2), round(p, 4), "Accepted" if p > 0.05 else "Rejected"

    a_stat, a_p, a_result = chi_square_test(arrival_times, arrival_dist, mean_arrival)
    s_stat, s_p, s_result = chi_square_test(service_times, service_dist, mean_service)

    chi_df = pd.DataFrame({
        "Test": ["Arrival Time", "Service Time"],
        "Chi-Square": [a_stat, s_stat],
        "P-Value": [a_p, s_p],
        "Result": [a_result, s_result]
    })
    st.dataframe(chi_df, use_container_width=True)

    # --- Download ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "queue_simulation.csv", "text/csv")
# --- Real-time Queue Playback ---
# --- Real-time Queue Playback ---
