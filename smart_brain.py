import os
import csv
import random
import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "1m_brain_memory.csv"
MODEL_FILE = "brain_model.pkl"

# ─── 1. SETUP SMART MEMORY ──────────────────────────────────────────────────
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["gid", "actual_price", "rsi", "ma25_distance", "predicted_action"])

round_memory = {}

# ─── 2. LOAD THE TRAINED MACHINE LEARNING MODEL ─────────────────────────────
ai_model = None
if os.path.exists(MODEL_FILE):
    try:
        ai_model = joblib.load(MODEL_FILE)
        print(f"🧠 [SUCCESS] Loaded Trained Neural Network: {MODEL_FILE}")
    except Exception as e:
        print(f"⚠️ [ERROR] Could not load model: {e}")
else:
    print("⚙️ [NOTICE] No trained model found. Running on Hardcoded TA Rules. Run train_brain.py later!")

# ─── 3. MARKET CONTEXT (BINANCE 1M KLINES) ────────────────────────────────
def get_1m_market_context(asset="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={asset}&interval=1m&limit=100"
        res = requests.get(url, timeout=3)
        data = res.json()
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])
        df['close'] = df['close'].astype(float)
        
        df['MA25'] = df['close'].rolling(window=25).mean()
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        return df.iloc[-1]
    except Exception as e:
        return None

# ─── 4. TACTICAL 7-2-1 SPREAD WITH JITTER ─────────────────────────────────
def generate_721_spread(price, action, up_range, down_range):
    spots = [round(price, 2)]
    step_up = up_range / 7
    step_down = down_range / 7

    if action == "BULLISH_DRIFT":
        for i in range(1, 8): spots.append(round(price + (i * step_up) + random.uniform(0.1, 0.9), 2))
        for i in range(1, 3): spots.append(round(price - (i * (down_range/2)) - random.uniform(0.1, 0.9), 2))
    elif action == "BEARISH_DRIFT":
        for i in range(1, 8): spots.append(round(price - (i * step_down) - random.uniform(0.1, 0.9), 2))
        for i in range(1, 3): spots.append(round(price + (i * (up_range/2)) + random.uniform(0.1, 0.9), 2))
    else:
        for i in range(1, 6): spots.append(round(price + (i * (up_range/5)) + random.uniform(0.1, 0.9), 2))
        for i in range(1, 5): spots.append(round(price - (i * (down_range/4)) - random.uniform(0.1, 0.9), 2))

    return sorted(list(set(spots)))[:10]

# ─── 5. API ENDPOINTS ───────────────────────────────────────────────────────
@app.get("/api/predict")
def predict_spots(current_price: float, up_range: float = 15, down_range: float = 15, gid: str = "0"):
    context = get_1m_market_context()
    
    action = "NEUTRAL_SPREAD"
    confidence = 50
    rsi = 50
    ma_distance = 0

    if context is not None:
        rsi = context['RSI']
        ma25 = context['MA25']
        ma_distance = current_price - ma25

        # 🧠 PHASE 2: USE THE MACHINE LEARNING MODEL
        if ai_model is not None:
            features = pd.DataFrame([[rsi, ma_distance]], columns=['rsi', 'ma25_distance'])
            prediction = ai_model.predict(features)[0]
            
            if prediction == 1:
                action = "BULLISH_DRIFT"
                confidence = 85
            else:
                action = "BEARISH_DRIFT"
                confidence = 85
                
        # ⚙️ PHASE 1: FALLBACK TO HARDCODED LOGIC (Data Collection Phase)
        else:
            if rsi < 35:
                action = "BULLISH_DRIFT"
                confidence = 80
            elif rsi > 65:
                action = "BEARISH_DRIFT"
                confidence = 80
            elif ma_distance > 0:
                action = "BULLISH_DRIFT"
                confidence = 60
            else:
                action = "BEARISH_DRIFT"
                confidence = 60

    spots = generate_721_spread(current_price, action, up_range, down_range)
    
    if gid != "0" and gid != "preview":
        round_memory[gid] = {
            "rsi": round(rsi, 2),
            "ma_distance": round(ma_distance, 2),
            "action": action
        }
    
    mode_str = "🧠 [ML MODEL]" if ai_model else "⚙️ [HARDCODED]"
    print(f"[{gid}] {mode_str} -> Action: {action} | RSI: {round(rsi, 1)} | MA Dist: {round(ma_distance, 1)}")

    return {
        "action": action,
        "confidence": confidence,
        "spots": spots
    }

@app.post("/api/feedback")
def log_feedback(data: dict):
    gid = data.get("gid", "unknown")
    actual_price = data.get("actual_price", 0)
    
    memory = round_memory.get(gid, {"rsi": 0, "ma_distance": 0, "action": "UNKNOWN"})
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([gid, actual_price, memory['rsi'], memory['ma_distance'], memory['action']])
        
    print(f"💾 Logged -> GID: {gid} | Price: {actual_price} | RSI was: {memory['rsi']}")
    
    if gid in round_memory:
        del round_memory[gid]
        
    return {"status": "success"}

if __name__ == "__main__":
    # 🔥 FIX: This must match the filename exactly!
    uvicorn.run("smart_brain:app", host="0.0.0.0", port=8000, log_level="warning")