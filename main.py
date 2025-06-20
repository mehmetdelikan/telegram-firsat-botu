import os
import asyncio
import requests
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Hataların anında loglarda görünmesi için
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("Program başlatılıyor...")

try:
    # Değişkenleri oku
    API_ID = int(os.environ.get('API_ID'))
    API_HASH = os.environ.get('API_HASH')
    SESSION_STRING = os.environ.get('SESSION_STRING')
    NTFY_TOPIC = os.environ.get('NTFY_TOPIC')

    # Değişkenlerin varlığını kontrol et
    if not all([API_ID, API_HASH, SESSION_STRING, NTFY_TOPIC]):
        print("HATA: Ortam değişkenlerinden biri veya birkaçı eksik!", file=sys.stderr)
        sys.exit(1)

    print("Değişkenler okundu. Client oluşturuluyor...")
    
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    TARGET_CHANNEL = 'onual_firsat'
    KEYWORDS = [
        "son 6 ayın en düşük fiyatı",
        "son 1 yılın en düşük fiyatı"
    ]

    def send_notification(message):
    """ntfy.sh servisine bildirim gönderir."""
    try:
        # Mesaj linkini oluştur
        message_link = f"https://t.me/{TARGET_CHANNEL}/{message.id}"
        
        # Telegram mesajında metin olup olmadığını kontrol et
        text_content = message.text if message.text else "İçerik bulunamadı, linke tıklayın."
        
        # Bildirim içeriğini oluştur: Mesaj metni + görünür link
        content = f"{text_content}\n\nLink: {message_link}"
        
        # --- BU BÖLÜM DEĞİŞTİRİLDİ ---
        # Türkçe karakter hatasını kesin olarak çözmek için başlığı değiştirdik.
        headers = {
            "Title": "Yeni Firsat Yakalandi!", # 'ı' harfleri 'i' ile değiştirildi
            "Tags": "tada",
            "Click": message_link, 
            "Priority": "high"
        }
        # ntfy'ye gönder
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=content.encode('utf-8'), headers=headers)
        # Başarılı olursa loglara not düş
        print(f"Bildirim başarıyla gönderildi.")

    except Exception as e:
        print(f"Bildirim gönderilirken hata oluştu: {e}", file=sys.stderr)

    @client.on(events.NewMessage(chats=TARGET_CHANNEL))
    async def handler(event):
        """Kanala gelen her yeni mesajı kontrol eder."""
        # Mesajda metin olmasa bile (sadece resim gibi) anahtar kelimeyi yakalamak için
        # event.raw_text kullanılır. Bu daha güvenilirdir.
        message_text_lower = event.raw_text.lower()
        if any(keyword in message_text_lower for keyword in KEYWORDS):
            print(f"Eşleşen mesaj bulundu: {event.raw_text}")
            send_notification(event.message)

    async def main():
        print("Bağlantı başarılı. Kanal dinleniyor...")
        await client.run_until_disconnected()

    # Programı çalıştır
    with client:
        client.loop.run_until_complete(main())

except Exception as e:
    # Genel bir hata olursa yakala ve logla
    import traceback
    print(f"KRİTİK HATA: Program başlatılamadı.", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
