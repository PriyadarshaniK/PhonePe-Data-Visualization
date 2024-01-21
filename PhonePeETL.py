import os
import git
import mysql.connector
import pandas as pd
import json

def GetData_git():
    try:
        os.environ["GIT_PYTHON_REFRESH"] = "quiet"
        username = 'PhonePe'
        repository = 'pulse'
        git.Git(f'{username}/').clone(f'https://github.com/{username}/{repository}.git')
    except:
        pass

#Download git data, this relative path will be later used in the code to access data.
GetData_git()

# connecting to the local database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepedb")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="phonepedb"
)

mycursor = mydb.cursor()


#create tables in PHONEPEDB
def create_tables():
    # Aggregate/Transaction table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Aggr_Trans 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        trans_name VARCHAR(50), 
                        trans_count INT, 
                        trans_amt BIGINT)""")
    # Aggregate/User table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Aggr_User 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        user_brand VARCHAR(50), 
                        user_count INT, 
                        user_pct FLOAT)""")

    # Aggregate/Insurance table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Aggr_Insurance 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        ins_name VARCHAR(50), 
                        ins_count MEDIUMINT, 
                        ins_amt BIGINT)""")
    # Map/Transaction table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Map_Trans 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        trans_count INT, 
                        trans_amt BIGINT)""")
    # Map/User table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Map_User 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        reg_users INT, 
                        app_opens INT)""")
    # Map/Insurance table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Map_Insurance 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        ins_count MEDIUMINT, 
                        ins_amt BIGINT)""")
    # Top/Transaction-District table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Trans_Dist 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        trans_count INT, 
                        trans_amt BIGINT)""")
    # Top/Transaction-Pincode table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Trans_Pin 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        pincode VARCHAR(10), 
                        pin_count INT, 
                        pin_amt BIGINT)""")
    # Top/User-District table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_User_Dist 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        reg_users INT)""")
    # Top/User-Pincode table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_User_Pin 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        pincode VARCHAR(10), 
                        reg_users MEDIUMINT)""")
    # Top/Insurance-District table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Ins_Dist 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        district_name VARCHAR(50), 
                        ins_count MEDIUMINT, 
                        ins_amt BIGINT)""")
    # Top/Insurance-Pincode table
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Top_Ins_Pin 
                        (state VARCHAR(50), 
                        year YEAR, 
                        quarter TINYINT, 
                        pincode VARCHAR(10), 
                        pin_count MEDIUMINT, 
                        pin_amount BIGINT)""")

# State names in phonePe Pulse data need to be converted to state names in geojson file so that data can be displayed on map
def modifyStateForGeoJson(state):
    if state == 'andaman-&-nicobar-islands':
        return 'Andaman & Nicobar'
    if state == 'andhra-pradesh':
        return 'Andhra Pradesh'
    if state == 'arunachal-pradesh':
        return 'Arunachal Pradesh'
    if state == 'assam':
        return 'Assam'
    if state == 'bihar':
        return 'Bihar'
    if state == 'chandigarh':
        return 'Chandigarh'
    if state == 'chhattisgarh':
        return 'Chhattisgarh'
    if state == 'dadra-&-nagar-haveli-&-daman-&-diu':
        return 'Dadra and Nagar Haveli and Daman and Diu'
    if state == 'delhi':
        return 'Delhi'
    if state == 'goa':
        return 'Goa'
    if state == 'gujarat':
        return 'Gujarat'
    if state == 'haryana':
        return 'Haryana'
    if state == 'himachal-pradesh':
        return 'Himachal Pradesh'
    if state == 'jammu-&-kashmir':
        return 'Jammu & Kashmir'
    if state == 'jharkhand':
        return 'Jharkhand'
    if state == 'karnataka':
        return 'Karnataka'
    if state == 'kerala':
        return 'Kerala'
    if state == 'ladakh':
        return 'Ladakh'
    if state == 'lakshadweep':
        return 'Lakshadweep'
    if state == 'madhya-pradesh':
        return 'Madhya Pradesh'
    if state == 'maharashtra':
        return 'Maharashtra'
    if state == 'manipur':
        return 'Manipur'
    if state == 'meghalaya':
        return 'Meghalaya'
    if state == 'mizoram':
        return 'Mizoram'
    if state == 'nagaland':
        return 'Nagaland'
    if state == 'odisha':
        return 'Odisha'
    if state == 'puducherry':
        return 'Puducherry'
    if state == 'punjab':
        return 'Punjab'
    if state == 'rajasthan':
        return 'Rajasthan'
    if state == 'sikkim':
        return 'Sikkim'
    if state == 'tamil-nadu':
        return 'Tamil Nadu'
    if state == 'telangana':
        return 'Telangana'
    if state == 'tripura':
        return 'Tripura'
    if state == 'uttar-pradesh':
        return 'Uttar Pradesh'
    if state == 'uttarakhand':
        return 'Uttarakhand'
    if state == 'west-bengal':
        return 'West Bengal'

# create dataframes from the phonepe pulse data and store them in individual tables
def create_data_dictionary():
    create_aggr_trans_insert()
    create_aggr_user_insert()
    create_aggr_ins_insert()

    create_map_trans_insert()
    create_map_user_insert()
    create_map_ins_insert()

    create_top_trans_dist_insert()
    create_top_trans_pin_insert()
    create_top_user_dist_insert()
    create_top_user_pin_insert()
    create_top_ins_dist_insert()
    create_top_ins_pin_insert()



# load the data into a dataframe and insert into the specific table
def create_aggr_trans_insert():
    
    #create the path to the point from which the names of states can be obtained.
    
    path="pulse/data/aggregated/transaction/country/india/state/"
    state_list=os.listdir(path)
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    trans_data={'State':[], 'Year':[],'Quarter':[],'Transaction_name':[], 'Transaction_count':[], 'Transaction_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for z in file_dict['data']['transactionData']:
                  name=z['name']
                  count=z['paymentInstruments'][0]['count'] # There is only one item inside the paymentInstruments list, hence can use index 0.
                  amount=z['paymentInstruments'][0]['amount']
                  trans_data['Transaction_name'].append(name)
                  trans_data['Transaction_count'].append(count)
                  trans_data['Transaction_amount'].append(amount)
                  trans_data['State'].append(modifyStateForGeoJson(i))
                  trans_data['Year'].append(j)
                  trans_data['Quarter'].append(int(k.strip('.json')))
    #Succesfully created a dataframe
    Agg_Trans=pd.DataFrame(trans_data)
    InsertDF6ToTable('aggr_trans',Agg_Trans)

def create_aggr_user_insert():
    path="pulse/data/aggregated/user/country/india/state/"
    state_list=os.listdir(path)
    
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    user_data={'State':[], 'Year':[],'Quarter':[],'User_brand':[], 'User_count':[], 'User_percentage':[]}
    
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                # print(path_k)
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                if (file_dict['data']['usersByDevice'] != None): 
                    for z in range(len(file_dict['data']['usersByDevice'])):                               
                      brand=file_dict['data']['usersByDevice'][z]['brand']
                      count=file_dict['data']['usersByDevice'][z]['count'] 
                      percentage=float(file_dict['data']['usersByDevice'][z]['percentage'])*100
                      user_data['User_brand'].append(brand)
                      user_data['User_count'].append(count)
                      user_data['User_percentage'].append(percentage)
                      user_data['State'].append(modifyStateForGeoJson(i))
                      user_data['Year'].append(j)
                      user_data['Quarter'].append(int(k.strip('.json')))
    
    #Succesfully created a dataframe
    Agg_User=pd.DataFrame(user_data)
    # insert this data into the table
    InsertDF6ToTable('aggr_user',Agg_User)

def create_aggr_ins_insert():
    
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/aggregated/insurance/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    ins_data={'State':[], 'Year':[],'Quarter':[],'Ins_name':[], 'Ins_count':[], 'Ins_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for z in file_dict['data']['transactionData']:
                  name=z['name']
                  count=z['paymentInstruments'][0]['count'] # There is only one item inside the paymentInstruments list, hence can use index 0.
                  amount=z['paymentInstruments'][0]['amount']
                  ins_data['Ins_name'].append(name)
                  ins_data['Ins_count'].append(count)
                  ins_data['Ins_amount'].append(amount)
                  ins_data['State'].append(modifyStateForGeoJson(i))
                  ins_data['Year'].append(j)
                  ins_data['Quarter'].append(int(k.strip('.json')))
    
    #Succesfully created a dataframe
    Agg_Ins=pd.DataFrame(ins_data)
    InsertDF6ToTable('aggr_insurance',Agg_Ins)

def create_map_trans_insert():
    
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/map/transaction/hover/country/india/state/"  
    state_list=os.listdir(path)

    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    trans_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'Transaction_count':[], 'Transaction_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for z in file_dict['data']['hoverDataList']:
                  name=z['name']
                  count=z['metric'][0]['count'] # There is only one item inside the metric list, hence can use index 0.
                  amount=z['metric'][0]['amount']
                  trans_data['district_name'].append(name)
                  trans_data['Transaction_count'].append(count)
                  trans_data['Transaction_amount'].append(amount)
                  trans_data['State'].append(modifyStateForGeoJson(i))
                  trans_data['Year'].append(j)
                  trans_data['Quarter'].append(int(k.strip('.json')))
    
    #Succesfully created a dataframe
    Map_Trans=pd.DataFrame(trans_data)
    InsertDF6ToTable('map_trans',Map_Trans)

def create_map_user_insert():
    
    #create the path to the point from which the names of states can be obtained.    
    path="pulse/data/map/user/hover/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    user_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'Reg_Users':[], 'App_Opens':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for z in file_dict['data']['hoverData'].items(): 
                  name=z[0] # 0 indicates key
                  reg_users=z[1]['registeredUsers'] # 1 indicates value
                  app_opens=z[1]['appOpens']
                  user_data['district_name'].append(name)
                  user_data['Reg_Users'].append(reg_users)
                  user_data['App_Opens'].append(app_opens)
                  user_data['State'].append(modifyStateForGeoJson(i))
                  user_data['Year'].append(j)
                  user_data['Quarter'].append(int(k.strip('.json')))
    
    #Succesfully created a dataframe
    Map_User=pd.DataFrame(user_data)
    InsertDF6ToTable('map_user',Map_User)

def create_map_ins_insert():
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/map/insurance/hover/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to dataframe
    Ins_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'ins_count':[], 'ins_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for z in file_dict['data']['hoverDataList']: 
                  name=z['name']
                  count=z['metric'][0]['count'] # There is only one item inside the metric list, hence can use index 0.
                  amount=z['metric'][0]['amount']
                  Ins_data['district_name'].append(name)
                  Ins_data['ins_count'].append(count)
                  Ins_data['ins_amount'].append(amount)
                  Ins_data['State'].append(modifyStateForGeoJson(i))
                  Ins_data['Year'].append(j)
                  Ins_data['Quarter'].append(int(k.strip('.json')))

    #Succesfully created a dataframe
    Map_Ins=pd.DataFrame(Ins_data)
    InsertDF6ToTable('map_insurance',Map_Ins)

def create_top_trans_dist_insert():
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/top/transaction/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    trans_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'Transaction_count':[], 'Transaction_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                
                for l in range(len(file_dict['data']['districts'])):
                    name=file_dict['data']['districts'][l]['entityName']
                    count=file_dict['data']['districts'][l]['metric']['count'] 
                    amount=file_dict['data']['districts'][l]['metric']['amount']
                    trans_data['district_name'].append(name)
                    trans_data['Transaction_count'].append(count)
                    trans_data['Transaction_amount'].append(amount)
                    trans_data['State'].append(modifyStateForGeoJson(i))
                    trans_data['Year'].append(j)
                    trans_data['Quarter'].append(int(k.strip('.json')))
                    
    
    #Succesfully created a dataframe
    Top_Trans_Dist=pd.DataFrame(trans_data)
    InsertDF6ToTable('top_trans_dist',Top_Trans_Dist)
    
def create_top_trans_pin_insert():
    path="pulse/data/top/transaction/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    trans_data={'State':[], 'Year':[],'Quarter':[], 'Pincode':[], 'Pin_count':[], 'Pin_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                
                for l in range(len(file_dict['data']['pincodes'])):
                    pin_name=file_dict['data']['pincodes'][l]['entityName']
                    pin_count=file_dict['data']['pincodes'][l]['metric']['count'] 
                    pin_amount=file_dict['data']['pincodes'][l]['metric']['amount']
                    trans_data['State'].append(modifyStateForGeoJson(i))
                    trans_data['Year'].append(j)
                    trans_data['Quarter'].append(int(k.strip('.json')))
                    trans_data['Pincode'].append(pin_name)
                    trans_data['Pin_count'].append(pin_count)
                    trans_data['Pin_amount'].append(pin_amount)
    
    #Succesfully created a dataframe
    Top_Trans_Pin=pd.DataFrame(trans_data)
    InsertDF6ToTable('top_trans_pin',Top_Trans_Pin)
    
def create_top_user_dist_insert():
    
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/top/user/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    user_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'Reg_User':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                for l in range(len(file_dict['data']['districts'])):
                    name=file_dict['data']['districts'][l]['name']
                    reg_users=file_dict['data']['districts'][l]['registeredUsers']
                    user_data['district_name'].append(name)
                    user_data['Reg_User'].append(reg_users)
                    user_data['State'].append(modifyStateForGeoJson(i))
                    user_data['Year'].append(j)
                    user_data['Quarter'].append(int(k.strip('.json')))
                    
    
    #Succesfully created a dataframe
    Top_User_Dist=pd.DataFrame(user_data)
    InsertDF5ToTable('top_user_dist',Top_User_Dist)
    
def create_top_user_pin_insert():
    path="pulse/data/top/user/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    user_data={'State':[], 'Year':[],'Quarter':[], 'Pincode':[], 'Reg_User':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                
                for l in range(len(file_dict['data']['pincodes'])):
                    pin_name=file_dict['data']['pincodes'][l]['name']
                    reg_users=file_dict['data']['pincodes'][l]['registeredUsers'] 
                    user_data['State'].append(modifyStateForGeoJson(i))
                    user_data['Year'].append(j)
                    user_data['Quarter'].append(int(k.strip('.json')))
                    user_data['Pincode'].append(pin_name)
                    user_data['Reg_User'].append(reg_users)
                    
    
    #Succesfully created a dataframe
    Top_User_Pin=pd.DataFrame(user_data)
    InsertDF5ToTable('top_user_pin',Top_User_Pin)

def create_top_ins_dist_insert():
    #create the path to the point from which the names of states can be obtained.
    path="pulse/data/top/insurance/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    ins_data={'State':[], 'Year':[],'Quarter':[],'district_name':[], 'Ins_count':[], 'Ins_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                
                for l in range(len(file_dict['data']['districts'])):
                    name=file_dict['data']['districts'][l]['entityName']
                    count=file_dict['data']['districts'][l]['metric']['count'] 
                    amount=file_dict['data']['districts'][l]['metric']['amount']
                    ins_data['district_name'].append(name)
                    ins_data['Ins_count'].append(count)
                    ins_data['Ins_amount'].append(amount)
                    ins_data['State'].append(modifyStateForGeoJson(i))
                    ins_data['Year'].append(j)
                    ins_data['Quarter'].append(int(k.strip('.json')))
    
    #Succesfully created a dataframe
    Top_Ins_Dist=pd.DataFrame(ins_data)
    InsertDF6ToTable('top_ins_dist',Top_Ins_Dist)
    
def create_top_ins_pin_insert():
    path="pulse/data/top/insurance/country/india/state/"  
    state_list=os.listdir(path)
    
    #This is to extract the statewise/yearwise/quarterwise data to create a dataframe
    #dictionary to hold the data which will be later converted to datafram
    
    # Top 10 Pincode and top 10 districts cudn't be combined bcoz in some json files, the districts are less ie not 10, hence pincode cannot be combined in the same list.
    ins_data={'State':[], 'Year':[],'Quarter':[], 'Pincode':[], 'Pin_count':[], 'Pin_amount':[]}
    
    for i in state_list:
        path_i=path+i+"/"
        year_list=os.listdir(path_i)
        for j in year_list:
            path_j=path_i+j+"/"
            json_file_list=os.listdir(path_j)
            for k in json_file_list:
                path_k=path_j+k
                json_file_handle=open(path_k,'r')
                file_dict=json.load(json_file_handle)
                
                for l in range(len(file_dict['data']['pincodes'])):
                    pin_name=file_dict['data']['pincodes'][l]['entityName']
                    pin_count=file_dict['data']['pincodes'][l]['metric']['count'] 
                    pin_amount=file_dict['data']['pincodes'][l]['metric']['amount']
                    ins_data['State'].append(modifyStateForGeoJson(i))
                    ins_data['Year'].append(j)
                    ins_data['Quarter'].append(int(k.strip('.json')))
                    ins_data['Pincode'].append(pin_name)
                    ins_data['Pin_count'].append(pin_count)
                    ins_data['Pin_amount'].append(pin_amount)
    
    #Succesfully created a dataframe
    Top_Ins_Pin=pd.DataFrame(ins_data)
    InsertDF6ToTable('top_ins_pin',Top_Ins_Pin)

# Get values from the DataFrame without the index
def InsertDF6ToTable(table_name,dataf):
    values = [tuple(row) for row in dataf.values]
    
    # Prepare the SQL query
    query = f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s, %s)"
    
    # Execute the query with the values    
    mycursor.executemany(query, values)
    
    # the connection is not autocommitted by default, so we must commit to save our changes
    mydb.commit()

# Get values from the DataFrame without the index
def InsertDF5ToTable(table_name,dataf):
    values = [tuple(row) for row in dataf.values]
    
    print(len(values))
    
    
    # Prepare the SQL query
    query = f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s)"
    
    # Execute the query with the values
    
    mycursor.executemany(query, values)
    
    # the connection is not autocommitted by default, so we must commit to save our changes
    mydb.commit()

create_tables()
create_data_dictionary()
