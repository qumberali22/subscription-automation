import requests, json
import os
import datetime
import hashlib
import hmac


COOKIE_STRING = 'YSC=sTRzEZaW-H4; VISITOR_INFO1_LIVE=WYLg1N1Cvlo; VISITOR_PRIVACY_METADATA=CgJQSxIEGgAgDg%3D%3D; __Secure-ROLLOUT_TOKEN=CMC03f6R5KKJLxDE_IPR97KNAxirm4PS97KNAw%3D%3D; _gcl_au=1.1.1817345507.1747775024; _ga=GA1.1.1385202271.1747775024; LOGIN_INFO=AFmmF2swRgIhAPX_7cHlXxl3-a-ke33k7ITCLUTmWkYL71q3D_8qaETyAiEAq0yShyCw1iUhR0AGWliWcr9vn4uX9IXFGhRG5cKr-zY:QUQ3MjNmeDNXQy1JLTVnQXctd1cxWlhSU3NGcnBzaWxuMncxbGM2LURadEU5ZGNNMmVtQXNLTmh1aVVUSURCMU1tcC0xbU1keDBmZ2ZmeG5NOXF4Q3g3Qkp0djhnVjFNVXVhUF9YT2tKV3JvTllFay1xSnhwS3Nad002QWdIY3JxVm5vdXJENHpydFJzTldUMHBBN0tIQ21NVDhQX2lBNUJ3; NID=524=MQN8cyx6xe0bC5_JX2jDMVxf4SF-jRuWxiqhRS5Bo1RvLiaeUKdOH51G8c8boEAJjobs89kkefugl9NYapRDs9EAl-2j719Z7J2_pJljahQjxCsfQZb-Vlhi0gZ-lezfNHfj8uf14JWdalQNw6Sjkd1maacQBp0UHhqrk3ge5g_-UR1x_LBfcucUu43a7r-vvTd9dGA1fhadxf2Kec7tky5ngQXeiycHFtYvZ-U0h8jA_jHsGi9EWi4; PREF=f6=40000000&tz=Asia.Karachi&f4=4000000; ajs_anonymous_id=%22bd0c736b-7570-4526-a075-50af2298874a%22; HSID=AspvIz-soxIkOupdz; SSID=AaxsgwTBRZygTr4W8; APISID=x3CnvY2V6UqOuqEx/AD7xOZKXcjEJQcjvO; SAPISID=hfKBd0X9a07_yD3Q/Apj3dwaoPJc_VipYW; __Secure-1PAPISID=hfKBd0X9a07_yD3Q/Apj3dwaoPJc_VipYW; __Secure-3PAPISID=hfKBd0X9a07_yD3Q/Apj3dwaoPJc_VipYW; SID=g.a000xAiuRHN4vF4UsCMDyjxQLZyNyfoIHHsoC9tR0Guk3LBX_p--02mo78lITaz5K_9jyoRfmQACgYKATkSARcSFQHGX2MiAX5D3Tn_-R_8cGtbUZSyaBoVAUF8yKpMoO2B4ETzrsuu1-YkN5l10076; __Secure-1PSID=g.a000xAiuRHN4vF4UsCMDyjxQLZyNyfoIHHsoC9tR0Guk3LBX_p--9ftPl50jJSpKENz2ysZHrAACgYKAfYSARcSFQHGX2MifvQunIeFUfZHRqigTz4kdBoVAUF8yKpFvpvGT-FGUS21DHYmXS510076; __Secure-3PSID=g.a000xAiuRHN4vF4UsCMDyjxQLZyNyfoIHHsoC9tR0Guk3LBX_p--Nk2s1wLFQBsN0wS95tW8pAACgYKAWkSARcSFQHGX2Mi1H1WlvK3fYyKZ6ldwP80KRoVAUF8yKp2aPDWIQ3XsKsTGyRQjP2M0076; __Secure-1PSIDTS=sidts-CjEBjplskODqg5-oGj5pqInG_9h4SCQW-sK80EGgwqRw8GghFfOmiiIU4OILIYukdhaWEAA; __Secure-3PSIDTS=sidts-CjEBjplskODqg5-oGj5pqInG_9h4SCQW-sK80EGgwqRw8GghFfOmiiIU4OILIYukdhaWEAA; _ga_VCGEPY40VB=GS2.1.s1747816454$o2$g1$t1747821359$j15$l0$h0$dzemQJM4wlZ-EOy2rbtkS-i2B6TU8CuDSGQ; SIDCC=AKEyXzWS1s5OdLbrxXmRC2cJw_gjejrOWCxiK3mn2fyYhOWgTrnbpz44AMJ48h9YfiiX2_aSBOQ; __Secure-1PSIDCC=AKEyXzU5_7-_e5vInaRpCxFmsKjhCM_PBahmSF0TTEm3cCpiZ-E1Hc0kqPmm1NztWyFr0TQQZg; __Secure-3PSIDCC=AKEyXzUdsFfHcLTs4Uq58zZI8WzNT2XjAilxTV06i9UAqM3CdsaffjW6u06dnTxmsRXgrzwb6zc; ST-x98jvm=session_logininfo=AFmmF2swRgIhAPX_7cHlXxl3-a-ke33k7ITCLUTmWkYL71q3D_8qaETyAiEAq0yShyCw1iUhR0AGWliWcr9vn4uX9IXFGhRG5cKr-zY%3AQUQ3MjNmeDNXQy1JLTVnQXctd1cxWlhSU3NGcnBzaWxuMncxbGM2LURadEU5ZGNNMmVtQXNLTmh1aVVUSURCMU1tcC0xbU1keDBmZ2ZmeG5NOXF4Q3g3Qkp0djhnVjFNVXVhUF9YT2tKV3JvTllFay1xSnhwS3Nad002QWdIY3JxVm5vdXJENHpydFJzTldUMHBBN0tIQ21NVDhQX2lBNUJ3'
SAPISID = "uPF0NwGPbGVly4GV/AgVd7WsQwQghuLiLX"  # Extract from cookie
ORIGIN = "https://www.youtube.com"

