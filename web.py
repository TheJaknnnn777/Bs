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

# Fungsi untuk mengambil daftar proxy dari file lokal
def fetch_proxies():
    proxy_file = "proxy.txt"
    try:
        with open(proxy_file, 'r') as file:
            raw_proxies = file.read().splitlines()
            print(f"Total proxies fetched: {len(raw_proxies)}")
            return raw_proxies
    except Exception as e:
        print(f"Error reading proxy file: {e}")
    return []

# Fungsi pencarian Google dengan proxy
def google_search_dork(query, proxies, num_pages=5):
    results = []
    for page in range(num_pages):
        # Pilih User-Agent dan Proxy secara acak
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        proxy = random.choice(proxies)
        proxy_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}

        # URL pencarian Google
        start = page * 10
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&start={start}"

        try:
            response = requests.get(search_url, headers=headers, proxies=proxy_dict, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch Google results on page {page + 1}. Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.select('a[href^="http"]'):
                url = link.get('href')
                if 'google.com' not in url and url.startswith("http"):
                    clean_url = url.split("&")[0]
                    results.append(clean_url)

            print(f"Fetched {len(results)} results from page {page + 1} using proxy {proxy}.")
        except Exception as e:
            print(f"Error on page {page + 1} with proxy {proxy}: {e}")
        
        # Jeda untuk menghindari deteksi bot
        time.sleep(random.uniform(1, 3))

    return results

# Fungsi untuk menyimpan hasil pencarian
def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for line in data:
            file.write(line + '\n')
    print(f"Hasil pencarian disimpan ke {file_name}")

if __name__ == "__main__":
    # Ambil daftar proxy
    print("Mengambil daftar proxy...")
    proxies = fetch_proxies()
    if not proxies:
        print("Tidak ada proxy yang tersedia. Coba lagi nanti.")
        exit(1)

    # Input dork dan jumlah halaman
    dork_query = input("Masukkan dork query yang ingin dicari: ")
    num_pages = int(input("Berapa banyak halaman yang ingin diambil (1 halaman = 10 website)? "))

    print("Mencari website menggunakan Google dork dengan proxy...")
    search_results = google_search_dork(dork_query, proxies, num_pages=num_pages)

    print(f"Total hasil yang diambil: {len(search_results)}.")
    if search_results:
        # Input nama file
        file_name = input("Masukkan nama file untuk menyimpan hasil (contoh: hasil.txt): ")
        save_to_file(file_name, search_results)
