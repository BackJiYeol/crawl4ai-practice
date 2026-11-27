import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai import LLMConfig 

# # Generate a schema (one-time cost)
# html = "<div class='product'><h2>Gaming Laptop</h2><span class='price'>$999.99</span></div>"

# # Using OpenAI (requires API token)
# schema = JsonCssExtractionStrategy.generate_schema(
#     html,
#     llm_config = LLMConfig(provider="openai/gpt-6-luna",api_token="your-openai-token")  # Required for OpenAI
# )

# # Or using Ollama (open source, no token needed)
# schema = JsonCssExtractionStrategy.generate_schema(
#     html,
#     llm_config = LLMConfig(provider="ollama/llama3.3", api_token=None)  # Not needed for Ollama
# )

# # Use the schema for fast, repeated extractions
# strategy = JsonCssExtractionStrategy(schema)

async def main():
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="raw://" + raw_html,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )
        # The JSON output is stored in 'extracted_content'
        data = json.loads(result.extracted_content)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())
