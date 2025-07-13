# sesli-asistan-api
# 🎧 Yapay Zeka Destekli Sesli Asistan Mikroservisi

Bu proje, dış aramalarda sesli asistan görevi görecek şekilde tasarlanmış bir mikroservistir. Kullanıcıdan gelen metin (transkript), duygu analizine tabi tutulur ve tespit edilen duyguya uygun bir yanıt üretilerek ses dosyasına dönüştürülür.


## Özellikler

- REST API endpoint: `/call-hook`
- JSON formatında çağrı verisi alır (`callerId`, `transcript`)
- TextBlob kütüphanesi ile duygu analizi yapar (pozitif, negatif, nötr)
- Yanıta göre Türkçe sesli cevap üretir (gTTS ile .mp3)
- Hata ve eksik parametre kontrolleri içerir


## Kurulum ve Çalıştırma

1. Projeyi klonlayın veya dosyaları indirin
git clone https://github.com/kullaniciadi/voice-assistant-api.git
cd voice-assistant-api

2. Sanal ortam oluşturun (isteğe bağlı)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

4. Uygulamayı çalıştırın
uvicorn main:app --reload

5. Tarayıcıdan veya Postman ile test edin
POST http://localhost:8000/call-hook
Content-Type: application/json

{
  "callerId": "+902422223344",
  "transcript": "Bu hizmet hiç yardımcı olmadı!"
}

Teknoloji   Açıklama                              

FastAPI   : RESTful API geliştirme                
TextBlob  : Basit duygu analizi                   
gTTS      : Google Text-to-Speech ile ses üretimi 
Python    : Programlama dili                      
Uvicorn   : ASGI server, FastAPI ile çalıştırma   

Adayın Kendi Değerlendirmesi
AI Kullanımı: Gelen çağırının yapay zeka destekli olarak karşılanması konusunda süreci simüle eden mikro hizmet geliştirilirken destek alındı. Projenin her aşamasında az da olsa deneyimsiz olmamdan kaynaklı yapayz zekadan destek alındı. 

Yanıt Üretimi: Yanıt üretimi duygu analizi kısımları daha kolay ve yapay zeka desteği olmadan yapılabilir durumdaydı. Fakat doğruluk kontorlü açısından ve iyileştirmek için yapay zekayla kontrol sağlandı

TTS: gTTS modülü ile yanıt sesi .mp3 formatında üretildi. 

🚧 Zorlayıcı Noktalar:
Türkçe metinlerde duygu analizi her zaman doğru sonuç vermeyebiliyor. Cümleleri ingilizce kullandığımızda duygu analizi daha net yapılabiliyor.Sektörde ve alanda yeni olmamdan kaynaklı olarak biraz genel olarak biraz zorlandım fakat öğrenmeye ve gelişmeye açık biri olarak gerek yapay zeka gerek de diğer kaynaklardan yararlanarak daha emin adımlarla ilereyebildim.

gTTS ile TTS çıktısı alırken dizin oluşturulmadığında hata oluşuyordu. Bu, os.makedirs() ile çözüldü.

Her yanıtın benzersiz ses dosyasına kaydedilmesi gerektiğinden uuid ile dosya isimlendirme yapıldı.

✅ Nasıl Çözüldü?
Yapay zekalardan destek alarak yapıldı kodlar düzenlendi.

TextBlob’ın duygu değerleri incelenerek eşik değerler (polarity > 0.2 / < -0.2) belirlendi.

gTTS modülü hata vermemesi için responses/ klasörü dinamik olarak oluşturuldu.

Kod modüler hale getirilerek sentiment.py ve tts.py dosyalarıyla düzenli yapı oluşturuldu.

