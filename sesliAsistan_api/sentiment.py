from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.2:
        return "pozitif"
    elif polarity < -0.2:
        return "negatif"
    else:
        return "nötr"
