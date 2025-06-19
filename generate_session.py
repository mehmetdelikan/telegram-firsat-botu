from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("Bu script, Railway'de kullanmak üzere bir Telethon Session String üretecektir.")
API_ID = input("Lütfen API ID'nizi girin: ")
API_HASH = input("Lütfen API Hash'inizi girin: ")

# StringSession kullanarak istemciyi başlatıyoruz
with TelegramClient(StringSession(), int(API_ID), API_HASH) as client:
    # Giriş yapıldıktan sonra session string'i alıyoruz
    session_string = client.session.save()
    
    print("\nOturum anahtarınız (Session String) aşağıdadır. Kopyalayıp güvenli bir yere kaydedin:")
    print("-----------------------------------------------------------------")
    print(session_string)
    print("-----------------------------------------------------------------")
    print("\nBu anahtarı Railway'de SESSION_STRING değişkenine yapıştıracaksınız.")