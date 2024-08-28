import requests
from datetime import datetime
from bs4 import BeautifulSoup
import boto3
import json

class TiktokScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
        self.sqs = boto3.client('sqs', endpoint_url='http://sqs:9324', region_name='elasticmq', aws_access_key_id='x', aws_secret_access_key='x')
        self.queue_url = 'http://sqs:9324/queue/data-music-q'
    
    def extract_relevant_data(self, chart_data , date):
        extracted_data = [] 

        chart_section = chart_data.find('div', class_='chart-results-list')

        chart_items = chart_section.find_all('div', class_='o-chart-results-list-row-container')

        for item in chart_items:
            #Getting the artist name and song name
            row = item.find('ul', class_='o-chart-results-list-row')
            li4 = row.find('li', class_='lrv-u-width-100p')
            artist_info = li4.find('ul', class_="lrv-a-unstyle-list")
            second_li = artist_info.find('li', class_='o-chart-results-list__item')
            artist_name = second_li.find('span', class_='c-label').get_text(strip=True)   
            song_name = second_li.find('h3', id='title-of-a-story').get_text(strip=True)

            #Getting the song link
            charts_results = item.find('div', class_='charts-result-detail')
            inner_div = charts_results.find('div', class_='lrv-u-flex')
            links_container = inner_div.find('div', class_='lrv-u-flex-grow-1')
            another_div = links_container.find('div', class_='o-chart-tabs-wrapper')
            tab_5_div = another_div.find('div', {'data-tabs-trigger': 'tab_5'})
            o_chart_share = tab_5_div.find('div', class_='o-chart-share')
            if o_chart_share:
                a_tags = o_chart_share.find_all('a')
                if len(a_tags) >= 5:
                    song_link = a_tags[4]['href']
                else:
                    song_link = None

            #Getting the rank value
            chart_section = row.find('li', class_='o-chart-results-list__item')
            rank_value = chart_section.find('span', class_='c-label').get_text(strip=True)



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
                        "chart_type": "Weekly",
                        "rank_value": rank_value,
                        "date": date,
                        "country": "GBL",
                    "source": "Tiktok Billboard",
                },
            })

        return extracted_data
    
    def fetch_charts(self):
        date = datetime.now().strftime("%Y-%m-%d")
        url = self.base_url
        response = requests.get(url, 'html.parser')
        html = BeautifulSoup(response.text, 'html.parser')
        
        relevant_data = self.extract_relevant_data(html, date)
        return relevant_data

def tiktok_handler(event, context):
    try:
        tiktok_scraper = TiktokScraper()
        generated_chart = tiktok_scraper.fetch_charts()

        response = tiktok_scraper.sqs.send_message(
            QueueUrl=tiktok_scraper.queue_url,
            MessageBody=json.dumps(generated_chart, ensure_ascii=False)
        )
        print(f"Data scraped and sent to SQS: {response}")
        return {"message": "Data scraped and sent to SQS", "SQSResponse": response}

    except Exception as e:
        print(f"Error: {e}")
        raise e



