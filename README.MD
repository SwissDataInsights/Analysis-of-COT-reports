# COT Analyst Project

## Description

The **COT Analyst Project** analyzes **Commitment of Traders (COT)** reports to provide insights into the positions of different market participants in futures markets. The project uses Python in a **Jupyter Notebook** environment to automate the process of downloading, processing, and visualizing COT data. This helps identify patterns and trends in trader behavior, which can be useful for making informed trading decisions.

Project Goals:

Market Sentiment Analysis:
The project analyzes the positions held by different groups of traders (e.g., commercial traders, non-commercial traders, hedgers, speculators) to understand the prevailing sentiment in the futures market.

Identification of Trading Patterns:
Based on historical COT reports, it is possible to detect recurring patterns in trader behavior that often precede price changes in the market.

Predictive Modeling:
The project enables the use of machine learning models (e.g., Random Forest, Voting Classifier) to analyze COT data and forecast potential market movements.

---

## Features

1. **Data Retrieval**:
   - Automatically downloads historical COT data from the official CFTC website.
   - Supports data for multiple years (e.g., 2017, 2018, 2019, 2020).

2. **Data Processing**:
   - Extracts and processes data from ZIP files.
   - Cleans and formats COT data for analysis.

3. **Visualization**:
   - Generates charts to visualize trader positions (e.g., Commercial Traders, Non-Commercial Traders).
   - Helps identify trends and sentiment shifts in futures markets.

4. **Model Comparison**:
   - Compares machine learning models (e.g., **Random Forest**, **Voting Classifier**) for analyzing COT data.
   - Provides evaluation metrics and model interpretations.

5. **Interpretation**:
   - Detailed interpretation of model results, including performance metrics such as accuracy, precision, and recall.

---

## Project Structure

```
COT_Analyst/
│-- COT_analyst.ipynb     # Jupyter Notebook with the full analysis
│-- data/                 # Directory for extracted COT data files
└-- README.md             # Project documentation (this file)
```

---

## Requirements

To run this project, you'll need:

- **Python 3.x**
- **Jupyter Notebook**
- **Libraries**:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `requests`
  - `yfinance`
  - `zipfile`

### Installation

You can install the required libraries using the following command:

```bash
pip install pandas numpy matplotlib requests yfinance
```

---

## How to Use the Project

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd COT_Analyst
   ```

2. **Launch Jupyter Notebook**:

   ```bash
   jupyter notebook COT_analyst.ipynb
   ```

3. **Run the Notebook**:
   - Execute each cell sequentially to download data, process it, visualize results, and compare models.
   - Follow the markdown instructions in the notebook to understand each step.

---

## Insights and Analysis

- **COT Data Analysis** helps identify positions held by different trader groups.
- **Model Comparison** offers a quantitative assessment of how different machine learning models perform on the COT data.
- **Visualizations** provide an intuitive understanding of market sentiment and trading patterns.

---

## Potential Improvements

1. **Expand Data Sources**:
   - Include additional years or other futures markets.

2. **Model Optimization**:
   - Explore more machine learning models or optimize current model parameters.

3. **Interactive Visualizations**:
   - Add interactive charts for deeper analysis.

---

## License

This project is licensed under the **MIT License**.

---

**Happy Analyzing!** 📈