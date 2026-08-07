# Metafide-Spot-On-Bot
Real-time hybrid ML trading signal backend built with Python, FastAPI, and Scikit-Learn. Integrates live Binance market data with a Random Forest Classifier, dynamic 7-2-1 spot price spreads, an automated feedback memory loop, and Metafide API authentication.
🚀 Quick Start Guide1. PrerequisitesPython 3.9+Pip package manager2. InstallationClone the repository and install required dependencies:Bashgit clone [https://github.com/YOUR_USERNAME/smart-brain-bot.git](https://github.com/YOUR_USERNAME/smart-brain-bot.git)
cd smart-brain-bot

pip install fastapi uvicorn pandas scikit-learn joblib requests
3. Running the API ServerStart the backend server using Uvicorn:Bashpython smart_brain.py
The API will run locally at: http://localhost:8000Interactive API Documentation (Swagger UI) is available at: http://localhost:8000/docs📡 API Endpoints1. Request Signal / Predict SpotsMethod: GETEndpoint: /api/predictQuery Parameters:current_price (float, required): Spot price of the asset.up_range (float, default: 15): Upper spread range limit.down_range (float, default: 15): Lower spread range limit.gid (string, default: "0"): Round/Game ID for tracking.Example Request:HTTPGET http://localhost:8000/api/predict?current_price=95000.00&up_range=20&down_range=20&gid=ROUND_101
Example Response:JSON{
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
2. Log Feedback / Store OutcomeMethod: POSTEndpoint: /api/feedbackBody (JSON):JSON{
  "gid": "ROUND_101",
  "actual_price": 95015.50
}
Example Response:JSON{
  "status": "success"
}
🧠 Training the Machine Learning BrainTo retrain the Random Forest Classifier on newly accumulated market logs:Ensure the bot has logged at least 50 rounds into 1m_brain_memory.csv.Run the training script:Bashpython train_brain.py
The script will:Load 1m_brain_memory.csv.Compute price direction targets ($\Delta P > 0$).Train an $80/20$ split Random Forest Classifier ($100$ estimators, max depth $5$).Print classification metrics and accuracy reports.Export serialized model weights to brain_model.pkl.🛠️ Tech Stack & DependenciesLanguage: PythonFramework: FastAPI / Uvicorn (REST API & CORS middleware)Machine Learning: Scikit-Learn (Random Forest, Decision Trees)Data Processing: Pandas, NumPyModel Serialization: JoblibMarket Integration: Requests (Binance REST API)📄 LicenseDistributed under the MIT License. See LICENSE for more information.
