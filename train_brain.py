import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

CSV_FILE = "1m_brain_memory.csv"
MODEL_FILE = "brain_model.pkl"

def train_brain():
    print("🧠 Initializing Neural Training Sequence...")

    # 1. Load the Memory
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found. Let the bot run for a few hours to gather data first.")
        return

    df = pd.read_csv(CSV_FILE)
    
    # We need at least a few dozen rounds to train anything meaningful
    if len(df) < 50:
        print(f"⚠️ Not enough data! Only {len(df)} rounds logged. Let the bot run longer.")
        return

    print(f"📊 Loaded {len(df)} rounds of 1-minute market history.")

    # 2. Clean and Prepare the Data
    # Drop any rows where the API failed to fetch price
    df = df.dropna(subset=['actual_price', 'rsi', 'ma25_distance'])
    
    # 3. Figure out the "True" Direction of the Market
    # By comparing the end price of round N to round N-1, we know if the 1m candle was green or red
    df['price_change'] = df['actual_price'].diff()
    
    # Drop the first row since it has no previous row to compare against
    df = df.dropna(subset=['price_change'])

    # Label the true outcome: 1 for Bullish (Price went up), 0 for Bearish (Price went down)
    df['target_action'] = df['price_change'].apply(lambda x: 1 if x > 0 else 0)

    # 4. Define our Features (What the AI looks at) and Target (What the AI predicts)
    X = df[['rsi', 'ma25_distance']]
    y = df['target_action']

    # Split the data to test how smart the AI actually got (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("⚙️ Training Random Forest Classifier on RSI and MA Support/Resistance...")
    
    # 5. Build and Train the Model
    # n_estimators=100 means we are building 100 different decision trees to vote on the outcome
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # 6. Grade the AI's Homework
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print("\n========================================")
    print(f"🏆 AI Training Complete!")
    print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")
    print("========================================\n")
    
    # Print a detailed report of how well it predicts Bullish vs Bearish
    target_names = ['Bearish (Down)', 'Bullish (Up)']
    print(classification_report(y_test, predictions, target_names=target_names))

    # 7. Save the Brain to Disk
    joblib.dump(model, MODEL_FILE)
    print(f"💾 Trained Brain saved to {MODEL_FILE}. Your smart_brain.py can now use this.")

if __name__ == "__main__":
    train_brain()