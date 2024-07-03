import pandas as pd
import streamlit as st 
import plotly.express as px 



excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

st.set_page_config(page_title='Survey Results')
st.header('Survey Results 2021')
st.subheader('Was the tutorial good?')

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_participants = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='F:G',
                   header=3)



# st.dataframe(df_participants)

df_participants.dropna(inplace=True)
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                          min_value=min(ages),
                          max_value=max(ages),
                          value=(min(ages), max(ages)))

department_selection = st.multiselect('Department: ',
                                      department,
                                      default=department)

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_results = df[mask].shape[0]
st.markdown(f'*Подходящих работников: {number_of_results}')

df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age':'Votes'})
df_grouped = df_grouped.reset_index()

bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Votes',
                   text='Votes',
                   template='plotly_white')
st.plotly_chart(bar_chart)
# st.dataframe(df)

pie_chart = px.pie(df_participants,
                   title='Total No. Partiticipants',
                   values='Participants',
                   names='Departments')

st.plotly_chart(pie_chart)