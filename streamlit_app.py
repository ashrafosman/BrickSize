import streamlit as st
import pandas as pd

# Initialize session state for storing use cases
if 'use_cases' not in st.session_state:
    st.session_state.use_cases = []

# Define the lookup table from the image (cost per day)
lookup_table = {
    "ETL - Light Transformations": [20, 70, 150, 300, 1000],
    "ETL - Heavy Transformations": [70, 150, 300, 500, 1000],
    "Ad-Hoc Analytics - Light < 10 Users": [20, 70, 150, 300, 1000],
    "Ad-Hoc Analytics - Med 10 > Users < 20": [20, 70, 150, 300, 1000],
    "Ad-Hoc Analytics - Heavy > 20 Users": [70, 150, 300, 500, 1000],
    "Data Warehouse - Light < 10 Users": [20, 70, 150, 300, 1000],
    "Data Warehouse - Med < 10 Users < 40": [20, 70, 150, 300, 1000],
    "Data Warehouse - Heavy > 40 Users": [150, 300, 1000],
    "ML - Scoring": [20, 70, 150],           # Only three data volumes available
    "ML - Training": [70, 150, 300],         # Only three data volumes available
    "Streaming": [1000],                     # Only one data volume available
    "Deep Learning": [20]                    # Only one data volume available
}

# Define data volume categories
data_volume_categories = ["<20 GB", "20GB-100GB", "100GB-1TB", "1TB-50TB", ">50TB"]

def calculate_costs(use_case_type, data_volume_index):
    # Ensure that we don't try to access an index that doesn't exist in the lookup table
    try:
        daily_cost = lookup_table[use_case_type][data_volume_index]
    except IndexError:
        st.error(f"The selected data volume is not available for '{use_case_type}'. Please select a valid volume.")
        return None
    
    # Calculate monthly and annual costs based on daily cost
    monthly_cost = daily_cost * 30
    annual_cost = daily_cost * 365

    return {
        "Use Case Type": use_case_type,
        "Daily Cost ($)": daily_cost,
        "Monthly Cost ($)": monthly_cost,
        "Annual Cost ($)": annual_cost
    }

st.title("Usecase Discovery Cost Estimate")

# Instructions for users
st.markdown("""
### Instructions:
1. **Select a Use Case Type**: Choose a use case type from the dropdown (e.g., ETL - Light Transformations).
2. **Select Data Volume Category**: Choose a data volume category that matches your expected daily data usage.
3. **Add Use Case**: After selecting both options and naming your use case, click 'Add Use Case' to calculate and store the cost.
4. **View Costs**: The app will display individual use case costs (daily/monthly/annual) and aggregate them for all entered use cases.
""")

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
        
        if costs:
            # Add the new use case to the session state
            st.session_state.use_cases.append((use_case_name, costs))

# Display all use cases and their costs
if st.session_state.use_cases:
    st.header("Use Cases Summary")
    
    total_daily_cost = total_monthly_cost = total_annual_cost = 0
    
    # Create an empty DataFrame to store all use case details for aggregation
    aggregated_df_list = []
    
    for name, costs in st.session_state.use_cases:
        st.subheader(f"Use Case: {name}")
        
        # Ensure all values are numeric before formatting them for display
        cost_df = pd.DataFrame.from_dict(costs, orient='index', columns=['Cost ($)'])
        
        # Convert any non-numeric values to NaN and skip formatting them as currency
        cost_df["Cost ($)"] = pd.to_numeric(cost_df["Cost ($)"], errors='coerce')
        
        st.table(cost_df.style.format("${:,.2f}"))
        
        # Aggregate total costs across all use cases
        total_daily_cost += costs["Daily Cost ($)"]
        total_monthly_cost += costs["Monthly Cost ($)"]
        total_annual_cost += costs["Annual Cost ($)"]
        
        # Add this use case's details to the aggregate list
        aggregated_df_list.append(pd.DataFrame({
            "Use Case Name": [name],
            "Use Case Type": [costs["Use Case Type"]],
            "Daily Cost ($)": [costs["Daily Cost ($)"]],
            "Monthly Cost ($)": [costs["Monthly Cost ($)"]],
            "Annual Cost ($)": [costs["Annual Cost ($)"]]
        }))
    
    # Concatenate all DataFrames into one aggregated DataFrame
    aggregated_df = pd.concat(aggregated_df_list)

    # Display aggregated totals at the bottom
    st.header("Aggregated Use Case Costs")
    
    # Display the full aggregated DataFrame with all individual use case details at the bottom
    if not aggregated_df.empty:
        st.table(aggregated_df.style.format({
            "Daily Cost ($)": "${:,.2f}", 
            "Monthly Cost ($)": "${:,.2f}", 
            "Annual Cost ($)": "${:,.2f}"
        }))
    
    # Display overall totals below the table
    st.markdown(f"**Total Daily Cost:** ${total_daily_cost:,.2f}")
    st.markdown(f"**Total Monthly Cost:** ${total_monthly_cost:,.2f}")
    st.markdown(f"**Total Annual Cost:** ${total_annual_cost:,.2f}")
