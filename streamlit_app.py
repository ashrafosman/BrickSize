import streamlit as st
import pandas as pd

# Initialize session state for storing use cases
if 'use_cases' not in st.session_state:
    st.session_state.use_cases = []

# Define the lookup table from the image
lookup_table = {
    "ETL - Light Transformations": [20, 70, 150, 300, 1000],
    "ETL - Heavy Transformations": [70, 150, 300, 500, 1000],
    "Ad-Hoc Analytics - Light < 10 Users": [20, 70, 150, 300, 1000],
    "Ad-Hoc Analytics - Med 10 > Users < 20": [20, 70, 150, 300, 1000],
    "Ad-Hoc Analytics - Heavy > 20 Users": [70, 150, 300, 500, 1000],
    "Data Warehouse - Light < 10 Users": [20, 70, 150, 300, 1000],
    "Data Warehouse - Med < 10 Users < 40": [20, 70, 150, 300, 1000],
    "Data Warehouse - Heavy > 40 Users": [150, 300, 1000],
    "ML - Scoring": [20, 70, 150],
    "ML - Training": [70, 150, 300],
    "Streaming": [1000], # Assuming Streaming is always high volume
    "Deep Learning": [20]
}

# Define data volume categories
data_volume_categories = ["<20 GB", "20GB-100GB", "100GB-1TB", "1TB-50TB", ">50TB"]

def calculate_costs(use_case_type, data_volume_index):
    # Get cost from lookup table based on selected use case and data volume
    cost = lookup_table[use_case_type][data_volume_index]
    
    # Placeholder calculations for other components (you can replace these with actual formulas)
    dlt_core_monthly_cost = cost * 1.5
    dlt_advanced_monthly_cost = dlt_core_monthly_cost * 1.8
    notebook_monthly_cost = cost * 2.5
    sql_low_monthly_cost = cost * 3.5
    sql_high_monthly_cost = sql_low_monthly_cost * 2
    model_serving_monthly_cost = cost * 4

    return {
        "Selected Use Case Cost": cost,
        "DLT Core": dlt_core_monthly_cost,
        "DLT Advanced": dlt_advanced_monthly_cost,
        "Notebooks": notebook_monthly_cost,
        "SQL Low": sql_low_monthly_cost,
        "SQL High": sql_high_monthly_cost,
        "Model Serving": model_serving_monthly_cost
    }

st.title("Usecase Discovery Cost Estimate")

# Form for entering a new use case
with st.form("use_case_form"):
    st.header("Add New Use Case")
    
    use_case_name = st.text_input("Use Case Name", "")
    
    # Select Use Case Type (from lookup table)
    use_case_type = st.selectbox("Select Use Case Type", list(lookup_table.keys()))
    
    # Select Data Volume Category (from lookup table)
    data_volume_category = st.selectbox("Select Data Volume Category", data_volume_categories)
    
    # Map data volume category to index in lookup table (for cost calculation)
    data_volume_index = data_volume_categories.index(data_volume_category)
    
    submitted = st.form_submit_button("Add Use Case")
    
    if submitted and use_case_name:
        costs = calculate_costs(use_case_type, data_volume_index)
        
        # Add the new use case to the session state
        st.session_state.use_cases.append((use_case_name, costs))

# Display all use cases and their costs
if st.session_state.use_cases:
    st.header("Use Cases Summary")
    
    total_df_list = []
    
    for name, costs in st.session_state.use_cases:
        st.subheader(f"Use Case: {name}")
        
        cost_df = pd.DataFrame.from_dict(costs, orient='index', columns=['Monthly Cost ($)'])
        cost_df['Annual Cost ($)'] = cost_df['Monthly Cost ($)'] * 12
        
        st.table(cost_df.style.format("${:,.2f}"))
        
        # Prepare data for aggregate table
        total_df_list.append(pd.DataFrame.from_dict({name: costs}, orient='index'))
    
    # Display aggregated totals in a single table
    total_df = pd.concat(total_df_list)
    
    total_df['Total Monthly Cost ($)'] = total_df.sum(axis=1)
    total_df['Total Annual Cost ($)'] = total_df['Total Monthly Cost ($)'] * 12
    
    st.header("Aggregated Use Case Costs")
    
    st.table(total_df.style.format("${:,.2f}"))
