import requests
import json
import os
import datetime
import hashlib
import hmac

# === CONFIGURATION ===
COOKIE_STRING = 'GPS=1; YSC=2tnC2SkE2xU; VISITOR_INFO1_LIVE=_tpf3yvlDWk; VISITOR_PRIVACY_METADATA=CgJQSxIEGgAgYQ%3D%3D; __Secure-ROLLOUT_TOKEN=CIfr8Lm5sI-kQBCH4abf77KNAxiJ9Yjg77KNAw%3D%3D; HSID=A5s6eqf_eUYoIwjPC; SSID=AcyZJ2XrU1C-eu_X_; APISID=Krajn_02IV0zUK0q/AVpm0l474lpE7LhY4; SAPISID=uPF0NwGPbGVly4GV/AgVd7WsQwQghuLiLX; __Secure-1PAPISID=uPF0NwGPbGVly4GV/AgVd7WsQwQghuLiLX; __Secure-3PAPISID=uPF0NwGPbGVly4GV/AgVd7WsQwQghuLiLX; LOGIN_INFO=AFmmF2swRQIhAOb2eKsZUMfmzHtcdJtPkz74XKGPxQziHLH65Ur4XEl6AiBTeJOxWCGAYbBYc891zR6-WF-iKRCumq2rnAuxGZWg6g:QUQ3MjNmd2lPYXVrZ1RULVlzT1dIVnpXSkhuRzBsX2Jlb25PLWtSMF83OFNMdXRycUZPLWYwXzdQZGtWU3AwRTBvcGlYWUlleTY5NnZOemo4ZExKMkxYcXRYU2t0Z1RRUVFhZ2ZtTXZDbzd5VTFZNTBzX3NMeE9aM0Z5UHdQSHNwZXk3NXZuMWdsbEFhcmdIbmNRQnFQT3VkWUxOYllDUk5R; _gcl_au=1.1.1631592467.1747772569; _ga=GA1.1.1985789938.1747772569; NID=524=HigyMIxMfo0tBn1vC1roEby7TAYfVQXx8BsAKIo8IPEDnolXijUykKHnQai3OLJCY96Bt_ep6hKeJtO-xQ4cTa4epCvCcdvR3H1Sbn5B-yNVMud0NZpHOefC1tXDht6GLOqZRAcB1qyyjNpiZBvQjqclfUeakzIpC9-YOq1WolGdQZJBOmDa6XZ2jx4o68nuMc7GcEam_7BKK5NawK8ZmRtfNP4; __Secure-1PSIDTS=sidts-CjEBjplskKMeW377ZVBoEVEaJPw-7u9hQSA1kWGmei4Zi7Z4C_uwqrmQoxJJefHzzWX4EAA; __Secure-3PSIDTS=sidts-CjEBjplskKMeW377ZVBoEVEaJPw-7u9hQSA1kWGmei4Zi7Z4C_uwqrmQoxJJefHzzWX4EAA; CONSISTENCY=AKreu9s6f7iWaHPn-8Declf4QhzFdz_nd3mYMV38Nf0m9_v3bBJrUZh70cB4KWVFNLO3g1fU5-X4sJX7bWZZa0Lk1rmtzyqt6e9tECh3f_69ClaSlnfjlROQVZ2cid9T-1sN6X_jzTvGsgr_3gfpyI1PfMMeFJAA3mkQuN0T-oo-z6GwBWLCXx3MvAlR; ajs_anonymous_id=%2287897045-5e1e-45e9-9554-ade30fc12900%22; PREF=f6=40000080&tz=Asia.Karachi&f4=4000000; SID=g.a000xAj0FNQWsSq9C0EJFErFFaYn-G5RqoO6PQCpLcJgp6IMMBrr6ppua-OpxPgfuWYXZTD9QQACgYKAVcSARQSFQHGX2MiTj3J-OdKT0tPDm2ER0JQAxoVAUF8yKr5enfftjHFs2fcR-6OP0em0076; __Secure-1PSID=g.a000xAj0FNQWsSq9C0EJFErFFaYn-G5RqoO6PQCpLcJgp6IMMBrrLqKdEEvLeclXk0DJc_8YTgACgYKAegSARQSFQHGX2Mi3GihxPnlLqR64LG3NTWDDBoVAUF8yKqXXRGyBx6NIz3TH2SMqjKt0076; __Secure-3PSID=g.a000xAj0FNQWsSq9C0EJFErFFaYn-G5RqoO6PQCpLcJgp6IMMBrrLftn1Qi6JFxkZd3PuHcbZAACgYKAaMSARQSFQHGX2MiegVuXZgz2mddQPzAIgfp0hoVAUF8yKrHVrnn73fy32oPhf9Zv1y20076; _ga_VCGEPY40VB=GS2.1.s1747772569$o1$g1$t1747773884$j58$l0$h0$dduqfTNw-O5iZkP6t85lRHXjpQRd1wcysSg; SIDCC=AKEyXzWXF0NcR9WpABLHToHEUenRz3_NpERttXP_UXBY1attqegU3Eddcq7ra9hqoiSke0e63Q; __Secure-1PSIDCC=AKEyXzWuJxYf2scJPt4UvfiY3XNBMa4Vhdg4kQNo_5WDMXdQaILFasBl1Js_NBjKnHWARN-P; __Secure-3PSIDCC=AKEyXzUYotkAzAmXhbKneHdqMBOtivuryvbtoa854bcdxQjQoU3VAzuyF2WX1Fo8hbk3C-JE4Q; ST-vzh386=session_logininfo=AFmmF2swRQIhAOb2eKsZUMfmzHtcdJtPkz74XKGPxQziHLH65Ur4XEl6AiBTeJOxWCGAYbBYc891zR6-WF-iKRCumq2rnAuxGZWg6g%3AQUQ3MjNmd2lPYXVrZ1RULVlzT1dIVnpXSkhuRzBsX2Jlb25PLWtSMF83OFNMdXRycUZPLWYwXzdQZGtWU3AwRTBvcGlYWUlleTY5NnZOemo4ZExKMkxYcXRYU2t0Z1RRUVFhZ2ZtTXZDbzd5VTFZNTBzX3NMeE9aM0Z5UHdQSHNwZXk3NXZuMWdsbEFhcmdIbmNRQnFQT3VkWUxOYllDUk5R; SIDCC=AKEyXzU6iGk7v4-yliTPNwPxtuUY5LaBNf4GTwmO0jvdHbDCz5zZKOBVr6T67WH0aTr0CTbPdA; __Secure-1PSIDCC=AKEyXzVl9GwEco2lBaowHP-Ka1LER85hEKSrl1NhNY77A-maLgIUgcQ6jGNI_5ViJ9qxQT3nlw; __Secure-3PSIDCC=AKEyXzXu-3JHQRyUpOblB8PWoYNhxkFp7zEPz10k-AQYrrGVoHqiYlW-wQZ3e9aALXuPg56E'
SAPISID = "uPF0NwGPbGVly4GV/AgVd7WsQwQghuLiLX"  # Extract from cookie
ORIGIN = "https://www.youtube.com"

