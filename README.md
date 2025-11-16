
# SymptomSense

**SymptomSense** is an AI-powered disease prediction application that provides instant health insights based on user-reported symptoms. Built with a **Flask backend** and **React frontend**, it leverages machine learning to offer disease predictions, medication guidance, detailed explanations, and tele-support connectivity.

---

## Features

- **Instant Disease Prediction** – Top 3 probable diseases with confidence scores.  
- **Medication Guidance** – Immediate treatment suggestions.  
- **Clear Explanations** – Detailed descriptions and severity levels.  
- **Tele-Support Integration** – Connect with medical professionals.  
- **User-Friendly Interface** – Responsive React-based frontend.  
- **RESTful API** – Well-documented Flask API for easy integration.

---

## Tech Stack

### Backend
- Python 3.x  
- Flask – Web framework  
- scikit-learn – Machine learning library  
- joblib – Model serialization  
- numpy – Numerical computing  
- flask-cors – Cross-Origin Resource Sharing  

### Frontend
- React 18 – UI library  
- React Router DOM – Client-side routing  
- Axios – HTTP client for API calls  
- CSS – Custom styling  

---

## Prerequisites

- Python 3.8+  
- Node.js 16+  
- npm or yarn  

---

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Ensure model files are present:
- `model.pkl` – Trained ML model  
- `tfidf.pkl` – TF-IDF vectorizer  
- `mapping.json` – Disease information mapping  
- `label_encoder.pkl` – Label encoder (optional)  

### Frontend Setup

```bash
cd frontend
npm install
```
```

---


### Application Flow
- **Home Page** – Overview of features  
- **Prediction Page** – Enter symptoms, age, and gender to get predictions  
- **Tele-Support Page** – Access telemedicine consultation  



## Project Structure

```
SymptomSense/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── model.pkl
│   ├── tfidf.pkl
│   ├── mapping.json
│   ├── label_encoder.pkl
│   └── symptomsense_final_40diseases.csv
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── api/client.js
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   ├── package.json
│   └── README.md
└── README.md
```

---

Author - SHAZIA AFRAZ
