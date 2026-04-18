# Pg_rent-_prediction
 PG Rent Prediction ML Project
# 🏠 PG Rent Prediction System

A Machine Learning-based web application that predicts PG (Paying Guest) rent in Pune based on location, sharing type, and amenities.

---

## 🚀 Project Overview

This project helps users:
- 💰 Predict PG rent instantly
- 📍 Select location & sharing type
- 🏡 Customize amenities
- 📊 View dataset & prediction history

---

## 🎯 Project Objectives

### 1️⃣ Rent Prediction
To develop a machine learning model that predicts PG rent based on:
- Location
- Sharing Type
- Amenities

### 2️⃣ PG Recommendation (Future Scope)
To suggest best PG accommodations based on:
- Budget
- Location
- Preferences

---

## 🧠 Machine Learning Model

- Model Used: **Random Forest Regressor**
- Features Used:
  - location
  - sharing_type
  - size_sqft
  - wifi, ac, food, parking, laundry
  - power_backup, security, housekeeping
  - attached_bathroom, geyser
  - gender, preferred_tenant, rating
- Target Variable:
  - rent

---
---

## 🌐 Deployment & Database

This project is deployed using **Streamlit Cloud**, enabling real-time interaction through a web-based interface.

- 🚀 **Frontend & Deployment:** Streamlit Cloud  
- 💻 **Backend:** Python (Machine Learning Model)  
- 🗄️ **Database (Optional / Scalable):** Railway (Cloud Database)

For deployment:
- The application is hosted on Streamlit Cloud using GitHub integration.
- Since local MySQL cannot be accessed in cloud environments, CSV is used for data handling during deployment.
- For scalable production use, the project can be connected to a cloud database such as **Railway**, allowing real-time data storage and retrieval.

This architecture ensures:
- 🌍 Accessibility from anywhere  
- ⚡ Fast deployment  
- 📈 Scalability for real-world applications  

---

## 📂 Project Structure
pg-rent-prediction/
│
├── app.py # Streamlit Application
├── pg_rent_model.pkl # Trained ML Model
├── le_location.pkl # Location Encoder
├── le_sharing.pkl # Sharing Encoder
├── pune_pg_dataset_1000.csv # Dataset
├── requirements.txt # Dependencies
└── README.md # Project Documentation


---

## ⚙️ Installation & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/pg-rent-prediction.git
cd pg-rent-prediction


---

## 📌 Conclusion

The **PG Rent Prediction System** is a practical machine learning application that helps users estimate rental prices based on real-world factors like location, sharing type, and amenities.

This project demonstrates:
- End-to-end ML pipeline (data → model → deployment)
- Real-world problem solving
- Interactive UI using Streamlit
- Integration of data, model, and user experience

It can be further expanded into a **full-scale rental platform** with recommendation systems, analytics dashboards, and real-time data integration.

---
# Deploy link

[https://pgrentprediction.streamlit.app/
](https://pgrentprediction.streamlit.app/)

## 👩‍💻 Author

**Shruti Gorgile**  
🎓 Aspiring Data Analyst | Machine Learning Enthusiast  

- 💼 Interested in: Data Science, ML, Analytics  
- 📍 Location: Pune, India  

---
