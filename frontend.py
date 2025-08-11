import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Page Config
st.set_page_config(page_title='House Price Prediction', page_icon='🏠', layout='wide') 

# Title and Intro
st.title('🏠 Bengaluru House Price Predictor')
st.markdown("### Welcome! Enter the details below to estimate the price of a house in Bengaluru.")
st.write("---")

# Load Data and Model
df = pd.read_csv('copied.csv')
with open('RFmodel.pkl', 'rb') as file:
    model = pickle.load(file)

# Sidebar for Dataset Preview
#with st.sidebar:
    #st.header("📊 Dataset Overview")
    #if st.checkbox("Show Data Sample"):
        #st.dataframe(df.head(10))

# Form for Input
with st.form("prediction_form", clear_on_submit=False): # Creating a form for user input
    col1, col2 = st.columns(2)
    
    location_list = sorted(df['location'].unique()) # Getting unique locations from the dataset
    loc = col1.selectbox('Select Location:', options=location_list)
    sqft = col2.number_input('Total Square Feet', min_value=300)
    bath = col1.number_input('Number of Bathrooms', min_value=1)
    bhk = col2.number_input('Number of Bedrooms (BHK)', min_value=1)
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1]) # Adjusting button columns
    with btn_col2:  # middle column
        submitted = st.form_submit_button("💡 Predict Price", use_container_width=True)

# Prediction
if submitted: # When the form is submitted
    loc_index = location_list.index(loc)
    input_values = [(loc_index, sqft, bath, bhk)]
    out = model.predict(input_values)
    
    price = out[0] * 100000 # Converting the output to actual price in rupees
    price_lakhs = price / 100000 # Converting price to lakhs
    price_crores = price / 10000000 # Converting price to crores
    
    st.success(f"Estimated Price: ₹ {price:,.0f}") # Displaying the price in a formatted way
    st.write(f"💰 In Lakhs: **₹ {price_lakhs:.2f} L**") 
    st.write(f"🏦 In Crores: **₹ {price_crores:.2f} Cr**")
    
    # Confidence Range (Assuming ±10% variation)
    st.info(f"Possible Price Range: ₹ {price*0.9:,.0f} - ₹ {price*1.1:,.0f}") # Displaying a range of possible prices

# Footer
#st.write("---")
#st.caption("📌 Disclaimer: This is an estimate based on historical data and may not reflect actual market prices.")

