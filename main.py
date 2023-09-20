import requests
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

def get_price(symbol, interval='1h', limit=60):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    if isinstance(data, list) and isinstance(data[0], list):
        prices = [float(item[4]) for item in data]  # item[4] is the close price
        now = int(time.time() * 1000)
        timestamps = [(now - int(item[0])) / (60 * 1000) for item in data]  # convert to minutes
        return prices, timestamps
    else:
        print(f"Error: Unexpected response from Binance API: {data}")
        return [], []

def update_price():
    symbol = symbol_entry.get()
    prices, timestamps = get_price(symbol)
    price_label.config(text=f"Latest Price: {prices[-1]}")
    draw_graph(prices, timestamps)

def draw_graph(prices, timestamps):
    ax.clear()
    ax.plot(timestamps, prices)  # no need to reverse the lists
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    canvas.draw()

def clear():
    ax.clear()
    canvas.draw()
    price_label.config(text="")

def show_popular_coins():
    popular_coins = get_popular_coins()
    popular_coins_text.delete(1.0, tk.END)
    popular_coins_text.insert(tk.END, "Popular coins:\n" + '\n'.join(popular_coins))

def get_popular_coins(limit=10):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&limit={limit}"
    response = requests.get(url)
    data = response.json()
    coins = [coin['symbol'].upper() + 'USDT' for coin in data]
    return coins

root = tk.Tk()
style = Style(theme='lumen')
root.title("Stockfish")

title = ttk.Label(root, text="Stockfish Stockmarket Beta", font=("Arial", 20))
title.grid(row=0, column=0, columnspan=2)

divider = ttk.Separator(root, orient='horizontal')
divider.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)

symbol_label = ttk.Label(root, text="Symbol:")
symbol_label.grid(row=2, column=0, sticky='nsew')

symbol_entry = ttk.Entry(root)
symbol_entry.grid(row=3, column=0, sticky='nsew')

price_label = ttk.Label(root, text="")
price_label.grid(row=4, column=0, sticky='nsew')

update_button = ttk.Button(root, text="Update", command=update_price)
update_button.grid(row=5, column=0, sticky='nsew')

clear_button = ttk.Button(root, text="Clear", command=clear)
clear_button.grid(row=6, column=0, sticky='nsew')

popular_coins_button = ttk.Button(root, text="Popular Coins", command=show_popular_coins)
popular_coins_button.grid(row=2, column=1, sticky='nsew')

popular_coins_text = tk.Text(root, height=10, width=30)
popular_coins_text.grid(row=3, column=1, rowspan=4, sticky='nsew')

fig, ax = plt.subplots(figsize=(4, 3), dpi=100)  # Adjusted figsize to make the graph smaller
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.draw()
canvas.get_tk_widget().grid(row=7, columnspan=2)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
