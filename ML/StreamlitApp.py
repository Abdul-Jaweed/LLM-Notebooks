import streamlit as st
import pandas as pd
import pickle


## Load the model

with open("laptopModel.pkl", "rb") as file:
    load_model = pickle.load(file)


st.title(":red[Laptop Price Predictor]")


brand = st.selectbox("Brand Name", [
    "ASUS",
    "Lenovo",
    "DELL",
    "HP",
    "acer",
    "RedmiBook",
    "MSI",
    "Infinix",
    "APPLE",
    "Others"
])

os = st.selectbox("Operating System", ['Windows', 'Mac', 'Others'])

ram_type = st.selectbox("Ram Type", ['DDR4', 'DDR5', 'Others'])

ram_size = st.selectbox("Ram Size (FB)", [4,8,16,32])

processor = st.selectbox("Processor", ["Intel", "AMD", "Others"])

gpu = st.selectbox("GPU", ["Intel", "AMD","NVIDIA", "Others"])

warranty = st.selectbox("Warranty (in Years)", [1, 2])

screen = st.selectbox("Screen Size", [14.0,15.6])

disk_type = st.selectbox("Disk Type", ["SSD", "HDD"])

disk_size = st.selectbox("Disk Size (GB)", [128,256, 512, 1024])



columns = ["Brand Name", "OS", "Ram Type", "RAM", "Processor", "GPU", "Warranty", "ScreenSize", "Disk Type", "DISK SIZE"]

new_data = pd.DataFrame([[
    brand,
    os,
    ram_type,
    ram_size,
    processor,
    gpu,
    warranty,
    screen,
     disk_type,
     disk_size
]], columns=columns)


if st.button("Predict Price"):
    predicted_price = load_model.predict(new_data)[0]
    round_of = abs(predicted_price)
    st.success(f"Estimated Laptop Price is : ₹ {round(round_of)}")