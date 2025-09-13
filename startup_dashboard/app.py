import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title='Startup Analysis')
def load_overall_analysis():
    st.title('Overall Analysis')

    #total invested amount
    amount=round(df['amount'].sum())
    #Max investment in a startup
    max=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #Average funding
    mean=round(df.groupby('startup')['amount'].sum().mean())
    #Total funded startups
    num=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total (Cr)", f"{amount}")
    with col2:
        st.metric("Max funding (Cr)", f"{max}")
    with col3:
        st.metric("Average funding(Cr)",f"{mean}")
    with col4:
        st.metric("Total funded startups",num)
    st.header('MoM Graph')
    #sel=st.selectbox('Select Type',['Total','Count'])
    #if(sel=='Total'):

    temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
    fig3, ax3= plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'], marker='o')  # x = years, y = amounts
    ax3.set_xlabel("Year and Month")
    ax3.set_ylabel("Amount")
    ax3.set_title("Investment by Year")
    st.subheader('MoM Investment')
    st.pyplot(fig3)
    
    temp_df=df.groupby(['year','month'])['startup'].count().reset_index()
    temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
    fig3, ax3= plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['startup'], marker='o')  # x = years, y = amounts
    ax3.set_xlabel("Year and Month")
    ax3.set_ylabel("count")
    ax3.set_title("No of Startups funded")
    st.subheader('MoM Investment')
    st.pyplot(fig3)


def load_investor_detail(investor):
    st.title(investor)
    #Show recent investments of the investor
    last_5_df=df[df['investors'].str.contains(investor)].head()[['date','startup','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5_df)
     
    #Biggest Investment
    big_series=df[df['investors'].str.contains(investor)].head()[['date','startup','city','round','amount']].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.subheader('Biggest Investments')
    st.dataframe(big_series)

    fig, ax = plt.subplots()
    ax.pie(big_series.values,labels=big_series.index,autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    st.pyplot(fig)
    
    #Sectors invested in
    sector_df= df[df['investors'].str.contains(investor)].head().groupby('vertical')['amount'].sum()
    st.subheader('Sectors invested')
    st.dataframe(sector_df)
    fig1, ax1 = plt.subplots()
    ax1.pie(sector_df.values,labels=sector_df.index,autopct='%1.1f%%', startangle=90)
    ax1.axis('equal') 
    st.pyplot(fig1)


    #Stage

    #City

    #YOY Investment
    year_series=df[df['investors'].str.contains('investor')].groupby('year')['amount'].sum()
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values, marker='o')  # x = years, y = amounts
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Total Investment Amount")
    ax2.set_title("Investment by Year")
    st.subheader('YOY Investment')
    st.pyplot(fig2)

    #Similar Investors

    

df=pd.read_csv('startup_dashboard/startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if(option=='Overall Analysis'):
    btn0=st.sidebar.button('show overall analysis')
    if btn0:
        load_overall_analysis()



elif(option=='Startup'):
    st.title("Startup Analysis")
    st.sidebar.selectbox('Select startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find startup details',)

elif(option=='Investor'):
    st.title("Investor Analysis")
    selected=st.sidebar.selectbox('select Investor',sorted(set(df['investors'].str.split(',').sum()))[1:])
    btn2=st.sidebar.button('Find Investor details')
    if btn2:
        load_investor_detail(selected)

