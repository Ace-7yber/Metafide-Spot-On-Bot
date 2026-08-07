# Metafide-Spot-On-Bot
Real-time hybrid ML trading signal backend built with Python, FastAPI, and Scikit-Learn. Integrates live Binance market data with a Random Forest Classifier, dynamic 7-2-1 spot price spreads, an automated feedback memory loop, and Metafide API authentication.
Here is a beautifully formatted, clean, and ready-to-use **`README.md`** file for your GitHub repository. It fixes syntax errors (like missing line breaks in bash commands), uses standard GitHub Markdown badges, and applies crisp visual formatting to make your repository look top-tier.

Copy and paste everything in the code block below directly into your **`README.md`** file:

```markdown
# 🧠 Smart Brain — ML Trading Bot & Signal API

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A real-time hybrid Machine Learning backend designed to forecast short-term cryptocurrency price movements and output tactical entry/exit spot price spreads.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have the following installed on your system:
* **Python 3.9+**
* **Pip** (Python package manager)

---

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/YOUR_USERNAME/smart-brain-bot.git](https://github.com/YOUR_USERNAME/smart-brain-bot.git)
cd smart-brain-bot

pip install fastapi uvicorn pandas scikit-learn joblib requests

```

---

### 3. Running the API Server

Start the backend service using **Uvicorn**:

```bash
python smart_brain.py

```

* 🌐 **API Base URL:** `http://localhost:8000`
* 📑 **Interactive Docs (Swagger UI):** `http://localhost:8000/docs`

---

## 📡 API Endpoints

### 1. Request Signal / Predict Spots

Retrieves predicted market action, confidence level, and generated spot price levels based on live market indicators.

* **Method:** `GET`
* **Endpoint:** `/api/predict`
* **Query Parameters:**

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `current_price` | `float` | **Yes** | — | Current spot price of the asset. |
| `up_range` | `float` | No | `15` | Upper spread range limit. |
| `down_range` | `float` | No | `15` | Lower spread range limit. |
| `gid` | `string` | No | `"0"` | Unique Round / Game ID for tracking. |

#### 📥 Example Request

```http
GET http://localhost:8000/api/predict?current_price=95000.00&up_range=20&down_range=20&gid=ROUND_101

```

#### 📤 Example Response

```json
{
  "action": "BULLISH_DRIFT",
  "confidence": 85,
  "spots": [
    94982.15,
    94990.43,
    95000.00,
    95003.45,
    95006.12,
    95009.80,
    95012.30,
    95015.65,
    95018.90,
    95021.10
  ]
}

```

---

### 2. Log Feedback / Store Outcome

Logs actual trade results back into memory to continuously build historical training data.

* **Method:** `POST`
* **Endpoint:** `/api/feedback`

#### 📥 Example Request Body

```json
{
  "gid": "ROUND_101",
  "actual_price": 95015.50
}

```

#### 📤 Example Response

```json
{
  "status": "success"
}

```

---

## 🧠 Training the Machine Learning Brain

To retrain the Random Forest Classifier on newly accumulated market feedback:

1. Ensure the bot has logged at least **50 rounds** into `1m_brain_memory.csv`.
2. Run the offline training script:

```bash
python train_brain.py

```

### ⚙️ What the Training Script Executed:

1. Loads historical market features from `1m_brain_memory.csv`.
2. Computes ground-truth price direction targets ($\Delta P > 0$).
3. Trains an **80/20 train-test split** Random Forest Classifier (100 estimators, max depth 5).
4. Displays classification performance metrics and accuracy evaluation reports.
5. Exports updated model weights to `brain_model.pkl` for immediate use by `smart_brain.py`.

---

## 🛠️ Tech Stack & Dependencies

| Component | Technology Used |
| --- | --- |
| **Language** | Python 3.9+ |
| **Web Framework** | FastAPI & Uvicorn (REST API & CORS Support) |
| **Machine Learning** | Scikit-Learn (Random Forest Classifier, Decision Trees) |
| **Data Engineering** | Pandas, NumPy |
| **Model Persistence** | Joblib |
| **Market Data** | Requests (Binance Public REST API) |

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

```

```
