# Tayyib Invest

Tayyib Invest is a FastAPI application designed for halal stock validation. It provides endpoints for searching companies and validating their compliance with halal investment principles.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features

- Search for companies using a query string.
- Validate if a stock is halal based on financial ratios and business sector.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ade-mola/tayyib-invest.git
   cd tayyib_invest
   ```

2. Install Poetry:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
   Alternatively, follow the installation instructions from the [official Poetry documentation](https://python-poetry.org/docs/#installation).

3. Create a virtual environment and install the required dependencies in the `pyproject.toml` file:
  
    ```bash
      poetry config virtualenvs.in-project false
      poetry shell
      poetry install
      ```

## Configuration

1. Create a `.env` file in the root directory of the project:

   ```plaintext
   FMP_API_KEY=your_api_key_here
   ```

2. Replace `your_api_key_here` with your actual API key from Financial Modeling Prep.

## Usage

To run the application, use the following command:

```bash
python tayyib_invest/app.py
```

## API Endpoints

### Search Company

- **Endpoint:** `POST /v1/search`
- **Request Body:**
  ```json
  {
      "query": "company_name"
  }
  ```
- **Response:**
  ```json
  {
      "results": [
          {
              "name": "Company Name (Symbol)",
              "symbol": "Symbol"
          }
      ]
  }
  ```

### Validate Halal Stock

- **Endpoint:** `POST /v1/validate_halal_stock`
- **Request Body:**
  ```json
  {
      "ticker": "AAPL"
  }
  ```
- **Response:**
  ```json
  {
      "status": "Halal",
      "reason": "Stock is Shariah compliant."
  }
  ```
