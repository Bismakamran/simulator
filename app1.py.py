# import streamlit as st 
# import numpy as np
# import pandas as pd
# import plotly.express as px
# import matplotlib.pyplot as plt
# from scipy import stats

# st.set_page_config(page_title="Simulator", layout="wide")
# st.title("🧮 Simulator of Queuing System")

# # Input from user
# dist_options = ["Exponential", "Poisson", "Uniform", "Normal"]
# arrival_dist = st.selectbox("Select Arrival Time Distribution", dist_options)
# mean_arrival = st.number_input("Enter mean inter-arrival time:", min_value=0.1, value=4.0)

# service_dist = st.selectbox("Select Service Time Distribution", dist_options)
# mean_service = st.number_input("Enter mean service time:", min_value=0.1, value=3.0)

# data = []  # Initialize here so it can be reused later

# if st.button("Run Simulation"):
#     arrival_times = []
#     service_times = []
#     inter_arrival_times = []
#     cumulative_prob = 0
#     customer = 0

#     def get_random(dist, mean, count=1):
#         if dist == "Exponential":
#             return np.random.exponential(mean, count)
#         elif dist == "Poisson":
#             return np.random.poisson(mean, count)
#         elif dist == "Uniform":
#             low = mean * 0.5
#             high = mean * 1.5
#             return np.random.uniform(low, high, count)
#         elif dist == "Normal":
#             return np.random.normal(mean, mean * 0.2, count)
#         else:
#             return np.zeros(count)

#     while cumulative_prob < 0.999:
#         customer += 1
#         inter_arrival = get_random(arrival_dist, mean_arrival)[0]
#         inter_arrival = max(inter_arrival, 0.01)
#         service_time = get_random(service_dist, mean_service)[0]
#         service_time = max(service_time, 0.01)

#         inter_arrival_times.append(inter_arrival)
#         service_times.append(service_time)
#         arrival_times.append(np.sum(inter_arrival_times))

#         # Stop condition based on exponential assumption
#         cumulative_prob += (1 - np.exp(-inter_arrival / mean_arrival))

#     num_customers = customer
#     data = arrival_times.copy()  # Save for chi-square test

#     start_service = [0.0] * num_customers
#     completion_time = [0.0] * num_customers
#     waiting_time = [0.0] * num_customers
#     turnaround_time = [0.0] * num_customers
#     response_time = [0.0] * num_customers

#     for i in range(num_customers):
#         if i == 0:
#             start_service[i] = arrival_times[i]
#         else:
#             start_service[i] = max(arrival_times[i], completion_time[i - 1])
#         completion_time[i] = start_service[i] + service_times[i]
#         waiting_time[i] = start_service[i] - arrival_times[i]
#         turnaround_time[i] = completion_time[i] - arrival_times[i]
#         response_time[i] = waiting_time[i]

#     total_service_time = sum(service_times)
#     total_time = completion_time[-1] - arrival_times[0]
#     utilization = total_service_time / total_time

#     df = pd.DataFrame({
#         "Customer": list(range(1, num_customers + 1)),
#         "Arrival Time": arrival_times,
#         "Service Time": service_times,
#         "Start Time": start_service,
#         "Completion Time": completion_time,
#         "Waiting Time": waiting_time,
#         "Turnaround Time": turnaround_time,
#         "Response Time": response_time
#     })

#     st.subheader("📋 Simulation Results")
#     st.dataframe(df.style.format(precision=2), width='stretch')

#     st.success(f"✅ Total Customers Simulated: {num_customers}")
#     st.info(f"⚙️ Utilization Factor: **{utilization:.2f}**")

#     # Gantt Chart
#     gantt_data = pd.DataFrame({
#         "Customer": [f"Customer {i+1}" for i in range(num_customers)],
#         "Start": start_service,
#         "Finish": completion_time
#     })

#     st.subheader("📊 Gantt Chart (Customer Service Timeline)")
#     fig = px.timeline(gantt_data, x_start="Start", x_end="Finish", y="Customer", color="Customer",
#                       labels={"Customer": "Customer"}, title="Service Time per Customer")
#     fig.update_yaxes(autorange="reversed")
#     st.plotly_chart(fig, width='stretch')

# # ---------------------- CHI-SQUARE SECTION -----------------------

# if len(data) > 0:
#     st.subheader("📈 Arrival time Chi-Square Goodness of Fit Test")

#     distribution = st.sidebar.selectbox("Select a distribution", 
#         ["Poisson", "Normal", "Binomial", "Exponential", "Gamma2", "Uniform", "Erlang"])
#     meaninput = st.sidebar.number_input("Enter mean of arrival time:", min_value=0.1, value=float(np.mean(data)))

