import urllib.request
import re
import json
from bs4 import BeautifulSoup
from rapidfuzz import process, utils

directory_url = "https://dlhd.pk/24-7-channels.php"
# A live database containing thousands of verified US logos and EPG IDs
epg_db_url = "https://iptv-org.github.io/api/channels.json"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

print("Loading comprehensive US metadata database...")

try:
    # 1. Fetch the big database of official US channels, logos, and IDs
    db_req = urllib.request.Request(epg_db_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(db_req, timeout=15) as response:
        db_data = json.loads(response.read().decode('utf-8'))
    
    # Filter down to just US channels that actually have an EPG ID
    us_db = {}
    for ch in db_data:
        if ch.get('country') == 'US' and ch.get('id'):
            clean_name = utils.default_process(ch['name'])
            us_db[clean_name] = {
                "id": ch['id'],
                "logo": ch.get('logo', '')
            }
            
    db_names_list = list(us_db.keys())

    print("Scraping DaddyLive and automatically mapping every channel...")
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/us.xml"\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    # Expanded list to grab your entire 200+ channel layout cleanly
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

            # Catch anything using our core tags or ending in "us"/"usa"
            is_us = any(k in name_lower for k in us_keywords) or name_lower.endswith(" us") or name_lower.endswith(" usa")
            
            if is_us:
                # Clean up "id:123" metadata strings
                clean_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
                clean_name = clean_name.rstrip('- ').rstrip('|').strip()
                
                # --- FUZZY AUTOPILOT MATCHING SYSTEM ---
                # This compares the messy scraped name to the official database list
                processed_scraped = utils.default_process(clean_name)
                best_match = process.extractOne(processed_scraped, db_names_list, score_cutoff=75)
                
                tvg_id = ""
                logo_url = ""
                
                if best_match:
                    matched_key = best_match[0]
                    tvg_id = us_db[matched_key]['id']
                    logo_url = us_db[matched_key]['logo']

                # Build the playlist metadata line automatically
                meta_string = f'#EXTINF:-1 group-title="USA"'
                if tvg_id:
                    meta_string += f' tvg-id="{tvg_id}"'
                if logo_url:
                    meta_string += f' tvg-logo="{logo_url}"'
                
                m3u_output += f"{meta_string},{clean_name}\n"
                m3u_output += f"{base_start}{channel_id}{base_end}\n"
                found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Automatically mapped guide metadata for {found_count} channels.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
