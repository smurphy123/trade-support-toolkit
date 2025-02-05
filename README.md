# trade-support-toolkit
Trade Log Monitoring Script

## 📌 Overview
This Python script reads FIX log messages, extracts trade details, and flags potential trade anomalies such as rejected orders.

## 📂 Project Structure

### 📁 trade-support-toolkit 
├── 📄 trade_log_monitor.py 
### Python script to parse trade logs 
├── 📄 sample_fix_log.txt 
### Sample FIX messages 
├── 📄 trade_log_output.csv 
### CSV file with parsed trades (generated) 
├── 📄 README.md # Project documentation


## 🚀 Features
✅ Parses trade logs from FIX messages  
✅ Extracts Order ID, Symbol, Price, and Status  
✅ Flags rejected and unusual trades  
✅ Saves parsed trade data to CSV  

## 🛠️ Setup Instructions
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/trade-support-toolkit.git
   cd trade-support-toolkit

2. **Activate Virtual Environment**
'''bash
python3 -m venv venv
source venv/bin/activate

3. Run the Script
'''bash
python trade_log_monitor.py

📊 Sample Output (trade_log_output.csv)
Order ID	Symbol	Price	Status
10001	AAPL	150.25	Filled
10002	TSLA	750.50	🚨 Rejected!
10003	GOOGL	2800.75	Partially Filled
10004	MSFT	320.00	Canceled


📌 **How to Create the File:**  
1. In your repo folder, run:
   ```bash
   touch README.md
