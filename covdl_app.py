

import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Download COVID-19 data by Country/Region",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )


# cov = st.cache(pd.read_csv)("WHOcov_cleaned.csv",index_col=0)

# @st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')
cov=pd.read_csv('covdl-app/WHOcov_cleaned.csv',index_col=0)

cov['Datetime']=pd.to_datetime(cov['Date'])
cov['Date']=cov['Datetime'].apply(lambda x: x.strftime('%y-%m-%d'))

col=['Date', 'Country', 'WHO_region', 'Cumulative_cases', 'New_cases',
        'Cumulative_deaths', 'New_deaths',  'Datetime']

cov_disp=cov[col]

sorted_country = sorted(cov_disp['Country'].unique())
sorted_region = sorted(cov_disp['WHO_region'].unique())

st.sidebar.header('Select Country or Region')
st.sidebar.caption('*There is an AND relation here')
selected_country = st.sidebar.multiselect('Select Country', sorted_country, ['Japan', 'South Africa'])
selected_region = st.sidebar.multiselect('Select Region', sorted_region, ['the Western Pacific Region', 'the_African_Region'])

if len(selected_country)==0 and len(selected_region)>0:
  csv_df = cov_disp[cov_disp['WHO_region'].isin(selected_region)]
elif len(selected_country)>0 and len(selected_region)>0:
  csv_df = cov_disp[(cov_disp['Country'].isin(selected_country)) & (cov_disp['WHO_region'].isin(selected_region))]# write dataframe to screen
elif len(selected_country)==0 and len(selected_region)==0:
  csv_df = cov_disp.copy()
elif len(selected_country)>0 and len(selected_region)==0:
  csv_df = cov_disp[cov_disp['Country'].isin(selected_country)]# write dataframe to screen

# layout
st.header('Download COVID-19 data by Country/Region')

st.subheader('Filtered data')
st.write(csv_df)
st.markdown(' ')

st.caption('Download data above')
csv = convert_df(csv_df)
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='covid19_cases.csv',
     mime='text/csv',
 )
st.markdown(' ')

st.subheader('Distribution of New Cases')
csv_df_dateindex=csv_df.set_index('Datetime')
st.line_chart(csv_df_dateindex.New_cases)
