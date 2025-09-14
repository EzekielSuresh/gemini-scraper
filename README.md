# gemini-scraper

> A concurrent, configurable web scraper powered by scrapling and Gemini for deep scraping of websites.

### Features

- intelligent content extraction and sub-URL discovery by Gemini models
- concurrent scraping of sub-URLs for high efficiency
- structured JSON output for every scraping session
- robust logging to both terminal and log file
- centralized config settings for all runtime options (model, max_worker etc.)

## Getting Started

1. Clone the repository
    ```sh
    git clone https://github.com/EzekielSuresh/gemini-scraper
    cd gemini-scraper
    ```

2. Create a virtual environment
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies
    ```sh
    pip install -r requirements.txt

    # NOTE: Run this command to install browser dependencies 
    scrapling install
    ```

4. Navigate to `config/settings.yaml` and add your Gemini api key
    ```sh
    api_key: "..."
    ```

5. Run the scraper
    ```sh
    python main.py
    ```


## Project Structure

```sh
gemini_scraper/
├── README.md
├── requirements.txt
├── main.py                        # Entry point: orchestrates the scraping workflow
├── scraper/                       # Scraper package
│   ├── __init__.py
│   ├── core_scraper.py            # Main scraping logic
│   ├── concurrent_scraper.py      # Concurrent scraping logic
│   ├── config.py                  # Config loader
│   └── utils.py                   # Helper functions (e.g., extract_suburls, save/load JSON)
├── results/                       # Scraped data storage
│   └── page/
│       ├── page.json
│       ├── subpage_1.json
│       └── ...
├── logs/                          # Log files
│   └── scraper.log
└── config/                        # Configuration files
    └── settings.yaml
```

## Configs

All settings are managed in `config/settings.yaml` for easy customization.

```yaml
model_name: "gemini-2.5-flash-lite"
api_key: "..."
max_workers: 4
output_dir: "results"
```

### Using Environment Variables
Any setting can be overridden at runtime using environment variables (see `scraper/config.py` for exact mappings). This is ideal for secrets (like API keys) and for adapting to different environments (development, production etc.). 

Example:
```sh
export SCRAPER_API_KEY="your-secret-api-key"
python main.py
```

## Logs
All scraping activity is printed to the terminal and stored in a dedicated log file. By default, logs are saved to `logs/scraper.log`.

Each log entry follows this format:
```log
[YYYY-MM-DD HH:MM:SS] | LEVEL | filename.py:line | process_id >>> Message
```

Example:
```log
[2025-09-15 05:24:00] | INFO | core_scraper.py:42 | 12345 >>> Successfully scraped [url]
```

## Contributing

Contributions are welcome! If you have suggestions for improvements, bug fixes or new features, feel free to open an [issue](https://github.com/EzekielSuresh/gemini-scraper).

## License

MIT License © [Ezekiel Suresh Murali](https://github.com/EzekielSuresh)
