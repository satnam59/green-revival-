import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import folium
from streamlit_folium import st_folium
import requests
import datetime
st.title("Project 2: Data Analysis and Visualization")
RECOMMENDED_ACTIONS_HEADER = "### 🔧 Recommended Actions:"
DISSOLVED_OXYGEN = "Dissolved Oxygen"
selected_type=st.sidebar.selectbox("Select any type",["choose below","Energy", "Water", "Forest"])
tab1,tab2,tab3,tab4,tab5=st.tabs(["Data","Visualization","Prediction","Awareness","Solution"])
if selected_type=="Energy":
    ENERGY_COLUMN = "Total electricity production, India"
    with tab1:
        st.header("Energy Data")
        energy_data=pd.read_csv("electricity.csv")
        st.dataframe(energy_data)
    with tab2:   
        st.header("Energy Visualization") 
        st.subheader("Energy Production Over the Years in india using Bar Chart")
        st.bar_chart(energy_data, x="Year", y=ENERGY_COLUMN,use_container_width=True)
        st.subheader("Energy Production Over the Years in india using Line Chart")
        st.line_chart(energy_data, x="Year", y=ENERGY_COLUMN)
        st.plotly_chart(px.scatter(energy_data, x="Year", y=ENERGY_COLUMN), use_container_width=True)
    with tab3:
        st.header("Energy Prediction")
        X = energy_data[["Year"]]
        y = energy_data[ENERGY_COLUMN]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        input_year = st.number_input("Enter a year to predict energy production:", min_value=2025, max_value=2100, value=2027)
        if st.button("Predict Energy Production"):
            future_years = np.array([[input_year]])
            predictions = model.predict(future_years)
            prediction_df = pd.DataFrame({"Year": future_years.flatten(), "Predicted Energy Production": predictions,"unit":"GWh"})
            st.dataframe(prediction_df)
    with tab4:
        st.header("⚡ Electricity Awareness")

        st.subheader("📊 Key Facts")
        st.write("""
        - Electricity demand is rising rapidly.
        - Most electricity comes from fossil fuels.
        - High consumption increases pollution.
        """)

        st.subheader("⚠️ Issues")
        st.write("""
        - Overconsumption of electricity
        - Dependence on non-renewable sources
        - Energy inefficiency
        """)

        st.subheader("🌍 Environmental Impact")
        st.write("""
        - Climate change due to carbon emissions
        - Water usage in power plants
        - Deforestation
        """)
    with tab5:
        import streamlit as st

        # Function to classify usage
        def classify_energy(consumption):
            if consumption < 900000:
                return "Low"
            elif consumption < 1500000:
                return "Medium"
            else:
                return "High"



        st.header("🌱 Electricity Solutions & Suggestions")

        # User Input
        consumption = st.number_input("Enter Electricity Consumption (GWh)")

        if consumption > 0:
            level = classify_energy(consumption)

            st.subheader(f"⚡ Usage Level: {level}")

            # Suggestions based on prediction
            if level == "High":
                st.error("🚨 High Electricity Consumption Detected")

                st.write(RECOMMENDED_ACTIONS_HEADER)
                st.write("""
                - Reduce unnecessary appliance usage  
                - Switch to energy-efficient devices (LED, inverter appliances)  
                - Install solar panels or renewable energy systems  
                - Avoid peak-time electricity usage  
                - Use smart meters to monitor consumption  
                """)

            elif level == "Medium":
                st.warning("⚠️ Moderate Electricity Consumption")

                st.write(RECOMMENDED_ACTIONS_HEADER)
                st.write("""
                - Optimize electricity usage  
                - Turn off unused devices  
                - Upgrade to energy-efficient appliances  
                - Monitor daily consumption  
                """)

            else:
                st.success("✅ Efficient Electricity Usage")

                st.write(RECOMMENDED_ACTIONS_HEADER)
                st.write("""
                - Maintain current usage levels  
                - Continue using eco-friendly practices  
                - Promote awareness among others  
                """)

        else:
            st.info("👆 Please enter consumption value to get suggestions")
