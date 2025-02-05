# Python script that monitors trade logs, extracts key trade data, and flags potential issues.

import re
import csv

# Sample FIX log entry: "8=FIX.4.2|35=8|11=123456|17=654321|55=AAPL|54=1|38=100|44=150.25|39=2|"
FIX_PATTERN = r"11=(?P<order_id>\d+).*?55=(?P<symbol>\w+).*?44=(?P<price>[\d.]+).*?39=(?P<status>\d+)"

# Mapping FIX status codes for clarity
FIX_STATUS = {
    "0": "New",
    "1": "Partially Filled",
    "2": "Filled",
    "4": "Canceled",
    "8": "Rejected"
}

def parse_fix_log(file_path):
    trade_data = []
    with open(file_path, "r") as file:
        for line in file:
            match = re.search(FIX_PATTERN, line.replace("|", " "))  # FIX uses | as delimiter
            if match:
                order_id = match.group("order_id")
                symbol = match.group("symbol")
                price = float(match.group("price"))
                status = FIX_STATUS.get(match.group("status"), "Unknown")

                # Detect anomalies (e.g., rejected trades)
                if status == "Rejected":
                    print(f"ALERT: Order {order_id} for {symbol} was REJECTED!")

                trade_data.append([order_id, symbol, price, status])

    return trade_data

def save_to_csv(trade_data, output_file="trade_log_output.csv"):
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Order ID", "Symbol", "Price", "Status"])
        writer.writerows(trade_data)
    print(f"Trade log analysis saved to {output_file}")

if __name__ == "__main__":
    trade_log = "sample_fix_log.txt"  # Replace with actual log file path
    parsed_trades = parse_fix_log(trade_log)
    save_to_csv(parsed_trades)


