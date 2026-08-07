# Metafide-Spot-On-Bot
Real-time hybrid ML trading signal backend built with Python, FastAPI, and Scikit-Learn. Integrates live Binance market data with a Random Forest Classifier, dynamic 7-2-1 spot price spreads, an automated feedback memory loop, and Metafide API authentication.
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
