import streamlit as st
import pandas as pd

# Initialize session state for storing use cases
if 'use_cases' not in st.session_state:
    st.session_state.use_cases = []

def calculate_costs(stream_hours, transformation_complexity, users, user_hours, 
                    warehouse_hours, concurrent_queries, models, peak_queries, model_hours):
    # Placeholder calculations - replace with actual formulas
    jobs_monthly_cost = stream_hours * 30 * 17.1
    dlt_core_monthly_cost = stream_hours * 30 * 34.1
    dlt_advanced_monthly_cost = dlt_core_monthly_cost * 1.8
    notebook_monthly_cost = users * user_hours * 22 * 8.25
    sql_low_monthly_cost = warehouse_hours * 30 * concurrent_queries * 35
    sql_high_monthly_cost = sql_low_monthly_cost * 2
    model_serving_monthly_cost = models * peak_queries * model_hours * 30 * 0.35

    return {
        "Stream Processing": jobs_monthly_cost,
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
    
    # Stream Processing Section
    st.subheader("Stream Processing")
    stream_hours = st.slider("Stream Hours per Day", 0, 24, 24)
    transformation_complexity = st.selectbox(
        "Transformation Complexity", 
        ["Simple", "Moderate", "Complex"],
        format_func=lambda x: f"{x}: {['Basic selects, filters', 'Aggregations/groups, small, single-key joins', 'Large/multi-key joins, regex parsing, explode, UDFs'][['Simple', 'Moderate', 'Complex'].index(x)]}"
    )
    
    # Building Pipelines & Data Science Section
    st.subheader("Building Pipelines & Data Science")
    users = st.number_input("Number of Users", min_value=1, value=10)
    user_hours = st.slider("User Active Hours per Day", 0, 24, 8)
    
    # Warehousing & SQL Analysis Section
    st.subheader("Warehousing & SQL Analysis")
    warehouse_hours = st.slider("Warehouse Query Hours per Day", 0, 24, 8)
    concurrent_queries = st.number_input("Concurrent Queries", min_value=0.1, value=1.0, step=0.1)
    
    # Model Serving Section
    st.subheader("Model Serving")
    models = st.number_input("Number of Models", min_value=1, value=1)
    peak_queries = st.number_input("Peak Queries", min_value=1, value=100)
    model_hours = st.slider("Model Request Hours per Day", 0, 24, 24)
    
    submitted = st.form_submit_button("Add Use Case")
    
    if submitted and use_case_name:
        costs = calculate_costs(stream_hours,
                                ["Simple", "Moderate", "Complex"].index(transformation_complexity) + 1,
                                users, user_hours,
                                warehouse_hours, concurrent_queries,
                                models, peak_queries, model_hours)
        
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
    
