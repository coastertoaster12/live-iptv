import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

# Base URL elements for formatting the playlist links
base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

print("Running clean US database filter with strict ESPN protection... Please wait.")

try:
    req = urllib.request.Request(
        directory_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )

    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')

    m3u_output = "#EXTM3U\n"
    found_count = 0

    # Broad international indicators to drop
    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    
    # Specific regions to block ONLY if the channel is an ESPN variant
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]

    us_database_keywords = [
        "usa", "nbc", "espn", "fox", "cbs", "abc", "philly", "philadelphia", "bally",
        "cartoon", "nickelodeon", "nick", "disney", "toon", "hbo", "starz", "cinemax", 
        "showtime", "tnt", "tbs", "truetv", "fx", "fxx", "discovery", "history", 
        "nat geo", "a&e", "paramount", "comedy", "amc", "bravo", "e!", "food", "hgtv",
        "syfy", "tcm", "tlc", "travel", "vice", "wgn", "pix11", "turner", "cw", "mtv", "vh1",
        "animal planet", "msnbc", "cnn", "fox news", "weather", "hallmark", "lifetime", "oxygen",
        "tv land", "realty", "golf", "tennis", "nfl", "nba", "mlb", "nhl", "sec", "acc", "big ten"
    ]

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        match = re.search(r'watch\.php\?id=(\d+)', href)
        if match:
            channel_id = match.group(1)
            raw_channel_name = a_tag.get_text(strip=True)
            name_lower = raw_channel_name.lower()

            # 1. Global block check
            if any(block in name_lower for block in strict_blocks):
                continue

            # 2. Strict ESPN international filter
            if "espn" in name_lower:
                if any(intl in name_lower for intl in espn_intl_blocks):
                    continue  # Instantly skip non-US ESPN networks

            # 3. Main keyword filter matching
            is_us_match = False
            for keyword in us_database_keywords:
                if keyword in name_lower:
                    is_us_match = True
                    break
            
            if name_lower.endswith(" us") or name_lower.endswith(" usa"):
                is_us_match = True

            if is_us_match:
                # Clean up "id:123" metadata patterns
                clean_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
                clean_name = clean_name.rstrip('- ').rstrip('|').strip()

                if not clean_name:
                    clean_name = f"US Channel {int(channel_id):04d}"

                m3u_output += f"#EXTINF:-1 group-title=\"USA\",{clean_name}\n"
                m3u_output += f"{base_start}{channel_id}{base_end}\n"
                found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Filtered down to {found_count} verified US channels.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
