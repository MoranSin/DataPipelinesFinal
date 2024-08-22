import requests_html
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from genericScraper import genericScraper


class SpotifyScraper(genericScraper):
    
    def scrape(self, run_only_on_latest_chart=True):
        
        url = 'https://charts.spotify.com/charts/view/regional-global-weekly/2024-08-08'
        
        # Initialize an HTMLSession
        session = HTMLSession()
        response = session.get(url)
        
        # Render the page to execute JavaScript
        response.html.render(timeout=20)  # You can adjust the timeout as needed
        
        # Now you can parse the fully rendered HTML with BeautifulSoup
        html_content = response.html.html
        soup = BeautifulSoup(html_content, 'html.parser')
        songs = []
        
        # Find the div with the specific data-testid
        div = soup.find('div', {'data-testid': 'charts-table'})
        print(div)
        print(html_content)

        # Uncomment and use this section to extract song details
        # for row in div.find_all('tr', class_='TableRow__TableRowElement-sc-1kuhzdh-0 cFcbDI'):
        #     rank = row.find('td', class_='TableCell__TableCellElement-sc-1nn7cfv-0 bdJpYG encore-text-body-small').text.strip()
        #     song_name = row.find('span', class_='styled__StyledTruncatedTitle-sc-135veyd-22 kkOJRc').text.strip()
        #     artist = row.find('span', class_='styled__StyledHyperlink-sc-135veyd-25 bVVLJU').text.strip()

        #     songs.append({
        #         'rank': rank,
        #         'song_name': song_name,
        #         'artist': artist,
        #     })

        return songs

spotify_scraper = SpotifyScraper()
songs_info = spotify_scraper.scrape()

for song in songs_info:
    print(f"Rank: {song['rank']}, Title: {song['song_name']}, Artist: {song['artist']}")
