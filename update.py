import requests
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROVIDER_DIR = os.path.join(BASE_DIR, 'Providers')
URL_FILE = os.path.join(BASE_DIR, 'urls.txt')

def ensure_provider_dir():
    """确保 Providers 目录存在"""
    if not os.path.exists(PROVIDER_DIR):
        os.makedirs(PROVIDER_DIR)

def read_urls_from_file(filepath):
    """从文本文件读取 URL 列表"""
    if not os.path.isfile(filepath):
        print(f"URL file not found: {filepath}")
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def download_file(url):
    """下载文件并保存到 Providers 目录"""
    try:
        res = requests.get(url)
        res.raise_for_status()
        filename = os.path.basename(url).replace('%20', '-')
        file_path = os.path.join(PROVIDER_DIR, filename)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(res.text)
        
        print(f"Downloaded: {filename}")
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")

def purge_jsdelivr_cache(filename):
    """调用 jsDelivr 清缓存"""
    purge_url = f'https://purge.jsdelivr.net/gh/fallssyj/Clash/Providers/{filename}'
    try:
        res = requests.get(purge_url)
        if res.status_code == 200:
            print(f"Purged cache for: {filename}")
        else:
            print(f"Failed to purge cache for {filename}: {res.status_code}")
    except requests.RequestException as e:
        print(f"Error purging cache: {e}")

def main():
    ensure_provider_dir()
    urls = read_urls_from_file(URL_FILE)

    if not urls:
        print("No URLs to process.")
        return

    for url in urls:
        download_file(url)

    yaml_files = [f for f in os.listdir(PROVIDER_DIR) if f.endswith('.yaml')]
    for yaml_file in yaml_files:
        purge_jsdelivr_cache(yaml_file)

if __name__ == '__main__':
    main()
