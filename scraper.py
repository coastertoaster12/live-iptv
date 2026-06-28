import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

print("Scraping index and running loose pattern matching layout...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = re.search(r'watch\.php\?id=(\d+)', href)
        if match:
            channel_id = match.group(1)
            raw_channel_name = a_tag.get_text(strip=True)
            name_lower = raw_channel_name.lower()

            # Filter international and non-US feeds
            if any(block in name_lower for block in strict_blocks):
                continue
            if "espn" in name_lower and any(intl in name_lower for intl in espn_intl_blocks):
                continue

            # Strip out trailing garbage annotations to clean up display text
            display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
            display_name = display_name.rstrip('- ').rstrip('|').strip()

            # LOOSE LOGO MATCHING REGEX ENGINE:
            # 1. Strip everything after common quality tags or regional marks
            clean_token = re.split(r'\s+(fhd|hd|sd|720p|1080p|us|usa|ca|uk)\b', name_lower)[0]
            # 2. Convert standard spaces and alternate symbol separators to uniform hyphens
            clean_token = re.sub(r'[\s\._|/&]+', '-', clean_token)
            # 3. Strip any weird remaining non-alphanumeric characters except basic hyphens
            clean_token = re.sub(r'[^a-z0-9\-]', '', clean_token)
            # 4. Strip extra hanging trailing dashes
            name_clean = clean_token.strip('-')

            # Special common edge cases to make matching flawless across the repository syntax
            if name_clean == "cartoon-network":
                name_clean = "cartoon"
            elif name_clean == "disney":
                name_clean = "disney-channel"
            elif name_clean == "discovery":
                name_clean = "discovery-channel"
            elif name_clean == "golf":
                name_clean = "golf-channel"
            elif name_clean == "tennis":
                name_clean = "tennis-channel"
            elif name_clean == "nba":
                name_clean = "nba-tv"
            elif name_clean == "ae":
                name_clean = "a-e"

            # Construct the exact URL layout targeting the repository path
            logo_url = f"https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/united-states/{name_clean}-us.png"

            meta_string = f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="USA"'
            m3u_output += f"{meta_string},{display_name}\n"
            m3u_output += f"{base_start}{channel_id}{base_end}\n"
            found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Generated playlist string tracking {found_count} loose-matched channel assets.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