#AUTHENTICATION HEADER GENERATION
def generate_sapisid_hash(sapisid, origin):
    now = int(datetime.datetime.now().timestamp())
    hash_str = f"{now} {sapisid} {origin}"
    digest = hmac.new(sapisid.encode(), hash_str.encode(), hashlib.sha1).hexdigest()
    return f"SAPISIDHASH {now}_{digest}"

# === HEADERS ===
headers = {
    "origin": ORIGIN,
    "referer": "https://www.youtube.com/paid_memberships?ybp=mAEO",
    "authorization": generate_sapisid_hash(SAPISID, ORIGIN),
    "cookie": COOKIE_STRING,
    "content-type": "application/json",
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

# === PAYLOAD (TRUNCATED OR PLACEHOLDER FOR DEMO) ===
payload = {
    "context": {
        "client": {
            "clientName": "WEB",
            "clientVersion": "2.20250519.01.00"
        }
    },
    "feedbackData": {
        "feedbackTokens": [
            "AB9zfpLZp-k3dclItpvnX..."
        ]
    },
    "itemParams": "Cg0IBhIJdW5saW1pdGVkGAXwAQA="
}



def cancel_youtube_membership():
    try:
        response = requests.post(
            "https://www.youtube.com/youtubei/v1/ypc/cancel_recurrence?prettyPrint=false",
            headers=headers,
            data=json.dumps(payload),
            timeout=20
        )
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
    except Exception as e:
        print("Request failed:", str(e))

# === RUN ===
if __name__ == "__main__":
    cancel_youtube_membership()