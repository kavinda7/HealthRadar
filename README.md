# 🩺 HealthRadar

**Predict Outbreaks Before They Spread**  
An AI-powered early warning system that combines satellite weather data, crowdsourced symptoms, and verified health intelligence to detect potential disease outbreaks.

---

## 🌐 Live Demo

[Coming Soon]  
📱 Mobile-friendly | 🔐 Public-first | 🛰️ Earth-aware
![image](https://github.com/user-attachments/assets/0566c9b3-bcb7-4419-b358-8331d737c800)

---

## ⚙️ How It Works

HealthRadar integrates four core data streams:

- **🌍 Copernicus Satellite Data**  
  - Sentinel-3: Land Surface Temperature  
  - Sentinel-5P: Air Pollution  
  - Sentinel-1: Soil Moisture & Flood Detection  

- **📡 Galileo GNSS Data**  
  - Precise location tracking for symptom reports  
  - Optional mobility insights  

- **👥 Community Symptom Reports**  
  - Real-time reports from users  
  - Includes severity and disease-specific symptoms  

- **📰 Verified Health Intelligence**  
  - WHO, ECDC, THL outbreak bulletins  
  - Scraped and analyzed for outbreak confirmation  

These inputs are processed using AI to generate:
- 🌡️ Environmental Risk Score  
- 📊 Symptom Clustering Score  
- 🚨 Outbreak Risk Score (ORS)

Smart alerts are triggered when threshold risk levels are reached.

---

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Mapbox GL  
- **Backend**: Node.js, Express (optional), Firebase (Auth + DB)  
- **Data Processing**: Python, Pandas, SentinelHub API, ERA5  
- **AI/ML**: Rule-based and threshold logic for ORS (PoC)  
- **Design**: Figma, Lovable (prototype), GitHub Actions (CI/CD)

---

## 📦 Features

- 🌍 Interactive map with heatmaps (temperature, pollution, flood zones)  
- 📍 Symptom pindrops with severity tooltips  
- 🧠 Disease-specific filters (COVID-19, Influenza, Heatstroke, Norovirus)  
- 📊 Live outbreak KPIs  
- 📝 Self-report form with geotagged inputs  
- 🧑‍⚕️ User profile with badges and reporting history  
- 🔔 Risk-based outbreak alerts  

---

## 👥 Team

- **David van Dommelen** – Project Lead | Product Owner, PyTorch Developer (HealthTech)  
- **Kavinda Kulasinghe** – Tech Lead | Software Development  
- **Máté Tóth** – Data Scientist / AI Engineer | Research Engineer  
- **Dr. Shanuri Ranasinghe** – Public Health Expert | Medical Doctor  
- **Shweta Mudaliar** – Marketing & Partnerships | International Business  
- **Niranjan Sreegith** – Full Stack Developer | Software Development  
- **Victor Nwankwo** – Business Strategist | Business Analytics

