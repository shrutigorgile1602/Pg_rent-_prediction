import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="PG Rent Prediction", layout="wide")

# -------------------------
# CUSTOM CSS (BLACK THEME)
# -------------------------
st.markdown("""
<style>

/* FULL BLACK BACKGROUND */
.stApp {
    background-color: #000000;
    color: #ffffff;
}

/* ALL TEXT WHITE */
h1, h2, h3, h4, h5, h6, p, label, span {
    color: #ffffff !important;
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    background-color: #111111 !important;
    color: white !important;
    border: 1px solid #ffffff !important;
    border-radius: 8px;
}

/* DROPDOWN OPTIONS */
div[role="listbox"] {
    background-color: #000000 !important;
}

div[role="option"] {
    color: #ffffff !important;
    background-color: #000000 !important;
}

/* HOVER EFFECT */
div[role="option"]:hover {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* BUTTON (GREEN) */
.stButton>button {
    background-color: #00ff88 !important;
    color: black !important;
    border-radius: 8px;
    font-weight: bold;
}

/* INPUT BOX */
input {
    background-color: #111111 !important;
    color: white !important;
}

/* SLIDER */
.stSlider span {
    color: #ffffff !important;
}

/* TABLE */
.dataframe {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# DATABASE CONNECTION
# -------------------------
try:
    import mysql.connector
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="pg_rent_dbase"
    )
    USE_DB = True
except:
    conn = None
    USE_DB = False

# -------------------------
# PREDICTION HISTORY (in-memory fallback)
# -------------------------
if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# -------------------------
# LOAD MODEL
# -------------------------
model = pickle.load(open("pg_rent_model.pkl", "rb"))
le_location = pickle.load(open("le_location.pkl", "rb"))
le_sharing = pickle.load(open("le_sharing.pkl", "rb"))

# -------------------------
# SESSION STATE
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

# -------------------------
# PAGE 1: WELCOME
# -------------------------
if st.session_state.page == 1:

    st.markdown("<h1>🏠 Welcome to PG Rent Prediction System</h1>", unsafe_allow_html=True)

    st.markdown("<h3>🎯 Predict rent easily based on location & sharing</h3>", unsafe_allow_html=True)
    location = st.selectbox("📍 Location", le_location.classes_)
    sharing_type = st.selectbox("👥 Sharing Type", le_sharing.classes_)

    if st.button("🚀 Predict Rent"):

        st.session_state.location = location
        st.session_state.sharing = sharing_type

        loc_encoded = le_location.transform([location])[0]
        share_encoded = le_sharing.transform([sharing_type])[0]

        input_data = np.array([[
            loc_encoded, share_encoded, 500,
            1,1,1,1,1,1,1,1,1,1,
            1,1,4.5
        ]])

        prediction = model.predict(input_data)

        st.session_state.predicted_rent = int(prediction[0])

        st.session_state.page = 2
        st.rerun()

# -------------------------
# PAGE 2: AMENITIES
# -------------------------
elif st.session_state.page == 2:

    st.title("🔍 Customize Amenities")

    st.success(f"💰 Base Rent: ₹ {st.session_state.predicted_rent}")

    wifi = st.selectbox("WiFi", [0,1])
    ac = st.selectbox("AC", [0,1])
    food = st.selectbox("Food", [0,1])
    parking = st.selectbox("Parking", [0,1])
    laundry = st.selectbox("Laundry", [0,1])
    power = st.selectbox("Power Backup", [0,1])
    security = st.selectbox("Security", [0,1])
    housekeeping = st.selectbox("Housekeeping", [0,1])
    bathroom = st.selectbox("Attached Bathroom", [0,1])
    geyser = st.selectbox("Geyser", [0,1])

    size = st.slider("Room Size", 300, 700, 500)

    if st.button("🔄 Update Prediction"):

        loc_encoded = le_location.transform([st.session_state.location])[0]
        share_encoded = le_sharing.transform([st.session_state.sharing])[0]

        input_data = np.array([[
            loc_encoded, share_encoded, size,
            wifi, ac, food,
            parking, laundry, power,
            security, housekeeping, bathroom,
            geyser,
            1,1,4.5
        ]])

        prediction = model.predict(input_data)

        st.session_state.predicted_rent = int(prediction[0])

        # SAVE TO DATABASE OR SESSION
        if USE_DB:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Rent_predictions (location, sharing_type, predicted_rent)
                VALUES (%s, %s, %s)
            """, (st.session_state.location, st.session_state.sharing, int(prediction[0])))
            conn.commit()
        else:
            st.session_state.prediction_history.append({
                "location": st.session_state.location,
                "sharing_type": st.session_state.sharing,
                "predicted_rent": int(prediction[0])
            })

        st.success(f"💰 Updated Rent: ₹ {int(prediction[0])}")

    if st.button("➡️ Go to Data Page"):
        st.session_state.page = 3
        st.rerun()

# -------------------------
# PAGE 3: DATA
# -------------------------
elif st.session_state.page == 3:

    st.title("📊 Data & Prediction History")

    st.subheader("📌 PG Dataset")

    try:
        if USE_DB:
            df = pd.read_sql("SELECT * FROM pune_pg_dataset_1000 LIMIT 50", conn)
        else:
            df = pd.read_csv("pune_pg_dataset_1000.csv").head(50)
        st.dataframe(df)
    except:
        st.warning("No data found")

    st.subheader("📜 Prediction History")

    try:
        if USE_DB:
            history = pd.read_sql(
                "SELECT * FROM Rent_predictions ORDER BY id DESC LIMIT 10",
                conn
            )
            st.dataframe(history)
        else:
            if st.session_state.prediction_history:
                history = pd.DataFrame(st.session_state.prediction_history)
                st.dataframe(history)
            else:
                st.info("No predictions yet. Go back and make some predictions!")
    except:
        st.warning("No history found")

    if st.button("🔙 Back to Home"):
        st.session_state.page = 1
        st.rerun()
