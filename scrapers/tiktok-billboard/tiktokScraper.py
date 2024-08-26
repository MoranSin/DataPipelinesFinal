import requests
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class TiktokScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
        self.rank_counter = 1

    
    def extract_relevant_data(self, chart_data , date):
        extracted_data = [] 

        chart_section = chart_data.find('div', class_='chart-results-list')

        chart_items = chart_section.find_all('li', class_='o-chart-results-list__item')

        for item in chart_items:
            # Extract the song title
            title_element = item.find(id="title-of-a-story")
            if title_element:
                song_name = title_element.get_text(strip=True)
                if song_name in ["Producer(s)", "Songwriter(s)"]:
                    continue
            else:
                continue

            # Extract the artist name
            artist_element = item.find('span', class_='c-label')
            if artist_element:
                artist_name = artist_element.get_text(strip=True)
                if not artist_name:
                    continue
            else:
                continue

            song_link = None

            # Extract the song link
            tiktok_links = []
            detail_elements = chart_data.find_all('div', class_='o-chart-share')

            # Iterate through each detail element to find TikTok links
            for element in detail_elements:
                # Find all <a> tags within the element
                link_elements = element.find_all('a', href=True)
                for link_element in link_elements:
                    tiktok_link = link_element['href']
                    # Check if the href contains 'tiktok'
                    if 'tiktok.com' in tiktok_link:
                        tiktok_links.append(tiktok_link)
                    else:
                        tiktok_links.append(None)
                        # tiktok_links.append(None)
                        continue

            # print(f"links: {len(tiktok_links)}")
            index = self.rank_counter - 1
            if 0 <= index < len(tiktok_links):
                if tiktok_links[index] == None:
                    print(f"Index {index} has no TikTok link for song {song_name}")
                    continue
                else:
                    song_link = tiktok_links[index]
                    print(f"Song: {song_name}, Artist: {artist_name}, TikTok Link: {song_link}")
                # else:
                    # song_link = None
            else:
                print(f"Index {index} is out of bounds for tiktok_links with length {len(tiktok_links)}")
                continue  # Default to the first link if index is out of bounds



            extracted_data.append({
            "artist": {
                "artist_name": artist_name,
                "artist_gender": None,
                "country": "GBL",
            },
            "song": {
                "song_name": song_name,
                "song_link": song_link,
                "song_length": None,
                "song_lyrics": None,
            },
            "chart": {
                    "chart_type":
                    "rank_value": self.rank_counter,
                    "date": date,
                    "country": "GBL",
                "source": "Tiktok Billboard",
            },
        })
            self.rank_counter += 1

        return extracted_data
    
    def fetch_charts(self):
        # dates = self.get_weekly_dates("2024-08-25")
        url = self.base_url + "2024-08-24" + "/"
        response = requests.get(url, 'html.parser')
        html = BeautifulSoup(response.text, 'html.parser')
        
        relevant_data = self.extract_relevant_data(html, "2024-08-24")
        print(relevant_data)


tiktok_scraper = TiktokScraper()
tiktok_scraper.fetch_charts()
    



