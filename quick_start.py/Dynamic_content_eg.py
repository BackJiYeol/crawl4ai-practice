import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy

async def extract_structured_data_using_css_extractor():
    print("\n--- Using JsonCssExtractionStrategy for Fast Structured Output ---")
    schema = {
        "name": "KidoCode Courses",
        "baseSelector": "li.track-six_item",
        "baseFields": [
            {
                "name": "card_clases",
                "type": "attribute",
                "attribute": "class"
            },
        ],
        "fields": [
            {
                "name": "category",
                "selector": ".track-six_eyebrow",
                "type": "text"
            },
            {
                "name": "course_name",
                "selector": ".track-six_name",
                "type": "text"
            },
            {
                "name": "build",
                "selector": ".track-six_build",
                "type": "text"
            },
            {
                "name": "learn",
                "selector": ".track-six_learn",
                "type": "text"
            },
        ],
        # "baseSelector": "section.charge-methodology .w-tab-content > div",
        # "fields": [
        #     {
        #         "name": "section_title",
        #         "selector": "h3.heading-50",
        #         "type": "text",
        #     },
        #     {
        #         "name": "section_description",
        #         "selector": ".charge-content",
        #         "type": "text",
        #     },
        #     {
        #         "name": "course_name",
        #         "selector": ".text-block-93",
        #         "type": "text",
        #     },
        #     {
        #         "name": "course_description",
        #         "selector": ".course-content-text",
        #         "type": "text",
        #     },
        #     {
        #         "name": "course_icon",
        #         "selector": ".image-92",
        #         "type": "attribute",
        #         "attribute": "src",
        #     },
        # ],
    }

    browser_config = BrowserConfig(headless=False, java_script_enabled=True)

    js_click_tabs = """
    (async () => {
        const tabs = document.querySelectorAll("section.charge-methodology .tabs-menu-3 > div");
        for(let tab of tabs) {
            tab.scrollIntoView();
            tab.click();
            await new Promise(r => setTimeout(r, 500));
        }
    })();
    """

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema),
        js_code=[js_click_tabs],
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            # url="https://www.quotes.toscrape.com", config=crawler_config
            url="https://www.kidocode.com/degrees/technology", config=crawler_config
        )

        companies = json.loads(result.extracted_content)
        print(f"Successfully extracted {len(companies)} companies")
        if companies:
            print(json.dumps(companies[0], indent=2))
        else:
            print("Nothing matched. Check the selectors.")
       
async def main():
    await extract_structured_data_using_css_extractor()

if __name__ == "__main__":
    asyncio.run(main())
   
