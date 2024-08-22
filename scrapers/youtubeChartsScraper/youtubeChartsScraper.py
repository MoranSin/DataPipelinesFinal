import requests
import time
from datetime import datetime, timedelta
import json


class YoutubeChartsScraper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://charts.youtube.com/youtubei/v1/browse?alt=json&key=AIzaSyCzEW7JUJdSql0-2V4tHUb6laYm4iAE_dM"
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7",
            "authorization": f"SAPISIDHASH {self.api_key}",
            "content-type": "application/json",
            "cookie": "HSID=Axtuf6XH3Z-XJfcOF; SSID=AyS-lrAUPJsntzO64; APISID=e8WrpF-lHEbBNMTX/A8ws0W-Ww42lUrTm-; SAPISID=TbCsTkETtWLEq4CP/AsP-TLqCyQocDT8Nw; __Secure-1PAPISID=TbCsTkETtWLEq4CP/AsP-TLqCyQocDT8Nw; __Secure-3PAPISID=TbCsTkETtWLEq4CP/AsP-TLqCyQocDT8Nw; VISITOR_PRIVACY_METADATA=CgJJTBIEGgAgJQ==; VISITOR_PRIVACY_METADATA=CgJJTBIEGgAgJQ==; VISITOR_INFO1_LIVE=6tqTlp7lYf0; LOGIN_INFO=AFmmF2swRgIhAJekmpDfANFqluEh4-hMY79X06A5IT0qPZ-3SAIQu0NCAiEA1X-ps8JUtoxnJLno8ziI45sQnRlkBAmMTP4KGLmOkuc:QUQ3MjNmd0tIM19vVS12T3JiLUIwdFF3WnFab1NXTU93cWtNY0U1MWJfRDVQQlBaTHo2WGFfbWlDUGJxaU55c2MzUlJKc25LdmZ6amtTZ0FCYmI2YW42WG9MMEVPMnRhVkJDeldOQjhPZWtDeG81QmJZQjU0c2VfNzRpdE5pQTI2bHg1QUIyckdlaVhUTk1nR0RMVmVPYVpRb3BJWnRSNGV3; PREF=f6=40000000&f7=4100&tz=Asia.Jerusalem&f4=4000000&f5=20000; SID=g.a000mghSKv9mVBjntOrV2ftJAW3s4yyDzR35QZH-B7VACxe1GNszBMHlDkSMRprYJlIDny4XWwACgYKAWQSARQSFQHGX2MiSECDxKXZDDS6bdPK6bY6DBoVAUF8yKosJVEzK3eIiqwm_XXT2M2X0076; __Secure-1PSID=g.a000mghSKv9mVBjntOrV2ftJAW3s4yyDzR35QZH-B7VACxe1GNszsbvcA2pcJZJY_6swaPxlhAACgYKAfQSARQSFQHGX2MiL1Kpm1NkcgKBpwc9CZb20xoVAUF8yKrjaVHN1gpMKUmT3YfYUTVU0076; __Secure-3PSID=g.a000mghSKv9mVBjntOrV2ftJAW3s4yyDzR35QZH-B7VACxe1GNsz1ZUexjMcSyLxu9NCmV0nkgACgYKAVQSARQSFQHGX2MiQarK0a8lJml8qCQ5NAcrABoVAUF8yKono-8tJgEAa5pD4Ira06Ue0076; __Secure-1PSIDTS=sidts-CjIBUFGoh8LHTrdrPvCtImKobMlQv92Qig1-vSfVi6jlncvsXCDJjmv0slM9OYon119lMxAA; __Secure-3PSIDTS=sidts-CjIBUFGoh8LHTrdrPvCtImKobMlQv92Qig1-vSfVi6jlncvsXCDJjmv0slM9OYon119lMxAA; YSC=XtVj1WCvKF8; SIDCC=AKEyXzWqhulDzn8tnOszAUMzVkAXONF6sUPqcQngtL27wx5fC6n2tNCmZjQki2GkBBypdNPq8dhK; __Secure-1PSIDCC=AKEyXzXMaYJQS_5cUeKC-oU44B_MC79vrZ7nG-DoDbahklcmLehPf4SC6ZGxt7eg45jdTs-yHu0; __Secure-3PSIDCC=AKEyXzVgSO296kjpnOLJVm67cw5fKgZwFZa179g_Wi7wrO8lBwHDjQ-uq70grk9D0daGiB2JKJQ",
            "origin": "https://charts.youtube.com",
            "priority": "u=1, i",
            "referer": "https://charts.youtube.com/charts/TopVideos/global/daily",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-arch": "\"x86\"",
            "sec-ch-ua-bitness": "\"64\"",
            "sec-ch-ua-form-factors": "\"Desktop\"",
            "sec-ch-ua-full-version": "\"127.0.6533.120\"",
            "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.120\", \"Chromium\";v=\"127.0.6533.120\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-model": "\"\"",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-ch-ua-platform-version": "\"10.0.0\"",
            "sec-ch-ua-wow64": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "x-client-data": "CJO2yQEIprbJAQipncoBCPqSywEIlKHLAQiFoM0BCLKezgEI/afOAQjwqc4BCOWvzgEIwbbOAQjat84BCOK7zgEYj87NARi5rs4BGJ2xzgEYwJPVIg==",
            "x-goog-authuser": "0",
            "x-origin": "https://charts.youtube.com",
            "x-youtube-ad-signals": "dt=1724315395750&flash=0&frm&u_tz=180&u_his=3&u_h=864&u_w=1536&u_ah=824&u_aw=1536&u_cd=24&bc=31&bih=703&biw=518&brdim=0%2C0%2C0%2C0%2C1536%2C0%2C1536%2C824%2C518%2C703&vis=1&wgl=true&ca_type=image",
            "x-youtube-client-name": "31",
            "x-youtube-client-version": "2.0",
            "x-youtube-page-cl": "663262755",
            "x-youtube-time-zone": "Asia/Jerusalem",
            "x-youtube-utc-offset": "180"
        }
        self.countries = [
            "ar",
            "au",
            "at",
            "be",
            "bo",
            "br",
            "ca",
            "cl",
            "co",
            "cr",
            "cz",
            "dk",
            "do",
            "ec",
            "eg",
            "sv",
            "ee",
            "fi",
            "fr",
            "de",
            "gt",
            "hn",
            "hu",
            "is",
            "in",
            "id",
            "ie",
            "il",
            "it",
            "jp",
            "ke",
            "lu",
            "mx",
            "nl",
            "nz",
            "ni",
            "ng",
            "no",
            "pa",
            "py",
            "pe",
            "pl",
            "pt",
            "ro",
            "ru",
            "sa",
            "rs",
            "za",
            "kr",
            "es",
            "se",
            "ch",
            "tz",
            "tr",
            "ug",
            "ug",
            "ua",
            "ae",
            "gb",
            "us",
            "uy",
            "zw",
        ]

    def extract_relevant_data(self, chart_data):
        extracted_data = []
        top_n = 10
        
        for entry in chart_data["videos"]:
            song_name = entry["title"]
            song_length = entry["videoDuration"]
            artist_name = entry["artists"][0]["name"]
            rank_value = entry["chartEntryMetadata"]["currentPosition"]
            
            extracted_data.append({
                "song": {
                    "song_name": song_name,
                    "song_link": None,
                    "song_length": song_length,
                    "artist": {
                        "artist_id": None,
                        "artist_name": artist_name,
                        "artist_genre": None,
                        "artist_gender": None,
                        "country": None
                    }
                },
                "chart": {
                    "rank_value": rank_value,
                    "date": None,
                    "country": None,
                    "source": "Youtube Charts",
                    "song_id": None
                }
            })
        
        return extracted_data
 
    def fetch_charts_daily(self):
        global_url = self.base_url + "global/daily"
        response = requests.post(global_url, headers=self.headers)
        if response.status_code == 200:
            print("Response text:", response.text)  # Add this line
            try:
                data = response.json()
                chart_data = data['contents']['sectionListRenderer']['contents']['musicAnalyticsSectionRenderer']['content']
                extracted_data = self.extract_relevant_data(chart_data)
                return extracted_data
            except json.JSONDecodeError:
                print("Failed to decode JSON from the response.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}, Response: {response.text}")



api_key ="SAPISIDHASH 1724315395_0ec369539e7ff366ca74852749fde028c13da163"
spotify_scraper = YoutubeChartsScraper(api_key)
spotify_scraper.fetch_charts_daily()