import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

#Dataframe Creation


#sql Connection
mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

cursor = mydb.cursor()


#aggregate_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1, columns=("State","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregate_transaction_df

cursor.execute("SELECT * FROM aggregated_transactions")
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2, columns=("State","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregate_user_df

cursor.execute("SELECT * FROM aggregated_user")
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3, columns=("State","Years","Quarter","Brands","Transaction_count","Percentage"))

#map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4, columns=("State","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5, columns=("State","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_df

cursor.execute("SELECT * FROM map_user")
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6, columns=("State","Years","Quarter","Districts","Registered_Users", "App_Opens"))

#top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7, columns=("State","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))


#top_transactions_df

cursor.execute("SELECT * FROM top_transaction")
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8, columns=("State","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user_df

cursor.execute("SELECT * FROM top_user")
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9, columns=("State","Years","Quarter","Pincodes","Registered_Users"))


def Transaction_amount_count_Y(df,year):

    

    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg,x="State",y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg,x="State",y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for feature in data["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale=px.colors.sequential.Electric_r,
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale=px.colors.sequential.Blugrn_r,
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="State",y="Transaction_amount", title=f"{tacy['Years'].min()} Year {quarter} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count=px.bar(tacyg,x="State",y="Transaction_count", title=f"{tacy['Years'].min()} Year {quarter} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1, col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data=json.loads(response.content)
        states_name=[]
        for feature in data["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()
        fig_india_1=px.choropleth(tacyg,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale=px.colors.sequential.Cividis_r,
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{tacy['Years'].min()} Year {quarter} TRANSACTION AMOUNT",fitbounds="locations",
                                height=650,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_count",color_discrete_map=px.colors.sequential.BuGn,
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_amount"].max()),
                                hover_name="State",title=f"{tacy['Years'].min()} Year {quarter} TRANSACTION COUNT",fitbounds="locations",
                                height=650,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Agrre_Trans_Transaction_type(df, state):


    tacy=df[df["State"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame= tacyg, names="Transaction_type",values="Transaction_amount",width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame= tacyg, names="Transaction_type",values="Transaction_count",width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pie_2)

def Aggre_user_plot_1(df,year):

    aguy= df[df["Years"]==2018]
    aguy.reset_index(drop= True, inplace=True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggre_User_Analysis_2

def Aggre_user_plot_2(df,quarter):

    aguyq= df[df["Quarter"]==quarter]
    aguyq.reset_index(drop= True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    

    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count", title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                    width=800,color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


# Aggre_user_analysis_3

def Aggre_user_plot_3(df,state):
    auyqs=df[df["State"]==state]
    auyqs.reset_index(drop=True,inplace=True)


    fig_line_1=px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                    title="BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000,markers=True)
    st.plotly_chart(fig_line_1)



#Map Insurance Districts

def Map_insurance_Districts(df, state):


    tacy=df[df["State"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x= "Transaction_amount", y="Districts", orientation="h",
                            title=f"{state} DISTRICT AND TRANSACTION AMOUNT", 
                            color_discrete_sequence=px.colors.sequential.Jet_r,height=800,
                            width=600)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg, x= "Transaction_count", y="Districts", orientation="h",
                            title=f"{state} DISTRICT AND TRANSACTION COUNT", 
                            color_discrete_sequence=px.colors.sequential.Hot,height=800,
                            width=600)
        st.plotly_chart(fig_bar_2)

#Map Transaction Districts

def Map_transaction_Districts(df, state):


    tacy=df[df["State"]==state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x= "Transaction_amount", y="Districts", orientation="h",
                            title=f"{state} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Jet_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg, x= "Transaction_count", y="Districts", orientation="h",
                            title=f"{state} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Hot)
        st.plotly_chart(fig_bar_2)

#Map User Analysis 1

def map_user_plot_1(df,year):

    muy= df[df["Years"]==year]
    muy.reset_index(drop= True, inplace=True)


    muyg=muy.groupby("State")[["Registered_Users","App_Opens"]].sum()
    muyg.reset_index(inplace=True)

    
    fig_line_1=px.line(muyg, x="State", y=["Registered_Users", "App_Opens"], 
                        title=f"{year} REGISTEREDUSER APPOPENS", width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)

#Map_User_Analysis_2

def map_user_plot_2(df,quarter):

    muyq_df= df[df["Quarter"]==quarter]
    muyq_df.reset_index(drop= True, inplace=True)


    muyQg=muyq_df.groupby("State")[["Registered_Users","App_Opens"]].sum()
    muyQg.reset_index(inplace=True)


    fig_line_1=px.line(muyQg, x="State", y=["Registered_Users", "App_Opens"], 
                        title=f"{quarter} QUARTER REGISTEREDUSER APPOPENS",
                        width=1000,height=800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_line_1)

    return muyq_df
# Top Insurance:
def top_insurance_plot_1(df,state):
    tiy= df[df["State"]==state]
    tiy.reset_index(drop= True, inplace=True)


    col1,col2=st.columns(2)
    with col1:

        fig_top_insur_bar_1=px.bar(tiy, x= "Quarter", y="Transaction_amount", hover_data="Pincodes",
                                title= " TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Magenta)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x= "Quarter", y="Transaction_count", hover_data="Pincodes",
                                title= " TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Sunset)
        st.plotly_chart(fig_top_insur_bar_2)

#Top Transaction
def top_transaction_plot_1(df,state):
    tty= df[df["State"]==state]
    tty.reset_index(drop= True, inplace=True)


    
    col1, col2=st.columns(2)
    with col1:

        fig_top_trans_bar_1=px.bar(tty, x= "Quarter", y="Transaction_amount", hover_data="Pincodes",
                                title= " TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Magenta)
        st.plotly_chart(fig_top_trans_bar_1)
    with col2:
        fig_top_trans_bar_2=px.bar(tty, x= "Quarter", y="Transaction_count", hover_data="Pincodes",
                                title= " TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Magenta)
        st.plotly_chart(fig_top_trans_bar_2)


#Top user
def top_user_plot_1(df,year):
    tuy= df[df["Years"]==year]
    tuy.reset_index(drop= True, inplace=True)

    tuyg= pd.DataFrame(tuy.groupby(["State", "Quarter"])[["Registered_Users"]].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1=px.bar(tuyg, x="State", y="Registered_Users", color="Quarter", width=1000,
                        height=800, color_discrete_sequence=px.colors.sequential.matter,
                        hover_name="State", title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#Top user state analysis
def top_user_plot_2(df,state):
    tuys= df[df["State"]==state]
    tuys.reset_index(drop= True, inplace=True)

    fig_top_plot_2=px.bar(tuys, x= "Quarter", y="Registered_Users", title= f"{state} REGISTEREDUSERS, PINCODES, QUARTER",
                        width=1000, height=800, color="Registered_Users", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Jet_r)
    st.plotly_chart(fig_top_plot_2)


#top charts
def top_chart_transaction_amount(table_name):
    # Connect to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

    cursor = mydb.cursor()

    # Plot 1: Top 10 transaction amounts
    query1 = f'''
    SELECT State, SUM(Transaction_amount) AS transaction_amount
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_amount DESC
    LIMIT 10;
    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()

    df_1 = pd.DataFrame(table_1, columns=["State", "Transaction_amount"])

    col1,col2=st.columns(2)
    with col1:


        fig_amount_1 = px.bar(df_1, x="State", y="Transaction_amount", title="Top 10 Transaction Amounts",
                            width=600, height=650, color="Transaction_amount",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Last 10 transaction amounts
    query2 = f'''
    SELECT State, SUM(Transaction_amount) AS transaction_amount
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_amount ASC
    LIMIT 10;
    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()

    df_2 = pd.DataFrame(table_2, columns=["State", "Transaction_amount"])

    with col2:

        fig_amount_2 = px.bar(df_2, x="State", y="Transaction_amount", title="Last 10 Transaction Amounts",
                            width=600, height=650, color="Transaction_amount",
                            color_continuous_scale=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Average transaction amounts
    query3 = f'''
    SELECT State, AVG(Transaction_amount) AS transaction_amount
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_amount;
    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()

    df_3 = pd.DataFrame(table_3, columns=["State", "Transaction_amount"])

    fig_amount_3 = px.bar(df_3, x="Transaction_amount", y="State", title="Average Transaction Amounts",
                          width=1000, height=800, color="Transaction_amount", orientation='h',
                          color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)

#Top Charts
#sql Connection
def top_chart_transaction_count(table_name):
    # Connect to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

    cursor = mydb.cursor()

    # Plot 1: Top 10 transaction counts
    query1 = f'''
    SELECT State, SUM(Transaction_count) AS transaction_count
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_count DESC
    LIMIT 10;
    '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()

    df_1 = pd.DataFrame(table_1, columns=["State", "Transaction_count"])
    col1,col2=st.columns(2)
    with col1:


        fig_amount_1 = px.bar(df_1, x="State", y="Transaction_count", title="Top 10 Transaction Counts",
                            width=600, height=800, color="Transaction_count",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Last 10 transaction counts
    query2 = f'''
    SELECT State, SUM(Transaction_count) AS transaction_count
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_count ASC
    LIMIT 10;
    '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()

    df_2 = pd.DataFrame(table_2, columns=["State", "Transaction_count"])
    with col2:


        fig_amount_2 = px.bar(df_2, x="State", y="Transaction_count", title="Last 10 Transaction Counts",
                            width=600, height=650, color="Transaction_count",
                            color_continuous_scale=px.colors.sequential.algae)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Average transaction counts
    query3 = f'''
    SELECT State, AVG(Transaction_count) AS transaction_count
    FROM {table_name}
    GROUP BY State
    ORDER BY transaction_count;
    '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()

    df_3 = pd.DataFrame(table_3, columns=["State", "Transaction_count"])

    fig_amount_3 = px.bar(df_3, x="Transaction_count", y="State", title="Average Transaction Counts",
                          width=1000, height=800, color="Transaction_count", orientation='h',
                          color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)


def top_chart_registered_user(table_name, state):
    # Connect to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

    cursor = mydb.cursor()

    # Plot 1: Top 10 registered users
    query1 = f'''
    SELECT Districts, SUM(Registered_Users) AS registered_users
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY registered_users DESC
    LIMIT 10;
    '''

    cursor.execute(query1)
    table_1 = cursor.fetchall()

    df_1 = pd.DataFrame(table_1, columns=["Districts", "Registered_Users"])
    col1, col2=st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="Districts", y="Registered_Users", title="Top 10 Registered Users",
                            width=600, height=800, color="Registered_Users",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Last 10 registered users
    query2 = f'''
    SELECT Districts, SUM(Registered_Users) AS registered_users
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY registered_users ASC
    LIMIT 10;
    '''

    cursor.execute(query2)
    table_2 = cursor.fetchall()

    df_2 = pd.DataFrame(table_2, columns=["Districts", "Registered_Users"])

    with col2:
        fig_amount_2 = px.bar(df_2, x="Districts", y="Registered_Users", title="Last 10 Registered Users",
                            width=600, height=800, color="Registered_Users",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Average registered users
    query3 = f'''
    SELECT Districts, AVG(Registered_Users) AS registered_users
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY registered_users;
    '''

    cursor.execute(query3)
    table_3 = cursor.fetchall()

    df_3 = pd.DataFrame(table_3, columns=["Districts", "Registered_Users"])

    fig_amount_3 = px.bar(df_3, x="Registered_Users", y="Districts", title="Average Registered Users",
                          width=1000, height=800, color="Registered_Users", orientation='h',
                          color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)

#Top charts app opens
def top_chart_app_opens(table_name, state):
    # Connect to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

    cursor = mydb.cursor()

    # Plot 1: Top 10 app opens
    query1 = f'''
    SELECT Districts, SUM(App_Opens) AS app_opens
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY app_opens DESC
    LIMIT 10;
    '''

    cursor.execute(query1)
    table_1 = cursor.fetchall()

    df_1 = pd.DataFrame(table_1, columns=["Districts", "App_Opens"])

    col1, col2= st. columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="Districts", y="App_Opens", title="Top 10 App Opens",
                            width=600, height=800, color="App_Opens",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Last 10 app opens
    query2 = f'''
    SELECT Districts, SUM(App_Opens) AS app_opens
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY app_opens ASC
    LIMIT 10;
    '''

    cursor.execute(query2)
    table_2 = cursor.fetchall()

    df_2 = pd.DataFrame(table_2, columns=["Districts", "App_Opens"])

    with col2:

        fig_amount_2 = px.bar(df_2, x="Districts", y="App_Opens", title="Last 10 App Opens",
                            width=600, height=800, color="App_Opens",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Average app opens
    query3 = f'''
    SELECT Districts, AVG(App_Opens) AS app_opens
    FROM {table_name}
    WHERE State = '{state}'
    GROUP BY Districts
    ORDER BY app_opens;
    '''

    cursor.execute(query3)
    table_3 = cursor.fetchall()

    df_3 = pd.DataFrame(table_3, columns=["Districts", "App_Opens"])

    fig_amount_3 = px.bar(df_3, x="App_Opens", y="Districts", title="Average App Opens",
                          width=600, height=650, color="App_Opens", orientation='h',
                          color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)

#top char top registered users

def top_chart_top_registered_user(table_name):
    # Connect to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Prashanthi@19',
        database='phonepe_data'
    )

    cursor = mydb.cursor()

    # Plot 1: Top 10 registered users by state
    query1 = f'''
    SELECT State, SUM(Registered_Users) AS registeredusers
    FROM {table_name}
    GROUP BY State
    ORDER BY registeredusers DESC
    LIMIT 10;
    '''

    cursor.execute(query1)
    table_1 = cursor.fetchall()

    df_1 = pd.DataFrame(table_1, columns=["State", "Registered_Users"])

    col1, col2=st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="State", y="Registered_Users", title="Top 10 Registered Users by State",
                            width=600, height=800, color="Registered_Users",
                            color_continuous_scale=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Last 10 registered users by state
    query2 = f'''
    SELECT State, SUM(Registered_Users) AS registeredusers
    FROM {table_name}
    GROUP BY State
    ORDER BY registeredusers ASC
    LIMIT 10;
    '''

    cursor.execute(query2)
    table_2 = cursor.fetchall()

    df_2 = pd.DataFrame(table_2, columns=["State", "Registered_Users"])

    with col2:
        fig_amount_2 = px.bar(df_2, x="State", y="Registered_Users", title="Last 10 Registered Users by State",
                            width=600, height=800, color="Registered_Users",
                            color_continuous_scale=px.colors.sequential.deep_r)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Average registered users by state
    query3 = f'''
    SELECT State, AVG(Registered_Users) AS registeredusers
    FROM {table_name}
    GROUP BY State
    ORDER BY registeredusers;
    '''

    cursor.execute(query3)
    table_3 = cursor.fetchall()

    df_3 = pd.DataFrame(table_3, columns=["State", "Registered_Users"])

    fig_amount_3 = px.bar(df_3, x="Registered_Users", y="State", title="Average Registered Users by State",
                          width=600, height=650, color="Registered_Users", orientation='h',
                          color_continuous_scale=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_amount_3)



#Streamlit Part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:

    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select=="HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Praveena\OneDrive\Desktop\projects\phone pe\pulse\download.jpeg"))

    col3, col4=st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\Praveena\OneDrive\Desktop\projects\phone pe\pulse\pulse-2.png"))

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
    col5, col6= st.columns(2)
    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")
    with col6:
        st.image(Image.open(r"C:\Users\Praveena\OneDrive\Desktop\projects\phone pe\pulse\pulse 3.png"))

elif select =="DATA EXPLORATION":

    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method=st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"])

        if method =="Insurance Analysis":

            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_y=Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_y, quarters)


        elif method=="Transaction Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_trans_tac_y=Transaction_amount_count_Y(Aggre_transaction, years)
            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_trans_tac_y["State"].unique())
            Agrre_Trans_Transaction_type(Aggre_trans_tac_y, states)


            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter",Aggre_trans_tac_y["Quarter"].min(),Aggre_trans_tac_y["Quarter"].max(),Aggre_trans_tac_y["Quarter"].min())
            Aggre_trans_tac_y_q=Transaction_amount_count_Y_Q(Aggre_trans_tac_y, quarters)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_type",Aggre_trans_tac_y_q["State"].unique())
            Agrre_Trans_Transaction_type(Aggre_trans_tac_y_q, states)


        elif method=="User Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_user_Y_Q["State"].unique())
            Aggre_user_Y_Q_S= Aggre_user_plot_3(Aggre_user_Y_Q, states)


    with tab2:
        method2=st.radio("Select the Method",["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])

        if method2 =="Map Insurance Analysis":

            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Years",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insur_tac_y=Transaction_amount_count_Y(Map_insurance, years)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Map_insur_tac_y["State"].unique())
            Map_insurance_Districts(Map_insur_tac_y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarters",Map_insur_tac_y["Quarter"].min(),Map_insur_tac_y["Quarter"].max(),Map_insur_tac_y["Quarter"].min())
            Map_insur_tac_y_q=Transaction_amount_count_Y_Q(Map_insur_tac_y, quarters)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_types",Map_insur_tac_y_q["State"].unique())
            Map_insurance_Districts(Map_insur_tac_y_q, states)
            
        elif method2=="Map Transaction Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Years",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_trans_tac_y=Transaction_amount_count_Y(Map_transaction, years)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Map_trans_tac_y["State"].unique())
            Map_transaction_Districts(Map_trans_tac_y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarters",Map_trans_tac_y["Quarter"].min(),Map_trans_tac_y["Quarter"].max(),Map_trans_tac_y["Quarter"].min())
            Map_trans_tac_y_q=Transaction_amount_count_Y_Q(Map_trans_tac_y, quarters)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_types",Map_trans_tac_y_q["State"].unique())
            Map_insurance_Districts(Map_trans_tac_y_q, states)

        elif method2=="Map User Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_mu",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y= map_user_plot_1(Map_user,years)

            
                
                  
    with tab3:
        method3=st.radio("Select the Method",["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])

        if method3 =="Top Insurance Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Years_TI",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_tac_y=Transaction_amount_count_Y(Top_insurance, years)
            
            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_ti",Top_insur_tac_y["State"].unique())
            top_insurance_plot_1(Top_insur_tac_y, states)
            
            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarters_ti",Top_insur_tac_y["Quarter"].min(),Top_insur_tac_y["Quarter"].max(),Top_insur_tac_y["Quarter"].min())
            top_insur_tac_y_q=Transaction_amount_count_Y_Q(Top_insur_tac_y, quarters)

        elif method3=="Top Transaction Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Years_Ttrans",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_trans_tac_y=Transaction_amount_count_Y(Top_transaction, years)
             
            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_tt",Top_trans_tac_y["State"].unique())
            top_transaction_plot_1(Top_trans_tac_y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters=st.slider("Select The Quarters_tt",Top_trans_tac_y["Quarter"].min(),Top_trans_tac_y["Quarter"].max(),Top_trans_tac_y["Quarter"].min())
            Top_trans_tac_y_q=Transaction_amount_count_Y_Q(Top_trans_tac_y, quarters)

        elif method3=="Top User Analysis":
            col1, col2=st.columns(2)
            with col1:

                years=st.slider("Select The Years_Tu",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_y=top_user_plot_1(Top_user, years)

            col1, col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State_tu",Top_user_y["State"].unique())
            top_user_plot_2(Top_user_y, states)

elif select =="TOP CHARTS":
    
    question= st.selectbox("Select the Question", ["1. Transcation Amount and Count of Aggregate Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Count of Map Transaction",
                                                   "6. Transaction Amount and Count of Top Transaction",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered Users of Map User",
                                                   "9. App opens of Map user",
                                                   "10. Registered Users of Top User",
                                                   ])
    
    if question== "1. Transcation Amount and Count of Aggregate Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question=="2. Transaction Amount and Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question=="3. Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question=="4. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transactions")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transactions")

    elif question=="5. Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question=="6. Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question=="7. Transaction Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question=="8. Registered Users of Map User":

        states=st.selectbox("Select the state", Map_user["State"].unique())
        st.subheader("Registered_Users")
        top_chart_registered_user("map_user", states)

    elif question=="9. App opens of Map user":

        states=st.selectbox("Select the state_mu", Map_user["State"].unique())
        st.subheader("App Opens")
        top_chart_app_opens("map_user", states)

    elif question=="10. Registered Users of Top User":

        st.subheader("REGISTERED USER")
        top_chart_top_registered_user("top_user")



