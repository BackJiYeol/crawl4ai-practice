import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilterLXML
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# DefaultMarkdownGenerator: Convert HTML into markdown
md_generator = DefaultMarkdownGenerator(

    # Choose filtering object specifically
    # Pruning filter
    content_filter=PruningContentFilterLXML(

        # Score for object which to filter 
        # threshold=0.4,

        # fixed: fixed standard for score, dynamic: automatic score 
        threshold_type='dynamic'
        # threshold_type='fixed'
    )
)

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator
)

async def main():
    # BrowserConfig: Controls browser behavior (headless/full UI/user agent/JavaScript toggles)
    # CrawlerRunConfig: Controls how each crawl runs (chching, extraction, timeouts, hooking)

    # BrowserConfig()
    # headless=True: crawling behind the scene, without popping up the tab
    # headless=False: popping up the tab, once done crawling(async with) closed immediately 
    browser_config = BrowserConfig(headless=True)


    
    run_config = CrawlerRunConfig(
        # cache_mode= ENABLED, BYPASS, DISABLED, READ_ONLY, WRITE_ONLY
        
        # BYPASS: Always bring latest
        # ENABLED: Update to latest if got else, bring remaning 
        # READ_ONLY: Read copy, no update
        # WRITE_ONLY: Update only, no read

        cache_mode=CacheMode.ENABLED
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com",
            config=config
        )
        print("Raw Markdown length:", 
              len(result.markdown))
        print("Fit Markdown length:",
              len(result.markdown.fit_markdown))

if __name__ == "__main__":
    asyncio.run(main())