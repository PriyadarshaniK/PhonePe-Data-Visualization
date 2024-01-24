#For the GUI part
import streamlit as st
import os
import git
import mysql.connector
import plotly.graph_objects as go
import pandas as pd
import json
import plotly.express as px
import random

st.set_page_config(
    page_title="PhonePe Data Visualization",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="phonepedb"
)

mycursor = mydb.cursor()


def execute_query(query):
    mycursor.execute(query)
    result = mycursor.fetchall()
    Dataf = pd.DataFrame(result, columns=mycursor.column_names)
    return Dataf

# Get the year list for dropdown
def year_list(type): # 1 = insurance, 0 = transaction, 2 = users
    if (type == 0 ): 
        mycursor.execute(
            "SELECT DISTINCT year FROM aggr_trans ORDER BY year asc;")
        years = mycursor.fetchall()
        year_lst = [i[0] for i in years]
        return year_lst
    if (type == 2 ): 
        mycursor.execute(
            "SELECT DISTINCT year FROM aggr_user ORDER BY year asc;")
        years = mycursor.fetchall()
        year_lst = [i[0] for i in years]
        return year_lst
    else:  # this is for insurance
        mycursor.execute(
            "SELECT DISTINCT year FROM aggr_insurance ORDER BY year asc;")
        years = mycursor.fetchall()
        year_lst = [i[0] for i in years]
        return year_lst

# Get the quarter list for dropdown
def quarter_list(year_val,type):# 1 = insurance, 0 = transaction, 2 = users
    if (type == 0 ): 
        mycursor.execute(
            "SELECT DISTINCT quarter FROM aggr_trans WHERE year ='" + str(year_val) + "' ORDER BY quarter asc;")
        quarters = mycursor.fetchall()
        quarter_list = [i[0] for i in quarters]
        return quarter_list
    if (type == 2 ): 
        mycursor.execute(
            "SELECT DISTINCT quarter FROM aggr_user WHERE year ='" + str(year_val) + "' ORDER BY quarter asc;")
        quarters = mycursor.fetchall()
        quarter_list = [i[0] for i in quarters]
        return quarter_list
    else:  # this is for insurance
        mycursor.execute(
            "SELECT DISTINCT quarter FROM aggr_insurance WHERE year ='" + str(year_val) + "' ORDER BY quarter asc;")
        quarters = mycursor.fetchall()
        quarter_list = [i[0] for i in quarters]
        return quarter_list
    

#Get the state list for dropdown
def state_list():
    mycursor.execute("""SELECT DISTINCT state 
                            FROM top_trans_dist
                            ORDER BY state asc;""")
    s = mycursor.fetchall()
    s_list = [i[0] for i in s]
    return s_list

# Get the district list for dropdown
def district_list(state_val,type): # 1 = insurance, 0 = transaction, 2 = users
    if (type == 0 ): 
        mycursor.execute(
            "SELECT DISTINCT district_name FROM top_trans_dist WHERE state ='" + str(state_val) + "' ORDER BY district_name asc;")
        dist = mycursor.fetchall()
        dist_list = [i[0] for i in dist]
        return dist_list
    elif (type == 2):
        mycursor.execute(
            "SELECT DISTINCT district_name FROM top_user_dist WHERE state ='" + str(state_val) + "' ORDER BY district_name asc;")
        dist = mycursor.fetchall()
        dist_list = [i[0] for i in dist]
        return dist_list
    else:
        mycursor.execute(
            "SELECT DISTINCT district_name FROM top_ins_dist WHERE state ='" + str(state_val) + "' ORDER BY district_name asc;")
        dist = mycursor.fetchall()
        dist_list = [i[0] for i in dist]
        return dist_list

def brand_list(state_val):
    mycursor.execute(
        "SELECT DISTINCT user_brand FROM aggr_user WHERE state ='" + str(state_val) + "' ORDER BY user_brand asc;")
    brand = mycursor.fetchall()
    brand_list = [i[0] for i in brand]
    return brand_list