elif selected_type=="Water":
    # ------------------ DATA TAB ------------------
    with tab1:
        st.header("💧 Water Data")
        water_data = pd.read_csv("water.csv")

        st.dataframe(water_data)
        st.subheader("Summary Statistics")
        st.table(water_data.describe())

    # ------------------ VISUALIZATION TAB ------------------
    with tab2:
        st.header("📊 Water Visualization")

        water_data = pd.read_csv("water.csv")

        # Clean column names

        # (Optional) If your dataset has min/max → create avg columns
        # Uncomment if needed
        # water_data["pH"] = (water_data["pH - Min"] + water_data["pH - Max"]) / 2
        # water_data["BOD"] = (water_data["BOD (mg/L) - Min"] + water_data["BOD (mg/L) - Max"]) / 2
        # water_data["Dissolved Oxygen"] = (water_data["Dissolved - Min"] + water_data["Dissolved - Max"]) / 2

        # Label function
        def label_water(row):
            if (6.5 <= row["pH"] <= 8.5) and (row["BOD"] < 3) and (row["Dissolved_Oxygen"] > 5) and (row["Nitrate"] < 10):
                return "Pure"
            else:
                return "Impure"

        # FIXED LINE ✅
        water_data["Water_Quality"] = water_data.apply(label_water, axis=1)

        # Correlation
        # st.subheader("📊 Correlation Heatmap")
        # st.write(water_data.select_dtypes(include='number').corr())

        # # Box Plot
        # st.subheader("📦 BOD Distribution")
        # st.plotly_chart(px.box(water_data, y="BOD"))

        # # Scatter Plot
        # st.subheader("🔬 pH vs Oxygen")
        # st.plotly_chart(px.scatter(
        #     water_data,
        #     x="pH",
        #     y="Dissolved_Oxygen",   # FIXED
        #     color="Water_Quality"
        # ))

        # Pie Chart
        st.subheader("🥧 Water Quality Distribution")
        st.plotly_chart(px.pie(
            water_data,
            names="Water_Quality",
            title="Water Quality Distribution",
        ))
    with tab3:
        st.header("💧 Water Purity Prediction")

        data = pd.read_csv("water.csv")
        
        data = data.drop(columns=["Unnamed: 0"], errors='ignore')
        data.columns = data.columns.str.strip()
        
        # Label creation
        def label_water(row):
            if (6.5 <= row["pH"] <= 8.5) and (row["BOD"] < 3) and (row["Dissolved_Oxygen"] > 5) and (row["Nitrate"] < 10):
                return 1
            else:
                return 0

        data["Water_Quality"] = data.apply(label_water, axis=1)

        # Features
        X = data[["Temperature", "pH", "Dissolved_Oxygen", "BOD", "Nitrate"]]
        y = data["Water_Quality"]
        
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        model = DecisionTreeClassifier(random_state=42, ccp_alpha=0.0)
        model.fit(X_train, y_train)
        
        # Input
        temp = st.number_input("Temperature")
        ph = st.slider("pH", 0.0, 14.0, 7.0)
        do = st.number_input("Dissolved Oxygen")
        bod = st.number_input("BOD")
        nitrate = st.number_input("Nitrate")

        if st.button("Predict Water Quality"):
            result = model.predict([[temp, ph, do, bod, nitrate]])

            if result.item() == 1:
                st.session_state["water_result"] = 1
                st.success("✅ Water is PURE")
            else:
                st.session_state["water_result"] = 0
                st.error("❌ Water is IMPURE")

            # Accuracy (optional)
            from sklearn.metrics import accuracy_score  # type: ignore[import]
            y_pred = model.predict(X_test)
            st.write("Model Accuracy:", accuracy_score(y_test, y_pred))
        
    with tab4:
        st.header("🌱 Water Solutions")

        if "water_result" in st.session_state:

            if st.session_state["water_result"] == 0:
                st.error("🚨 Water is Polluted")

                st.write("""
                - Treat wastewater before use  
                - Reduce industrial discharge  
                - Avoid dumping waste in water bodies  
                - Use filtration systems  
                """)

            else:
                st.success("✅ Water is Safe")

                st.write("""
                - Maintain water quality  
                - Prevent contamination  
                - Regular monitoring  
                """)

        else:
            st.info("👆 Please predict water quality first")
