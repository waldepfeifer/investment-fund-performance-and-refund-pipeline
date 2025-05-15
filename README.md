<img width="1485" alt="image" src="https://github.com/user-attachments/assets/46d02092-5bf6-4610-ad15-31b58d47bd30" />


# Investment Fund Performance and Refund Pipeline

## 📖 Project Overview

This project provides an automated pipeline to:

- **Analyze the quarterly performance** of an investment fund portfolio compared to a benchmark index (e.g., SPX500)
- **Calculate investor-specific refunds** based on individual investments and market performance

The system is designed for portfolio managers and data teams to generate reports and manage client reimbursements with full data traceability.

## 🎯 Objectives

- Load and clean market price data
- Calculate fund performance by quarter
- Compare fund returns vs benchmark index
- Load user investment data
- Calculate and allocate refunds to users based on underperformance
- Export reports and results for further analysis

## 🛠 Technologies Used

- Python 3.x
- Pandas
- Matplotlib
- CSV data files
- Command-line scripts

## 📂 Project Structure

investment_fund_quarterly_performance_analysis.ipynb  
investment_user_refunds_calculation.py  
market_data/ (folder with CSV price data)  
users.csv (user investment file)  
users_refund.csv (generated refund results)  
README.md  
requirements.txt (optional)

## 🚀 How It Works

### 1️⃣ Analyze Quarterly Fund Performance

Open and run `investment_fund_quarterly_performance_analysis.ipynb`:

- Load historical price data from `market_data/` folder
- Calculate returns for fund holdings
- Plot quarterly returns of fund vs SPX500 benchmark
- Visualize fund composition using pie charts
- Export any intermediate or final data as needed

The fund holdings are defined as:

- Facebook (Meta) (15%)
- Netflix (10%)
- Apple (25%)
- Tesla (15%)
- Google (Alphabet) (20%)
- Amazon (15%)

### 2️⃣ Calculate Investor Refunds

Run the user refund calculation as a script:

(Here you would normally use a bash command like)  
python3 investment_user_refunds_calculation.py

The script will:

- Load user investments from `users.csv`
- Load market prices from `market_data/`
- Calculate how much each user should be refunded if the fund underperformed
- Export `users_refund.csv` with final refund amounts by user

### Example `users.csv` Format

user_id, amount_invested  
1001, 5000  
1002, 10000  
1003, 7500  

### Example `users_refund.csv` Output

user_id, refund_amount  
1001, 150  
1002, 300  
1003, 225  

## ⚙ Data Assumptions

- All price data must be in `market_data/` folder with filenames formatted as `<SYMBOL>_market_data.csv`
- User investments are read from `users.csv`
- Refund logic and fund composition are defined in the scripts

## 📝 Example Workflow

1. Monthly market data CSVs are added to `market_data/`
2. User investment data is prepared in `users.csv`
3. Jupyter notebook is run for fund performance analysis
4. Python script is executed for automated refund calculations
5. `users_refund.csv` file is generated for finance team

## ⚠ Notes

- Ensure all CSV files follow the correct formatting
- All date columns must be parseable by pandas as datetime
- The project is designed for educational and prototype use; additional validations may be required for production use

## 📜 License

This project is licensed under the MIT License. See LICENSE file for details.
