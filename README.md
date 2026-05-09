# Pathologist Workload Billing System

A desktop application built for **Trillium Health Partners** to help pathologists log, track, and export their quarterly workload for billing purposes.

## Overview

Pathologists perform many different types of procedures, each mapped to a standardized billing code with an associated unit value. This system lets pathologists record which codes they worked on and in what quantity, then calculates total units worked and exports the data as a quarterly CSV report.

## Features

- **Insert** new case entries (Case ID, part, billing codes + quantities, pathologist name)
- **Update** existing entries by Case ID and part
- **Search** for a specific case by Case ID and part
- **Delete** entries by Case ID and part
- **Display** the full database in a sortable table view
- **Billing Code Dictionary** — browse all ~300 procedure codes and their unit values
- **Save Quarterly Workload** — calculates units worked per entry and exports to a dated CSV (`Q{quarter}_{year}_filename.csv`), then clears the database for the next quarter

## Tech Stack

| Layer | Technology |
|-------|-----------|
| GUI | Python `tkinter` |
| Local storage | SQLite (`sqlite3`) |
| Data processing | `pandas` |
| Language | Python 3 |

## Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd pathologist-billing-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python THP-IS-01.3.py
   ```

> The SQLite database file (`SQL_File.db`) is created automatically on first run and removed after each quarterly export.

## Usage

### Logging work
Click **Insert** and enter:
- **Case ID** — the hospital case identifier
- **Part** — the specimen part (e.g. `A`, `B`)
- **Code/Quantity** — space-separated list of `CODE/quantity` pairs (e.g. `GI140/2 SK100/1`)
- **Pathologist** — the pathologist's name

### Exporting a quarterly report
Click **Save Quarterly Workload**. The app will:
1. Calculate units worked for each entry (`quantity × unit value`)
2. Prompt you to choose a save location
3. Export a CSV prefixed with the current quarter (e.g. `Q2_2026_report.csv`)
4. Clear the database in preparation for the next quarter

### Billing Code Dictionary
Click **Billing Code Dictionary** to browse all procedure codes, their descriptions, and unit values. The dictionary was provided by Dr. Matthew Cesari.

## Project Structure

```
THP-IS-01.3.py     # Main application
requirements.txt   # Python dependencies
```

## License

Built as a contractor project for Trillium Health Partners.
