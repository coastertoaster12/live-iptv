import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

# Explicit 1:1 logo dictionary map
manual_logo_map = {
    "abc us": "abc",
    "animal planet us": "animal-planet",
    "cbs us": "cbs",
    "comedy central us": "comedy-central",
    "cartoon network us": "cartoon-network",
    "cnn us": "cnn",
    "cozi tv us": "cozi-tv",
    "disney channel us": "disney-channel",
    "disney xd us": "disney-xd",
    "espn us": "espn",
    "espn 2 us": "espn2",
    "espn2 us": "espn2",
    "espnu us": "espnu",
    "fox sports 2 us": "fox-sports-2",
    "fs2 us": "fox-sports-2",
    "fox us": "fox",
    "fx us": "fx",
    "fxx us": "fxx",
    "fox news us": "fox-news-channel",
    "golf channel us": "golf-channel",
    "hbo us": "hbo",
    "hbo 2 us": "hbo2",
    "hbo2 us": "hbo2",
    "hbo comedy us": "hbo-comedy",
    "hbo family us": "hbo-family",
    "usa network us": "usa-network",
    "ion mystery us": "ion-mystery",
    "mtv us": "mtv",
    "mlb network us": "mlb-network",
    "newsmax us": "newsmax",
    "pbs us": "pbs",
    "cw us": "the-cw",
    "food network us": "food-network",
    "the weather channel us": "the-weather-channel",
    "weather channel us": "the-weather-channel",
    "nickelodeon us": "nickelodeon",
    "nick us": "nickelodeon",
    "vice tv us": "vice",
    "yes network us": "yes-network",
    "game show network us": "gsn",
    "gsn us": "gsn"
}

# General keywords to make sure any other US channel passes the entry filter
us_keywords = [
    "usa", "us", "philly", "philadelphia", "bally", "tcm", "tlc", "travel", "vice", "wgn", 
    "pix11", "turner", "cw", "mtv", "vh1", "animal planet", "oxygen", "tv land", "sec", "acc", 
    "big ten", "cinemax", "starz", "showtime", "bravo", "amc", "paramount", "history", "discovery"
]

print("Scraping DaddyLive (All US Channels Intact, Selective 1:1 Logos)...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport", "viaplay", "optus", "stan sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = re.search(r'watch\.php\?id=(\d+)', href)
        if match:
            channel_id = match.group(1)
            raw_channel_name = a_tag.get_text(strip=True)
            name_lower = raw_channel_name.lower()

            # Filter international blocks immediately
            if any(block in name_lower for block in strict_blocks):
                continue
            if "espn" in name_lower and any(intl in name_lower for intl in espn_intl_blocks):
                continue

            # Ensure it's a US stream using the broad allowlist or suffix checks
            is_us = any(k in name_lower for k in us_keywords) or any(k in name_lower for k in manual_logo_map.keys()) or name_lower.endswith(" us") or name_lower.endswith(" usa")
            if not is_us:
                continue

            display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
            display_name = display_name.rstrip('- ').rstrip('|').strip()

            # Match against the 1:1 map if available
            logo_file = ""
            for site_name, repo_name in manual_logo_map.items():
                if site_name in name_lower:
                    logo_file = repo_name
                    break

            meta_string = '#EXTINF:-1'
            if logo_file:
                logo_url = f"https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/united-states/{logo_file}-us.png"
                meta_string += f' tvg-logo="{logo_url}"'
            
            meta_string += f' group-title="USA"'
            
            m3u_output += f"{meta_string},{display_name}\n"
            m3u_output += f"{base_start}{channel_id}{base_end}\n"
            found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Kept all {found_count} US channels with targeted logo injection.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
