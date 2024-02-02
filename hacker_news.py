from contextlib import suppress
from dataclasses import dataclass
from pprint import pprint
from urllib.parse import urljoin
from typing import Optional

from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse


scrapfly = ScrapflyClient(key="scp-live-8a1e940f91e64100a2f5df069ed65a8f")

api_response: ScrapeApiResponse = scrapfly.scrape(
    ScrapeConfig(
        url="https://news.ycombinator.com/",
    )
)


@dataclass
class Article:
    title:Optional[str]=None
    rank:Optional[int]=None
    link:Optional[str]=None
    user:Optional[str]=None
    score:Optional[int]=None
    comments:Optional[int]=None

    def is_valid(self) -> bool:
        if self.title is None or self.link is None:
            return False

        return True

print(api_response)