# TMDB Media Scraper

A web scraper for collecting information about top-rated movies and TV shows from [The Movie Database (TMDB)](https://www.themoviedb.org/).

## Features

- Supports scraping both movies and TV shows
- Automatically retrieves TMDB's highest-rated media list
- Scrapes TOP 250 movies and TOP 150 TV shows by default
- Saves media links locally and supports resume functionality
- Collects title, overview, and main cast for each media item
- Data saved in JSON format

## Requirements

1. Python 3.6+
2. Google Chrome Browser
3. Required Python packages:
    ```bash
    pip install selenium
    ```

4. ChromeDriver:
   - Download from [ChromeDriver download page](https://sites.google.com/chromium.org/driver/)
   - Make sure to download the version matching your Chrome browser
   - Place the driver in a directory included in your system's PATH

## Usage

1. To scrape movies:
    ```python
    from media_scraper import MediaScraper

    movie_scraper = MediaScraper(media_type='movie')
    movie_scraper.run()
    ```

2. To scrape TV shows:
    ```python
    from media_scraper import MediaScraper

    tv_scraper = MediaScraper(media_type='tv')
    tv_scraper.run()
    ```

## Output Files

The script generates the following files:

- `movie_links.json`: Contains scraped movie URLs
- `movies.json`: Contains detailed movie information
- `tv_links.json`: Contains scraped TV show URLs
- `tvs.json`: Contains detailed TV show information

## Data Format

The scraped data is structured as follows:

```json
{
    "title": "Media title",
    "overview": "Plot summary",
    "cast": ["Character 1", "Character 2", ...],
    "url": "TMDB page URL"
}
```


## Important Notes

1. Ensure a stable internet connection
2. Consider adjusting scraping intervals to respect the website's rate limits
3. The script supports resuming from where it left off if interrupted
4. Please respect TMDB's terms of service and scraping guidelines

## Contributing

Feel free to open issues or submit pull requests if you have any improvements or bug fixes.

## License

MIT License