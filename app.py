import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st


bmore_pop_data = pd.read_csv('baltimore_population_2000_2023.csv')

# rename columns for referencing 
bmore_pop_data = bmore_pop_data.rename(columns={"Year": "year", 
                                                "Population": "population", 
                                                "Year on Year Change": "year_on_year_change", 
                                                "Change in Percent": "change_in_percent"})

# remove commas from pop values so they can be converted from objs to ints
bmore_pop_data['population'] = bmore_pop_data['population'].str.replace(',', '')

# convert population values to integer values 
bmore_pop_data['population'] = bmore_pop_data['population'].astype('int')

# remove "-" from first row 
bmore_pop_data['year_on_year_change'] = bmore_pop_data['year_on_year_change'].replace('-', "0")

# remove commas from pop values so they can be converted from objs to ints
bmore_pop_data['year_on_year_change'] = bmore_pop_data['year_on_year_change'].str.replace(',', '')

# convert population values to integer values 
bmore_pop_data['year_on_year_change'] = bmore_pop_data['year_on_year_change'].astype('int')

# remove "-" from first row 
bmore_pop_data['change_in_percent'] = bmore_pop_data['change_in_percent'].replace('-', "0")

# Calculate average loss per year
avg_pop_loss = int(bmore_pop_data['year_on_year_change'].mean())

# Calculate total population loss
total_pop_loss = int(bmore_pop_data['population'].max() - bmore_pop_data['population'].min())

# Scatterplot using year vs population to show decline in population since 2000
fig = px.scatter(bmore_pop_data, x='year', y='population',
                 labels={'year': 'Year', 'population': 'Population'})

fig2 = px.bar(bmore_pop_data, x='year', y='year_on_year_change',  
             labels={'year_on_year_change': '# of people per year', 'year': 'Year'})

st.title("Tracking Baltimore City's Population Decline (2000-2023)")
st.write('')



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

# Baltimore pop. dataframe
st.write(bmore_pop_data)

# Scatterplot
show_data = st.checkbox('Show scatterplot')

if show_data:
    st.plotly_chart(fig)

    st.text(f'''        The chart above shows a significant decrease from 2000-2023. There was a slight 
    boom in population around 2010, then a flatline, followed by another dip in 2015. 
    The total decrease equaling {total_pop_loss} people.''')
else:
    st.write('Check the box to see info.')

# Histogram
show_data2 = st.checkbox('Show histogram')

if show_data2:
    st.plotly_chart(fig2)

    st.text('''     This chart offers a different perspective, highlighting both the positive and 
    negative population changes over the past 23 years, and illustrating the patterns of 
    inflows vs outflows of people.''')
else:
    st.write('Check the box to see info.')


