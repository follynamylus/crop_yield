import streamlit as st
import pandas as pd
import numpy as np
import pickle

tab_1,tab_2 = st.tabs(['VIEW PREDICTION','DATAFRAME AND DOWNLOAD'])

option = st.sidebar.selectbox("Choose the type of prediction to perform",["Single","Multiple"])

model = pickle.load(open("finalized_model.pkl", 'rb'))

if option.lower() == "single" :
    st.sidebar.title("Data Input")
    rain = st.sidebar.number_input("Input the amount of Rain",0,500)
    season = st.sidebar.selectbox("Select Season",["Kharif","Rabi","Summer","Whole Year","Winter","Autumn"])
    temp = st.sidebar.number_input("Input the amount of temperature",-10,40)
    crop = st.sidebar.selectbox("Select Crop",["Maize","Rice","Moong(Green Gram)","Urad","Groundnut","Sesamum",
                                            "Wheat","Rapeseed &Mustard","Arhar/Tur","Jowar","Gram","Dry chillies",
                                            "Onion","Potato","Sugarcane"])
    ph = st.sidebar.number_input("Input the PH value",3,8)
    nitro = st.sidebar.number_input("Input the soil nitrogen value",180,600)
    elect = st.sidebar.number_input("Input the soil electrical conductivity",1,6)

    df = pd.DataFrame()

    df['Rainfall'] = [rain]
    df['Season'] = [season]
    df['Temperature'] = [temp]
    df['Crop'] = [crop]
    df["pH"] = [ph]
    df['Nitrogen(kg/ha)'] = [nitro]
    df['ElectricalConductivity(ds/m)'] = [elect]

    cols = ["Season","Crop"]

    dummied_cols = pd.get_dummies(df[cols])
    lists = []


    encode_cols = ['Season_Autumn', 'Season_Kharif', 'Season_Rabi', 'Season_Summer',
        'Season_Whole Year', 'Season_Winter', 'Crop_Arhar/Tur',
        'Crop_Dry chillies', 'Crop_Gram', 'Crop_Groundnut', 'Crop_Jowar',
        'Crop_Maize', 'Crop_Moong(Green Gram)', 'Crop_Onion', 'Crop_Potato',
        'Crop_Rapeseed &Mustard', 'Crop_Rice', 'Crop_Sesamum', 'Crop_Sugarcane',
        'Crop_Urad', 'Crop_Wheat']

    df_encode = pd.DataFrame()
    for i in (encode_cols) : 
        if i in (dummied_cols.columns) :
            df_encode[i] = [1]
        else :
            df_encode[i] = [0]


    data = df.drop(cols,axis=1)
    data = data.join(df_encode)

    pred = model.predict(data)
    
    if pred < 0 :
        pred = 0
    else :
        pred = pred

    df['Predict'] = [pred]
    tab_1.write(f"""When the value for rainfall is {rain}, the season is {season}, temperature as {temp},
                the crop as {crop}, soil PH as {ph}, Soil nitrogen as {nitro},
                and soil electrical conductivity as {elect} will yield {pred}
        
        """)

    tab_2.dataframe(df) # <--------------- Display the dataframe on tab2
    @st.cache_data # <------------- IMPORTANT: Cache the conversion to prevent computation on every rerun

    def convert_df(df): # <--------------- Function declaration
        '''
        Convert_df function converts the resulting dataframe to a CSV file.
        It takes in a data frame as a aprameter.
        It returns a CSV file
        '''
        
        return df.to_csv().encode('utf-8') # <--------------- Return dataframe as a CSV file
    csv = convert_df(df) # <------------ Convert_df function calling and assigning to a variable.
    tab_2.success("Print Result as CSV file") # <--------------- A widget as heading for the download option in tab 2
    tab_2.download_button("Download",csv,"Prediction.csv",'text/csv') # <------------------ Download button widget in tab 2
    tab_2.write(df)

    
else :
    file = st.sidebar.file_uploader("Input File")
    if file == None :
        st.write("A file should be uploaded")
    else :
        @st.cache_data
        def load(data) :
            df = pd.read_csv(data)
            return df
        
        df = load(file)

        data = df.copy()

        cols = ["Season","Crop"]
        new_df = pd.get_dummies(data[cols])
        data = data.drop(cols,axis=1)
        data = data.join(new_df)

        pred = model.predict(data)
        lists = []
        for i in pred :

            if i < 0 :
                lists.append(0)
            else :
                lists.append(i)


        df['prediction'] = lists

        tab_1.write(df)

        tab_2.dataframe(df) # <--------------- Display the dataframe on tab2
        @st.cache_data # <------------- IMPORTANT: Cache the conversion to prevent computation on every rerun

        def convert_df(df): # <--------------- Function declaration
            '''
            Convert_df function converts the resulting dataframe to a CSV file.
            It takes in a data frame as a aprameter.
            It returns a CSV file
            '''
            
            return df.to_csv().encode('utf-8') # <--------------- Return dataframe as a CSV file
        csv = convert_df(df) # <------------ Convert_df function calling and assigning to a variable.
        tab_2.success("Print Result as CSV file") # <--------------- A widget as heading for the download option in tab 2
        tab_2.download_button("Download",csv,"Prediction.csv",'text/csv') # <------------------ Download button widget in tab 2.