#AUTHENTICATION HEADER GENERATION
def generate_sapisid_hash(sapisid, origin):
    now = int(datetime.datetime.now().timestamp())
    hash_str = f"{now} {sapisid} {origin}"
    digest = hmac.new(sapisid.encode(), hash_str.encode(), hashlib.sha1).hexdigest()
    return f"SAPISIDHASH {now}_{digest}"

headers = {
    "origin": ORIGIN,
    "referer": "https://www.youtube.com/paid_memberships?ybp=mAEO",
    "authorization": "SAPISIDHASH 1747821373_51ec43b8c04189df474eb7258f58e4436bd2036e_u SAPISID1PHASH 1747821373_51ec43b8c04189df474eb7258f58e4436bd2036e_u SAPISID3PHASH 1747821373_51ec43b8c04189df474eb7258f58e4436bd2036e_u",
    "cookie": COOKIE_STRING,
    "content-type": "application/json",
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

payload = {
  "context": {
    "client": {
      "hl": "en",
      "gl": "PK",
      "remoteHost": "58.65.220.34",
      "deviceMake": "Apple",
      "deviceModel": "",
      "visitorData": "CgtfdHBmM3l2bERXayjg1LPBBjIKCgJQSxIEGgAgYQ%3D%3D",
      "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36,gzip(gfe)",
      "clientName": "WEB",
      "clientVersion": "2.20250519.01.00",
      "osName": "Macintosh",
      "osVersion": "10_15_7",
      "originalUrl": "https://www.youtube.com/paid_memberships?ybp=mAEO",
      "screenPixelDensity": 2,
      "platform": "DESKTOP",
      "clientFormFactor": "UNKNOWN_FORM_FACTOR",
      "configInfo": {
        "appInstallData": "CODUs8EGELeGzxwQhJDPHBDins8cENuvrwUQvYqwBRCRjP8SEMnmsAUQ6YjPHBCThs8cEODg_xIQvZmwBRCdprAFEMvRsQUQibDOHBD1g88cEInorgUQp-POHBDi1K4FEL2azxwQ6-j-EhDN0bEFEP6ezxwQ2JzPHBDn484cEKr4zhwQjcywBRC45M4cEMyJzxwQ6ZvPHBC52c4cEJmNsQUQiYS4IhCliIATEPb-_xIQ37jOHBCa9M4cEMzfrgUQpZ3PHBCcm88cEPyyzhwQu9nOHBDgzbEFEMn3rwUQgc3OHBCU_rAFENPhrwUQ3rzOHBD-8_8SEIjjrwUQ9quwBRCIh7AFEKaasAUQ7qDPHBC9tq4FELCJzxwQ8OLOHBCZmLEFEODczhwQndCwBRCnjM8cEMOKgBMQt-r-EhCKgoATEOTn_xIQ18GxBRCDhLgiEIeszhwQm_bOHBC6jYATEMiXzxwqMENBTVNJQlVib0wyd0ROSGtCcFNDRXVmaTVndVA5QTd2LXdiNTdBUEozQVdFTXgwSA%3D%3D",
        "coldConfigData": "CODUs8EGEPG6rQUQvbauBRDi1K4FEL2KsAUQndCwBRDP0rAFEOP4sAUQpL6xBRDXwbEFEJLUsQUQ9rLOHBD8ss4cEODczhwQ9tzOHBDL4s4cEKfjzhwQ5-POHBDw684cEJv2zhwQqvjOHBCVgM8cEKqAzxwQ9YPPHBCThs8cELeGzxwQsInPHBCnjM8cENCOzxwQgJDPHBCEkM8cEJ-QzxwQuZXPHBDfls8cEMiXzxwQvZrPHBDWms8cEJybzxwQ6ZvPHBDYnM8cEKWdzxwQ4p7PHBD-ns8cEIOEuCIQiYS4IhoyQU9qRm94MUxDeDhCbXZPUU5XNnZTeG50dV9uMnNuUExwOThXLWt2cmkwcF9MQkU1NHciMkFPakZveDJDZU9oV09maGg3dTNFTV9jd043VThOVldWLUpkb1p2LVRsalctM3dOVW5nKnxDQU1TVncwaXVOMjNBdDRVemcyWEg2Z3F0UVM5RmYwRGc0V2FFTDhBMndHRUF1b0NpQVB0QUJPc0hSVXBtYkczSDRXa0JacTdCdjladUlBQ0JJcXJCcE11b2FnRTNkMEdCYkVva0h2emlBYk5Mb1F6dlVXNUM2YndCZz09",
        "coldHashData": "CODUs8EGEhM3NzM4MTAyNDcyNTcwNzQzMzUxGODUs8EGMjJBT2pGb3gxTEN4OEJtdk9RTlc2dlN4bnR1X24yc25QTHA5OFcta3ZyaTBwX0xCRTU0dzoyQU9qRm94MkNlT2hXT2ZoaDd1M0VNX2N3TjdVOE5WV1YtSmRvWnYtVGxqVy0zd05VbmdCfENBTVNWdzBpdU4yM0F0NFV6ZzJYSDZncXRRUzlGZjBEZzRXYUVMOEEyd0dFQXVvQ2lBUHRBQk9zSFJVcG1iRzNINFdrQlpxN0J2OVp1SUFDQklxckJwTXVvYWdFM2QwR0JiRW9rSHZ6aUFiTkxvUXp2VVc1QzZid0JnPT0%3D",
        "hotHashData": "CODUs8EGEhM5NTg4OTgyNTM5NTgwNTc3MTUyGODUs8EGKJTk_BIopdD9Eiiekf4SKMjK_hIot-r-EijBg_8SKJGM_xIozcf_EiiZ8v8SKP7z_xIo9v7_EijHgIATKIqCgBMotIOAEyjzhYATKNeGgBMopYiAEyi9iYATKMOKgBMoxYuAEyj-i4ATKLqNgBMyMkFPakZveDFMQ3g4Qm12T1FOVzZ2U3hudHVfbjJzblBMcDk4Vy1rdnJpMHBfTEJFNTR3OjJBT2pGb3gyQ2VPaFdPZmhoN3UzRU1fY3dON1U4TlZXVi1KZG9adi1UbGpXLTN3TlVuZ0I4Q0FNU0pnMElvdGY2RmE3QkJ2bzNrUjd5Q3JrRUZSVGR6OElNeHFmdEM0VEhEdHlOQXFYQUJkWlg%3D"
      },
      "screenDensityFloat": 2,
      "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
      "timeZone": "Asia/Karachi",
      "browserName": "Chrome",
      "browserVersion": "136.0.0.0",
      "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "deviceExperimentId": "ChxOelV3TmpZek1qTTNPRFk0T0RjME5URXdPQT09EODUs8EGGODUs8EG",
      "rolloutToken": "CIfr8Lm5sI-kQBCH4abf77KNAxiJ9Yjg77KNAw%3D%3D",
      "screenWidthPoints": 1792,
      "screenHeightPoints": 421,
      "utcOffsetMinutes": 300,
      "connectionType": "CONN_CELLULAR_4G",
      "memoryTotalKbytes": "8000000",
      "mainAppWebInfo": {
        "graftUrl": "https://www.youtube.com/paid_memberships?ybp=mAEO",
        "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
        "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
        "isWebNativeShareAvailable": True
      }
    },
    "user": {
      "lockedSafetyMode": False
    },
    "request": {
      "useSsl": True,
      "consistencyTokenJars": [
        {
          "encryptedTokenJarContents": "AKreu9s6f7iWaHPn-8Declf4QhzFdz_nd3mYMV38Nf0m9_v3bBJrUZh70cB4KWVFNLO3g1fU5-X4sJX7bWZZa0Lk1rmtzyqt6e9tECh3f_69ClaSlnfjlROQVZ2cid9T-1sN6X_jzTvGsgr_3gfpyI1PfMMeFJAA3mkQuN0T-oo-z6GwBWLCXx3MvAlR"
        }
      ],
      "internalExperimentFlags": []
    },
    "clientScreenNonce": "ZYj3-grZYzxw8YV-",
    "clickTracking": {
      "clickTrackingParams": "CAIQ8dsFIhMIvteq4vWyjQMVhAcGAB3YzBMg"
    },
    "adSignalsInfo": {
      "params": [
        {
          "key": "dt",
          "value": "1747774049113"
        },
        {
          "key": "flash",
          "value": "0"
        },
        {
          "key": "frm",
          "value": "0"
        },
        {
          "key": "u_tz",
          "value": "300"
        },
        {
          "key": "u_his",
          "value": "2"
        },
        {
          "key": "u_h",
          "value": "1120"
        },
        {
          "key": "u_w",
          "value": "1792"
        },
        {
          "key": "u_ah",
          "value": "1005"
        },
        {
          "key": "u_aw",
          "value": "1792"
        },
        {
          "key": "u_cd",
          "value": "24"
        },
        {
          "key": "bc",
          "value": "31"
        },
        {
          "key": "bih",
          "value": "421"
        },
        {
          "key": "biw",
          "value": "1792"
        },
        {
          "key": "brdim",
          "value": "0,25,0,25,1792,25,1792,988,1792,421"
        },
        {
          "key": "vis",
          "value": "1"
        },
        {
          "key": "wgl",
          "value": "true"
        },
        {
          "key": "ca_type",
          "value": "image"
        }
      ]
    }
  },
  "feedbackData": {
    "feedbackTokens": [
      "AB9zfpLZp-k3dclItpvnXbxaq2qVGWRlVKBHdh3679BDdrlQUaqte02zl073xSMrzt9ZZUoF9SRLHyxD8uO0c4lurQKDswS2Obk9lkzdljGsoV2yI0xg5W0y7ydNRgJv0JX-z65pMFWL"
    ]
  },
  "itemParams": "Cg0IBhIJdW5saW1pdGVkGAXwAQA%3D"
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

if __name__ == "__main__":
    cancel_youtube_membership()