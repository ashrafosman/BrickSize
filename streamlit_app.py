import streamlit as st
import pandas as pd

def calculate_costs(stream_hours, transformation_complexity, users, user_hours, 
                    warehouse_hours, concurrent_queries, models, peak_queries, model_hours):
    # Placeholder calculations - replace with actual formulas
    stream_cost = stream_hours * 100
    dlt_core_cost = transformation_complexity * 1000
    dlt_advanced_cost = dlt_core_cost * 1.8
    notebook_cost = users * user_hours * 10
    sql_low_cost = warehouse_hours * concurrent_queries * 70
    sql_high_cost = sql_low_cost * 2
    model_serving_cost = models * peak_queries * model_hours * 5

    return {
        "Stream Processing": stream_cost,
        "DLT Core": dlt_core_cost,
        "DLT Advanced": dlt_advanced_cost,
        "Notebooks": notebook_cost,
        "SQL Low": sql_low_cost,
        "SQL High": sql_high_cost,
        "Model Serving": model_serving_cost
    }

st.title("Usecase Discovery Cost Estimate")

st.header("Stream Processing")
stream_hours = st.slider("Hours per day the stream is up", 0, 24, 24)
transformation_complexity = st.selectbox("Transformation complexity", 
                                         ["Simple", "Moderate", "Complex"], 
                                         format_func=lambda x: f"{x}: {['Basic selects, filters', 'Aggregations/groups, small, single-key joins', 'Large/multi-key joins, regex parsing, explode, UDFs'][['Simple', 'Moderate', 'Complex'].index(x)]}")

st.header("Building Pipelines & Data Science")
users = st.number_input("Number of users/developers/engineers/data scientists", min_value=1, value=10)
user_hours = st.slider("Hours per workday users are active", 0, 24, 8)

st.header("Warehousing & SQL Analysis")
warehouse_hours = st.slider("Hours per day of active querying", 0, 24, 8)
concurrent_queries = st.number_input("Average concurrent queries", min_value=0.0, value=1.0, step=0.1)

st.header("Model Serving")
models = st.number_input("Number of models being served", min_value=1, value=1)
peak_queries = st.number_input("Maximum queries during peak time", min_value=1, value=100)
model_hours = st.slider("Hours per day model receives requests", 0, 24, 24)

costs = calculate_costs(stream_hours, ["Simple", "Moderate", "Complex"].index(transformation_complexity) + 1,
                        users, user_hours, warehouse_hours, concurrent_queries, 
                        models, peak_queries, model_hours)

st.header("Estimated Costs")
cost_df = pd.DataFrame.from_dict(costs, orient='index', columns=['Monthly Cost ($)'])
cost_df['Annual Cost ($)'] = cost_df['Monthly Cost ($)'] * 12
st.table(cost_df)

total_monthly = cost_df['Monthly Cost ($)'].sum()
total_annual = cost_df['Annual Cost ($)'].sum()

st.markdown(f"**Total Estimated Monthly Cost: ${total_monthly:,.2f}**")
st.markdown(f"**Total Estimated Annual Cost: ${total_annual:,.2f}**")