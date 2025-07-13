from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Global değişkenler (yeni mezun tarzı)
calls_list = []
call_counter = 1


def check_sentiment(text):
    """Basit sentiment analizi"""
    bad_words = ['kötü', 'berbat', 'hiç', 'yardımcı olmadı', 'sorun']
    good_words = ['güzel', 'harika', 'teşekkür', 'memnun']

    text = text.lower()

    bad_count = 0
    good_count = 0

    for word in bad_words:
        if word in text:
            bad_count = bad_count + 1

    for word in good_words:
        if word in text:
            good_count = good_count + 1

    if bad_count > good_count:
        return 'negative'
    elif good_count > bad_count:
        return 'positive'
    else:
        return 'neutral'


def create_response(sentiment):
    """AI yanıt oluştur"""
    if sentiment == 'negative':
        return "Üzgünüm, yaşadığınız sorun için. Size nasıl yardımcı olabilirim?"
    elif sentiment == 'positive':
        return "Teşekkürler! Memnuniyetinizi duymak güzel. Başka bir şey var mı?"
    else:
        return "Size nasıl yardımcı olabilirim?"


@app.route('/call-hook', methods=['POST'])
def call_hook():
    global call_counter

    # JSON verisini al
    request_data = request.get_json()

    # Kontrolü yap
    if not request_data:
        return jsonify({'error': 'JSON verisi gerekli'}), 400

    # Gerekli alanları kontrol et
    if 'callerId' not in request_data:
        return jsonify({'error': 'callerId gerekli'}), 400

    if 'transcript' not in request_data:
        return jsonify({'error': 'transcript gerekli'}), 400

    caller_id = request_data['callerId']
    transcript = request_data['transcript']

    # Boş mu kontrol et
    if not caller_id or not transcript:
        return jsonify({'error': 'callerId ve transcript boş olamaz'}), 400

    # Sentiment analizi yap
    sentiment = check_sentiment(transcript)

    # AI yanıt oluştur
    ai_response = create_response(sentiment)

    # Çağrı kaydını oluştur
    call_record = {
        'id': call_counter,
        'callerId': caller_id,
        'transcript': transcript,
        'sentiment': sentiment,
        'aiResponse': ai_response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Listeye ekle
    calls_list.append(call_record)
    call_counter = call_counter + 1

    # Ekrana yazdır
    print('Yeni çağrı geldi:')
    print(f'Arayan: {caller_id}')
    print(f'Mesaj: {transcript}')
    print(f'Sentiment: {sentiment}')
    print(f'Yanıt: {ai_response}')
    print('---')

    # Başarılı yanıt döndür
    return jsonify({
        'success': True,
        'callId': call_record['id'],
        'sentiment': sentiment,
        'response': ai_response,
        'timestamp': call_record['timestamp']
    })


# Diğer endpoint'ler
@app.route('/calls', methods=['GET'])
def get_all_calls():
    return jsonify({
        'success': True,
        'total': len(calls_list),
        'calls': calls_list
    })


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'working',
        'message': 'API çalışıyor',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Sesli Asistan API v1.0',
        'usage': 'POST /call-hook ile çağrı gönder'
    })


if __name__ == '__main__':
    print('Sesli Asistan API başlatılıyor...')
    print('Port: 5000')
    print('Debug modu: Açık')
    app.run(debug=True, port=5000)

# Test komutları:
"""
# Negatif test
curl -X POST http://localhost:5000/call-hook \
  -H "Content-Type: application/json" \
  -d '{"callerId": "+902422223344", "transcript": "Bu hizmet hiç yardımcı olmadı!"}'

# Pozitif test  
curl -X POST http://localhost:5000/call-hook \
  -H "Content-Type: application/json" \
  -d '{"callerId": "+905551234567", "transcript": "Hizmetiniz gerçekten harika, teşekkürler!"}'

# Tüm çağrıları göster
curl http://localhost:5000/calls

# Health check
curl http://localhost:5000/health
"""