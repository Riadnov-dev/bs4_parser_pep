# 🐍 bs4_parser_pep — Python Web Scraper

A **command-line tool** for scraping structured information from the official **Python.org documentation site**.  
Built with **BeautifulSoup4**, **requests-cache**, and robust **logging** for debugging.

---

## 📌 About the Project

**bs4_parser_pep** automates retrieval of structured Python documentation data.  
The scraper is modular, optimized with **HTTP request caching**, and stores results as **CSV files** for further analysis.  

Users can:  
- Parse **PEP indexes** with statuses and metadata  
- Extract the list of **latest Python versions**  
- Collect **"What’s New"** articles for releases  
- Download **documentation files** in PDF  
- Save data in **CSV format**  
- Benefit from detailed **logging** for debugging  

---

## 🧰 Tech Stack

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/BeautifulSoup4-8A2BE2?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Requests-FF9800?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Requests--Cache-4CAF50?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Logging-696969?style=for-the-badge&logo=python&logoColor=white"/>

---

## ✨ Features

- 📜 **PEP index parsing** — fetch all Python Enhancement Proposals with status & metadata  
- 🆕 **Latest versions extraction** — list Python versions and links  
- 📖 **"What’s New" articles** — parse release notes per version  
- 📥 **Documentation download** — grab PDF files from Python.org  
- 🗂️ **CSV export** — structured results for analysis  
- 💾 **HTTP caching** — faster repeated runs, less load on server  
- 🛠️ **Logging** — detailed logs for tracking & debugging  

---



### 🚀 Quick Start

Clone the repository
```
git clone https://github.com/Riadnov-dev/bs4_parser_pep.git
cd bs4_parser_pep/src
```

Create & activate virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies
```
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

Parse all PEPs
```
python main.py pep
```

Get latest versions
```
python main.py latest-versions
```

What's New articles
```
python main.py whats-new
```

Download documentation PDF
```
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

