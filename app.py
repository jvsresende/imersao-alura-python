import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Data Visualization Dashboard',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='collapsed',
)

df = pd.read_csv("dados-imersao-final.csv")
st.sidebar.header('Filter 🔍')

available_years = df['work_year'].unique()
selected_years = st.sidebar.multiselect('Work Year',available_years, default=available_years)

experience_available = df['experience_level'].unique()
selected_experience = st.sidebar.multiselect('Experience Level', experience_available, default=experience_available)

available_contracts = df['remote_ratio'].unique()
selected_contracts = st.sidebar.multiselect('Remote Ratio', available_contracts, default=available_contracts)

available_size = sorted(df['company_size'].unique())
selected_size = st.sidebar.multiselect('Company Size', available_size, default=available_size)

df_filtered = df[
    (df['work_year'].isin(selected_years)) &
    (df['experience_level'].isin(selected_experience)) &
    (df['remote_ratio'].isin(selected_contracts)) &
    (df['company_size'].isin(selected_size))
]

st.title('Data Visualization Dashboard 📊')
st.markdown('This dashboard allows you to explore salary data across different years, seniority levels, contract types, and company sizes.')    

st.subheader('General Metrics (Yearly Average Salary)')
if not df_filtered.empty:
    avg_salary = df_filtered['salary_in_usd'].mean()
    max_salary = df_filtered['salary_in_usd'].max()
    total_entries = df_filtered.shape[0]    
    more_frequent_job = df_filtered['job_title'].mode()[0]
else:
    avg_salary, median_salary, min_salary, max_salary, total_entries, more_frequent_job = 0, 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Salary", f"${avg_salary:,.0f}")
col2.metric("Maximum Salary", f"${max_salary:,.0f}")
col3.metric("Total Entries", f"{total_entries:,}")
col4.metric("More Frequent Job", more_frequent_job)

st.markdown("---")

st.subheader("Graphics")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtered.empty:
        top_positions = df_filtered.groupby('job_title')['salary_in_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        job_chart = px.bar(
            top_positions,
            x='salary_in_usd',
            y='job_title',
            orientation='h',
            title='Top 10 Jobs by Average Salary (USD)',
            labels={'salary_in_usd': 'Average Salary (USD)', 'job_title': 'Job Title'},
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        job_chart.update_layout(title_x=0.1,yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(job_chart, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

with col_graf2:
    if not df_filtered.empty:
        hist_graph = px.histogram(
            df_filtered,
            x='salary_in_usd',
            nbins=30,
            title='Salary Distribution',
            labels={'salary_in_usd': 'Salary (USD)','count':''},
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        hist_graph.update_layout(title_x=0.1)
        st.plotly_chart(hist_graph, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

col_graf3, col_graph4 = st.columns(2)

with col_graf3:
        if not df_filtered.empty:
            remote_count = df_filtered['remote_ratio'].value_counts().reset_index()
            remote_count.columns = ['work_type', 'quantity']
            pie_chart = px.pie(
                remote_count,
                names='work_type',
                values='quantity',
                title='Work Modality Distribution',
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Magma
            )
            pie_chart.update_traces(textinfo='percent+label')
            pie_chart.update_layout(title_x=0.1)
            st.plotly_chart(pie_chart, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")   

with col_graph4:
    if not df_filtered.empty:
        df_ds = df_filtered[df_filtered['job_title'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('employee_residence_iso3')['salary_in_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='employee_residence_iso3',
            color='salary_in_usd',
            color_continuous_scale='viridis',
            title='Average Salary of Data Scientists by Country',
            labels={'salary_in_usd': 'Salário médio (USD)', 'employee_residence_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

st.subheader('Data Table')
st.dataframe(df_filtered, use_container_width=True)