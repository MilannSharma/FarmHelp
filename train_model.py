import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np
import requests
from datetime import datetime
import time

def generate_synthetic_data(n_samples=100):
    """Generate synthetic agricultural data for training"""
    print(f"🌱 Generating {n_samples} synthetic data samples...")

    # Define crop types and their typical conditions
    crop_conditions = {
        'Rice': {'temp': (20, 35), 'humidity': (70, 90), 'ph': (5.5, 7.0), 'rainfall': (100, 200)},
        'Wheat': {'temp': (15, 25), 'humidity': (40, 70), 'ph': (6.0, 7.5), 'rainfall': (50, 100)},
        'Maize': {'temp': (20, 35), 'humidity': (50, 80), 'ph': (5.8, 7.0), 'rainfall': (60, 120)},
        'Sugarcane': {'temp': (20, 35), 'humidity': (60, 85), 'ph': (6.0, 7.5), 'rainfall': (100, 200)},
        'Cotton': {'temp': (20, 35), 'humidity': (50, 75), 'ph': (6.0, 8.0), 'rainfall': (50, 100)},
        'Soybean': {'temp': (20, 30), 'humidity': (50, 80), 'ph': (6.0, 7.0), 'rainfall': (60, 120)}
    }

    synthetic_data = []

    for _ in range(n_samples):
        crop = np.random.choice(list(crop_conditions.keys()))
        conditions = crop_conditions[crop]

        sample = {
            'temperature': np.random.uniform(conditions['temp'][0], conditions['temp'][1]),
            'humidity': np.random.uniform(conditions['humidity'][0], conditions['humidity'][1]),
            'ph': np.random.uniform(conditions['ph'][0], conditions['ph'][1]),
            'rainfall': np.random.uniform(conditions['rainfall'][0], conditions['rainfall'][1]),
            'label': crop
        }
        synthetic_data.append(sample)

    return pd.DataFrame(synthetic_data)

def load_and_combine_data():
    """Load existing data and combine with synthetic data"""
    print("📊 Loading and combining datasets...")

    # Load existing datasets
    data_frames = []

    try:
        farmer_data = pd.read_csv("farmer_data.csv")
        data_frames.append(farmer_data)
        print(f"✅ Loaded farmer_data.csv with {len(farmer_data)} samples")
    except FileNotFoundError:
        print("⚠️  farmer_data.csv not found")

    try:
        crops_data = pd.read_csv("crops_dataset.csv")
        data_frames.append(crops_data)
        print(f"✅ Loaded crops_dataset.csv with {len(crops_data)} samples")
    except FileNotFoundError:
        print("⚠️  crops_dataset.csv not found")

    # Combine existing data
    if data_frames:
        combined_data = pd.concat(data_frames, ignore_index=True)
        print(f"📊 Combined existing data: {len(combined_data)} samples")
    else:
        combined_data = pd.DataFrame()
        print("⚠️  No existing data found")

    # Generate synthetic data
    synthetic_data = generate_synthetic_data(n_samples=500)

    # Combine with synthetic data
    if not combined_data.empty:
        final_data = pd.concat([combined_data, synthetic_data], ignore_index=True)
    else:
        final_data = synthetic_data

    print(f"🎯 Final dataset: {len(final_data)} samples")
    return final_data

def train_enhanced_model():
    """Train the enhanced crop prediction model"""
    print("🚀 Starting Enhanced Crop Prediction Model Training")
    print("=" * 60)

    # Load and combine data
    data = load_and_combine_data()

    if data.empty:
        print("❌ No data available for training")
        return False

    # Clean target labels: remove NaN and convert all to string lowercase
    data = data.dropna(subset=['label'])
    data['label'] = data['label'].astype(str).str.lower()

    # Prepare features and target
    X = data[['temperature', 'humidity', 'ph', 'rainfall']]
    y = data['label']

    print(f"📈 Training with {len(X)} samples")
    print(f"🌾 Target crops: {y.unique()}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Try multiple models for best accuracy
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.model_selection import cross_val_score

    models = {
        'DecisionTree': DecisionTreeClassifier(random_state=42),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'SVM': SVC(kernel='rbf', random_state=42)
    }

    best_model = None
    best_accuracy = 0
    best_name = ""

    print("🔍 Evaluating multiple models for best accuracy...")
    print("=" * 60)

    for name, model in models.items():
        # Cross-validation for better evaluation
        cv_scores = cross_val_score(model, X, y, cv=5)
        mean_cv_accuracy = cv_scores.mean()

        # Train and test
        model.fit(X_train, y_train)
        test_accuracy = model.score(X_test, y_test)

        print(f"{name}:")
        print(f"   Cross-Val Accuracy: {mean_cv_accuracy:.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"   Test Accuracy: {test_accuracy:.4f}")

        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            best_model = model
            best_name = name

    print("=" * 60)
    print(f"🏆 Best Model: {best_name} with Test Accuracy: {best_accuracy:.4f}")
    print("=" * 60)

    # Use the best model
    model = best_model

    # Save model
    joblib.dump(model, "model.pkl")
    print("💾 Model saved as model.pkl")

    # Save enhanced dataset for future use
    data.to_csv("enhanced_farmer_data.csv", index=False)
    print("💾 Enhanced dataset saved as enhanced_farmer_data.csv")

    print("✅ Enhanced model training completed!")
    return True

if __name__ == "__main__":
    success = train_enhanced_model()
    if success:
        print("\n🎉 Model enhancement successful! Ready for improved predictions.")
    else:
        print("\n❌ Model training failed.")
