import streamlit as st
import math

def factorial(n):
    return math.factorial(n)

# M/M/1 Model
def mm1_p0(rho):
    return 1 - rho

def mm1_lq(lambda_, mu):
    rho = lambda_ / mu
    return (rho ** 2) / (1 - rho)

def mm1_pn(rho, n):
    return (1 - rho) * (rho ** n)

def mm1_wq(lq, lambda_):
    return lq / lambda_

# M/G/1 Model
def mg1_lq(lambda_, mu, sigma):
    rho = lambda_ / mu
    return (lambda_**2 * sigma**2 + rho**2) / (2 * (1 - rho))

# M/M/c Model
def calculate_p0_mmc(lambda_, mu, c):
    rho = lambda_ / (c * mu)
    sum_term = sum((lambda_ / mu) ** n / factorial(n) for n in range(c))
    sum_term += ((lambda_ / mu) ** c / (factorial(c) * (1 - rho)))
    return 1 / sum_term

def calculate_lq_mmc(lambda_, mu, c, p0):
    rho = lambda_ / (c * mu)
    return (p0 * (lambda_ / mu) ** c * rho) / (factorial(c) * (1 - rho) ** 2)

# M/G/c Model
def calculate_lq_mgc(lambda_, mu, c, sigma, p0):
    lq_mmc = calculate_lq_mmc(lambda_, mu, c, p0)
    c_s2 = (sigma ** 2) * (mu ** 2)
    return ((c_s2 + 1) * lq_mmc) / 2

# G/G/c Model
def calculate_lq_ggc(lambda_, mu, c, sigma, ca):
    p0 = calculate_p0_mmc(lambda_, mu, c)
    lq_mmc = calculate_lq_mmc(lambda_, mu, c, p0)
    c_s2 = (sigma ** 2) * (mu ** 2)
    return (lambda_ / mu) ** 2 * (ca ** 2 + c_s2) / (2 * (1 - (lambda_ / (c * mu)))) * lq_mmc

# General formulas
def calculate_ws(wq, mu):
    return wq + (1 / mu)

def calculate_ls(lq, lambda_, mu):
    return lq + (lambda_ / mu)

# Streamlit UI
st.title("Queueing Model Calculator")

queue_model = st.radio("Select Queueing Model:", ("M/M/1", "M/G/1", "M/M/c", "M/G/c", "G/G/c"))

lambda_ = st.number_input("Enter Arrival Rate (λ):", min_value=0.1, value=5.0)
mu = st.number_input("Enter Service Rate (μ):", min_value=0.1, value=3.0)

if queue_model in ["M/M/c", "M/G/c", "G/G/c"]:
    c = st.number_input("Enter Number of Servers (c):", min_value=1, value=2)

if queue_model in ["M/G/1", "M/G/c", "G/G/c"]:
    sigma = st.number_input("Enter Service Time Standard Deviation (σ):", min_value=0.0, value=1.0)

if queue_model == "G/G/c":
    ca = st.number_input("Enter Coefficient of Variation of Arrival Time (Cₐ²):", min_value=0.0, value=1.0)

n = 10

if st.button("Calculate"):
    rho = lambda_ / (c * mu) if queue_model in ["M/M/c", "M/G/c", "G/G/c"] else lambda_ / mu

    if rho >= 1:
        st.error("System is unstable (ρ ≥ 1). Increase servers or service rate.")
    else:
        if queue_model == "M/M/1":
            p0 = mm1_p0(rho)
            lq = mm1_lq(lambda_, mu)
            wq = mm1_wq(lq, lambda_)
            ws = calculate_ws(wq, mu)
            ls = calculate_ls(lq, lambda_, mu)
            pn = mm1_pn(rho, n)
            st.write(f"### **Results for M/M/1**")

        elif queue_model == "M/G/1":
            p0 = mm1_p0(rho)
            lq = mg1_lq(lambda_, mu, sigma)
            wq = mm1_wq(lq, lambda_)
            ws = calculate_ws(wq, mu)
            ls = calculate_ls(lq, lambda_, mu)
            pn = mm1_pn(rho, n)
            st.write(f"### **Results for M/G/1**")

        elif queue_model == "M/M/c":
            p0 = calculate_p0_mmc(lambda_, mu, c)
            lq = calculate_lq_mmc(lambda_, mu, c, p0)
            wq = mm1_wq(lq, lambda_)
            ws = calculate_ws(wq, mu)
            ls = calculate_ls(lq, lambda_, mu)
            pn = mm1_pn(rho, n)
            st.write(f"### **Results for M/M/c**")

        elif queue_model == "M/G/c":
            p0 = calculate_p0_mmc(lambda_, mu, c)
            lq = calculate_lq_mgc(lambda_, mu, c, sigma, p0)
            wq = mm1_wq(lq, lambda_)
            ws = calculate_ws(wq, mu)
            ls = calculate_ls(lq, lambda_, mu)
            pn = mm1_pn(rho, n)
            st.write(f"### **Results for M/G/c**")

        elif queue_model == "G/G/c":
            p0 = calculate_p0_mmc(lambda_, mu, c)
            lq = calculate_lq_ggc(lambda_, mu, c, sigma, ca)
            wq = mm1_wq(lq, lambda_)
            ws = calculate_ws(wq, mu)
            ls = calculate_ls(lq, lambda_, mu)
            pn = mm1_pn(rho, n)
            st.write(f"### **Results for G/G/c**")

        st.write(f"**Utilization Factor (ρ):** {rho:.4f}")
        st.write(f"**P₀ (Server idleness):** {p0:.4f}")
        st.write(f"**Lq (Average queue length):** {lq:.4f}")
        st.write(f"**Ls (Average number of customers in system):** {ls:.4f}")
        st.write(f"**Wq (Average waiting time in queue):** {wq:.4f} units")
        st.write(f"**Ws (Average time in system):** {ws:.4f} units")
        st.write(f"**Pₙ (Probability of {n} customers in the system):** {pn:.4f}")
