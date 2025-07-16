# 🏏 Cricsheet Match Data Analysis

This project is a complete data pipeline for scraping, processing, storing, and analyzing cricket match data from [Cricsheet](https://cricsheet.org/matches/). It leverages Python, SQL, and visualization libraries to generate actionable insights from historical cricket matches across formats like Test, ODI, and T20.

---

## 📁 Project Structure

```text
Cricsheet_analysis/
├── scraping/              # Step 1: Scrapes match JSONs using Selenium
│   └── cricsheet_scraper.py
├── processing/            # Step 2: Converts JSONs to Pandas DataFrames
│   └── json_to_df.py
├── database/              # Step 3: Loads data into SQLite & runs SQL queries
│   ├── load_to_sqlite.py
│   └── run_query.py
├── sql/                   # SQL query files for analysis
│   └── analysis_queries.sql
├── eda/                   # Step 5: EDA visualizations with plots saved
│   ├── eda_analysis.py
│   └── plots/
├── run_all_queries.py     # Step 4: Executes consolidated queries
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```


## ⚙️ How to Run This Project

### ✅ Step 0: Install Requirements

Make sure Python is installed, then install all dependencies:

```bash
pip install -r requirements.txt
```
Note: No need to download chromedriver manually — it's handled via webdriver_manager.

🔁 Execution Steps
---
1️⃣ Scrape Match Data (JSON)
Downloads JSON data for all formats from Cricsheet:

```bash
python scraping/cricsheet_scraper.py
```

 ---
🧑‍💻 Special Setup for GitHub Codespaces
If you are running this project in GitHub Codespaces, follow these extra steps to install Google Chrome for Selenium:

🧩 Why?
GitHub Codespaces does not include Google Chrome by default. Selenium needs Chrome to run the scraper (even in headless mode).

✅ One-Time Setup in Terminal
Copy and paste the following commands into the Codespaces terminal:

```bash
sudo apt update
sudo apt install -y wget curl gnupg unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
```
✅ Then run the scraper like normal:
```bash
python scraping/cricsheet_scraper.py
```
 ---
2️⃣ Convert JSONs to CSV
Processes all downloaded JSONs and stores as matches.csv and deliveries.csv:

```bash
python processing/json_to_df.py
```
3️⃣ Load CSV to SQLite
Creates a SQLite database and loads the CSV data into tables:

```bash
python database/load_to_sqlite.py
```
4️⃣ Run SQL Queries
Executes predefined SQL queries on the database:

```bash
python database/run_query.py
```
5️⃣ Run Additional Queries
Executes additional summary queries for quick stats:

```bash
python run_all_queries.py
```
6️⃣ Perform EDA and Generate Visualizations
Runs exploratory data analysis and saves plots to the eda/plots/ folder:

```bash
python eda/eda_analysis.py
```
📦 Requirements
The following Python libraries are used:

```nginx
matplotlib
pandas
plotly
requests
seaborn
selenium
tqdm
webdriver_manager
```
📌 Notes
---
✅ JSON and zip data are saved in data/json/ and data/zips/ (excluded from GitHub).

✅ SQLite database file is stored in database/.

✅ Visual plots are saved in eda/plots/.

❌ Files like chromedriver.exe, raw data, and output images are ignored from version control via .gitignore.

🧰 Tech Stack
---
- **Web Scraping**: Selenium, webdriver_manager

- **Data Wrangling**: Pandas

- **Database**: SQLite, SQL queries

- **Visualization**: Matplotlib, Seaborn, Plotly

- **Dashboards**: Power BI
 
- **Automation**: Python scripting
 

🧠 Outcome
---
This project showcases end-to-end automation of:

- Scraping cricket match data

- Structuring it into relational form

- Performing SQL-based analysis

- Visual storytelling with Python

- It can help data analysts, sports analysts, and enthusiasts derive powerful cricket insights using code.
---

## 📁 Project Deliverables

The following files are required for submission and are included in the `deliverables/` folder:

| File | Description |
|------|-------------|
| [Cricsheet Match Data Analysis.pptx](./deliverables/Cricsheet%20Match%20Data%20Analysis.pptx) | Final project presentation containing overview, methodology, EDA visuals, and key insights |
| [cricsheet.pbix](./deliverables/cricsheet.pbix) | Power BI dashboard showing interactive visual analysis of the cricket dataset |



---
👤 Jaisrinivas P K
--
This project was developed as part of the GUVI Capstone submission for the Cricsheet Match Data Analysis project.