def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
                'font_color':'red',
            },
            title={
                "text": label,
                "font": {'color':'red',"size": 12},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    #fig.show()

    st.plotly_chart(fig, use_container_width=True)


#Create the first screen of the streamlit application, to display few radio buttons on the sidebar and for user inputs on the right.
header = st.container()

sidebar1 = st.sidebar

with header:
    st.subheader("Phonepe Pulse Data Visualization and Exploration")

with sidebar1:
    selection = sidebar1.radio("What's your choice of task?",[":house: Home",":bar_chart:(Data-Insights)"])

if selection == ":house: Home": 
    st.markdown("PhonePe, which registers 40% of all UPI transactions through its app, decided in September,2021, to make available anonymised payments data across states, districts and 19,098 PIN code zones across the country")
    st.markdown("The data gives granular insights, including the nature of payment (merchant, utility or P2P), the phone model used, and the average transaction size. ")
    st.markdown("The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics.")
    st.markdown("The goal of this project is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.")
    st.markdown("The application has the following features:")
    st.markdown("- Extract data from the Phonepe pulse Github repository through scripting and clone it.")
    st.markdown("- Transform the data into a suitable format and perform any necessary cleaning and pre-processing steps.")
    st.markdown("- Insert the transformed data into a MySQL database for efficient storage and retrieval.")
    st.markdown("- Create a live geo visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner.")
    st.markdown("- Fetch the data from the MySQL database to display in the dashboard.")

    st.markdown("Insights gained from analysing this data through this project - ")
    st.markdown("- The data on 2,000 crore transactions are showcased on an interactive map of the country")
    st.markdown("- The data shows that recharges, bill payments and P2P categories are higher in tier-2 cities and beyond, as for many this has been the first digital bill payment option.")
    st.markdown("- This is unlike urban areas where customers have been using online payments and other channels for bill payments long before the launch of UPI.")
    st.markdown("- Other insights reveal that two-thirds of insurance purchases made using PhonePe are in tier-3 cities and beyond.")
        
if selection == ":bar_chart:(Data-Insights)":
    
    col1, col2, col3,col4 = st.columns([2,1,1,6])
    with col1:
        choice = st.selectbox('Select the type of payments', options = ['Transactions','Users','Insurance'])
        
    
    with col4:
        col_a,col_b,col_c = st.columns([1,3,2])
    col5,col6 = st.columns([1,1]) # col5 - for display of map, col6 for display of other query visualization
    col7,col8,col9,col10 = st.columns([3,3,2,3]) # Bottom row of data visualization - col8 for graph and col9 left empty for space, col10 for dataframe.
####################### - col a has been left blank for some space.#######################

        

    if choice == 'Transactions':

        with col2:
            choice_year = st.selectbox('Select the year', options = year_list(0))
        with col3:
            if choice_year:
                choice_quarter = st.selectbox('Select the quarter', options = quarter_list(choice_year,0))
        ########### total transactions, counts and average ###########
        with col_b:
            st.subheader(choice)
            query = """SELECT FORMAT(SUM(trans_amt),0) as amount, FORMAT(SUM(trans_count),0) as count, SUM(trans_amt)/SUM(trans_count) as average FROM map_trans ;"""
            df = execute_query(query)
            st.write('All PhonePe Trans(UPI+Cards+Wallets):',df['count'][0])
            st.write("Total payment value:",df['amount'][0])
            st.write("Avg. Transaction value:",df['average'][0])
        ########### total transactions ###########
        with col_c:
            query = """SELECT SUM(trans_count) as count,SUM(trans_amt) as amount FROM aggr_trans;"""
            df = execute_query(query)
            plot_metric(
                    "Total Transactions",
                    df['amount'][0],
                    prefix="\u20B9",
                    suffix="",
                    show_graph=True,
                    color_graph="rgba(0, 104, 201, 0.2)"
                )
            ########### Map details for year, quarter ###########
        with col5:
            query = ("""SELECT state,FORMAT(SUM(trans_count),0) as count,FORMAT(SUM(trans_amt),0) as amount, SUM(trans_amt)/SUM(trans_count) as average 
                    FROM map_trans 
                    WHERE year = """ + str(choice_year) + """ AND quarter = """ + str(choice_quarter) + """
                    GROUP BY state;""")
            df = execute_query(query)
    
            for col in df.columns:
                df[col] = df[col].astype(str)
            
            #'India' + '<br>' + df['state'] + '<br><br>' + \
            df['text'] =  'Transaction Value' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                'Total transactions ' + '<br>' + df['count']
            
            fig = go.Figure(data=go.Choropleth(       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df['state'],
                z=df['average'],
                text=df['text'], # hover text
                
                autocolorscale=False,
                colorscale='Reds',
                marker_line_color='peachpuff',
            
                colorbar=dict(
                    title={'text': "Average PhonePe" + "<br>Transaction Amount"},
                    thickness=15,
                    len=0.35,
                    bgcolor='rgba(0,0,0,0.9)',     
                    ticks="outside",
                    tick0=500,
                    dtick=500,
                    tickvals=[1500, 2000, 2500, 3000,3500,4000],
                    tickprefix = "\u20B9",
                    tickmode="array",
        
                    xanchor='left',
                    x=0.01,
                    yanchor='bottom',
                    y=0.13
                )
            ))
            
            fig.update_geos(
                visible=False,
                projection=dict(
                    type='conic conformal',
                    parallels=[12.472944444, 35.172805555556],
                    rotation={'lat': 24, 'lon': 80}
                ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]}
            )
            
            fig.update_layout(
                title=dict(
                    text="Statewise PhonePe Transactions<br>(Hover for breakdown)",
                    xanchor='center',
                    x=0.5,
                    yref='paper',
                    yanchor='bottom',
                    y=1,
                    pad={'b': 10}
                ),
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                height=800,
                width=600
            )
            
            st.write(fig)
            ################### Map Transaction over ############
    ########### Different type of transactions and their value ###########
        with col6:
        
            query = """SELECT trans_name as Transaction,aggr_trans.year as year, FORMAT(SUM(trans_count),0) as count,FORMAT(SUM(trans_amt),0) as amount, FORMAT( (SUM(trans_amt)/SUM(trans_count)),2) as average FROM aggr_trans GROUP BY trans_name,aggr_trans.year;"""
            df = execute_query(query)
            fig = px.line(df, x='year', y='amount', color='Transaction', markers=True, hover_data=['count','average'],title="Transactions for each type each year")
            fig.update_layout( autosize=False, width=650, height=300 )
            fig.update_layout(autotypenumbers='convert types')
            st.plotly_chart(fig)
    
            ########### Top 10 transactions ###########
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            option = st.radio("Top 10 transactions in - ", ["***State***", "***District***", "***Pincode***"],index=None)
    
            if option == "***State***":
                query = """SELECT state, FORMAT(SUM(trans_amt),0) AS amount, FORMAT(SUM(trans_count),0) as count,FORMAT((SUM(trans_amt)/SUM(trans_count)),2) as average
                    FROM aggr_trans
                    GROUP BY state
                    ORDER BY SUM(trans_amt) DESC
                    LIMIT 10 """
                df = execute_query(query)
                df['text'] =  'Transaction Value' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                        'Total transactions ' + '<br>' + df['count']+  '<br><br>' + \
                        'Average Value' + '<br>'"\u20B9" + df['average']
                fig = px.bar(df, x='state', y='amount',hover_name="state",hover_data=['text'],color='average')
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***District***":
                query = """ (SELECT district_name, FORMAT(SUM(trans_amt),0) AS amount, FORMAT(SUM(trans_count),0) as count,FORMAT((SUM(trans_amt)/SUM(trans_count)),2) as average
                    FROM top_trans_dist
                    GROUP BY district_name
                    ORDER BY SUM(trans_amt) DESC
                    LIMIT 10 )"""
                df = execute_query(query)
                df['text'] =  'Transaction Value' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                        'Total transactions ' + '<br>' + df['count']+  '<br><br>' + \
                        'Average Value' + '<br>'"\u20B9" + df['average']
                fig = px.bar(df, x='district_name', y='amount',hover_name="district_name",hover_data=['text'],color='average')
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***Pincode***": 
                    query = """ SELECT pincode, FORMAT(SUM(pin_amt),0) AS amount, FORMAT(SUM(pin_count),0) as count,FORMAT((SUM(pin_amt)/SUM(pin_count)),2) as average
                    FROM top_trans_pin
                    GROUP BY pincode
                    ORDER BY SUM(pin_amt) 
                    LIMIT 10;"""
                    
                    df = execute_query(query)           
                    df['text'] =  'Transaction Value' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                            'Total transactions ' + '<br>' + df['count']+  '<br><br>' + \
                            'Average Value' + '<br>'"\u20B9" + df['average']
                    
                    fig = px.line(df, x='pincode', y='amount', color='average', markers=True, hover_data=['text'])
                    fig.update_xaxes(type='category')
                    
                    fig.update_layout( autosize=False, width=650, height=400 )
                    
                    st.write(fig)

    ##### col 7 : 2 select boxes, col 8 : graph of query, col9: blank, col10: dataframe of query
    ########### Choose State, District to get transaction details ###########
        with col7:
            choice_state = st.selectbox('Select the state', options = state_list())
            if choice_state:
                choice_dist = st.selectbox('Select the district', options = district_list(choice_state,0))
        with col8:
            query = (f" SELECT year,FORMAT(SUM(trans_count),0) as count,FORMAT(SUM(trans_amt),0) as amount,FORMAT((SUM(trans_amt)/SUM(trans_count)),0) as average "          f" FROM top_trans_dist "
                            f" WHERE state = '{choice_state}'  AND district_name= '{choice_dist}' "
                            f"GROUP BY year;")
            df = execute_query(query)
            fig = px.scatter(df, x=df['year'], y=df['amount'],symbol=df['average'],
    	          color=df['count'],title="Transaction details for a specific district each year"
                )
            fig.update_layout( autosize=False, width=550, height=400 )
            st.write(fig)
        with col10:
            st.write(df)
        
