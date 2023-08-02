import tkinter as tk
from tkinter import ttk
import requests

def get_currency_data():
    base_url = "http://data.fixer.io/api/latest?access_key=6fdd67153cc2da2108ceca771514745e"
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()
        return data.get("rates", {}), list(data.get("rates", {}).keys())
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return {}, []

def calculate_lot_size():
    try:
        deposit_amount = float(deposit_entry.get())

        # Get the exchange rate for the selected deposit currency
        deposit_currency = deposit_currency_entry.get()
        deposit_exchange_rate = exchange_rates.get(deposit_currency, 1.0)
        selected_pair = selected_currency_pair.get()
        selected_pair_exchange_rate = exchange_rates.get(selected_pair, 1.0)

        leverage = int(leverage_entry.get())  
        exchange_rate = float(exchange_rate_entry.get())
        converted_amount = deposit_amount *(selected_pair_exchange_rate / deposit_exchange_rate)

        lot_size = (converted_amount * leverage) / (exchange_rate * 100000)
        lot_size_result.set(f"{lot_size:.2f} lots")
        converted_amount_label.config(text=f"Converted Amount: {converted_amount:.2f} ")
    except ValueError:
        lot_size_result.set("Invalid input")

def update_exchange_rate(*args):
    selected_pair = selected_currency_pair.get()
    if selected_pair:
        exchange_rate = exchange_rates.get(selected_pair)
        if exchange_rate:
            exchange_rate_entry.config(state="normal")  # Enable the entry temporarily to set the value
            exchange_rate_entry.delete(0, "end")  # Clear the current value
            exchange_rate_entry.insert(0, str(exchange_rate))  # Set the new value
            exchange_rate_entry.config(state="disabled")  # Disable the entry again
            exchange_rate_label.config(text=f"Exchange Rate: {exchange_rate:.4f}")
        else:
            exchange_rate_entry.config(state="normal")  # Enable the entry if the rate is not available
            exchange_rate_entry.delete(0, "end")  # Clear the current value
            exchange_rate_entry.config(state="disabled")  # Disable the entry again
            exchange_rate_label.config(text="")
    else:
        exchange_rate_entry.config(state="normal")  # Enable the entry if no pair is selected
        exchange_rate_entry.delete(0, "end")  # Clear the current value
        exchange_rate_entry.config(state="disabled")  # Disable the entry again
        exchange_rate_label.config(text="")

# Create a Tkinter window
root = tk.Tk()
root.title("Lot Size Calculator")


# Create a label for "Currency Pairs with base EURO"
currency_pairs_label = ttk.Label(root, text="Currency pairs with EURO as base")
currency_pairs_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)




# Create entry fields for deposit amount, leverage, and exchange rate
deposit_currency_label = ttk.Label(root, text="Select Deposit Currency")
deposit_currency_label.grid(row=1, column=0, padx=5, pady=5)
deposit_label = ttk.Label(root, text="Initial Deposit Amount")

leverage_label = ttk.Label(root, text="Enter Leverage 1: ")
exchange_rate_label = ttk.Label(root, text="Exchange Rate")

deposit_entry = ttk.Entry(root)
leverage_entry = ttk.Entry(root)
exchange_rate_entry = ttk.Entry(root)

calculate_button = ttk.Button(root, text="Calculate", command=calculate_lot_size)

# Create a label to display the result
lot_size_result = tk.StringVar()
result_label = ttk.Label(root, textvariable=lot_size_result)

# Get currency pairs and exchange rates from the API
exchange_rates, currency_pairs = get_currency_data()

deposit_currency_entry = ttk.Combobox(root, values=currency_pairs , state="readonly")
deposit_currency_entry.set("Select Currency")  # Set a default value for the dropdown
deposit_currency_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a dropdown menu for currency pairs
selected_currency_pair = ttk.Combobox(root, values=currency_pairs, state="readonly")
selected_currency_pair.set("CP with base EURO")  # Set a default value for the dropdown
selected_currency_pair.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a label to display the exchange rate
exchange_rate_label = ttk.Label(root, text="")
exchange_rate_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Bind the callback function to the ComboboxSelected event
selected_currency_pair.bind("<<ComboboxSelected>>", update_exchange_rate)

converted_amount_label = ttk.Label(root, text="")
converted_amount_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


# Grid the remaining widgets
deposit_label.grid(row=2, column=0, padx=5, pady=5)
deposit_entry.grid(row=2, column=1, padx=5, pady=5)
leverage_label.grid(row=3, column=0, padx=5, pady=5)
leverage_entry.grid(row=3, column=1, padx=5, pady=5)
exchange_rate_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

exchange_rate_entry.grid(row=5, column=0, padx=5, pady=5)
calculate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)
result_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
