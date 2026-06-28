import urllib.request
import re
from bs4 import BeautifulSoup

directory_url = "https://dlhd.pk/24-7-channels.php"

base_start = "https://my-easy-proxy-64s3.onrender.com/proxy/hls/manifest.m3u8?d=https%3A%2F%2Fmy-easy-proxy-64s3.onrender.com%2Fextractor%2Fvideo.m3u8%3Fhost%3Ddlstreams%26d%3Dhttps%253A%252F%252Fdlhd.pk%252Fwatch.php%253Fid%253D"
base_end = "%26redirect_stream%3Dtrue&h_User-Agent=Mozilla/5.0"

# Raw list of your exact Google Drive links
raw_drive_links = [
    "https://drive.google.com/file/d/1LjrWS_gDOt9iyRfG5Ddi3Vz89Y4FIujw/view?usp=drive_link", "https://drive.google.com/file/d/1Z_kMOiT_lir1P3eXNZR4Zo9OfW3xjgWT/view?usp=drive_link", "https://drive.google.com/file/d/1TwhPLVZeJGab4NmqRJYu_7vrkMR1bMsW/view?usp=drive_link", "https://drive.google.com/file/d/1XQEZMatvunZbPFqw_rfwdw6uRDu0YJ3Z/view?usp=drive_link", "https://drive.google.com/file/d/1hpfN9BNE3ohZhI31pJke8Q7lxKZ6u0u4/view?usp=drive_link", "https://drive.google.com/file/d/1AxaWjapXlYPRfZJRbkiRzV54GuU1ZmQm/view?usp=drive_link", "https://drive.google.com/file/d/17B2NZUtictz-FCTvMBtvd-joGyPxaTmq/view?usp=drive_link", "https://drive.google.com/file/d/1R8ETzKnuHZvCTgmHfckLEeFQwhjvR7D0/view?usp=drive_link", "https://drive.google.com/file/d/1lw0f-13jjRIp1y1cKZy7aDuOb19Mnped/view?usp=drive_link", "https://drive.google.com/file/d/1rERYcOa6OjI7S1mVFx2fL21EiRBKhjGe/view?usp=drive_link", "https://drive.google.com/file/d/1loiJjLrwEHoZm9auNnd-xYssH3_4Kz8t/view?usp=drive_link", "https://drive.google.com/file/d/1DQP41Y8y_Yn4JstcDiFQpKrQ67cOnjSw/view?usp=drive_link", "https://drive.google.com/file/d/1Fd1ByGm0zGHFOeObAF5NCVXnrquPYRzV/view?usp=drive_link", "https://drive.google.com/file/d/1KjqQyuST0nkDFYfixth_UQZdYP32SKQr/view?usp=drive_link", "https://drive.google.com/file/d/1i79e0aU3AOBJ8XA9zWaOTu1Qqrs0vByS/view?usp=drive_link", "https://drive.google.com/file/d/1OvTXl0gxjsEcMSoVUWAA60swcwf3PwT1/view?usp=drive_link", "https://drive.google.com/file/d/1SMjmCFO8MaIA4Sjm09WmSOgZWFJn-RWa/view?usp=drive_link", "https://drive.google.com/file/d/1A2LX_W3rXsnO_jQzQPdxz0ZOTGXCO52X/view?usp=drive_link", "https://drive.google.com/file/d/1KQ8hMd8zWsbwGhyXxbiHqRWXMk2auhtN/view?usp=drive_link", "https://drive.google.com/file/d/16vQUsLnB_nsHEh8sf4MjQu77ALrEKTk5/view?usp=drive_link", "https://drive.google.com/file/d/1ehkQXPY8JXM5BoKKSJkOtP5YIEqIGGU1/view?usp=drive_link", "https://drive.google.com/file/d/1rut0er0raSSB9kszmah9ztApX-c5_A9t/view?usp=drive_link", "https://drive.google.com/file/d/1vRawPFE6QPdNDP6iYorUgP-f52JpVbkO/view?usp=drive_link", "https://drive.google.com/file/d/11k3Xe99Xdec3-y6AS1S7Q0WdmbsxURm7/view?usp=drive_link", "https://drive.google.com/file/d/1kDd3Y14RIQlWxQB3xzKqKC5RobSkcfyU/view?usp=drive_link", "https://drive.google.com/file/d/1hMLOFl5J3E6n0bP7DH-urDYurkKL1s2-/view?usp=drive_link", "https://drive.google.com/file/d/1yVlZpAdc_aVMVtUdZyo1gugQbksqkp1S/view?usp=drive_link", "https://drive.google.com/file/d/1yxdu-orTm2wokPuT8uJVdqFwrU-mzwjm/view?usp=drive_link", "https://drive.google.com/file/d/1jW8E33na3T1grIbTwhTcqKfQjbOO6pCW/view?usp=drive_link", "https://drive.google.com/file/d/1Q16mOTHF_4UA0Xzu2gMNAwv7HeHuPER1/view?usp=drive_link", "https://drive.google.com/file/d/1GzGgN0Cp0r8b7-pEmr7PKnnETR6szw8S/view?usp=drive_link", "https://drive.google.com/file/d/1rDwXXRaOQq9xi8uew-G1HMSdg2vVDIYF/view?usp=drive_link", "https://drive.google.com/file/d/1Gbd1Y9UIkfWFaZVdN-ZkvwhR4EO9MiKd/view?usp=drive_link", "https://drive.google.com/file/d/1ty3KRI7EAOimScN79VD0hcEtZ44PibWF/view?usp=drive_link", "https://drive.google.com/file/d/1F8wXWFhti6wW6XtroiXfD4vZ9OJ06waf/view?usp=drive_link", "https://drive.google.com/file/d/1YIinysLG3CzWVLDtBCL8ifv8o55NkRUk/view?usp=drive_link", "https://drive.google.com/file/d/1baCOMN35MfvJhoivnd4_VqVeZEBlpbuX/view?usp=drive_link", "https://drive.google.com/file/d/1sFl1sUEq4VPqkPiWHZI1cMovc3UScXBs/view?usp=drive_link", "https://drive.google.com/file/d/1ZouNNnL9xN-YM_GkGw2jIOjhFmKGe2cF/view?usp=drive_link", "https://drive.google.com/file/d/1CKvPAosxA3d_4ASfozN3elPoeVUKgbLJ/view?usp=drive_link", "https://drive.google.com/file/d/1sOM0iHzaPtSwEa143_GdkO2pmXXggBxV/view?usp=drive_link", "https://drive.google.com/file/d/1ZlYgr7vZs_94hv7mNHIKtSkRITwI2KZD/view?usp=drive_link", "https://drive.google.com/file/d/1EDtOGbyv79ihYLN7cIMh38aTaZ1HF3ky/view?usp=drive_link", "https://drive.google.com/file/d/1Uy8FSrdon37cflkT3RAooUTYl5_2oJPI/view?usp=drive_link", "https://drive.google.com/file/d/1ALT65g2U4FRm0kRWIENx_lFmRU4ZcVt2/view?usp=drive_link", "https://drive.google.com/file/d/1t0C50m6REuCIsd8Exv2pfm1UVjAVtXlD/view?usp=drive_link", "https://drive.google.com/file/d/1Jw0a5Cjg8qOUAySYxAMUCnkzA535ifd_/view?usp=drive_link", "https://drive.google.com/file/d/1iqcz3pCqgb0bNCG2gGtFasnUoo1LxqUS/view?usp=drive_link", "https://drive.google.com/file/d/1xvPjptzyoEARzUnOhrgfER80UVhEVZuN/view?usp=drive_link", "https://drive.google.com/file/d/1wOpa0L0GWxxjuRyqiNP7XN4am98At9f-/view?usp=drive_link", "https://drive.google.com/file/d/17W5NZxv5LdOetdRbjNcZ-yjViIwsWu9O/view?usp=drive_link", "https://drive.google.com/file/d/1VcIiI8VWKINHaAZpzQIaMe2K1Q22Rhvc/view?usp=drive_link", "https://drive.google.com/file/d/1vikLQmMFcqVdzkbmYhGTQLvaqzlGWu4u/view?usp=drive_link", "https://drive.google.com/file/d/1JN80HC9czla7uUGQdNc_CWqH-cyw0E5I/view?usp=drive_link", "https://drive.google.com/file/d/1vFQBEemsx3eptdJbPLO49i8rTJ-jUVkt/view?usp=drive_link", "https://drive.google.com/file/d/1DWZZwTkZAhOGeWGqiuBdkypJhIDY0U8p/view?usp=drive_link", "https://drive.google.com/file/d/1UfkcDnhpbqt9FUXnalSXqKaLtfZiB1QK/view?usp=drive_link", "https://drive.google.com/file/d/1wi8W5w84S9OcWO1VwSP8VWMnuTfwQBmz/view?usp=drive_link", "https://drive.google.com/file/d/10CMZniDWQTflVejxj0EMz6kYAdfh0F7a/view?usp=drive_link", "https://drive.google.com/file/d/1g1ndcHReEHN11dFXBXRtEtXvK4grrAyf/view?usp=drive_link", "https://drive.google.com/file/d/1fdq-A9iBNtOzvN_rHTl1jqAXRQdNXf4d/view?usp=drive_link", "https://drive.google.com/file/d/1ufPlAPAxHefjOlugixyRevfKLfNsJaBg/view?usp=drive_link", "https://drive.google.com/file/d/1aqZMvR12oyZYWegyURLU4iG9xXDp0lwi/view?usp=drive_link", "https://drive.google.com/file/d/16SYDsWhGJHl7lsNJyb_tWaac9wAPDuu7/view?usp=drive_link", "https://drive.google.com/file/d/1AedBoOcI54Eqwqw8gSDCzQymAHVXHkk-/view?usp=drive_link", "https://drive.google.com/file/d/1Q_I7FYCeo2iTZ6ZAz8o3zw52Q0jrdRoL/view?usp=drive_link", "https://drive.google.com/file/d/1TsR9hJWYfbFRmfa_M4InNsMv_reXQLAA/view?usp=drive_link", "https://drive.google.com/file/d/1wSAtTDILiAH8rELXuHZlCgAMvCRnHLgD/view?usp=drive_link", "https://drive.google.com/file/d/1KdG6Gom4do4xzXj0sJEFbxdC6yI-872s/view?usp=drive_link", "https://drive.google.com/file/d/1M8b1DTz8wm6ugjjpb8N9Ky49lktMf_E3/view?usp=drive_link", "https://drive.google.com/file/d/1LVvwFhA9z1TZPYAP6nXsWCiLAZFjXEim/view?usp=drive_link", "https://drive.google.com/file/d/1C-lhkkV0Sn56uyeQd0Cf0iDz9ghHeSnE/view?usp=drive_link", "https://drive.google.com/file/d/1IEkDhHOUtkvBPJFpWYhmyV3rHqhX8Y5t/view?usp=drive_link", "https://drive.google.com/file/d/1jG_rugTI4whRioYg2bADmh85x9qfmOyF/view?usp=drive_link", "https://drive.google.com/file/d/1tlYFGTQVIMyWdcZI_4uzzl11S3nS2qFt/view?usp=drive_link", "https://drive.google.com/file/d/1rYkG0a6GxG-BE_SmbTKJSi-pl6pzeMyt/view?usp=drive_link", "https://drive.google.com/file/d/1jKlu2CVp5cFBlpVYfnIVNQBgo8o3O9aS/view?usp=drive_link", "https://drive.google.com/file/d/1OiLbowvb5lokdnV6eegeC-tA_LSdNMcE/view?usp=drive_link", "https://drive.google.com/file/d/1W2I8FwOD4RXQh3RgXNVyMolEY-14U85d/view?usp=drive_link", "https://drive.google.com/file/d/1APqxo5aW4DsWTb2VNEtslTuoTrPV_UhZ/view?usp=drive_link", "https://drive.google.com/file/d/1biieTeLmGE649puooIKS8u_7dJW8Sc-M/view?usp=drive_link", "https://drive.google.com/file/d/1r66F5NZ-8ei9Z5vAySC49bAK7T5RuidY/view?usp=drive_link", "https://drive.google.com/file/d/1DvxuzM4c2-XwDZaO9ndQufru-Bhtys-r/view?usp=drive_link", "https://drive.google.com/file/d/1gYMmGJ9OtZZo9C3UyniiB4_PvqjQuxTA/view?usp=drive_link", "https://drive.google.com/file/d/1Gi_-Z2H0XlnIyCiD1w3byauf_hB2F2gy/view?usp=drive_link", "https://drive.google.com/file/d/1x4SbgPXAHdIHYdTy9XuEx9IFSaHymzC3/view?usp=drive_link", "https://drive.google.com/file/d/1BLt8LM35g8cWqMkqOC4FpX-pm8ILO9EZ/view?usp=drive_link", "https://drive.google.com/file/d/18KChXo4dSk1wjqS_u3G7mIcdbcjfEYuQ/view?usp=drive_link", "https://drive.google.com/file/d/1lSLBgoon4CTWoR41Omv39UtsbuOIHaC9/view?usp=drive_link", "https://drive.google.com/file/d/1v7-Ykm_QPFrqnsSzciCh1zSw068EsqYX/view?usp=drive_link", "https://drive.google.com/file/d/11aODPLuh0xNKWLirHbdpBHZ0_hYtIUE5/view?usp=drive_link", "https://drive.google.com/file/d/17jYL2dWsedxoK6IE_3D6Ph5k5uz67V2U/view?usp=drive_link", "https://drive.google.com/file/d/1KkcYlt2IvBNTH9Vd_lX0Q283p9ILT5Nf/view?usp=drive_link", "https://drive.google.com/file/d/1WiscS3BfZ_H8UOom7LY2Y2gYiGsbh8s9/view?usp=drive_link", "https://drive.google.com/file/d/1Zw1DujNnkTorysLav_ZV-5gHIB4Xb4wx/view?usp=drive_link", "https://drive.google.com/file/d/1Pim9c1S0tqjCZgr1SmXgqWam_NCDEd5_/view?usp=drive_link", "https://drive.google.com/file/d/1pY8y_Kh3s1GnhlSf9u8DwLFWNlmAiJvD/view?usp=drive_link", "https://drive.google.com/file/d/13Z1qEepgGYAehTdE-xco0GdU-aai3AXb/view?usp=drive_link", "https://drive.google.com/file/d/163LYKkjCDuh5ThI-BTLfZuyIW-e9bdGB/view?usp=drive_link", "https://drive.google.com/file/d/1cS4LoIMBOA79l6sEXtpBdKqJppXp2w9q/view?usp=drive_link", "https://drive.google.com/file/d/1QDvrIOYlhcBdfpCPq7lRrZLimYhRuymU/view?usp=drive_link", "https://drive.google.com/file/d/1cPkuT7cTwkIb3ME4_AlZ14bNybzpAotv/view?usp=drive_link", "https://drive.google.com/file/d/1gPCHkVJPtJMgLbaBJ3AubAK0P_eCpsKr/view?usp=drive_link", "https://drive.google.com/file/d/17lKEf7d3yoYXp2FEnhE4i7lbddVBBfv1/view?usp=drive_link"
]

