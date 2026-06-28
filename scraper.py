import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

# Direct string mapping to match their exact repo filenames
repo_logos = {
    "abc": "abc-us.png",
    "nbc": "nbc-us.png",
    "cbs": "cbs-us.png",
    "fox": "fox-us.png",
    "espn": "espn-us.png",
    "tnt": "tnt-us.png",
    "tbs": "tbs-us.png",
    "fx": "fx-us.png",
    "fxx": "fxx-us.png",
    "disney": "disney-channel-us.png",
    "nickelodeon": "nickelodeon-us.png",
    "nick": "nickelodeon-us.png",
    "cartoon": "cartoon-network-us.png",
    "discovery": "discovery-channel-us.png",
    "history": "history-us.png",
    "a&e": "ae-us.png",
    "paramount": "paramount-network-us.png",
    "comedy": "comedy-central-us.png",
    "amc": "amc-us.png",
    "bravo": "bravo-us.png",
    "cnn": "cnn-us.png",
    "msnbc": "msnbc-us.png",
    "hbo": "hbo-us.png",
    "showtime": "showtime-us.png",
    "starz": "starz-us.png",
    "cinemax": "cinemax-us.png",
    "golf": "golf-channel-us.png",
    "tennis": "tennis-channel-us.png",
    "nfl": "nfl-network-us.png",
    "nba": "nba-tv-us.png",
    "mlb": "mlb-network-us.png",
    "nhl": "nhl-network-us.png",
    "hallmark": "hallmark-channel-us.png",
    "lifetime": "lifetime-us.png",
    "weather": "the-weather-channel-us.png",
    "food": "food-network-us.png",
    "hgtv": "hgtv-us.png"
}

print("Scraping DaddyLive directory...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    us_keywords = list(repo_logos.keys()) + ["usa", "philly", "philadelphia", "bally", "tcm", "tlc", "travel", "vice", "wgn", "pix11", "turner", "cw", "mtv", "vh1", "animal planet", "oxygen", "tv land", "sec", "acc", "big ten"]

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
                display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
                display_name = display_name.rstrip('- ').rstrip('|').strip()
                
                logo_url = ""
                for key, filename in repo_logos.items():
                    if key in name_lower:
                        # Construct direct link to the tv-logo raw repository source
                        logo_url = f"https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/united-states/{filename}"
                        break

                meta_string = '#EXTINF:-1'
                if logo_url:
                    meta_string += f' tvg-logo="{logo_url}"'
                
                meta_string += f' group-title="USA"'
                
                m3u_output += f"{meta_string},{display_name}\n"
                m3u_output += f"{base_start}{channel_id}{base_end}\n"
                found_count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_output)

    print(f"\nSuccess! Generated playlist linked to dark-background assets.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
