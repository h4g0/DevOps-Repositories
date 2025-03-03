# GitHub DevOps Tools Analysis

A data collection and analysis toolkit for gathering insights from GitHub repositories related to DevOps tools.

## Overview

This project contains scripts to collect, process, and analyze data from GitHub repositories focusing on DevOps tools. The toolkit allows you to:

- Fetch repositories based on creation date and popularity
- Process and store repository data in MongoDB
- Run statistical analysis on collected datasets

## Installation

```bash
# Ensure Python 3 is installed
python --version  # Should be 3.6 or higher

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Before using the tool, you must configure API credentials in the `keys.py` file:

### Required Parameters

1. **GitHub API Key (`key`)**
   - Personal access token for GitHub API authentication
   - Generate one at: GitHub → Settings → Developer settings → Personal access tokens
   - Required scopes: `repo`, `read:user`, `read:org`

2. **MongoDB Connection URI (`uri`)**
   - Connection string for your MongoDB database
   - Format: `mongodb://username:password@host:port/database`

### Example Configuration

```python
# keys.py
key = "ghp_YourGitHubPersonalAccessTokenHere"
uri = "mongodb://username:password@localhost:27017/devops_analysis"
```

## Usage

The tool provides several commands through the main script:

### Fetch Repositories

Retrieves repositories from GitHub based on date range and minimum star count.

```bash
python main.py get_repositories  <start_date> <end_date> <min_stars>
```

| Parameter | Format | Description |
|-----------|--------|-------------|
| `start_date` | YYYY-MM-DD | Start date for repository creation |
| `end_date` | YYYY-MM-DD | End date for repository creation |
| `min_stars` | Integer | Minimum star count threshold |

**Example:**
```bash
python main.py get_repositories  2022-01-01 2022-12-31 100
```

### Process Repositories

Process and enrich repository data stored in the database.

```bash
python main.py process
```

This command:
- Retrieves raw repository data from the database
- Enriches it with additional metadata relating to CI/CD technologies used
- Analyzes repository contents
- Updates the database with processed information

### Run Statistics

Execute statistical analysis on a dataset and save results.

```bash
python main.py run_stats <dataset> <stats_folder>
```

| Parameter | Description |
|-----------|-------------|
| `dataset` | Name of the dataset to analyze |
| `stats_folder` | Output folder for statistical results |

**Example:**
```bash
python main.py run_stats devops_tools_2022 ./analysis/stats_results
```

## Example Workflow

```bash
# 1. Set up configuration
vim keys.py
# Edit keys.py with your credentials

# 2. Collect repositories from 2023 with at least 500 stars
python main.py get_repositories 2023-01-01 2023-12-31 500

# 3. Process the collected repositories
python main.py process

# 4. Run statistical analysis
python main.py run_stats devops_2023 ./results
```

## Troubleshooting

- **API Rate Limiting**: GitHub API has rate limits. If you encounter limit errors, wait or use a token with higher limits.
- **MongoDB Connection Issues**: Verify your connection string and ensure MongoDB is running.
- **Missing Dependencies**: Run `pip install -r requirements.txt` to ensure all dependencies are installed.
