# 🅿️ AI-Based Smart Parking System
### A Beginner-Friendly Streamlit Web App | College Mini Project

---

## 📌 Project Overview

This is a **Smart Parking Management System** built with Python and Streamlit.
It simulates an AI-powered parking system with real-time slot management,
automated booking, AI slot suggestions, demand prediction, and analytics.

---

## 🗂️ Project Structure

```
smart_parking/
│
├── app.py              ← Main application file (all code here)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## 🚀 How to Run

### Step 1 — Make sure Python is installed
```bash
python --version
# Should show Python 3.8 or higher
```

### Step 2 — (Optional) Create a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

### Step 5 — Open in browser
The app will automatically open at:
```
http://localhost:8501
```

---

## 🎯 Features

| Page           | Description                                      |
|----------------|--------------------------------------------------|
| 🏠 Home        | Dashboard with live metrics and occupancy chart |
| 🗺️ View Slots  | Visual map of all 30 parking slots (A1–C10)     |
| 📝 Book Slot   | Booking form — auto-assigns best available slot |
| 🤖 AI Suggest  | AI engine recommends the optimal slot           |
| 📈 Prediction  | 24-hour demand forecast with chart              |
| 🔧 Admin Panel | Manage bookings, update slots, reset system     |
| 📊 Reports     | Charts and analytics on usage and bookings      |

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** — Web UI framework
- **Pandas** — Data management
- **NumPy** — Numerical operations
- **Plotly** — Interactive charts

---

## 📚 How It Works

### Parking Slots
- 30 slots total: Rows A, B, C × 10 slots each
- Statuses: Available (🟢), Occupied (🔴), Reserved (🟡)

### Booking System
- User fills a form → System finds best available slot → Status updates to Reserved

### AI Suggestion Logic
```
Score = Distance from Entrance + (Occupied slots in zone × 0.5)
→ Lowest score = Best slot recommendation
```

### Demand Prediction
- Simulated 24-hour traffic pattern using sample data
- Time-of-day insights (Morning rush, Afternoon peak, etc.)

---

## 👨‍💻 For Students

This project is intentionally kept simple so you can:
- **Understand** every line of code
- **Modify** it easily for your own ideas
- **Present** it confidently as a mini project

Feel free to add features like:
- Login/authentication
- Database (SQLite) for persistent storage
- Real sensor data integration
- Email/SMS notifications

---

## 📝 License

Free to use for academic and educational purposes.
