# Company Email Scraper

This repository contains a Python script that scrapes company information and emails from various tower websites in Moscow. It utilizes `selenium` for web scraping and `BeautifulSoup` for parsing HTML.

## Features

- Scrapes multiple websites for company information and emails
- Outputs data in both JSON and CSV formats
- Headless ChromeDriver for improved performance

## How to Run

Ensure you have Python installed on your system, and then install the necessary dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python scraper.py
```

## Scheduling

The script can be scheduled to run automatically every 7 days using cron jobs (Linux/Mac) or Task Scheduler (Windows).

## Contributing

Please feel free to submit pull requests with improvements or open an issue if you find any bugs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