#     # Chi-square bins
#     num_bins = 10
#     hist, bin_edges = np.histogram(data, bins=num_bins)
#     observed_frequencies = hist
#     expected_frequencies = []

#     if distribution == "Poisson":
#         lam = meaninput
#         expected_frequencies = [
#             len(data) * (stats.poisson.cdf(bin_edges[i+1], lam) - stats.poisson.cdf(bin_edges[i], lam))
#             for i in range(num_bins)
#         ]
#     elif distribution == "Normal":
#         mu, sigma = meaninput, np.std(data)
#         expected_frequencies = [
#             len(data) * (stats.norm.cdf(bin_edges[i+1], mu, sigma) - stats.norm.cdf(bin_edges[i], mu, sigma))
#             for i in range(num_bins)
#         ]
#     elif distribution == "Exponential":
#         lam = 1 / meaninput
#         expected_frequencies = [
#             len(data) * (stats.expon.cdf(bin_edges[i+1], scale=1/lam) - stats.expon.cdf(bin_edges[i], scale=1/lam))
#             for i in range(num_bins)
#         ]
#     elif distribution == "Gamma2":
#         shape, scale = 2, meaninput / 2
#         expected_frequencies = [
#             len(data) * (stats.gamma.cdf(bin_edges[i+1], shape, scale=scale) - stats.gamma.cdf(bin_edges[i], shape, scale=scale))
#             for i in range(num_bins)
#         ]
#     elif distribution == "Uniform":
#         a, b = np.min(data), np.max(data)
#         expected_frequencies = [
#             len(data) * (stats.uniform.cdf(bin_edges[i+1], a, b-a) - stats.uniform.cdf(bin_edges[i], a, b-a))
#             for i in range(num_bins)
#         ]

#     expected_frequencies = np.array(expected_frequencies)
#     expected_frequencies *= sum(observed_frequencies) / sum(expected_frequencies)

#     chi_sq_stat, p_value = stats.chisquare(observed_frequencies, expected_frequencies)
#     df_deg = num_bins - 1 - 1
#     alpha = 0.05
#     critical_value = stats.chi2.ppf(1 - alpha, df_deg)

#     st.write("### Chi-Square Test Results")
#     chi_sq_table = pd.DataFrame({
#         "Chi Observed Value": [round(chi_sq_stat, 4)],
#         "Critical Value": [round(critical_value, 4)],
#         "Degrees of Freedom (df)": [df_deg],
#         "Alpha": [alpha],
#         "P-Value": [round(p_value, 4)]
#     })
#     st.table(chi_sq_table)

#     if p_value > alpha:
#         st.success(f"✅ The data follows a {distribution} distribution (Fail to reject H0).")
#     else:
#         st.error(f"❌ The data does not follow a {distribution} distribution (Reject H0).")

#     # Histogram Plot
#     fig, ax = plt.subplots(figsize=(8, 5))
#     ax.hist(data, bins=num_bins, alpha=0.6, color="skyblue", edgecolor="black", label="Observed")
#     ax.plot((bin_edges[:-1] + bin_edges[1:]) / 2, expected_frequencies, "ro--", label="Expected")
#     ax.set_title(f"Observed vs Expected - {distribution}")
#     ax.set_xlabel("Arrival Time")
#     ax.set_ylabel("Frequency")
#     ax.legend()
#     st.pyplot(fig)


import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hand Simulation", layout="wide")
st.title("🧮 Hand Simulation of Queuing System")

# Input from user
dist_options = ["Exponential", "Poisson", "Uniform", "Normal"]
arrival_dist = st.selectbox("Select Arrival Time Distribution", dist_options)
service_dist = st.selectbox("Select Service Time Distribution", dist_options)

mean_arrival = st.number_input("Enter mean inter-arrival time:", min_value=0.1)
mean_service = st.number_input("Enter mean service time:", min_value=0.1)

def get_random(dist, mean, count=1):
    if dist == "Exponential":
        return np.random.exponential(mean, count)
    elif dist == "Poisson":
        return np.random.poisson(mean, count)
    elif dist == "Uniform":
        low = mean * 0.5
        high = mean * 1.5
        return np.random.uniform(low, high, count)
    elif dist == "Normal":
        return np.random.normal(mean, mean * 0.2, count)
    else:
        return np.zeros(count)

