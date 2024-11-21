import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
]

TELEGRAM_TOKEN = "8173488085:AAHeEmVQNc1E5fVA4fptgvtrBEMBXBVcGmY"
CHAT_ID = "7321328717"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"Gagal mengirim pesan ke Telegram. Status code: {response.status_code}, response: {response.text}")

def get_proxies():
    proxy_url = "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt"
    response = requests.get(proxy_url)
    proxies = [proxy for proxy in response.text.split("\n") if proxy]
    return proxies

def google_search_dork(query, num_pages=15):
    results = []
    proxies = get_proxies()
    for page in range(num_pages):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        proxy = {"http": random.choice(proxies)}
        start = page * 10
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

        try:
            response = requests.get(search_url, headers=headers, proxies=proxy, timeout=15)
            if response.status_code != 200:
                print(f"Failed to fetch Google results on page {page + 1}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            page_results = []
            for link in soup.select('a[href^=\"http\"]'):
                url = link.get('href')
                if 'google.com' not in url and url.startswith("http"):
                    clean_url = url.split("&")[0]
                    page_results.append(clean_url)
                    results.append(clean_url)

            if page_results:
                result_text = "\n".join(page_results)
                send_telegram_message(result_text)

            print(f"Fetched {len(page_results)} results from page {page + 1}.")
        except Exception as e:
            print(f"Error on page {page + 1}: {e}")

        # Tambahkan jeda yang lebih lama untuk menghindari deteksi bot
        time.sleep(random.uniform(15, 20))

    return results

if __name__ == "__main__":
    with open('dork.txt', 'r') as file:
        dorks = file.readlines()
    
    for dork_query in dorks:
        dork_query = dork_query.strip()
        if not dork_query:
            continue
        
        print(f"Mencari website menggunakan Google dork: {dork_query}...")
        search_results = google_search_dork(dork_query, num_pages=15)

        print(f"Total hasil yang diambil untuk dork '{dork_query}': {len(search_results)}.")

        # Jeda 3 menit sebelum melanjutkan ke dork berikutnya
        time.sleep(3 * 60)
        
