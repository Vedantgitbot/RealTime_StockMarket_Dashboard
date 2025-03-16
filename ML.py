import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def train_random_forest_model(data):
    if len(data) < 60:
        raise ValueError("Not enough data to train the model")


    data['5-day MA'] = data['Close'].rolling(window=5).mean()
    data['20-day MA'] = data['Close'].rolling(window=20).mean()
    data['Price Change'] = data['Close'].pct_change()
    data['RSI'] = 100 - (100 / (1 + data['Price Change'].rolling(window=14).mean()))

    data = data.dropna()

    features = ['Close', '5-day MA', '20-day MA', 'Price Change', 'RSI']
    data['Target'] = data['Price Change'].shift(-1)
    data['Target'] = data['Target'].apply(lambda x: 2 if x < 0 else (1 if x > 0 else 0))

    X = data[features]
    y = data['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

   
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)


    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, scaler

def predict_buy_sell_random_forest(data, model, scaler):
    if len(data) < 60:
        return "Not enough data for prediction"

    data['5-day MA'] = data['Close'].rolling(window=5).mean()
    data['20-day MA'] = data['Close'].rolling(window=20).mean()
    data['Price Change'] = data['Close'].pct_change()
    data['RSI'] = 100 - (100 / (1 + data['Price Change'].rolling(window=14).mean()))

    data = data.dropna()
    features = ['Close', '5-day MA', '20-day MA', 'Price Change', 'RSI']
    
    last_data = data[features].iloc[-1]
    last_data = scaler.transform([last_data])

    prediction = model.predict(last_data)

    if prediction == 1:
        return "Buy"
    elif prediction == 2:
        return "Sell"
    else:
        return "Hold"
