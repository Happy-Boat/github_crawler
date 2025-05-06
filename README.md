# GitHub Crawler

## Project Introduction
The `GitHub Crawler` is a tool designed to scrape relevant information about GitHub users and generate visual charts. It can retrieve the followers, followings of specified users, and the follow relationships between these users. Finally, it presents these relationships in the form of a network graph on an HTML page.

## Features
1. **Data Scraping**: Capable of scraping the followers, followings of specified GitHub users, and the follow relationships between them.
2. **Data Storage**: Saves the scraped data as JSON files for subsequent analysis and usage.
3. **Visualization**: Generates an independent HTML file based on the scraped data, using the D3.js library to draw a network graph of GitHub follow relationships.

## Installation Dependencies
This project is implemented using Python and JavaScript. The following dependencies need to be installed:
- Python 3.x
- `requests` library: Used to send HTTP requests and obtain GitHub API data.
- `json` library: Used to handle JSON data.
- `time` library: Used for time-related operations, such as waiting for API rate limits.
- `threading` library: Used for multi-threaded processing to improve data scraping efficiency.
- D3.js: Used to draw network graphs.

You can install the Python dependencies using the following command:
```bash
pip install requests
```

## Usage Instructions

### 1. Configure GitHub Token
In the `github_crawler/fetch.py` file, find the `GITHUB_TOKEN` variable and replace it with your own GitHub Token. The GitHub Token is used to authenticate requests and avoid rate limits caused by unauthenticated requests.
```python
GITHUB_TOKEN = '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'
```

### 2. Run the Data Scraping Script
Run the following command in the terminal to start the data scraping script:
```bash
python github_crawler/fetch.py
```
This script will scrape the followers, followings of the specified user (default is `hwfan`), and the follow relationships between these users, and save the data as `followers.json`, `following.json`, and `relationship.json` files.

### 3. Generate the Visualization HTML File
Run the following command to generate an independent HTML file:
```bash
python github_crawler/generate_web.py
```
This script will read the data from the `followers.json`, `following.json`, and `relationship.json` files and generate an HTML file named `standalone_follow_graph.html` to display the GitHub follow relationship network graph.

### 4. View the Visualization Results
Open the generated `standalone_follow_graph.html` file in a browser to view the GitHub follow relationship network graph. You can click on the nodes to highlight the follow relationship between two nodes.

## Code Structure
- `github_crawler/star_fetch.py`: Used to scrape the starred repositories of a specified user and save the data as a `star.json` file.
- `github_crawler/fetch.py`: Used to scrape the followers, followings of a specified user, and the follow relationships between these users, and save the data as `followers.json`, `following.json`, and `relationship.json` files.
- `github_crawler/generate_web.py`: Used to read the data from the `followers.json`, `following.json`, and `relationship.json` files and generate an independent HTML file to display the GitHub follow relationship network graph.
- `github_crawler/relationship.json`: Stores the scraped follow relationship data between users.
- `github_crawler/followers.json`: Stores the list of followers of the specified user.
- `github_crawler/following.json`: Stores the list of followings of the specified user.
- `github_crawler/standalone_follow_graph.html`: The generated independent HTML file used to display the GitHub follow relationship network graph.

## Notes
- Ensure that you have correctly configured the GitHub Token; otherwise, requests may fail due to rate limits.
- Since the GitHub API has rate limits, scraping a large amount of data may take a long time. Please be patient.
- This project is only for learning and research purposes. Please comply with GitHub's terms of use and API rules.

## Contribution
If you find any issues or have suggestions for improvement, please feel free to submit an Issue or a Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).