########################### end of  Transaction Data Visualisation ############################################################## 
    if choice == 'Users':

        with col2:
            choice_year = st.selectbox('Select the year', options = year_list(2))
        with col3:
            if choice_year:
                choice_quarter = st.selectbox('Select the quarter', options = quarter_list(choice_year,2))
        #####total users, appopens, and appopens/user####
        with col_b:
                st.subheader(choice)
                query = """SELECT FORMAT(SUM(reg_users),0) as users, FORMAT(SUM(app_opens),0) as appopens, SUM(app_opens)/SUM(reg_users) as average FROM map_user;"""
                df = execute_query(query)
                st.write('Registered PhonePe Users:',df['users'][0])
                st.write("PhonePe App Opens:",df['appopens'][0])
                st.write("App Opens Per User:",df['average'][0])
        with col_c:
            ########### Total users ###########
            query = """SELECT SUM(user_count) as count FROM aggr_user;"""
            df = execute_query(query)
            plot_metric(
                    "Total Users",
                    df['count'][0],
                    prefix="",
                    suffix="",
                    show_graph=True,
                    color_graph="rgba(104, 0, 201, 0.2)"
                )
        ########### Map data per year, per quarter, for Users All over India ###########
        with col5:
            if (choice_year == 2018 or (choice_year == 2019 and choice_quarter == 1)):
                st.markdown("Map: AppOpens Data available only from 2019 quarter 2")
            query = ("""SELECT state, FORMAT(SUM(reg_users),0) as users,FORMAT(SUM(app_opens),0) as appopen, FORMAT( (SUM(app_opens)/SUM(reg_users)),0) as average 
                        FROM map_user
                        WHERE year = """ + str(choice_year) + """ AND quarter = """ + str(choice_quarter) + """
                        GROUP BY state;""")
            df = execute_query(query)
    
            for col in df.columns:
                df[col] = df[col].astype(str)
            
            #'India' + '<br>' + df['state'] + '<br><br>' + \
            df['text'] =  'Registered Users' + '<br>' + df['users']+  '<br><br>' + \
                'App Opens' + '<br>' + df['appopen']
            
            fig = go.Figure(data=go.Choropleth(       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df['state'],
                z=df['average'],
                text=df['text'], # hover text
                
                autocolorscale=False,
                colorscale='Reds',
                marker_line_color='peachpuff',
            
                colorbar=dict(
                    title={'text': "Average AppOpens" + "<br>per User"},
                    thickness=15,
                    len=0.35,
                    bgcolor='rgba(0,0,0,0.9)',     
                    ticks="outside",
                    tick0=0,
                    dtick=25,
                    tickvals=[0,25,50,75,100],
                    tickprefix = "",
                    tickmode="array",
        
                    xanchor='left',
                    x=0.01,
                    yanchor='bottom',
                    y=0.05
                )
            ))
            
            fig.update_geos(
                visible=False,
                projection=dict(
                    type='conic conformal',
                    parallels=[12.472944444, 35.172805555556],
                    rotation={'lat': 24, 'lon': 80}
                ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]}
            )
            
            fig.update_layout(
                title=dict(
                    text="Statewise PhonePe AppOpens per User<br>(Hover for breakdown)",
                    xanchor='center',
                    x=0.5,
                    yref='paper',
                    yanchor='bottom',
                    y=1,
                    pad={'b': 10}
                ),
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                height=800,
                width=600
            )
            
            st.write(fig)