def chi_square_test(data, dist, mean, title):
    st.subheader(f"📈 Chi-Square Goodness of Fit: {title}")
    num_bins = 10
    hist, bin_edges = np.histogram(data, bins=num_bins)
    observed = hist

    if dist == "Exponential":
        lambda_exp = 1 / mean
        expected = [
            len(data) * (stats.expon.cdf(bin_edges[i+1], scale=1/lambda_exp) -
                         stats.expon.cdf(bin_edges[i], scale=1/lambda_exp))
            for i in range(len(bin_edges)-1)
        ]
    elif dist == "Poisson":
        expected = [
            len(data) * (stats.poisson.cdf(bin_edges[i+1], mean) -
                         stats.poisson.cdf(bin_edges[i], mean))
            for i in range(len(bin_edges)-1)
        ]
    elif dist == "Normal":
        std = np.std(data)
        expected = [
            len(data) * (stats.norm.cdf(bin_edges[i+1], mean, std) -
                         stats.norm.cdf(bin_edges[i], mean, std))
            for i in range(len(bin_edges)-1)
        ]
    elif dist == "Uniform":
        a, b = min(data), max(data)
        expected = [
            len(data) * (stats.uniform.cdf(bin_edges[i+1], a, b-a) -
                         stats.uniform.cdf(bin_edges[i], a, b-a))
            for i in range(len(bin_edges)-1)
        ]
    else:
        expected = [1] * len(observed)

    expected = np.array(expected)
    expected *= sum(observed) / sum(expected)  # Normalize

    chi_stat, p_val = stats.chisquare(f_obs=observed, f_exp=expected)
    df_chi = len(observed) - 1 - 1  # bins - 1 - parameters
    critical_val = stats.chi2.ppf(0.95, df_chi)

    # Show results
    st.write(f"**Chi-Square Statistic:** {chi_stat:.4f}")
    st.write(f"**Critical Value (α=0.05):** {critical_val:.4f}")
    st.write(f"**Degrees of Freedom:** {df_chi}")
    st.write(f"**P-Value:** {p_val:.4f}")
    if p_val > 0.05:
        st.success("✅ The data fits the distribution (Fail to reject H₀)")
    else:
        st.error("❌ The data does not fit the distribution (Reject H₀)")

    # Plot
    fig, ax = plt.subplots()
    ax.hist(data, bins=bin_edges, alpha=0.6, label="Observed", edgecolor="black")
    ax.plot((bin_edges[:-1] + bin_edges[1:]) / 2, expected, 'ro--', label="Expected")
    ax.set_title(f"{title} Histogram: Observed vs Expected")
    ax.legend()
    st.pyplot(fig)


if st.button("Run Simulation"):
    arrival_times = []
    service_times = []
    inter_arrival_times = []
    cumulative_prob = 0
    customer = 0

    while cumulative_prob < 1:
        customer += 1
        inter_arrival = get_random(arrival_dist, mean_arrival)[0]
        inter_arrival = max(inter_arrival, 0.01)

        service_time = get_random(service_dist, mean_service)[0]
        service_time = max(service_time, 0.01)

        inter_arrival_times.append(inter_arrival)
        service_times.append(service_time)
        arrival_times.append(np.sum(inter_arrival_times))
        cumulative_prob += (1 - np.exp(-inter_arrival / mean_arrival))

    num_customers = customer
    start_service = [0.0] * num_customers
    completion_time = [0.0] * num_customers
    waiting_time = [0.0] * num_customers
    turnaround_time = [0.0] * num_customers
    response_time = [0.0] * num_customers

    for i in range(num_customers):
        if i == 0:
            start_service[i] = arrival_times[i]
        else:
            start_service[i] = max(arrival_times[i], completion_time[i - 1])
        completion_time[i] = start_service[i] + service_times[i]
        waiting_time[i] = start_service[i] - arrival_times[i]
        turnaround_time[i] = completion_time[i] - arrival_times[i]
        response_time[i] = waiting_time[i]

    total_service_time = sum(service_times)
    total_time = completion_time[-1] - arrival_times[0]
    utilization = total_service_time / total_time

    df = pd.DataFrame({
        "Customer": list(range(1, num_customers + 1)),
        "Arrival Time": arrival_times,
        "Service Time": service_times,
        "Start Time": start_service,
        "Completion Time": completion_time,
        "Waiting Time": waiting_time,
        "Turnaround Time": turnaround_time,
        "Response Time": response_time
    })

    st.subheader("📋 Simulation Results")
    st.dataframe(df.style.format(precision=2), width='stretch')
    st.success(f"✅ Total Customers Simulated: {num_customers}")
    st.info(f"⚙️ Utilization Factor: **{utilization:.2f}**")

    # Gantt Chart
    gantt_data = pd.DataFrame({
        "Customer": [f"Customer {i+1}" for i in range(num_customers)],
        "Start": start_service,
        "Finish": completion_time
    })

    st.subheader("📊 Gantt Chart (Customer Service Timeline)")
    fig = px.timeline(gantt_data, x_start="Start", x_end="Finish", y="Customer", color="Customer")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, width='stretch')

    # Chi-square test for arrival time and service time
    chi_square_test(inter_arrival_times, arrival_dist, mean_arrival, "Arrival Time")
    chi_square_test(service_times, service_dist, mean_service, "Service Time")
























