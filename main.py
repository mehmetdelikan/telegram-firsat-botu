import os
import asyncio
import requests
import sys
from telethon import TelegramClient, events
from telethon.sessions import StringSession # Bu satır eklendi

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
    
    # --- BURASI DÜZELTİLDİ ---
    # Client'ı doğrudan Session String ile başlatıyoruz
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    
    TARGET_CHANNEL = 'onual_firsat'
    KEYWORDS = [
        "son 6 ayın en düşük fiyatı",
        "son 1 yılın en düşük fiyatı"
    ]

    def send_notification(message):
        """ntfy.sh servisine bildirim gönderir."""
        try:
            content = (message.text[:200] + '..') if len(message.text) > 200 else message.text
            message_link = f"https://t.me/{TARGET_CHANNEL}/{message.id}"
            headers = { "Title": "Yeni Fırsat Yakalandı!", "Tags": "tada", "Click": message_link, "Priority": "high" }
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=content.encode('utf-8'), headers=headers)
            print(f"Bildirim gönderildi: {content}")
        except Exception as e:
            print(f"Bildirim gönderilirken hata oluştu: {e}", file=sys.stderr)

    @client.on(events.NewMessage(chats=TARGET_CHANNEL))
    async def handler(event):
        """Kanala gelen her yeni mesajı kontrol eder."""
        message_text_lower = event.message.text.lower()
        if any(keyword in message_text_lower for keyword in KEYWORDS):
            print(f"Eşleşen mesaj bulundu: {event.message.text}")
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
