# 🐍 bs4_parser_pep — Python Web Scraper for Python.org
A command-line tool to scrape structured information from the official Python documentation website. Supports extracting PEP indexes, latest versions, "What's New" articles, and downloading documentation files. Built with BeautifulSoup for HTML parsing, requests-cache for HTTP caching, and robust logging for debugging.

## 📌 Description
bs4_parser_pep automates the retrieval of structured Python documentation data.
The scraper is modular, easy to extend, and optimized with request caching to reduce load on the Python.org server.
Outputs are stored as CSV files for further analysis.

Key features:

📜 PEP index parsing — fetch all Python Enhancement Proposals with status and metadata

🆕 Latest versions extraction — list all Python versions and links

📖 "What's New" articles — parse release notes for each Python version

📥 Documentation download — get selected PDF documentation files

🗂 CSV export — structured results for further processing

💾 HTTP caching — speed up repeated runs

🛠 Logging — detailed logs for debugging and tracking


## 🛠 Tech Stack

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-HTML%20parser-8A2BE2?logo=python)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/Requests-HTTP%20client-FF9800?logo=python)](https://requests.readthedocs.io/)
[![Requests-Cache](https://img.shields.io/badge/Requests--Cache-HTTP%20caching-4CAF50?logo=python)](https://requests-cache.readthedocs.io/)
[![Logging](https://img.shields.io/badge/Logging-built--in-lightgrey?logo=python)](https://docs.python.org/3/library/logging.html)



### 🚀 Quick Start
```
# Clone the repository
git clone https://github.com/Riadnov-dev/bs4_parser_pep.git
cd bs4_parser_pep/src

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### ⚙️ Usage
Run from the src directory with a chosen mode:

```
cd src
python main.py [mode]
```

Available modes:

pep — Parse the PEP index and retrieve details for each PEP

latest-versions — Get the list of latest Python versions

whats-new — Parse "What's New" articles for Python releases

download — Download selected Python documentation PDFs

📂 Example Commands
```
# Parse all PEPs
python main.py pep

# Get latest versions
python main.py latest-versions

# What's New articles
python main.py whats-new

# Download documentation PDF
python main.py download
```

### 📊 Output
Results are saved as .csv in:

```
src/results/
```
Example:
```
pep_statuses.csv
```

### 🔐 Logging
Logging is configured in configs.py.
Levels:

INFO — progress updates

DEBUG — detailed parsing flow

ERROR — parsing failures

### 💾 Caching
requests_cache stores HTTP responses locally

Improves repeated runs speed

Reduces requests to Python.org

### 📂 Project Structure

```
bs4_parser_pep/
├── src/
│   ├── configs.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── main.py
│   ├── outputs.py
│   ├── utils.py
│   └── results/
│       └── pep_statuses.csv
├── requirements.txt
└── README.md
```

### 👤 Author

Nikita Riadnov

GitHub: https://github.com/Riadnov-dev