##################################  map part over Users  ##############################
            ########### Brandwise top user counts each year ###########
        with col6:
            query = """SELECT user_brand as brand, aggr_user.year, FORMAT(SUM(user_count),0) as count
            FROM aggr_user GROUP BY user_brand,aggr_user.year
            ORDER BY count 
            LIMIT 10;"""
            df = execute_query(query)
            fig = px.line(df, x='year', y='count', color='brand', markers=True, hover_data=['count','brand'],title="Brandwise top user counts each year")
            #fig = px.pie(df, values='count', names='brand', title='Top 10 Brands based on User Count')
            fig.update_layout( autosize=False, width=650, height=300 )
            fig.update_layout(autotypenumbers='convert types')
            st.plotly_chart(fig)
    
            ########### Top 10 user counts ###########
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            option = st.radio("Top 10 User Counts in - ", ["***State***", "***District***", "***Pincode***"],index=None)
    
            if option == "***State***":
                query = """SELECT state, FORMAT(SUM(user_count),0) AS count
                    FROM aggr_user
                    GROUP BY state
                    ORDER BY SUM(user_count) DESC
                    LIMIT 10 """
                df = execute_query(query)
                df['text'] =  'Total Users:' + '<br>' + df['count']
                        
                fig = px.bar(df, x='state', y='count',hover_name="state",hover_data=['text'])
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***District***":
                query = """ SELECT district_name, FORMAT(SUM(reg_users),0) AS count
                    FROM top_user_dist
                    GROUP BY district_name
                    ORDER BY SUM(reg_users) DESC
                    LIMIT 10;"""
                df = execute_query(query)
                df['text'] =  'Total Users:' + '<br>' + df['count']
                fig = px.bar(df, x='district_name', y='count',hover_name="district_name",hover_data=['text'])
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***Pincode***": 
                    query = """ SELECT pincode, FORMAT(SUM(reg_users),0) AS count
                    FROM top_user_pin
                    GROUP BY pincode
                    ORDER BY SUM(reg_users) 
                    LIMIT 10;"""
                    
                    df = execute_query(query)           
                    df['text'] =  'Total Users:' + '<br>' + df['count']
                    # fig = px.bar(df, x='pincode', y='count',hover_name="pincode",hover_data=['text']) #- makes the pincode also into a number in 200K
                    fig = px.line(df, x='pincode', y='count', markers=True, hover_data=['text'])
                    fig.update_xaxes(type='category')
                    fig.update_layout( autosize=False, width=650, height=400 )
                    
                    st.write(fig)
                ########### Select state and brand for specific data ###########
        with col7:
            choice_state = st.selectbox('Select the state', options = state_list())
            if choice_state:
                choice_brand = st.selectbox('Select the brand name', options = brand_list(choice_state))
        with col8:
            query = (f" SELECT user_brand AS brand, aggr_user.year AS year , FORMAT(SUM(user_count), 0) AS count"
                     f" FROM aggr_user "
                            f" WHERE state = '{choice_state}'  AND user_brand= '{choice_brand}' "
                            f"GROUP BY user_brand, aggr_user.year")
            df = execute_query(query)
            fig = px.scatter(df, x=df['year'], y=df['count'],symbol=df['brand'],
    	          color=df['count'],title = "Brand specific users for each year for a state"
                )
            fig.update_layout( autosize=False, width=550, height=400 )
            st.write(fig)
        with col10:
            st.write(df)

    ###################################################### Users part over ###########
    if choice == 'Insurance':
        with col2:
            choice_year = st.selectbox('Select the year', options = year_list(1))
        with col3:
            if choice_year:
                choice_quarter = st.selectbox('Select the quarter', options = quarter_list(choice_year,1))
        
        ########### total transactions, counts and average ###########
        with col_b:
            st.subheader(choice)
            query = """SELECT FORMAT(SUM(ins_amt),0) as amount, FORMAT(SUM(ins_count),0) as count, SUM(ins_amt)/SUM(ins_count) as average FROM map_insurance ;"""
            df = execute_query(query)
            st.write('Total Policies purchased (Nos.):',df['count'][0])
            st.write("Total Premium value:",df['amount'][0])
            st.write("Avg. Premium value:",df['average'][0])
        ########### total transactions ###########
        with col_c:
            query = """SELECT SUM(ins_count) as count,SUM(ins_amt) as amount FROM aggr_insurance;"""
            df = execute_query(query)
            plot_metric(
                    "Total Premium",
                    df['amount'][0],
                    prefix="\u20B9",
                    suffix="",
                    show_graph=True,
                    color_graph="rgba(0, 104, 201, 0.2)"
                )
            
       ########### Map : Each year, quarter Insurance transactions ###########
        with col5:
            query = ("""SELECT state,FORMAT(SUM(ins_count),0) as count,FORMAT(SUM(ins_amt),0) as amount, SUM(ins_amt)/SUM(ins_count) as average 
                    FROM map_insurance
                    WHERE year = """ + str(choice_year) + """ AND quarter = """ + str(choice_quarter) + """
                    GROUP BY state;""")
            df = execute_query(query)
    
            for col in df.columns:
                df[col] = df[col].astype(str)
            
            #'India' + '<br>' + df['state'] + '<br><br>' + \
            df['text'] =  'Total Premium Value' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                'Insurance Policies(Nos.)' + '<br>' + df['count']
            
            fig = go.Figure(data=go.Choropleth(       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locationmode='geojson-id',
                locations=df['state'],
                z=df['average'],
                text=df['text'], # hover text
                
                autocolorscale=False,
                colorscale='Reds',
                marker_line_color='peachpuff',
            
                colorbar=dict(
                    title={'text': "Average PhonePe" + "<br>Insurance Amount"},
                    thickness=15,
                    len=0.35,
                    bgcolor='rgba(0,0,0,0.9)',     
                    ticks="outside",
                    tick0=1000,
                    dtick=250,
                    tickvals=[1000, 1250, 1500, 1750,2000,2250,2500],
                    tickprefix = "\u20B9",
                    tickmode="array",        
                    xanchor='left',
                    x=0.01,
                    yanchor='bottom',
                    y=0.05
                )
            ))
            
            fig.update_geos(
                visible=False,
                projection=dict(
                    type='conic conformal',
                    parallels=[12.472944444, 35.172805555556],
                    rotation={'lat': 24, 'lon': 80}
                ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]}
            )
            
            fig.update_layout(
                title=dict(
                    text="Statewise PhonePe Insurance payments<br>(Hover for breakdown)",
                    xanchor='center',
                    x=0.5,
                    yref='paper',
                    yanchor='bottom',
                    y=1,
                    pad={'b': 10}
                ),
                margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
                height=800,
                width=600
            )
            st.write(fig)
    ################### Map Insurance over ############
    ########### Insurance transactions and their value ###########
        with col6:
        
            query = """SELECT aggr_insurance.year as year, FORMAT(SUM(ins_count),0) as count,FORMAT(SUM(ins_amt),0) as amount, FORMAT( (SUM(ins_amt)/SUM(ins_count)),2) as average FROM aggr_insurance GROUP BY aggr_insurance.year;"""
            df = execute_query(query)
            fig = px.line(df, x='year', y='amount', color='average', markers=True, hover_data=['count','average'],title="Insurance payments for each year")
            fig.update_layout( autosize=False, width=650, height=300 )
            fig.update_layout(autotypenumbers='convert types')
            st.plotly_chart(fig)
    
            ########### Top 10 transactions ###########
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            option = st.radio("Top 10 insurance payments in - ", ["***State***", "***District***", "***Pincode***"],index=None)
    
            if option == "***State***":
                query = """SELECT state, FORMAT(SUM(ins_amt),0) AS amount, FORMAT(SUM(ins_count),0) as count,FORMAT((SUM(ins_amt)/SUM(ins_count)),2) as average
                    FROM aggr_insurance
                    GROUP BY state
                    ORDER BY SUM(ins_amt) DESC
                    LIMIT 10 """
                df = execute_query(query)
                df['text'] =  'Insurance Payment' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                        'Total policies ' + '<br>' + df['count']+  '<br><br>' + \
                        'Average Value' + '<br>'"\u20B9" + df['average']
                fig = px.bar(df, x='state', y='amount',hover_name="state",hover_data=['text'],color='average')
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***District***":
                query = """ (SELECT district_name, FORMAT(SUM(ins_amt),0) AS amount, FORMAT(SUM(ins_count),0) as count,FORMAT((SUM(ins_amt)/SUM(ins_count)),2) as average
                    FROM top_ins_dist
                    GROUP BY district_name
                    ORDER BY SUM(ins_amt) DESC
                    LIMIT 10 )"""
                df = execute_query(query)
                df['text'] =  'Insurance Payment' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                        'Total policies ' + '<br>' + df['count']+  '<br><br>' + \
                        'Average Value' + '<br>'"\u20B9" + df['average']
                fig = px.bar(df, x='district_name', y='amount',hover_name="district_name",hover_data=['text'],color='average')
                fig.update_layout(autotypenumbers='convert types')
                fig.update_layout( autosize=False, width=650, height=400 )
                fig.update_layout(yaxis={'categoryorder':'total descending'})
                st.write(fig)
    
            if option == "***Pincode***": 
                    query = """ SELECT pincode, FORMAT(SUM(pin_amount),0) AS amount, FORMAT(SUM(pin_count),0) as count,FORMAT((SUM(pin_amount)/SUM(pin_count)),2) as average
                    FROM top_ins_pin
                    GROUP BY pincode
                    ORDER BY SUM(pin_amount) 
                    LIMIT 10;"""
                    
                    df = execute_query(query)           
                    df['text'] =  'Insurance payment' + '<br>'"\u20B9" + df['amount']+  '<br><br>' + \
                            'Total policies ' + '<br>' + df['count']+  '<br><br>' + \
                            'Average Value' + '<br>'"\u20B9" + df['average']
                    
                    fig = px.line(df, x='pincode', y='amount', color='average', markers=True, hover_data=['text'])
                    
                    fig.update_xaxes(type='category')
                    fig.update_layout( autosize=False, width=650, height=400 )
                    
                    st.write(fig)

    ##### col 7 : 2 select boxes, col 8 : graph of query, col9: blank, col10: dataframe of query
    ########### Choose State, District to get transaction details ###########
        with col7:
            choice_state = st.selectbox('Select the state', options = state_list())
            if choice_state:
                choice_dist = st.selectbox('Select the district', options = district_list(choice_state,1))
        with col8:
            query = (f" SELECT year,FORMAT(SUM(ins_count),0) as count,FORMAT(SUM(ins_amt),0) as amount,FORMAT((SUM(ins_amt)/SUM(ins_count)),0) as average "          f" FROM top_ins_dist "
                            f" WHERE state = '{choice_state}'  AND district_name= '{choice_dist}' "
                            f"GROUP BY year;")
            df = execute_query(query)
            fig = px.scatter(df, x=df['year'], y=df['amount'],symbol=df['average'],
    	          color=df['count'],title="Insurance payments for a specific district each year"
                )
            fig.update_layout( autosize=False, width=550, height=400 )
            st.write(fig)
        with col10:
            st.write(df)
        
########################### end of  Transaction Data Visualisation ##############################################################   
        

    



