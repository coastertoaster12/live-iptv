import urllib.request
import re
import json
from bs4 import BeautifulSoup
from rapidfuzz import process, utils

directory_url = "https://dlhd.pk/24-7-channels.php"
# Fetching the official iptv-org consolidated channel dataset
epg_db_url = "https://iptv-org.github.io/api/channels.json"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

print("Loading global logo registry...")

try:
    db_req = urllib.request.Request(epg_db_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(db_req, timeout=15) as response:
        db_data = json.loads(response.read().decode('utf-8'))
    
    # Store clean root names mapped straight to their public image links
    logo_registry = {}
    for ch in db_data:
        name_str = ch.get('name')
        logo_url = ch.get('logo') or ch.get('logo_url')
        if name_str and logo_url:
            # Tokenize names to catch quick matches
            clean_db_key = utils.default_process(name_str)
            logo_registry[clean_db_key] = logo_url
            
    registry_keys = list(logo_registry.keys())

    print("Scraping live index & extracting images...")
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    us_keywords = [
        "usa", "nbc", "espn", "fox", "cbs", "abc", "philly", "philadelphia", "bally", "cartoon", 
        "nickelodeon", "nick", "disney", "tnt", "tbs", "fx", "fxx", "discovery", "history", 
        "a&e", "paramount", "comedy", "amc", "bravo", "e!", "food", "hgtv", "syfy", "tcm", 
        "tlc", "travel", "vice", "wgn", "pix11", "turner", "cw", "mtv", "vh1", "animal planet", 
        "msnbc", "cnn", "weather", "hallmark", "lifetime", "oxygen", "tv land", "golf", "tennis", 
        "nfl", "nba", "mlb", "nhl", "sec", "acc", "big ten", "hbo", "starz", "cinemax", "showtime"
    ]

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = re.search(r'watch\.php\?id=(\d+)', href)
        if match:
            channel_id = match.group(1)
            raw_channel_name = a_tag.get_text(strip=True)
            name_lower = raw_channel_name.lower()

            if any(block in name_lower for block in strict_blocks):
                continue
            if "espn" in name_lower and any(intl in name_lower for intl in espn_intl_blocks):
                continue

            is_us = any(k in name_lower for k in us_keywords) or name_lower.endswith(" us") or name_lower.endswith(" usa")
            
            if is_us:
                # Aggressively clean descriptive labels to leave just the root network name
                display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
                display_name = display_name.rstrip('- ').rstrip('|').strip()
                
                # Strip out noisy structural additions that throw off matching engines
                search_name = display_name.replace("USA", "").replace("US", "").replace("HD", "").replace("FHD", "").strip()
                processed_search = utils.default_process(search_name)
                
                # Drop score threshold to 50 to maximize logo hits via token extraction
                best_match = process.extractOne(processed_search, registry_keys, score_cutoff=50)
                
                logo_string = ""
                if best_match:
                    logo_string = logo_registry[best_match[0]]

                # Construct M3U row emphasizing the logo tag
                meta_string = '#EXTINF:-1'
                if logo_string:
                    meta_string += f' tvg-logo="{logo_string}"'
                
                meta_string += f' group-title="USA"'
                
                m3u_output += f"{meta_string},{display_name}\n"
                m3u_output += f"{base_start}{channel_id}{base_end}\n"
                found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Found logos and written links for {found_count} streams.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
