\
# BlockPhantom — Web3 Risk Intelligence  
Analyze ETH & ADA wallets with advanced scoring, transaction simulation, and PDF reporting.

BlockPhantom is a cross-chain risk-analysis engine built for blockchain research, security demos, and hackathon projects.  
It provides **real-time wallet scoring**, **risk probability**, **breakdowns**, **transaction activity**, and **auto-generated PDF reports** — with a fully responsive React UI.

---

## Features

### Backend (FastAPI)
- Smart randomized risk scoring engine  
- 70% scores between 40–55 (realistic range)  
- Probability model tied to score  
- Simulated realistic wallet statistics  
- Fake on-chain transactions  
- PDF report generation  
- Instant response (<5ms)  
- CORS enabled for React frontend  

### Frontend (React)
- Clean professional UI  
- Auto chain detection (Cardano / Ethereum)  
- Real-time analysis  
- Beautiful score breakdown cards  
- Fake transaction displays  
- PDF download with one click  
- Gradient purple theme  
- Fully mobile responsive  

---

## Folder Structure

blockphantom/
│
├── backend/
│ ├── app.py # FastAPI backend
│ ├── requirements.txt
│ └── README_backend.md
│
├── blockphantom-frontend/
│ ├── src/
│ │ ├── App.js # Main frontend file
│ │ ├── App.css
│ │ └── components/
│ ├── public/
│ └── package.json
│
└── README.md # Main documentation


