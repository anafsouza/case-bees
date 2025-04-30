import requests
import logging
from typing import List, Dict, Optional
from ..utils.logs import Logger

class BreweryAPIClient:
    """
    Client for retrieving data from the Open Brewery DB API.

    API documentation: https://www.openbrewerydb.org/

    This client supports automatic pagination and collects brewery data
    across multiple pages.
    """

    BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

    def __init__(
        self, 
        per_page: int = 100, 
        max_pages: Optional[int] = None, 
        timeout: int = 10
    ):
        """
        Initialize the Brewery API client.

        Args:
            per_page (int): Number of records per page. Maximum allowed is 100.
            max_pages (Optional[int]): Maximum number of pages to fetch. If None, fetches all.
            timeout (int): Timeout for each API request, in seconds.
        """
        self.per_page = min(per_page, 100)
        self.max_pages = max_pages
        self.timeout = timeout
        self.logger = Logger(name="brewery_api_client").get_logger()

    def fetch_all_breweries(self) -> List[Dict]:
        """
        Fetch all brewery records from the API, paginating automatically.

        Returns:
            List[Dict]: A list of brewery records from the API.
        """
        breweries = []
        page = 1

        while True:
            self.logger.info(f"Fetching page {page} from Brewery API...")
            response = self._make_request(page)
            
            if not response:
                self.logger.info("No more data returned. Stopping fetch.")
                break

            breweries.extend(response)

            if self.max_pages and page >= self.max_pages:
                self.logger.info(f"Maximum page limit reached: {self.max_pages}")
                break

            page += 1

        self.logger.info(f"Total breweries retrieved: {len(breweries)}")
        return breweries

    def _make_request(self, page: int) -> Optional[List[Dict]]:
        """
        Perform a GET request to the API for a specific page.

        Args:
            page (int): Page number to retrieve.

        Returns:
            Optional[List[Dict]]: List of brewery data or None if the request fails.
        """
        try:
            response = requests.get(
                self.BASE_URL,
                params={"page": page, "per_page": self.per_page},
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data if data else None

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch page {page}: {e}")
            return None
