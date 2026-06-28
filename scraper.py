import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

print("Scraping DaddyLive (Strict US Filtering + Fixed Logo Matching)...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    # Strict international blocking rules
    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport", "viaplay", "optus", "stan sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    # Baseline US keyword indicator block
    us_keywords = [
        "abc", "nbc", "cbs", "fox", "espn", "tnt", "tbs", "fx", "fxx", "disney", "nickelodeon", 
        "nick", "cartoon", "discovery", "history", "a&e", "paramount", "comedy", "amc", "bravo", 
        "cnn", "msnbc", "hbo", "showtime", "starz", "cinemax", "golf", "tennis", "nfl", "nba", 
        "mlb", "nhl", "hallmark", "lifetime", "weather", "food", "hgtv", "usa", "philly", 
        "philadelphia", "bally", "tcm", "tlc", "travel", "vice", "wgn", "pix11", "turner", 
        "cw", "mtv", "vh1", "animal planet", "oxygen", "tv land", "sec", "acc", "big ten"
    ]

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = re.search(r'watch\.php\?id=(\d+)', href)
        if match:
            channel_id = match.group(1)
            raw_channel_name = a_tag.get_text(strip=True)
            name_lower = raw_channel_name.lower()

            # 1. STRICT FILTERING: Drop non-US channels immediately
            if any(block in name_lower for block in strict_blocks):
                continue
            if "espn" in name_lower and any(intl in name_lower for intl in espn_intl_blocks):
                continue

            is_us = any(k in name_lower for k in us_keywords) or name_lower.endswith(" us") or name_lower.endswith(" usa")
            if not is_us:
                continue

            # Clean up trailing stream garbage for clean UI display
            display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
            display_name = display_name.rstrip('- ').rstrip('|').strip()

            # 2. STRICT LOGO STRING CLEANING
            # Strip metadata suffixes out entirely before processing filenames
            name_clean = name_lower
            name_clean = re.sub(r'\s*(fhd|hd|sd|720p|1080p|us|usa|ca|uk|id\s*:.*)', '', name_clean).strip()
            
            # Standardize spacing and dashes
            name_clean = re.sub(r'[\s._|/&]+', '-', name_clean)
            name_clean = re.sub(r'[^a-z0-9\-]', '', name_clean)
            name_clean = name_clean.strip('-')

            # Remap main network structural name shifts to fit the repo file names perfectly
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
            elif name_clean == "ae" or name_clean == "a-e":
                name_clean = "ae"

            # Rebuild using the exact branch url you provided
            logo_url = f"https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/united-states/{name_clean}-us.png"

            meta_string = f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="USA"'
            m3u_output += f"{meta_string},{display_name}\n"
            m3u_output += f"{base_start}{channel_id}{base_end}\n"
            found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Found {found_count} US channels with matching logo assets assigned.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
