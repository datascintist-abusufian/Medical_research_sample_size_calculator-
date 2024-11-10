import streamlit as st
import plotly.graph_objects as go
from utils import calculate_sample_size, calculate_effect_size, create_power_curve

# Set page config
st.set_page_config(
    page_title="Medical Research Sample Size Calculator by Md Abu Sufian",
    page_icon="🏥",
    layout="wide"
)

# Display GIFs at the top center
col_a, col_b, col_c = st.columns([1, 3, 1])
with col_b:
    st.image("/mnt/data/hist_errorbars_nn10_sd1_mu00_mu11_nsims10.gif", use_column_width=True)
    
# Title and introduction
st.title("🏥 Medical Research Sample Size Calculator by Md Abu Sufian")
st.markdown("""
This dashboard helps medical science researchers to determine the appropriate sample size for medical studies.
It supports both parallel group and paired study designs..
""")

# Create two columns for input parameters
col1, col2 = st.columns(2)

with col1:
    st.subheader("Study Parameters")
    
    study_type = st.radio(
        "Study Design",
        ["parallel", "paired"],
        help="Choose between parallel group or paired study design"
    )
    
    effect_size = st.slider(
        "Effect Size (Cohen's d)",
        min_value=0.1,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="Standardized effect size (0.2: small, 0.5: medium, 0.8: large)"
    )
    
    alpha = st.slider(
        "Significance Level (α)",
        min_value=0.01,
        max_value=0.10,
        value=0.05,
        step=0.01,
        help="Type I error rate"
    )

with col2:
    st.subheader("Additional Settings")
    
    power = st.slider(
        "Statistical Power (1-β)",
        min_value=0.5,
        max_value=0.99,
        value=0.80,
        step=0.01,
        help="1 minus Type II error rate"
    )
    
    if study_type == "parallel":
        allocation_ratio = st.slider(
            "Allocation Ratio (n2/n1)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            help="Ratio of control to treatment group sizes"
        )
    else:
        allocation_ratio = 1.0

# Calculate sample size
n1, n2 = calculate_sample_size(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    allocation_ratio=allocation_ratio,
    study_type=study_type
)

# Display results
st.subheader("📊 Results")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Treatment Group Size", n1)
with col4:
    st.metric("Control Group Size", n2)
with col5:
    st.metric("Total Sample Size", n1 + n2)

# Create power curve
powers, sample_sizes = create_power_curve(effect_size, alpha, allocation_ratio, study_type)

# Plot power curve
st.subheader("📈 Power Analysis")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=powers,
    y=sample_sizes,
    mode='lines+markers',
    name='Required Sample Size'
))
fig.update_layout(
    title="Power vs. Required Sample Size",
    xaxis_title="Statistical Power (1-β)",
    yaxis_title="Required Sample Size (per group)",
    hovermode='x'
)
st.plotly_chart(fig, use_container_width=True)

# Effect size calculator
st.subheader("🔍 Effect Size Calculator")
st.markdown("Use this section to calculate the standardized effect size (Cohen's d) from your raw data.")

col6, col7, col8 = st.columns(3)

with col6:
    mean1 = st.number_input("Group 1 Mean", value=0.0)
with col7:
    mean2 = st.number_input("Group 2 Mean", value=0.0)
with col8:
    pooled_sd = st.number_input("Pooled Standard Deviation", value=1.0, min_value=0.1)

calculated_effect_size = calculate_effect_size(mean1, mean2, pooled_sd)
st.metric("Calculated Effect Size", round(calculated_effect_size, 3))

# Add explanatory notes
st.subheader("📝 Notes")
st.markdown("""
* **Effect Size Guidelines**:
  * Small effect: 0.2
  * Medium effect: 0.5
  * Large effect: 0.8

* **Power**: Typically set to 0.80 (80%) or higher

* **Significance Level**: Typically set to 0.05 (5%)

* **Study Types**:
  * Parallel: Two independent groups
  * Paired: Same subjects measured twice
""")

# Footer
st.markdown("---")
st.markdown("Created for medical researchers and statisticians to assist in study planning © 2024 Md Abu Sufian. All rights reserved,UK.")
