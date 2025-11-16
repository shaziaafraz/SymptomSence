"""
Flask Backend API for Disease Prediction Chatbot
"""

import json
import pickle
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        # Fallback: use ASCII-safe characters
        pass

# ASCII-safe symbols for Windows compatibility
CHECK = "[OK]"
CROSS = "[X]"
WARN = "[!]"

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variables to store loaded models and data
model = None
tfidf = None
mapping = None
label_encoder = None

def load_resources():
    """Load model.pkl, tfidf.pkl, and mapping.json files"""
    global model, tfidf, mapping, label_encoder
    
    try:
        # Check if files exist
        if not os.path.exists('model.pkl'):
            raise FileNotFoundError("model.pkl not found in current directory")
        if not os.path.exists('tfidf.pkl'):
            raise FileNotFoundError("tfidf.pkl not found in current directory")
        
        # Load the trained ML model with proper error handling
        print("Loading model.pkl...")
        try:
            # Try joblib first (more reliable for sklearn models)
            try:
                from joblib import load as joblib_load
                file_size = os.path.getsize('model.pkl')
                if file_size == 0:
                    raise ValueError("model.pkl is empty")
                model = joblib_load('model.pkl')
                print(f"{CHECK} Model loaded successfully with joblib (size: {file_size} bytes)")
            except ImportError:
                # Fallback to pickle if joblib not available
                with open('model.pkl', 'rb') as f:
                    file_size = os.path.getsize('model.pkl')
                    if file_size == 0:
                        raise ValueError("model.pkl is empty")
                    model = pickle.load(f)
                    print(f"{CHECK} Model loaded successfully with pickle (size: {file_size} bytes)")
        except Exception as e:
            print(f"{CROSS} Error loading model.pkl: {e}")
            print("  Tip: Try regenerating pickle files from your training script")
            raise
        
        # Load the TF-IDF vectorizer with proper error handling
        print("Loading tfidf.pkl...")
        try:
            # Try joblib first (more reliable for sklearn models)
            try:
                from joblib import load as joblib_load
                file_size = os.path.getsize('tfidf.pkl')
                if file_size == 0:
                    raise ValueError("tfidf.pkl is empty")
                tfidf = joblib_load('tfidf.pkl')
                print(f"{CHECK} TF-IDF vectorizer loaded successfully with joblib (size: {file_size} bytes)")
            except ImportError:
                # Fallback to pickle if joblib not available
                with open('tfidf.pkl', 'rb') as f:
                    file_size = os.path.getsize('tfidf.pkl')
                    if file_size == 0:
                        raise ValueError("tfidf.pkl is empty")
                    tfidf = pickle.load(f)
                    print(f"{CHECK} TF-IDF vectorizer loaded successfully with pickle (size: {file_size} bytes)")
        except Exception as e:
            print(f"{CROSS} Error loading tfidf.pkl: {e}")
            print("  Tip: Try regenerating pickle files from your training script")
            raise
        
        # Load label encoder if it exists (optional)
        if os.path.exists('label_encoder.pkl'):
            print("Loading label_encoder.pkl...")
            try:
                # Try joblib first
                try:
                    from joblib import load as joblib_load
                    label_encoder = joblib_load('label_encoder.pkl')
                    print(f"{CHECK} Label encoder loaded successfully with joblib")
                except ImportError:
                    # Fallback to pickle
                    with open('label_encoder.pkl', 'rb') as f:
                        label_encoder = pickle.load(f)
                    print(f"{CHECK} Label encoder loaded successfully with pickle")
            except Exception as e:
                print(f"{WARN} Warning: Could not load label_encoder.pkl: {e}")
                print("  Label encoder is optional, continuing without it...")
        
        # Load mapping.json (fallback to disease_info.json if mapping.json doesn't exist)
        if os.path.exists('mapping.json'):
            with open('mapping.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            print(f"{CHECK} mapping.json loaded successfully")
        elif os.path.exists('disease_info.json'):
            with open('disease_info.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            print(f"{CHECK} disease_info.json loaded successfully (fallback)")
        else:
            raise FileNotFoundError("Neither mapping.json nor disease_info.json found")
            
        # Verify model has classes_ attribute
        if not hasattr(model, 'classes_'):
            print(f"{WARN} Warning: Model does not have 'classes_' attribute")
        else:
            print(f"{CHECK} Model has {len(model.classes_)} disease classes")
            
    except FileNotFoundError as e:
        print(f"{CROSS} Error loading files: {e}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        raise
    except Exception as e:
        print(f"{CROSS} Error loading resources: {e}")
        print(f"Error type: {type(e).__name__}")
        raise

@app.route('/predict', methods=['POST'])
def predict():
    """
    POST endpoint to predict diseases from symptoms
    
    Expected JSON input:
    {
        "symptoms": "text",
        "age": 22,
        "gender": "female"
    }
    
    Returns top 3 probable diseases with medication, recommendation, and description
    """
    try:
        # Validate that models are loaded
        if model is None or tfidf is None or mapping is None:
            return jsonify({
                "error": "Models not loaded. Please ensure all required files are present."
            }), 500
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract input parameters
        symptoms = data.get('symptoms', '')
        age = data.get('age', None)
        gender = data.get('gender', None)
        
        # Validate symptoms input
        if not symptoms or not isinstance(symptoms, str):
            return jsonify({"error": "Symptoms text is required"}), 400
        
        if not symptoms.strip():
            return jsonify({"error": "Symptoms text cannot be empty"}), 400
        
        # Transform symptoms using TF-IDF vectorizer
        symptoms_vectorized = tfidf.transform([symptoms])
        
        # Get probability predictions for all diseases
        probabilities = model.predict_proba(symptoms_vectorized)[0]
        
        # Get all possible class labels (disease names)
        disease_classes = model.classes_
        
        # Create list of (disease, probability) pairs
        disease_probs = list(zip(disease_classes, probabilities))
        
        # Sort by probability (descending) and get top 3
        disease_probs_sorted = sorted(disease_probs, key=lambda x: x[1], reverse=True)
        top_3 = disease_probs_sorted[:3]
        
        # Build results list
        results = []
        for disease_label, probability in top_3:
            # Convert disease label to string (handles numpy int64, int, string, etc.)
            # If label_encoder exists, use it to decode numeric labels to disease names
            if label_encoder is not None:
                try:
                    # If disease_label is numeric, use inverse_transform
                    if isinstance(disease_label, (int, np.integer)):
                        disease = label_encoder.inverse_transform([disease_label])[0]
                    else:
                        # Already a string, use as is
                        disease = str(disease_label)
                except:
                    # Fallback to string conversion
                    disease = str(disease_label)
            else:
                # No label encoder, convert to string
                disease = str(disease_label)
            
            # Ensure disease is a string for mapping lookup and other operations
            disease = str(disease)
            
            # Get disease information from mapping (try both string and original format)
            disease_info = mapping.get(disease, {})
            if not disease_info:
                # Try with original label if disease is different
                disease_info = mapping.get(disease_label, {})
            
            # Extract information with defaults if not found
            severity = disease_info.get('severity', 'Low')
            medication = disease_info.get('medication', 'Consult a doctor for proper medication')
            recommendation = disease_info.get('recommendation', 'Consult a healthcare professional')
            
            # Safe description generation (convert disease to string for .lower())
            disease_str = str(disease).lower() if disease else "unknown condition"
            description = disease_info.get('description', f'Condition related to {disease_str}')
            
            results.append({
                "disease": disease,  # Return as string
                "probability": round(float(probability), 2),  # Round to 2 decimal places
                "severity": severity,
                "medication": medication,
                "recommendation": recommendation,
                "description": description
            })
        
        # Build and return response
        response = {
            "results": results,
            "tele_consult_link": "https://appointment.com"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        # Error handling
        error_message = str(e)
        print(f"{CROSS} Error in /predict endpoint: {error_message}")
        return jsonify({
            "error": "An error occurred while processing your request",
            "details": error_message
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    status = {
        "status": "healthy",
        "model_loaded": model is not None,
        "tfidf_loaded": tfidf is not None,
        "mapping_loaded": mapping is not None
    }
    return jsonify(status), 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Disease Prediction API",
        "version": "1.0",
        "endpoints": {
            "POST /predict": "Predict diseases from symptoms",
            "GET /health": "Health check endpoint"
        }
    }), 200

if __name__ == '__main__':
    print("=" * 50)
    print("Disease Prediction API - Starting Server")
    print("=" * 50)
    
    # Load all resources before starting the server
    try:
        load_resources()
        print("\n" + "=" * 50)
        print("Server starting on http://127.0.0.1:5000")
        print("=" * 50 + "\n")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"\n{CROSS} Failed to start server: {e}")
        print("Please ensure all required files (model.pkl, tfidf.pkl, mapping.json) are present.")
