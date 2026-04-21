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

        # Raw probabilities from the model (index 0 -> phishing, index 1 -> legitimate)
        probs = model.predict_proba(x)[0]
        phish_prob = float(probs[0])
        legit_prob = float(probs[1])

        # Convert to percentage for business rule
        phish_percent = phish_prob * 100

        # Business rule: treat URL as suspicious only when phishing probability >= 70%
        if phish_percent >= 70:
            prediction = 0  # suspicious
            confidence = phish_prob
        else:
            prediction = 1  # legitimate
            confidence = legit_prob

        return Response({
            "prediction": prediction,
            # Confidence for the final verdict (0-1). Frontend multiplies by 100.
            "probability": round(confidence, 4),
            # Keep raw probabilities available too
            "probability_phishing": round(phish_prob, 4),
            "probability_legitimate": round(legit_prob, 4),
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
