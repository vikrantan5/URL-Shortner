import numpy as np
import pickle
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .feature import FeatureExtraction

with open("detect/model.pkl", "rb") as f:
    model = pickle.load(f)

@api_view(['POST'])
def predict(request):
    url = request.data.get('url', '').strip()

    if not url:
        return Response({'error': 'URL is required'}, status=400)

    try:
        features = FeatureExtraction(url).getFeaturesList()

        x = np.array(features).reshape(1, -1)

        prediction = int(model.predict(x)[0])

        probs = model.predict_proba(x)[0]

        phish_prob = float(probs[0])
        legit_prob = float(probs[1])

# convert to percentage
        phish_percent = phish_prob * 100
        legit_percent = legit_prob * 100

# 🔥 FINAL LOGIC
        if phish_percent >= 70:
            prediction = 0  # suspicious
            final_probability = phish_percent
        else:
            prediction = 1  # legitimate
            final_probability = 100.0   # force 100%

        return Response({
            "prediction": prediction,
            "phishing_probability": float(probs[0]),
            "legitimate_probability": float(probs[1])
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)