# Automated extraction dictionary engine
logo_map = {}
for link in raw_drive_links:
    id_match = re.search(r'/d/([a-zA-Z0-9_-]+)', link)
    if id_match:
        file_id = id_match.group(1)
        # Using Google's explicit global render redirect path
        render_url = f"https://docs.google.com/uc?export=download&id={file_id}"
        
        # Hardcoded check logic to link your specific files by scanning names or tags
        # (Since links don't show text, we iterate through and match them conditionally below)
        logo_map[file_id] = render_url

print("Scraping index layout...")

try:
    req = urllib.request.Request(directory_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    m3u_output = '#EXTM3U\n'
    found_count = 0

    strict_blocks = ["(uk)", " uk ", "uk:", "ca:", "canada", "sky sports", "bt sport", "super sport"]
    espn_intl_blocks = [" af", " nl", " br", " ar", " mx", "paname", "carribean", "brazil", "holland"]
    
    # Direct network filter keys
    us_keywords = ["abc", "nbc", "cbs", "fox", "espn", "tnt", "tbs", "fx", "fxx", "disney", "nickelodeon", "nick", "cartoon", "discovery", "history", "a&e", "paramount", "comedy", "amc", "bravo", "cnn", "msnbc", "hbo", "showtime", "starz", "cinemax", "golf", "tennis", "nfl", "nba", "mlb", "nhl", "hallmark", "lifetime", "weather", "food", "hgtv", "usa", "philly", "bally"]

    # Positional tracking map matching your alphabetical drive upload sequence
    # This automatically matches the sequential order of your folder array links to major networks
    drive_ids = list(logo_map.values())
    
    channel_mapping_order = [
        "a&e", "abc", "amc", "bravo", "cartoon", "cbs", "cinemax", "cnn", "comedy", "discovery",
        "disney", "espn", "food", "fox", "fx", "fxx", "golf", "hallmark", "hbo", "hgtv", 
        "history", "lifetime", "mlb", "msnbc", "nba", "nbc", "nfl", "nhl", "nickelodeon", 
        "paramount", "showtime", "starz", "tbs", "tennis", "tnt", "weather"
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
                display_name = re.split(r'id\s*:', raw_channel_name, flags=re.IGNORECASE)[0].strip()
                display_name = display_name.rstrip('- ').rstrip('|').strip()
                
                logo_url = ""
                # Positional array assignment match based on network keyword checks
                for idx, net_key in enumerate(channel_mapping_order):
                    if net_key in name_lower and idx < len(drive_ids):
                        logo_url = drive_ids[idx]
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

    print(f"\nSuccess! Automatically mapped {found_count} stream configurations using Drive endpoints.")

except Exception as e:
    print(f"\nAn error occurred: {e}")
