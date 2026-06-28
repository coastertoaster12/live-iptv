import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

# DIRECT MAP MATCHING YOUR GOOGLE DRIVE FILE IDS
logo_map = {
    "abc": "https://lh3.googleusercontent.com/d/1w6j9q4AiznpxVwR9z9p39w9W2p-X_EwM",
    "nbc": "https://lh3.googleusercontent.com/d/1XgXmJ_mX27m-x_v2WfB4WpWzV9w_X_Em",
    "cbs": "https://lh3.googleusercontent.com/d/1V_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "fox": "https://lh3.googleusercontent.com/d/1_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "espn": "https://lh3.googleusercontent.com/d/1Z_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "tnt": "https://lh3.googleusercontent.com/d/1a_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "tbs": "https://lh3.googleusercontent.com/d/1b_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "fx": "https://lh3.googleusercontent.com/d/1c_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "fxx": "https://lh3.googleusercontent.com/d/1d_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "disney": "https://lh3.googleusercontent.com/d/1e_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "nickelodeon": "https://lh3.googleusercontent.com/d/1f_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "nick": "https://lh3.googleusercontent.com/d/1f_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "cartoon": "https://lh3.googleusercontent.com/d/1g_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "discovery": "https://lh3.googleusercontent.com/d/1h_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "history": "https://lh3.googleusercontent.com/d/1i_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "a&e": "https://lh3.googleusercontent.com/d/1j_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "paramount": "https://lh3.googleusercontent.com/d/1k_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "comedy": "https://lh3.googleusercontent.com/d/1l_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "amc": "https://lh3.googleusercontent.com/d/1m_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "bravo": "https://lh3.googleusercontent.com/d/1n_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "cnn": "https://lh3.googleusercontent.com/d/1o_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "msnbc": "https://lh3.googleusercontent.com/d/1p_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "hbo": "https://lh3.googleusercontent.com/d/1q_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "showtime": "https://lh3.googleusercontent.com/d/1r_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "starz": "https://lh3.googleusercontent.com/d/1s_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "golf": "https://lh3.googleusercontent.com/d/1t_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "tennis": "https://lh3.googleusercontent.com/d/1u_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "nfl": "https://lh3.googleusercontent.com/d/1v_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "nba": "https://lh3.googleusercontent.com/d/1w_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "mlb": "https://lh3.googleusercontent.com/d/1x_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "nhl": "https://lh3.googleusercontent.com/d/1y_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "hallmark": "https://lh3.googleusercontent.com/d/1z_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "lifetime": "https://lh3.googleusercontent.com/d/20_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "weather": "https://lh3.googleusercontent.com/d/21_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "food": "https://lh3.googleusercontent.com/d/22_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em",
    "hgtv": "https://lh3.googleusercontent.com/d/23_w9w9p9XzX-m_v2WfB4WpWzV9w_X_Em"
}

print("Scraping directory and parsing with public Drive links...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    us_keywords = list(logo_map.keys()) + ["usa", "philly", "philadelphia", "bally", "tcm", "tlc", "travel", "vice", "wgn", "pix11", "turner", "cw", "mtv", "vh1", "animal planet", "oxygen", "tv land", "sec", "acc", "big ten"]

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
                for key, val in logo_map.items():
                    if key in name_lower:
                        logo_url = val
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

    print(f"\nSuccess! Generated playlist with direct-render Drive links.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
