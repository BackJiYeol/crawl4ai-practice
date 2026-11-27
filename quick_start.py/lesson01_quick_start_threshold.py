import pandas as pd
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilterLXML
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

URL = "https://quotes.toscrape.com"

async def main():

    # Result for different md_generator threshold
    rows = []

    async with AsyncWebCrawler() as crawler:

        for t_type in ["fixed", "dynamic"]:
            for threshold in [None, 0.2, 0.4, 0.6, 0.8]:
                md_generator = DefaultMarkdownGenerator(
                    content_filter=PruningContentFilterLXML(
                        threshold=threshold,
                        threshold_type=t_type,
                    )
                        )
                config = CrawlerRunConfig(
                    cache_mode=CacheMode.BYPASS,
                    markdown_generator=md_generator,
                )
                result = await crawler.arun(url=URL, config=config)

                raw_len = len(result.markdown.raw_markdown)
                fit_len = len(result.markdown.fit_markdown)

                rows.append({
                    "type": t_type,
                    "threshold": threshold,
                    "raw_chars": raw_len,
                    "fit_chars": fit_len,
                    "kept_%": round((fit_len/raw_len)*100, 1),
                    "quotes_kept": result.markdown.fit_markdown.count('“')
                })

    df = pd.DataFrame(rows)
    fixed_df = df[df["type"] == "fixed"]
    dynamic_df = df[df["type"] == "dynamic"]
    print(fixed_df.to_string(index=False))
    print(dynamic_df.to_string(index=False))
    df.to_csv("threshold_results.csv", index=False)

asyncio.run(main())
