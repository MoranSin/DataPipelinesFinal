
from abc import ABC, abstractmethod

class genericScraper:
    @abstractmethod
    def scrape(self, run_only_on_latest_chart = True):
        pass

