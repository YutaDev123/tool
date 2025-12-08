import pytz
import base64
import hashlib
import json
import os
import platform
import random
import re
import string
import subprocess
import sys
import time
import urllib.parse
import uuid
from datetime import datetime, timedelta, timezone
from time import sleep

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    import pytz
    import requests
    from tabulate import tabulate
# ... (Phần code hiện tại trong file update.py) ...
except ImportError:
    print('__Đang cài đặt các thư viện cần thiết, vui lòng chờ...')
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pip", 
        "install", 
        "--upgrade",
        "requests", 
        "colorama", 
        "pytz", 
        "tabulate", 
        "certifi" 
    ])
    print('__Cài đặt hoàn tất, vui lòng chạy lại Tool')
    sys.exit()



def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def rgb(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def banner():
    banner_text = r"""
╔════════════════════════════════════════════════════════════════╗
║    ____  __  ____  ____  __    ___   __  ____________          ║
║   / __ )/ / / /  |/  / |/ /   /   | / / / /_  __/ __ \         ║
║  / __  / / / / /|_/ /|   /   / /| |/ / / / / / / / / /         ║
║ / /_/ / /_/ / /  / //   |   / ___ / /_/ / / / / /_/ /          ║
║/_____/\____/_/  /_//_/|_|  /_/  |_\____/ /_/  \____/           ║
║                                                                ║
║                                      🔥Coded By KhoiNguyen  🔥 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
    colors = [
        (255, 0, 0), (255, 85, 0), (255, 170, 0),
        (255, 255, 0), (170, 255, 0), (85, 255, 0),
        (0, 255, 0), (0, 255, 85), (0, 255, 170),
        (0, 255, 255), (0, 170, 255), (0, 85, 255),
        (0, 0, 255), (85, 0, 255), (170, 0, 255),
        (255, 0, 255), (255, 0, 170), (255, 0, 85)
    ]
    color_index = 0
    for line in banner_text.split('\n'):
        for char in line:
            if char != ' ':
                r, g, b = colors[color_index % len(colors)]
                print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end='')
                time.sleep(0.0001)
                color_index += 1
            else:
                print(' ', end='')
        print()
    print(rgb(255, 255, 255, "═" * 64))
    print(rgb(255, 255, 255, "💡Đói quá phải vì miếng cơm💡"))
    print(rgb(255, 255, 255, "═" * 64))
    print()
# Tên file cờ (flag file)
TERMUX_FLAG_FILE = '.termux_api_ok'

# 🔑 KIỂM TRA TẠI ĐÂY
if platform.system() == 'Linux' and 'TERMUX_VERSION' in os.environ:
    
    
    if os.path.exists(TERMUX_FLAG_FILE):

        pass 
    else:
        
        print(rgb(5, 255, 255, '>> Đang kiểm tra/cài đặt API...'))
        try:
            # Lệnh cài đặt termux-api
            subprocess.check_call(['pkg', 'install', 'termux-api', '-y'])
            
            # CÀI ĐẶT THÀNH CÔNG: TẠO FILE CỜ
            with open(TERMUX_FLAG_FILE, 'w') as f:
                f.write('OK')
            
            print(rgb(5, 255, 0, '>>API đã sẵn sàng'))
            time.sleep(2)
            
        except Exception as e:
            print(rgb(255, 0, 0, f'>> Lỗi khi cài đặtapi: {e}'))
            print(rgb(255, 255, 0, '>> Vui lòng chạy lệnh: pkg install termux-api'))
            time.sleep(3)
def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def prints(*args, **kwargs):
    r, g, b = 255, 255, 255
    text = "text"
    end = "\n"
    if len(args) == 1:
        text = args[0]
    elif len(args) >= 3:
        r, g, b = args[0], args[1], args[2]
        if len(args) >= 4:
            text = args[3]
    if "text" in kwargs:
        text = kwargs["text"]
    if "end" in kwargs:
        end = kwargs["end"]
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

# ---------------- UI HELPERS ----------------
def ui_print(msg, prefix="  ", style="info"):
    if style == "success":
        prints(0, 255, 128, prefix, end='')
        prints(200, 255, 200, msg)
    elif style == "error":
        prints(255, 80, 80, prefix, end='')
        prints(255, 200, 200, msg)
    elif style == "warn":
        prints(255, 200, 0, prefix, end='')
        prints(255, 230, 150, msg)
    elif style == "accent":
        prints(100, 200, 255, prefix, end='')
        prints(200, 230, 255, msg)
    else:
        prints(180, 200, 255, prefix, end='')
        prints(230, 230, 255, msg)

def ui_input(prompt_text, hint=None):
    if hint:
        prints(100, 200, 255, "💬 ", end='')
        prints(200, 200, 255, f"{prompt_text} ", end='')
        prints(150, 150, 150, f"({hint})", end='')
        return input(" " )
    else:
        prints(100, 200, 255, "💬 ", end='')
        prints(200, 200, 255, f"{prompt_text} ", end='')
        return input(" ")

def ui_status(msg):
    prints(150, 255, 200, "⚙️  ", end='')
    prints(220, 220, 255, msg)
# ---------------- end UI HELPERS ----------------


# =========================================================================
# 💡 PHẦN CODE KIỂM TRA BẢN QUYỀN (LICENSE/HWID/IP) - BẮT ĐẦU
# =========================================================================


# THAY URL WEB APP ĐÃ DEPLOY CỦA BẠN VÀO ĐÂY
API_URL = "https://script.google.com/macros/s/AKfycbxQj6evdBT3lJub5cXF5EOWaAy1-XDyNqOcAiKV5hyLVQhxJMChhNSAjaYrZxGu1SMPOw/exec" 


LICENSE_FILE = 'kng-key.json' 

def get_saved_license():
    """
    Kiểm tra và tải Key đã lưu từ file kng-key.json.
    """
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_license(key): 
    """
    Lưu Key bản quyền vào file JSON cục bộ (chỉ lưu key).
    """
    data = {"key": key} 
    try:
        with open(LICENSE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        ui_print(f'Đã lưu key mới vào {LICENSE_FILE}', style='success')
    except Exception as e:
        ui_print(f'Lỗi khi lưu key: {e}', style='error')

def check_license_key_api(key: str, hwid: str, ip: str) -> dict:
    """
    Kiểm tra key bản quyền, liên kết HWID, và cập nhật IP cuối cùng.
    """
    
    params = {
        "action": "checkAndBind",
        "key": key,
        "hwid": hwid,
        "ip": ip 
    }
    
    try:
        response = requests.post(API_URL, data=params, timeout=30)
        response.raise_for_status() 
        api_res = response.json()
        return api_res
        
    except requests.exceptions.RequestException as e:
        return {"valid": False, "message": f"Lỗi kết nối server: {e}"}
    except json.JSONDecodeError:
        return {"valid": False, "message": "Lỗi định dạng phản hồi từ server. Vui lòng kiểm tra lại Apps Script."}
    except Exception as e:
        return {"valid": False, "message": f"Lỗi không xác định: {e}"}

# Hàm Lấy HWID
def get_stable_hwid():
    """
    Tạo HWID bằng cách sử dụng MAC Address (uuid.getnode()) và ID File System của Home Path.
    """
    try:
        # 1. Lấy MAC Address (Duy nhất phần cứng)
        # Sẽ thất bại trên nhiều môi trường ảo, nhưng nên thử
        try:
            mac_address = uuid.getnode() 
            mac_string = f"{mac_address:x}"
        except Exception:
            mac_string = "MAC_READ_ERROR" # Fallback ổn định, không random
        
        # 2. Lấy Unique File System ID (Khó bị clone hơn Home Path)
        # Sử dụng os.stat để lấy st_dev (Device ID) của thư mục Home
        home_path = os.path.expanduser('~')
        try:
            stat_info = os.stat(home_path)
            # st_dev: ID của thiết bị chứa file (ổn định)
            device_id = str(stat_info.st_dev)
        except Exception:
            device_id = "STAT_READ_ERROR"

        # 3. Kết hợp tất cả các yếu tố: Home Path (ổn định nhất) + MAC Address + File System ID
        # HWID chỉ trùng khi TẤT CẢ 3 yếu tố này giống nhau.
        raw_hwid_string = f"{home_path}-{mac_string}-{device_id}-V11_ULTRA_FIX" 

        final_hwid = hashlib.sha256(raw_hwid_string.encode()).hexdigest()
        
        return final_hwid

    except Exception:
        # KHỐI DỰ PHÒNG TĨNH CUỐI CÙNG (Dù lỗi vẫn ra HWID ổn định)
        print("Lỗikhi tạo HWID")
        # Đây là lỗi chỉ xảy ra khi os.stat và uuid.getnode() đều lỗi
        return hashlib.sha256("FINAL_STATIC_FALLBACK_HWID_V11".encode()).hexdigest()
# Hàm Lấy IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "IP_FETCH_FAIL"
    except Exception:
        return "IP_FETCH_ERROR"

# Khai báo các biến toàn cục (HWID KHÔNG IN RA)
GLOBAL_HWID = get_stable_hwid()
GLOBAL_IP = get_public_ip()

# Hàm in thông tin key sau khi xác minh thành công
# =========================================================================
# 💡 HÀM MỚI ĐÃ CHUYỂN ĐỔI NGÀY HẾT HẠN SANG GIỜ VIỆT NAM (GMT+7)
#    VÀ THAY ĐỔI MÀU HIỂN THỊ THÀNH MÀU VÀNG
# =========================================================================
def print_license_info(key, user_name, expiry_date_iso, ip):
    
    # Định nghĩa múi giờ Việt Nam
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    
    try:
        dt_utc = datetime.strptime(expiry_date_iso.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        dt_utc = pytz.utc.localize(dt_utc)
        dt_vn = dt_utc.astimezone(vn_tz)
        expiry_display = dt_vn.strftime('%d/%m/%Y %H:%M:%S')
        
    except Exception:
        expiry_display = expiry_date_iso 
        ui_print(f"Lỗi chuyển đổi múi giờ. Hiển thị chuỗi thô.", style='warn', prefix='⚠️ ')
        
    # ---------- THAY ĐỔI MÀU Ở ĐÂY (Sử dụng hàm prints trực tiếp) ----------
    TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B = 255, 255, 0 # Màu Vàng
    
    # Hàm in thông tin key
    prints(255, 255, 255, "═" * 64)
    prints(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B, f"🔑 Key: {key}")
    prints(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B, f"👤 Owner: {user_name}")
    prints(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B, f"⏳ Hạn dùng: {expiry_display} (VN Time)")
    prints(TEXT_COLOR_R, TEXT_COLOR_G, TEXT_COLOR_B, f"🌍 IP máy: {ip}")
    prints(255, 255, 255, "═" * 64)

# =========================================================================
# =========================================================================
# 💡 PHẦN CODE KIỂM TRA BẢN QUYỀN (LICENSE/HWID/IP) - KẾT THÚC
# =========================================================================

def facebook_info(cookie: str, timeout: int = 15):
    try:
        session = requests.Session()
        session_id = str(uuid.uuid4())
        fb_dtsg = ""
        jazoest = ""
        lsd = ""
        name = ""
        user_id = cookie.split("c_user=")[1].split(";")[0]

        headers = {
            "authority": "www.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "vi",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/106.0.0.0 Safari/537.36",
            "viewport-width": "1366",
            "Cookie": cookie
        }

        url = session.get(f"https://www.facebook.com/{user_id}", headers=headers, timeout=timeout).url
        response = session.get(url, headers=headers, timeout=timeout).text

        fb_token = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
        if fb_token:
            fb_dtsg = fb_token[0]

        jazo = re.findall(r'jazoest=(.*?)\"', response)
        if jazo:
            jazoest = jazo[0]

        lsd_match = re.findall(r'"LSD",\[\],\{"token":"(.*?)"\}', response)
        if lsd_match:
            lsd = lsd_match[0]

        get = session.get("https://www.facebook.com/me", headers=headers, timeout=timeout).url
        url = "https://www.facebook.com/" + get.split("%2F")[-2] + "/" if "next=" in get else get
        response = session.get(url, headers=headers, params={"locale": "vi_VN"}, timeout=timeout)

        data_split = response.text.split('"CurrentUserInitialData",[],{')
        json_data_raw = "{" + data_split[1].split("},")[0] + "}"
        parsed_data = json.loads(json_data_raw)

        user_id = parsed_data.get("USER_ID", "0")
        name = parsed_data.get("NAME", "")

        if user_id == "0" and name == "":
            print("[!] Cookie is invalid or expired.")
            return {'success': False}
        elif "828281030927956" in response.text:
            print("[!] Account is under a 956 checkpoint.")
            return {'success': False}
        elif "1501092823525282" in response.text:
            print("[!] Account is under a 282 checkpoint.")
            return {'success': False}
        elif "601051028565049" in response.text:
            print("[!] Account action is blocked (spam).")
            return {'success': False}

        json_data = {
            'success': True,
            'user_id': user_id,
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'lsd': lsd,
            'name': name,
            'session': session,
            'session_id': session_id,
            'cookie': cookie,
            'headers': headers
        }
        return json_data

    except Exception as e:
        print(f"[Facebook.info] Error: {e}")
        return {'success': False}

def get_post_id(session,cookie,link):
    prints(255,255,0,f'Đang lấy post id',end='\r')
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'dpr': '1',
        'priority': 'u=0, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'cookie': cookie,
    }
    try:
        response = session.get(link, headers=headers, timeout=15).text
        response= re.sub(r"\\", "", response)
        
        page_id=''
        post_id=''
        stories_id=''
        permalink_id=''
        try:
            if '"post_id":"' in str(response):
                permalink_id=re.findall('"post_id":".*?"',response)[0].split(':"')[1].split('"')[0]
                prints(255,255,0,f'permalink_id là: {permalink_id[:20]}      ',end='\r')
        except:
            pass
        try:
            if 'posts' in str(response):
                post_id=response.split('posts')[1].split('"')[0]
                post_id=post_id.replace("/", "")
                post_id = re.sub(r"\\", "", post_id)
                prints(255,255,0,f'Post id là: {post_id[:20]}       ',end='\r')
        except:
            pass
        try:
            if 'storiesTrayType' in response and not '"profile_type_name_for_content":"PAGE"' in response:
                stories_id=re.findall('"card_id":".*?"',response)[0].split('":"')[1].split('"')[0]
                prints(255,255,0,f'stories_id là: {stories_id[:20]}      ',end='\r')
        except:
            pass
        try:
            if '"page_id"' in response:
                page_id=re.findall('"page_id":".*?"',response)[0].split('id":"')[1].split('"')[0]
                prints(255,255,0,f'page_id là: {page_id[:20]}        ',end='\r')
        except:
            pass
        return {'success':True,'post_id':post_id,'permalink_id':permalink_id,'stories_id':stories_id,'page_id':page_id}
    except Exception as e:
        print(Fore.RED+f'Lỗi khi lấy ID post: {e}')
        return {'success':False}

def react_post_perm(data,object_id,type_react):
    prints(255,255,0,f'Đang thả {type_react} vào {object_id[:20]}       ',end='\r')

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/'+str(object_id),
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie'],
    }
    react_list = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
    
    json_data = {
        'av': str(data['user_id']),
        '__user': str(data['user_id']),
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': str(data['jazoest']),
        'lsd': str(data['lsd']),
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
        'variables': '{"input":{"attribution_id_v2":"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,'+str(int(time.time()*1000))+',893597,,,","feedback_id":"'+encode_to_base64(str('feedback:'+object_id))+'","feedback_reaction_id":"'+str(react_list.get(type_react.upper()))+'","feedback_source":"OBJECT","is_tracking_encrypted":true,"tracking":["AZWEqXNx7ELYfHNA7b4CrfdPexzmIf2rUloFtOZ9zOxrcEuXq9Nr8cAdc1kP5DWdKx-DdpkffT5hoGfKYfh0Jm8VlJztxP7elRZBQe5FqkP58YxifFUwdqGzQnJPfhGupHYBjoq5I5zRHXPrEeuJk6lZPblpsrYQTO1aDBDb8UcDpW8F82ROTRSaXpL-T0gnE3GyKCzqqN0x99CSBp1lCZQj8291oXhMoeESvV__sBVqPWiELtFIWvZFioWhqpoAe_Em15uPs4EZgWgQmQ-LfgOMAOUG0TOb6wDVO75_PyQ4b8uTdDWVSEbMPTCglXWn5PJzqqN4iQzyEKVe8sk708ldiDug7SlNS7Bx0LknC7p_ihIfVQqWLQpLYK6h4JWZle-ugySqzonCzb6ay09yrsvupxPUGp-EDKhjyEURONdtNuP-Fl3Oi1emIy61-rqISLQc-jp3vzvnIIk7r_oA1MKT065zyX-syapAs-4xnA_12Un5wQAgwu5sP9UmJ8ycf4h1xBPGDmC4ZkaMWR_moqpx1k2Wy4IbdcHNMvGbkkqu12sgHWWznxVfZzrzonXKLPBVW9Y3tlQImU9KBheHGL_ADG_8D-zj2S9JG2y7OnxiZNVAUb1yGrVVrJFnsWNPISRJJMZEKiYXgTaHVbZBX6CdCrA7gO25-fFBvVfxp2Do3M_YKDc5Ttq1BeiZgPCKogeTkSQt1B67Kq7FTpBYJ05uEWLpHpk1jYLH8ppQQpSEasmmKKYj9dg7PqbHPMUkeyBtL69_HkdxtVhDgkNzh1JerLPokIkdGkUv0RALcahWQK4nR8RRU2IAFMQEp-FsNk_VKs_mTnZQmlmSnzPDymkbGLc0S1hIlm9FdBTQ59--zU4cJdOGnECzfZq4B5YKxqxs0ijrcY6T-AOn4_UuwioY"],"session_id":"'+data['session_id']+'","actor_id":"'+str(data['user_id'])+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '24034997962776771',
    }
    try:
        response = data['session'].post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, timeout=15).text
        return True
    except Exception:
        return False

def react_post_defaul(data,object_id,type_react):
    prints(255,255,0,f'Đang thả {type_react} vào {object_id[:20]}       ',end='\r')

    react_list = {"LIKE": "1635855486666999","LOVE": "1678524932434102","CARE": "613557422527858","HAHA": "115940658764963","WOW": "478547315650144","SAD": "908563459236466","ANGRY": "444813342392137"}
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/'+str(object_id),
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'CometUFIFeedbackReactMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie'],
    }
    
    json_data = {
        'av': str(data['user_id']),
        '__user': str(data['user_id']),
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': data['jazoest'],
        'lsd': data['lsd'],
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
        'variables': '{"input":{"attribution_id_v2":"CometSinglePostDialogRoot.react,comet.post.single_dialog,via_cold_start,'+str(int(time.time()*1000))+',912367,,,","feedback_id":"'+encode_to_base64(str('feedback:'+object_id))+'","feedback_reaction_id":"'+str(react_list.get(type_react.upper()))+'","feedback_source":"OBJECT","is_tracking_encrypted":true,"tracking":["AZWEqXNx7ELYfHNA7b4CrfdPexzmIf2rUloFtOZ9zOxrcEuXq9Nr8cAdc1kP5DWdKx-DdpkffT5hoGfKYfh0Jm8VlJztxP7elRZBQe5FqkP58YxifFUwdqGzQnJPfhGupHYBjoq5I5zRHXPrEeuJk6lZPblpsrYQTO1aDBDb8UcDpW8F82ROTRSaXpL-T0gnE3GyKCzqqN0x99CSBp1lCZQj8291oXhMoeESvV__sBVqPWiELtFIWvZFioWhqpoAe_Em15uPs4EZgWgQmQ-LfgOMAOUG0TOb6wDVO75_PyQ4b8uTdDWVSEbMPTCglXWn5PJzqqN4iQzyEKVe8sk708ldiDug7SlNS7Bx0LknC7p_ihIfVQqWLQpLYK6h4JWZle-ugySqzonCzb6ay09yrsvupxPUGp-EDKhjyEURONdtNuP-Fl3Oi1emIy61-rqISLQc-jp3vzvnIIk7r_oA1MKT065zyX-syapAs-4xnA_12Un5wQAgwu5sP9UmJ8ycf4h1xBPGDmC4ZkaMWR_moqpx1k2Wy4IbdcHNMvGbkkqu12sgHWWznxVfZzrzonXKLPBVW9Y3tlQImU9KBheHGL_ADG_8D-zj2S9JG2y7OnxiZNVAUb1yGrVVrJFnsWNPISRJJMZEKiYXgTaHVbZBX6CdCrA7gO25-fFBvVfxp2Do3M_YKDc5Ttq1BeiZgPCKogeTkSQt1B67Kq7FTpBYJ05uEWLpHpk1jYLH8ppQQpSEasmmKKYj9dg7PqbHPMUkeyBtL69_HkdxtVhDgkNzh1JerLPokIkdGkUv0RALcahWQK4nR8RRU2IAFMQEp-FsNk_VKs_mTnZQmlmSnzPDymkbGLc0S1hIlm9FdBTQ59--zU4cJdOGnECzfZq4B5YKxqxs0ijrcY6T-AOn4_UuwioY"],"session_id":"'+str(data['session_id'])+'","actor_id":"'+data['user_id']+'","client_mutation_id":"1"},"useDefaultActor":false,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '24034997962776771',
    }
    try:
        response = data['session'].post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, timeout=15)
        response.raise_for_status()
        return True
    except:
        return False

def react_stories(data,object_id):
    prints(255,255,0,f'Đang tim story {object_id[:20]}      ',end='\r')

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'useStoriesSendReplyMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie']
    }

    json_data = {
        'av': str(data['user_id']),
        '__user': str(data['user_id']),
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': str(data['jazoest']),
        'lsd': data['lsd'],
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useStoriesSendReplyMutation',
        'variables': '{"input":{"attribution_id_v2":"StoriesCometSuspenseRoot.react,comet.stories.viewer,via_cold_start,'+str(int(time.time()*1000))+',33592,,,","lightweight_reaction_actions":{"offsets":[0],"reaction":"❤️"},"message":"❤️","story_id":"'+str(object_id)+'","story_reply_type":"LIGHT_WEIGHT","actor_id":"'+str(data['user_id'])+'","client_mutation_id":"2"}}',
        'server_timestamps': 'true',
        'doc_id': '9697491553691692',
    }
    try:
        response = data['session'].post('https://www.facebook.com/api/graphql/',  headers=headers, data=json_data, timeout=15).json()
        if response.get('extensions', {}).get('is_final') == True:
            return True
        else:
            return False
    except Exception:
        return False

def react_post(data,link,type_react):
    res_object_id=get_post_id(data['session'],data['cookie'],link)
    if not res_object_id.get('success'):
        return False
        
    if res_object_id.get('stories_id'):
        return react_stories(data,res_object_id['stories_id'])
    elif res_object_id.get('permalink_id'):
        return react_post_perm(data,res_object_id['permalink_id'],type_react)
    elif res_object_id.get('post_id'):
        return react_post_defaul(data,res_object_id['post_id'],type_react)
    return False

def comment_fb(data,object_id,msg):
    prints(255,255,0,f'Đang comment vào {object_id[:20]}        ',end='\r')

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'useCometUFICreateCommentMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie'],
    }

    json_data = {
        'av': data['user_id'],
        '__user': str(data['user_id']),
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': data['jazoest'],
        'lsd': data['lsd'],
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useCometUFICreateCommentMutation',
        'variables': '{"feedLocation":"DEDICATED_COMMENTING_SURFACE","feedbackSource":110,"groupID":null,"input":{"client_mutation_id":"4","actor_id":"'+str(data['user_id'])+'","attachments":null,"feedback_id":"'+str(encode_to_base64('feedback:'+str(object_id)))+'","formatting_style":null,"message":{"ranges":[],"text":"'+msg+'"},"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,'+str(int(time.time()*1000))+',521928,4748854339,,","is_tracking_encrypted":true,"tracking":["AZX3K9tlBCG5xFInZx-hvHkdaGUGeTF2WOy5smtuctk2uhOd_YMY0HaF_dyAE8WU5PjpyFvAAM8x4Va39jb7YmcxubK8j4k8_16X1jtlc_TqtbWFukq-FUR93cTOBLEldliV6RILPNqYHH_a88DnwflDtg8NvluALzkLO-h8N8cxTQoSUQDPh206jaottUIfOxdZheWcqroL_1IaoZq9QuhwAUY4qu551-q7loObYLWHMcqA7XZFpDm6SPQ8Ne86YC3-sDPo093bfUGHae70FqOts742gWgnFy_t4t7TgRTmv1zsx0CXPdEh-xUx3bXPC6NEutzyNyku7Kdqgg1qTSabXknlJ7KZ_u9brQtmzs7BE_x4HOEwSBuo07hcm-UdqjaujBd2cPwf-Via-oMAsCsTywY-riGnW49EJhhycbj4HvshcHRDqk4iUTOaULV2CAOL7nGo5ACkUMoKbuWFl34uLoHhFJnpWaxPUef3ceL0ed19EChlYsnFl122VMJzRf6ymNtBQKbSfLkDF_1QYIofGvcRktaZOrrhnHdwihCPjBbHm17a3Cc3ax2KNJ6ViUjdj--KFE704jEjkJ9RXdZw3UIO-JjkvbCCeJ3Y-viGeank-vputYKtK1L05t2q5_6ool7PCIOufjNUrACbyeuOiLTyicyVvT013_jbYefSkhJ55PAtIqKn3JVbUpEWBYTWO8mkbU_UyjOnnhCZcagjWXYHKQ_Ne2gfLZN_WrpbEcLKdOtEm-l8J1RdnvYSTc13XVd85eL-k3da2OTamH7cJ_7bS6eJhQ0oSsrlGSJahq_JT9TV5IOffVeZWJ_SpcBwdPvzCRlMJIRljjSmgrCtfJrak8OgGtZM6jIZp6iZluUDlPEv1c_apazECx9CPC3pM1iu4QVdSdEzyBXbhul5hMDkSon4ahxJbWQ5ALpj-QAjfiCyz-aM0L5BqZLRug8_MdPk_ZWO3e70OX2LGHWKsd0ZGWP5kzpMqSMnkgTN5fGQ4A1QJ6EdEisqjclnSrD258ghVgKVEK9_PcIpGmmseB7fzrL1c5R65D4UZQq-kEpsuM42EhkAgfEEzrCTosmpRd7xibmd6aoVsOqCvJrvy_83bLE3-YTkhotHJeQxuLPWF1uvDSkhc_cs3ApJ1xFxHDZc5dikuMXne1azhKp5","{\\"assistant_caller\\":\\"comet_above_composer\\",\\"conversation_guide_session_id\\":\\"'+data['session_id']+'\\",\\"conversation_guide_shown\\":null}"],"feedback_source":"DEDICATED_COMMENTING_SURFACE","idempotence_token":"client:'+str(uuid.uuid4())+'","session_id":"'+data['session_id']+'"},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"focusCommentID":null,"__relay_internal__pv__CometUFICommentAvatarStickerAnimatedImagerelayprovider":false,"__relay_internal__pv__IsWorkUserrelayprovider":false}',
        'server_timestamps': 'true',
        'doc_id': '9379407235517228',
    }
    try:
        response = data['session'].post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, timeout=15).json()
        comment_text = response['data']['comment_create']['feedback_comment_edge']['node']['preferred_body']['text']
        prints(5,255,0,f'Đã comment "{comment_text}"',end='\r')
        if comment_text == msg:
            return True
        return False
    except Exception as e:
        prints(255,0,0,f"Lỗi khi comment: {e}")
        return False

def dexuat_fb(data,object_id,msg):
    prints(255,255,0,f'Đang đề xuất Fanpage {object_id[:20]}        ',end='\r')
    if len(msg)<=25:
        msg+=' '*(26-len(msg))

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': 'https://www.facebook.com/'+object_id,
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'ComposerStoryCreateMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie']
    }

    json_data = {
        'av': str(data['user_id']),
        '__user': str(data['user_id']),
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': data['jazoest'],
        'lsd': data['lsd'],
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'ComposerStoryCreateMutation',
        'variables': '{"input":{"composer_entry_point":"inline_composer","composer_source_surface":"page_recommendation_tab","idempotence_token":"'+str(uuid.uuid4()) + "_FEED"+'","source":"WWW","audience":{"privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"}},"message":{"ranges":[],"text":"'+str(msg)+'"},"page_recommendation":{"page_id":"'+str(object_id)+'","rec_type":"POSITIVE"},"logging":{"composer_session_id":"'+data['session_id']+'"},"navigation_data":{"attribution_id_v2":"ProfileCometReviewsTabRoot.react,comet.profile.reviews,unexpected,'+str(int(time.time()*1000))+','+str(random.randint(111111,999999))+',250100865708545,,;ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,'+str(int(time.time()*1000))+','+str(random.randint(111111,999999))+',250100865708545,,"},"tracking":[null],"event_share_metadata":{"surface":"newsfeed"},"actor_id":"'+str(data['user_id'])+'","client_mutation_id":"1"},"feedLocation":"PAGE_SURFACE_RECOMMENDATIONS","feedbackSource":0,"focusCommentID":null,"scale":1,"renderLocation":"timeline","useDefaultActor":false,"isTimeline":true,"isProfileReviews":true,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":true}',
        'server_timestamps': 'true',
        'doc_id': '24952395477729516',
    }
    try:
        response_json = data['session'].post('https://www.facebook.com/api/graphql/', headers=headers, data=json_data, timeout=15).json()
        
        post_id = response_json['data']['story_create']['profile_review_edge']['node']['post_id']
        my_id = response_json['data']['story_create']['profile_review_edge']['node']['feedback']['owning_profile']['id']
        link_post = f'https://www.facebook.com/{my_id}/posts/{post_id}'
        
        link_p=get_lin_share(data,link_post)
        return link_p
    except Exception as e:
        prints(5,255,0,f'Lỗi khi đánh giá Fanpage: {e}')
        return False

def wallet(authorization):
    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    try:
        response = requests.get('https://api-v2.bumx.vn/api/business/wallet', headers=headers, timeout=10).json()
        return response.get('data', {}).get('balance', 'N/A')
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except json.JSONDecodeError:
        return "Error decoding server response"

def load(session,authorization,job):
    prints(255,255,0,f'Đang mở nhiệm vụ...',end='\r')

    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }

    json_data = {'buff_id': job['buff_id']}
    try:
        response = session.post('https://api-v2.bumx.vn/api/buff/load-mission', headers=headers, json=json_data, timeout=10).json()
        return response
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        prints(255,0,0,f'Lỗi khi tải thông tin NV')
        return None

def get_job(session,authorization):
    prints(255,255,0,f'Đang lấy nhiệm vụ...',end='\r')
    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    params = {'is_from_mobile': 'true'}
    
    try:
        response = session.get('https://api-v2.bumx.vn/api/buff/mission', params=params, headers=headers, timeout=10)
        response.raise_for_status()
        response_json = response.json()
    except requests.exceptions.RequestException:
        prints(255,0,0,f'Lỗi khi lấy NV')
        return []
    except json.JSONDecodeError:
        prints(255,0,0,f'Lỗi giải mã JSON khi lấy NV.')
        return []

    prints(Fore.LIGHTWHITE_EX+f"Đã tìm thấy {response_json.get('count', 0)} NV",end='\r')
    
    JOB=[]
    for i in response_json.get('data', []):
        json_job={
            "_id":i['_id'],
            "buff_id":i['buff_id'],
            "type":i['type'],
            "name":i['name'],
            "status":i['status'],
            "object_id":i['object_id'],
            "business_id":i['business_id'],
            "mission_id":i['mission_id'],
            "create_date":i['create_date'],
            "note":i['note'],
            "require":i['require'],
        }
        JOB.insert(0,json_job)
    return JOB

def reload(session, authorization, type_job, retries=3):
    prints(255, 255, 0, f'Đang nhấn tải danh sách nhiệm vụ...', end='\r')
    if retries == 0:
        prints(255, 0, 0, 'Tải danh sách nhiệm vụ thất bại. Bỏ qua chu kỳ này.')
        return

    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    json_data = {'type': type_job}
    try:
        response = session.post('https://api-v2.bumx.vn/api/buff/get-new-mission', headers=headers, json=json_data, timeout=10).json()
    except Exception:
        prints(255, 0, 0, f'Lỗi khi tải lại NV. Thử lại trong 2s...')
        time.sleep(2)
        return reload(session, authorization, type_job, retries - 1)

def submit(session,authorization,job,reslamjob,res_load):
    prints(255,255,0,f'Đang nhấn hoàn thành nhiệm vụ',end='\r')
    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    json_data = {
        'buff_id': job['buff_id'],
        'comment': None, 'comment_id': None, 'code_submit': None,
        'attachments': [], 'link_share': '', 'code': '',
        'is_from_mobile': True, 'type': job['type'], 'sub_id': None, 'data': None,
    }

    if job['type']=='like_facebook':
        json_data['comment'] = 'tt nha'
    elif job['type']=='like_poster':
        json_data['comment'] = res_load.get('data')
        json_data['comment_id'] = res_load.get('comment_id')
    elif job['type']=='review_facebook':
        json_data['comment'] = 'Helo Bạn chúc Bạn sức khỏe '
        json_data['link_share'] = reslamjob
    
    try:
        response = session.post('https://api-v2.bumx.vn/api/buff/submit-mission', headers=headers, json=json_data, timeout=10).json()
        if response.get('success') == True:
            message = response.get('message', '')
            _xu = '0'
            sonvdalam = '0'
            try:
                _xu = message.split('cộng ')[1].split(',')[0]
                sonvdalam = message.split('làm: ')[1]
            except IndexError:
                pass
            return [True,_xu,sonvdalam]
        return [False,'0','0']
    except Exception:
        prints(255,0,0,f'Lỗi khi submit')
        return [False,'0','0']
    
def report(session, authorization, job, retries=3):
    prints(255, 255, 0, f'Đang báo lỗi...', end='\r')
    if retries == 0:
        prints(255, 0, 0, f'Báo lỗi thất bại sau nhiều lần thử. Bỏ qua...')
        return

    headers = {
        'User-Agent': 'Dart/3.3 (dart:io)',
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    json_data = {'buff_id': job['buff_id']}
    try:
        response = session.post('https://api-v2.bumx.vn/api/buff/report-buff', headers=headers, json=json_data, timeout=10).json()
        prints(255, 165, 0, 'Đã báo lỗi thành công và bỏ qua NV.')
    except Exception:
        prints(255, 165, 0, f'Báo lỗi không thành công, thử lại... ({retries-1} lần còn lại)')
        time.sleep(2)
        return report(session, authorization, job, retries - 1)

def lam_job(data,jobs,type_job_doing):
    prints(255,255,0,f'Đang làm NV...',end='\r')

    link='https://www.facebook.com/'+jobs['object_id']
    if type_job_doing=='review_facebook':
        res_get_post_id=get_post_id(data['session'],data['cookie'],link)
        if res_get_post_id.get('page_id'):
            return dexuat_fb(data,res_get_post_id['page_id'],jobs['data'])
    elif type_job_doing=='like_facebook':
        react_type = 'LIKE'
        icon = jobs.get('icon', '').lower()
        if 'love' in icon or 'thuongthuong' in icon: react_type='LOVE'
        elif 'care' in icon: react_type='CARE'
        elif 'wow' in icon: react_type='WOW'
        elif 'sad' in icon: react_type='SAD'
        elif 'angry' in icon: react_type='ANGRY'
        elif 'haha' in icon: react_type='HAHA'
        return react_post(data,link,react_type.upper())
    elif type_job_doing=='like_poster':
        res_get_post_id=get_post_id(data['session'],data['cookie'],link)
        post_id_to_comment = res_get_post_id.get('post_id') or res_get_post_id.get('permalink_id')
        if post_id_to_comment:
            return comment_fb(data,post_id_to_comment,jobs['data'])
    return False
        
def countdown(seconds):
    seconds = int(seconds)
    if seconds < 1: return
    for i in range(seconds, 0, -1):
        prints(147, 112, 219, '[', end='')
        prints(0, 255, 127, "NGUYEN", end='')
        prints(147, 112, 219, ']', end='')
        prints(255, 255, 255, '[', end='')
        prints(255, 215, 0, "WAIT", end='')
        prints(255, 255, 255, ']', end='')
        prints(255, 20, 147, ' ➤ ', end='')
        prints(0, 191, 255, f"⏳ {i}s...", end='\r')
        time.sleep(1)
    print(' ' * 50, end='\r')

def get_lin_share(data,link):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'priority': 'u=1, i',
        'referer': link,
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-fb-friendly-name': 'useLinkSharingCreateWrappedUrlMutation',
        'x-fb-lsd': data['lsd'],
        'cookie': data['cookie'],
    }

    payload = {
        'av': data['user_id'],
        '__user': data['user_id'],
        'fb_dtsg': data['fb_dtsg'],
        'jazoest': data['jazoest'],
        'lsd': data['lsd'],
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useLinkSharingCreateWrappedUrlMutation',
        'variables': '{"input":{"client_mutation_id":"3","actor_id":"'+str(data['user_id'])+'","original_content_url":"'+link+'","product_type":"UNKNOWN_FROM_DEEP_LINK"}}',
        'server_timestamps': 'true',
        'doc_id': '30568280579452205',
    }
    try:
        response = requests.post('https://www.facebook.com/api/graphql/',  headers=headers, data=payload, timeout=15).json()
        return response['data']['xfb_create_share_url_wrapper']['share_url_wrapper']['wrapped_url']
    except Exception as e:
        prints(255,0,0,f'Lỗi khi lấy link share của post: {e}')
        return ''

def add_account_fb(session,authorization,user_id):
    headers = {
        'Content-Type': 'application/json',
        'lang': 'en',
        'version': '37',
        'origin': 'app',
        'authorization': authorization,
    }
    json_data = {'link': f'https://www.facebook.com/profile.php?id={str(user_id)}'}
    try:
        response = session.post('https://api-v2.bumx.vn/api/account-facebook/connect-link', headers=headers, json=json_data, timeout=10).json()
        prints(255,255,0,f"Khai báo tài khoản FB: {response.get('message', 'No message')}")
    except Exception as e:
        prints(255,0,0,f"Lỗi khai báo tài khoản FB: {e}")

# --- PHẦN DASHBOARD MỚI (VIP PRO + FIX LỆCH) ---
job_dashboard_store = {}
job_type_counts = {}

def update_and_print_dashboard(status_job, _xu, jobdalam, dahoanthanh, tongcanhoanthanh, type_job, name_acc, balance, list_type_job):
    # 1. Cập nhật dữ liệu
    hanoi_tz = timezone(timedelta(hours=7))
    now = datetime.now(hanoi_tz).strftime("%H:%M:%S")
    
    if type_job and type_job not in job_dashboard_store:
        job_dashboard_store[type_job] = "---"
    
    if _xu != '0':
        job_dashboard_store[type_job] = f"+{_xu.strip()} xu"
        job_type_counts[type_job] = job_type_counts.get(type_job, 0) + 1

    clear_screen()
    banner()

    header_info = [
        rgb(0, 255, 255, "👤 TÀI KHOẢN"), 
        rgb(255, 215, 0, "🕒 THỜI GIAN"), 
        rgb(0, 255, 127, "💰 SỐ DƯ"), 
        rgb(255, 0, 255, "✅ TIẾN ĐỘ")
    ]
    
    row_info = [
        rgb(255, 255, 255, name_acc),
        rgb(255, 255, 255, now),
        rgb(255, 255, 0, f"{balance} xu"),
        rgb(173, 255, 47, f"{dahoanthanh} / {tongcanhoanthanh}")
    ]

  
    table_1 = tabulate([row_info], headers=header_info, tablefmt="fancy_grid", colalign=("center", "center", "center", "center"))
    
    table_1 = table_1.replace("│", " ").replace("╤", "─").replace("╧", "─").replace("┼", "─")
    print(table_1)
    
    type_NV = {
        'like_facebook': (0, 191, 255, '💖 CẢM XÚC'),
        'like_poster': (0, 250, 154, '💬 COMMENT'),
        'review_facebook': (255, 105, 180, '⭐ FANPAGE')
    }
    
    sorted_jobs = [t for t in ['like_facebook', 'like_poster', 'review_facebook'] if t in list_type_job]
    
    job_headers = []
    row_rewards = []
    row_counts = []
    
    for t in sorted_jobs:
        r, g, b, label = type_NV.get(t, (255, 255, 255, t))
        job_headers.append(rgb(r, g, b, label))
        val = job_dashboard_store.get(t, "---")
        row_rewards.append(rgb(255, 255, 0, val))
        count = job_type_counts.get(t, 0)
        row_counts.append(rgb(0, 255, 255, f"Job: {count}"))
        
    if job_headers:

        table_2 = tabulate([row_rewards, row_counts], headers=job_headers, tablefmt="fancy_grid", colalign=("center",)*len(job_headers))

        table_2 = table_2.replace("│", " ").replace("╤", "─").replace("╧", "─").replace("┼", "─").replace("╪", "─")
        print(table_2)


def switch_facebook_account(cookie, authorization):
    prints(0, 255, 255, "\n--- Chuyển đổi tài khoản Facebook ---")
    data = facebook_info(cookie)
    if not data or not data.get('success'):
        prints(255, 0, 0, 'Cookie không hợp lệ. Bỏ qua tài khoản này.')
        return None
    
    prints(5, 255, 0, f"Đang sử dụng tài khoản: {data['name']} ({data['user_id']})")
    add_account_fb(data['session'], authorization, data['user_id'])
    return data


def main_bumx_free():
    clear_screen()
    banner() 
    
    # Bỏ qua in IP tại đây, chuyển sang in sau khi Key hợp lệ

    # =========================================================================
    # 💡 LOGIC KIỂM TRA KEY & BIND HWID - VỊ TRÍ MỚI
    # =========================================================================
    
    license_info = get_saved_license()
    current_key = license_info.get('key') 
    
    # Kết quả Key hợp lệ được lưu vào đây để in ra sau vòng lặp
    final_api_res = None
    
    # Bắt đầu vòng lặp kiểm tra key
    while True:
        # A. KIỂM TRA KEY ĐÃ LƯU
        if current_key:
            ui_status(f"Đang kiểm tra key đã lưu: {current_key}...")
            api_res = check_license_key_api(current_key, GLOBAL_HWID, GLOBAL_IP) 
            
            if api_res.get("valid"):
                ui_print(f"✅ Key hợp lệ. Bắt đầu chạy tool...", style='success')
                save_license(current_key) 
                final_api_res = api_res
                break # <--- THOÁT KHỎI VÒNG LẶP NẾU KEY HỢP LỆ
            else:
                ui_print(f"❌ Key {current_key} không hợp lệ. {api_res.get('message', '')}", style='error')
                current_key = None 
        
        # B. YÊU CẦU NHẬP KEY MỚI
        if not current_key:
            new_key = ui_input("Nhập Key đã mua: ").strip()
            if not new_key:
                ui_print("Key không được để trống.", style='error')
                time.sleep(1)
                continue
                
            ui_status(f"Đang kiểm tra Key mới: {new_key}...")
            api_res = check_license_key_api(new_key, GLOBAL_HWID, GLOBAL_IP)

            if api_res.get("valid"):
                current_key = new_key
                ui_print(f"✅ Key hợp lệ. Bắt đầu chạy tool...", style='success')
                save_license(current_key) 
                final_api_res = api_res
                break # <--- THOÁT KHỎI VÒNG LẶP NẾU KEY HỢP LỆ
            else:
                ui_print(f"❌ Key {new_key} không hợp lệ hoặc đã hết hạn. {api_res.get('message', '')}", style='error')
                time.sleep(2)
                
    # =========================================================================
    # 💡 KẾT THÚC LOGIC KIỂM TRA KEY
    # =========================================================================
    
    # -------------------------------------------------------------------------
    # 🔑 IN THÔNG TIN KEY RA MÀN HÌNH SAU KHI XÁC MINH THÀNH CÔNG
    # -------------------------------------------------------------------------
    if final_api_res:
        prints(255, 255, 255, "\n")
        print_license_info(
            key=current_key,
            user_name=final_api_res.get('user_name', 'Chưa rõ'),
            expiry_date_iso=final_api_res['expiry_date'],
            ip=GLOBAL_IP
        )
        prints(255, 255, 255, "\n")
    
    
    # -------------------------------------------------------------------------
    # ⬅️ TOÀN BỘ CODE CHẠY TOOL BUMX CỦA BẠN BẮT ĐẦU TỪ ĐÂY (VỊ TRÍ CŨ)
    # -------------------------------------------------------------------------
    
    if os.path.exists('kng-auth.txt'):
        x = ui_input('Bạn có muốn dùng lại authorization Bumx đã lưu không (y/n):').lower()
        if x=='y':
            with open('kng-auth.txt','r',encoding='utf-8') as f:
                authorization=f.read().strip()
        else:
            authorization = ui_input('Nhập authorization BUMX của bạn:').strip()
            with open('kng-auth.txt','w',encoding='utf-8') as f: f.write(authorization)
            ui_print('Đã lưu authorization vào kng-auth.txt', style='success')
    else:
        authorization = ui_input('Nhập authorization BUMX của bạn:').strip()
        with open('kng-auth.txt','w',encoding='utf-8') as f: f.write(authorization)
        ui_print('Đã lưu authorization vào kng-auth.txt', style='success')
    
    # Giữ nguyên code Tool của bạn
    ui_print(f'Số dư: {wallet(authorization)}', style='accent')

    num_cookies = int(ui_input('Nhập số lượng cookie Facebook muốn chạy:'))
    cookies_list = []
    # ... (phần còn lại của code Tool) ...
    
    for i in range(num_cookies):
        cookie_file = f'kng-cookie-{i+1}.txt'
        cookie = ''
        if os.path.exists(cookie_file):
            x = input(Fore.LIGHTCYAN_EX + f'Bạn có muốn dùng lại cookie FB đã lưu trong file {cookie_file} không (y/n): ').lower()
            if x == 'y':
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    cookie = f.read().strip()
            else:
                cookie = ui_input(f'Nhập cookie FB thứ {i+1} của bạn:').strip()
                with open(cookie_file, 'w', encoding='utf-8') as f:
                    f.write(cookie)
                prints(5, 255, 0, f'Đã lưu cookie vào {cookie_file}')
        else:
            cookie = ui_input(f'Nhập cookie FB thứ {i+1} của bạn:').strip()
            with open(cookie_file, 'w', encoding='utf-8') as f:
                f.write(cookie)
            prints(5, 255, 0, f'Đã lưu cookie vào {cookie_file}')
        if cookie:
            cookies_list.append(cookie)

    if not cookies_list:
        ui_print('Không có cookie nào được nhập. Dừng tool.', style='error')
        sys.exit(1)

    switch_threshold = int(ui_input('Sau bao nhiêu nhiệm vụ thì đổi cookie FB:'))

    list_type_job=[]
    prints(66, 245, 245, '''
Các loại nhiệm vụ:
 1. Thả cảm xúc
 2. Comment
 3. Đánh giá Fanpage
Nhập STT các loại NV cần làm (ví dụ: 12 để làm cảm xúc và comment): ''',end='')
    
    x=input()
    job_map = {'1': 'like_facebook', '2': 'like_poster', '3': 'review_facebook'}
    for i in x:
        job_type = job_map.get(i)
        if job_type:
            list_type_job.append(job_type)
        else:
            prints(255,0,0,f'Lựa chọn "{i}" không hợp lệ. Vui lòng chạy lại tool và nhập lại!')
            sys.exit(1)

    SO_NV = int(ui_input('Làm bao nhiêu NV thì dừng:'))
    SO_NV1=SO_NV
    demht=0
    demsk=0
    
    delay1 = int(ui_input('Nhập delay tối thiểu khi làm job (giây):'))
    delay2 = int(ui_input('Nhập delay tối đa khi làm job (giây):'))

    current_cookie_index = 0
    tasks_on_current_cookie = 0
    valid_cookies = []
    
    for ck in cookies_list:
        info = facebook_info(ck)
        if info and info.get('success'):
            valid_cookies.append(ck)
        else:
            prints(255, 165, 0, f"Cookie ...{ck[-20:]} không hợp lệ, sẽ được bỏ qua.")
    
    if not valid_cookies:
        prints(255,0,0,"Không có cookie nào hợp lệ. Vui lòng kiểm tra lại.")
        sys.exit(1)
        
    data = switch_facebook_account(valid_cookies[current_cookie_index], authorization)
    if not data:
        prints(255,0,0,"Cookie đầu tiên không hợp lệ. Không thể bắt đầu.")
        sys.exit(1)

    # Khởi tạo bảng lần đầu
    # Lưu ý: Cần đảm bảo job_dashboard_store và job_type_counts đã được khai báo
    # Nếu chưa, bạn cần thêm khai báo GLOBAL ở đây hoặc ở ngoài hàm
    # global job_dashboard_store, job_type_counts 
    try:
        for t in list_type_job: 
            job_dashboard_store[t] = "---"
            job_type_counts[t] = 0 
        update_and_print_dashboard('', '0', '0', 0, SO_NV, None, data['name'], wallet(authorization), list_type_job)
    except NameError:
         prints(255, 165, 0, "Lỗi: Thiếu khai báo biến 'job_dashboard_store' hoặc 'job_type_counts' cho dashboard.")
         # Giả định các biến này đã được khai báo ở đâu đó trong code Tool gốc

    while demht < SO_NV1:
        try:
            if tasks_on_current_cookie >= switch_threshold and len(valid_cookies) > 1:
                current_cookie_index = (current_cookie_index + 1) % len(valid_cookies)
                new_data = switch_facebook_account(valid_cookies[current_cookie_index], authorization)
                if new_data:
                    data = new_data
                    tasks_on_current_cookie = 0
                else:
                    prints(255, 0, 0, f"Lỗi với cookie thứ {current_cookie_index+1}, loại bỏ khỏi danh sách chạy.")
                    valid_cookies.pop(current_cookie_index)
                    if not valid_cookies:
                        prints(255,0,0,"Tất cả cookie đều lỗi. Dừng tool.")
                        break
                    current_cookie_index = current_cookie_index % len(valid_cookies)
                    data = switch_facebook_account(valid_cookies[current_cookie_index], authorization)
                    tasks_on_current_cookie = 0

            if not list_type_job:
                prints(5,255,0,'Đã hết loại nhiệm vụ để làm.')
                break
            
            for type_job in list_type_job:
                reload(data['session'],authorization,type_job)
            
            time.sleep(4)
            JOB = get_job(data['session'], authorization)
            
            if not JOB:
                prints(255,255,0,'Không tìm thấy nhiệm vụ rồi địt mẹ chờ xíu lấy job , chờ 10 giây...', end='\r')
                time.sleep(10)
                continue

            for job in JOB:
                if demht >= SO_NV1: break
                try:
                    res_load = load(data['session'], authorization, job)
                    time.sleep(random.randint(2,4))
                    
                    if res_load and res_load.get('success') and job['type'] in list_type_job:
                        delay = random.randint(delay1, delay2)
                        start_job = time.time()
                        
                        status_job = lam_job(data, res_load, job['type'])
                        
                        if status_job:
                            res_submit = submit(data['session'], authorization, job, status_job, res_load)
                            if res_submit[0]:
                                demht += 1
                                tasks_on_current_cookie += 1
                                balance = wallet(authorization)
                                update_and_print_dashboard('complete', res_submit[1], res_submit[2], demht, SO_NV1, job['type'], data['name'], balance, list_type_job)
                                countdown(delay - (time.time() - start_job))
                            else:
                                raise Exception("Submit thất bại")
                        else:
                            raise Exception("Hành động (react/comment) thất bại")
                    else:
                        raise Exception("Load nhiệm vụ thất bại hoặc sai loại job")

                except Exception:
                    prints(255, 165, 0, "NV đang bị lỗi; bỏ qua job này")
                    report(data['session'], authorization, job)
                    demsk += 1
                    time.sleep(4)
        
        except KeyboardInterrupt:
            prints(255,255,0, "\nBạn sợ à?.")
            break
        except Exception as e:
            prints(255,0,0,f'Lỗi vòng lặp chính: {e}')
            time.sleep(10)

    prints(5,255,0,f'\n---Quá Múpp---')
    prints(5,255,0,f'Số nhiệm vụ đã hoàn thành: {demht}')
    prints(5,255,0,f'Số nhiệm vụ đã bỏ qua: {demsk}')
    prints(5,255,0,f'Tổng: {demsk+demht}')

if __name__ == "__main__":
    main_bumx_free()
