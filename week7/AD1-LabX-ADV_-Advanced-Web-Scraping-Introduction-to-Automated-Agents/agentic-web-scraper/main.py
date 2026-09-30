from pathlib import Path
from src.config_parser import ConfigParser
from src.scraper_agent import ScraperAgent
from src.utils import save_data_to_json

def main():
    # Resolve paths from this file so `python main.py` also works when the
    # current directory is the parent folder (for example, week7).
    project_dir = Path(__file__).resolve().parent
    config_path = project_dir / "configs" / "example_site_config.json"
    output_path = project_dir / "data" / "scraped_products.json"

    # 1. Load and parse config
    parser = ConfigParser(config_path)
    config = parser.load_config()

    # 2. Initialize and run scraper agent
    # ปรับ headless=False หากต้องการเปิดเบราว์เซอร์ดูการทำงานจริง
    agent = ScraperAgent(config=config, browser="chrome", headless=True)
    results = agent.run()

    # 3. Save results
    save_data_to_json(results, str(output_path))
    print(
        f"Successfully scraped {len(results)} items and saved to "
        "data/scraped_products.json"
    )

if __name__ == "__main__":
    main()
