import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

# Import csv data 
bmore_pop_data = pd.read_csv('baltimore_population_2000_2023.csv')

# Rename columns for referencing 
bmore_pop_data = bmore_pop_data.rename(columns={"Year": "year", 
                                                "Population": "population", 
                                                "Year on Year Change": "year_on_year_change", 
                                                "Change in Percent": "change_in_percent"})

# remove "-" from first row 
bmore_pop_data['year_on_year_change'] = bmore_pop_data['year_on_year_change'].replace('-', np.nan)
bmore_pop_data['change_in_percent'] = bmore_pop_data['change_in_percent'].replace('-', np.nan)

# ['population'] remove commas and convert values to int
bmore_pop_data['population'] = bmore_pop_data['population'].str.replace(',', '')
bmore_pop_data['population'] = bmore_pop_data['population'].astype('int')

# ['year_on_year_change'] remove commas, fill NaN values and convert to int
bmore_pop_data['year_on_year_change'] = bmore_pop_data['year_on_year_change'].str.replace(',', '')
bmore_pop_data['year_on_year_change'] = pd.to_numeric(bmore_pop_data['year_on_year_change'], 
                                                      errors='coerce').fillna(0).astype(int)


# Calculate statistics , avg and total loss since 2000
def calculate_statistics(df):
    avg_pop_loss = int(df['year_on_year_change'].mean())
    total_pop_loss = int(df['population'].max() - df['population'].min())
    return avg_pop_loss, total_pop_loss

avg_pop_loss, total_pop_loss = calculate_statistics(bmore_pop_data)


# Render scatter_plot 
scatter_plot = px.scatter(bmore_pop_data, x='year', y='population',
                 labels={'year': 'Year', 'population': 'Population'})

# Render bar_plot
bar_plot = px.bar(bmore_pop_data, x='year', y='year_on_year_change',  
             labels={'year_on_year_change': '# of people per year', 'year': 'Year'})



# Streamlit app components 

# Title
st.title("Tracking Baltimore City's Population Decline (2000-2023)")

# Paragraph about population decline in Baltimore City
st.write('''Baltimore's population has been steadily declining for the past several decades, 
with a significant drop in residents over the last 23 years. This trend has deep implications 
for the city's future. A shrinking population can lead to a reduced tax base, impacting funding 
for essential services like public education, infrastructure, and public safety. It can also signal 
broader socioeconomic challenges, such as job losses, crime, or the migration of businesses and talent 
to more prosperous regions. For Baltimore, the decline emphasizes the need for strategic urban planning, 
investment in economic development, and efforts to revitalize neighborhoods. If left unaddressed, this 
population loss could exacerbate existing disparities and hinder long-term growth, making it harder for 
the city to compete and thrive in an increasingly competitive national landscape.''')

# Render dataset table
table = go.Figure(data=[go.Table(
    header=dict(values=list(bmore_pop_data.columns),
               fill_color='black',
               align='center'),
    cells=dict(values=[bmore_pop_data[col] for col in bmore_pop_data.columns],
               fill_color='black',
               align='center'))
])

# Baltimore pop. df table & Plots
if st.checkbox('Show data table'):
    st.plotly_chart(table)

if st.checkbox('Show scatterplot'):
    st.plotly_chart(scatter_plot)
    st.text(f'''The chart above shows a significant decrease from 2000-2023. There was a slight 
    boom in population around 2010, then a flatline, followed by another dip in 2015. 
    The total decrease equaling {total_pop_loss} people.''')

if st.checkbox('Show bar chart'):
    st.plotly_chart(bar_plot)
    st.text('''This chart offers a different perspective, highlighting both the positive and 
    negative population changes over the past 23 years, and illustrating the patterns of 
    inflows vs outflows of people.''')




