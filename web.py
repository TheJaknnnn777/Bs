import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

# Daftar User-Agent untuk menghindari deteksi bot
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
]

# Token dan Chat ID bot Telegram
TELEGRAM_TOKEN = "7335390954:AAEdshNZLWcSmzzsgVUO13wtDo9ZbEmIwio"
CHAT_ID = "6070764928"

# Fungsi untuk mengirim pesan ke bot Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"Gagal mengirim pesan ke Telegram. Status code: {response.status_code}, response: {response.text}")

# Fungsi pencarian Google tanpa proxy
def google_search_dork(query, num_pages=5):
    results = []
    for page in range(num_pages):
        # Pilih User-Agent secara acak
        headers = {"User-Agent": random.choice(USER_AGENTS)}

        # URL pencarian Google
        start = page * 10
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch Google results on page {page + 1}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.select('a[href^=\"http\"]'):
                url = link.get('href')
                if 'google.com' not in url and url.startswith("http"):
                    clean_url = url.split("&")[0]
                    results.append(clean_url)

            print(f"Fetched {len(results)} results from page {page + 1}.")
        except Exception as e:
            print(f"Error on page {page + 1}: {e}")
        
        # Jeda untuk menghindari deteksi bot
        time.sleep(random.uniform(1, 3))

    return results

if __name__ == "__main__":
    # Input dork dan jumlah halaman
    dork_query = input("Masukkan dork query yang ingin dicari: ")
    num_pages = int(input("Berapa banyak halaman yang ingin diambil (1 halaman = 10 website)? "))

    print("Mencari website menggunakan Google dork...")
    search_results = google_search_dork(dork_query, num_pages=num_pages)

    print(f"Total hasil yang diambil: {len(search_results)}.")
    if search_results:
        # Gabungkan hasil menjadi satu string
        result_text = "\n".join(search_results)
        # Kirim hasil ke bot Telegram
        # Bagi pesan jika lebih dari 4096 karakter
        max_length = 4096
        for i in range(0, len(result_text), max_length):
            send_telegram_message(result_text[i:i + max_length])
