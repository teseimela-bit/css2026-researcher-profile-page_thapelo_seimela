# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 12:10:23 2026

@author: tesei
"""

import streamlit as st
import pandas as pd
import numpy as np

st.markdown("""
<style>
    .stApp{
        background-color: #87CEEB;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Target the sidebar container using its data-testid */
    [data-testid="stSidebarContent"] {
        background-color: #87CEEB; /* Example: Red background */
        color: white; /* Example: Change text color for contrast */
    }

    /* Target the overall sidebar element if needed (less common) */
    [data-testid="stSidebar"] {
        background-image: none; /* Ensure no default image interferes */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Set page title
st.set_page_config(page_title="Researcher Profile and STEM Data Explorer", layout="wide")

# Sidebar Menu
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Researcher Profile", "Publications", "STEM Data Explorer", "Contact"],
)

# Dummy STEM data
physics_data = pd.DataFrame({
    "Device": ["Pristine", "1%", "2%", "3%"],
    "FF (%)": [68.24, 68.36, 67.91, 68.18],
    "Jsc (mA/cm^2)": [10.81, 13.00, 14.92, 11.78],
    "Voc (V)": [0.632, 0.634, 0.627, 0.630],
    "PCE (%)": [4.67, 5.63, 6.36, 5.06],
    "Date": pd.date_range(start="2025-09-05", end = "2025-09-25", periods=4),
})

chargetransport_data = pd.DataFrame({
    "Device": ["Pristine", "1%", "2%", "3%"],
    "Jsat (mA/cm^2)": [10.96, 11.92, 13.11, 15.03],
    "Gmax (×10^26 m^-3 s^-1)": [5.04, 6.61, 8.58, 6.05],
    "M (×10^-4 cm^-2 V^-1 s^-1)":  [2.28, 2.69, 3.62, 2.56]
})

xrd_data = pd.DataFrame({
    "Peak":[111, 200, 220],
    "2 theta (deg)":[42.8, 49.9, 74.5],
    "FWHM (deg)":[0.867, 0.964, 0.714],
    "D (nm)": [9.737, 8.999, 13.823]
    
})

# Sections based on menu selection
if menu == "Researcher Profile":
    st.title("Researcher Profile")
    st.sidebar.header("Profile Options")

    # Collect basic information
    name = "Thapelo Seimela"
    field = "Material Scientist| Solar energy"
    department = "Department of Physics"
    institution = "University of Pretoria"
    address = "Lynnwood Rd, Hatfield, Pretoria, 0002"

    # Display basic profile information
    st.write(f"**Name:** {name}")
    st.write(f"**Field of Research:** {field}")
    st.write(f"**Department:** {department}")
    st.write(f"**Institution:** {institution}")
    st.write(f"**Address:** {address}")
    
    st.image(
    "20230422_143007.jpg",
    caption="University of Pretoria (Hatfield)"
)

elif menu == "Publications":
    st.title("Publications")
    st.sidebar.header("Upload and Filter")

    # Upload publications file
    uploaded_file = st.file_uploader("Upload a CSV of Publications", type="csv")
    if uploaded_file:
        publications = pd.read_csv("Publications.csv")
        st.dataframe(publications)

        # Add filtering for year or keyword
        keyword = st.text_input("Filter by keyword", "")
        if keyword:
            filtered = publications[
                publications.apply(lambda row: keyword.lower() in row.astype(str).str.lower().values, axis=1)
            ]
            st.write(f"Filtered Results for '{keyword}':")
            st.dataframe(filtered)
        else:
            st.write("Showing all publications")

        # Publication trends
        if "Year" in publications.columns:
            st.subheader("Publication Trends")
            year_counts = publications["Year"].value_counts().sort_index()
            st.bar_chart(year_counts)
        else:
            st.write("The CSV does not have a 'Year' column to visualize trends.")

elif menu == "STEM Data Explorer":
    st.title("STEM Data Explorer")
    st.sidebar.header("Data Selection")
    
    # Tabbed view for STEM data
    data_option = st.sidebar.selectbox(
        "Choose a dataset to explore", 
        ["Solar Cell Performance", "Charge Transport", "XRD Data"]
    )
    st.image(
        "Solar_cell_schem.jpg",
        caption = "Schematic diagram of organic solar cell containg copper nanorods and it's energy band diagram"
        )
    if data_option == "Solar Cell Performance":
        st.write("### A summary of device performance for the OSC with ITO/PEDOT:PSS/P3HT:PCBM/PDINO:CuNRs/Ag")
        st.dataframe(physics_data)
        # Add widget to filter by Energy levels
        performance_filter = st.slider("Filter by PCE (%))", 4.0, 7.0, (4.0, 7.0))
        filtered_physics = physics_data[
            physics_data["PCE (%)"].between(performance_filter[0], performance_filter[1])
        ]
        st.write(f"Filtered Results for PCE (%) {performance_filter}:")
        st.dataframe(filtered_physics)

    elif data_option == "Charge Transport":
        st.write("### Charge transport parameters of ITO/PEDOT:PSS/P3HT:PCBM/PDINO:CuNRs/Ag.")
        st.dataframe(chargetransport_data)
        # Add widget to filter by M
        chargetranport_filter = st.slider("Filter by M (M (×10^-4 cm^-2 V^-1 s^-1))", 2.0, 4.0, (2.0, 4.0))
        filtered_chargetransport = chargetransport_data[
            chargetransport_data["M (×10^-4 cm^-2 V^-1 s^-1)"].between(chargetranport_filter[0], chargetranport_filter[1])
        ]
        st.write(f"Filtered Results for Charge Transport {chargetranport_filter}:")
        st.dataframe(filtered_chargetransport)

    elif data_option == "XRD Data":
        st.write("### XRD Data")
        st.dataframe(xrd_data)
        # Add widgets to filter by temperature and humidity
        temp_filter = st.slider("Filter by FWHM (deg)", 0.0, 10.0, (0.0, 10.0))
        humidity_filter = st.slider("Filter by D (nm)", 8, 14, (8, 14))
        filtered_xrd = xrd_data[
            xrd_data["FWHM (deg)"].between(temp_filter[0], temp_filter[1]) &
            xrd_data["D (nm)"].between(humidity_filter[0], humidity_filter[1])
        ]
        st.write(f"Filtered Results for Temperature {temp_filter} and Humidity {humidity_filter}:")
        st.dataframe(filtered_xrd)
        
        
elif menu == "Contact":
    # Add a contact section
    st.header("Contact Information")
    email = "teseimela@gmail.com.com"
    linkedin = "https://www.linkedin.com/in/thapelo-seimela-680185b8/"
    orcid = "https://orcid.org/my-orcid?orcid=0000-0001-9961-4106"
    
    st.write(f"You can reach me at {email}.")
    st.write(f"My LinkedIn account in {linkedin}.")
    st.write(f"My Orcid {orcid}")
