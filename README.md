# Tayyib Invest

Tayyib Invest is a FastAPI application designed for halal stock validation. It provides endpoints for searching companies and validating their compliance with halal investment principles.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Acknowledgments](#acknowledgments)

## Features

- Search for companies using their names or symbols.
- Validate if a stock is halal based on financial ratios and business sector.
- Generate comprehensive analyses of stocks using AI.

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

1. Create a `.env` file in `tayyib_invest/backend` directory of the project:

   ```plaintext
   GROQ_API_KEY: Your API key for the Groq service.
   FMP_API_KEY: Your API key for the Financial Modeling Prep service.
   ```

## Usage

To run the application, use the following command:

```bash
python -m tayyib_invest.backend.app
```

## API Endpoints

#### 1. POST /v1/search Search

- **Description**: Search for companies based on a query string.
- **Request Body**: 
    ```json
    {
      "query": "string"
    }
    ```
- **Response**:
    - **Success (200)**:
    ```json
    [
      {
        "name": "Company Name (Symbol)",
        "symbol": "Symbol"
      }
     
    ]
    ```
    - **Error (500)**:
    ```json
    {
      "detail": "Error message"
    }
    ```

#### 2. POST /v1/validate_halal_stock Validate Halal Stock

- **Description**: Validate if a stock is halal.
- **Request Body**: 
    ```json
    {
      "ticker": "string"
    }
    ```
- **Response**:
    - **Success (200)**:
    ```json
    {
      "status": "Halal",
      "reason": "Stock is Shariah compliance."
    }
    ```
    - **Error (500)**:
    ```json
    {
      "detail": "Error message"
    }
    ```

#### 3. POST /v1/generate_ai_analysis Generate AI Analysis

- **Description**: Generate an AI analysis for a given stock.
- **Request Body**: 
    ```json
    {
      "ticker": "string"
    }
    ```
- **Response**:
    - **Success (200)**:
    ```json
    "AI-generated analysis content here."
    ```
    - **Error (500)**:
    ```json
    {
      "detail": "Error message"
    }
    ```

#### 4. POST /v1/comprehensive_screening Comprehensive Screening

- **Description**: Perform a comprehensive screening of a stock.
- **Request Body**: 
    ```json
    {
      "ticker": "string"
    }
    ```
- **Response**:
    - **Success (200)**:
    ```json
    {
      "ticker": "TICKER",
      "long_name": "Company Long Name",
      "shariah_compliance": {
        "overall_compliant": {
          "status": "Halal",
          "reason": "Stock is Shariah compliance."
        }
      },
      "ai_analysis": "AI-generated analysis content here."
    }
    ```
    - **Error (500)**:
    ```json
    {
      "detail": "Error message"
    }
    ```
  

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework.
- [yfinance](https://pypi.org/project/yfinance/) for fetching financial data.
- [Groq](https://groq.com/) for LLM capabilities.
