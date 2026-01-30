# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import websocket
import json
import threading
import requests

class BTCRealtimeGUI:
    """GUI hien dai de theo doi gia Bitcoin real-time"""

    def __init__(self, root):
        self.root = root
        self.root.title("Bitcoin Real-Time Price Tracker")
        self.root.geometry("600x500")
        self.root.configure(bg='#1e1e1e')

        # WebSocket
        self.ws = None
        self.ws_ticker = None
        self.running = False

        # Bien luu gia tri
        self.current_price = 0
        self.previous_price = 0
        self.price_history = []
        self.max_history = 50
        self.high_24h = 0
        self.low_24h = 0

        # Currency and Asset selection
        self.current_asset = "BTC"  # Default asset
        self.current_currency = "USD"  # USD or VND
        self.usd_to_vnd = 25000  # Ty gia USD/VND

        # Danh sach cac coin - se load tu Binance API
        self.available_coins = {}
        self.all_coin_list = []  # Danh sach tat ca coin cho search
        self.coins_loaded = False

        self.setup_ui()

        # Load coins in background thread
        load_thread = threading.Thread(target=self.load_coins_from_binance, daemon=True)
        load_thread.start()

    def load_coins_from_binance(self):
        """Load tat ca coins tu Binance API"""
        try:
            # Get all trading pairs from Binance
            url = "https://api.binance.com/api/v3/exchangeInfo"
            response = requests.get(url, timeout=10)
            data = response.json()

            # Filter only USDT pairs
            usdt_pairs = []
            for symbol_info in data['symbols']:
                if (symbol_info['symbol'].endswith('USDT') and
                    symbol_info['status'] == 'TRADING' and
                    symbol_info['quoteAsset'] == 'USDT'):

                    base_asset = symbol_info['baseAsset']
                    symbol = symbol_info['symbol']

                    # Skip some pairs
                    if any(x in base_asset for x in ['UP', 'DOWN', 'BULL', 'BEAR']):
                        continue

                    usdt_pairs.append({
                        'code': base_asset,
                        'symbol': symbol,
                        'name': base_asset  # Ten mac dinh la code
                    })

            # Sort by code
            usdt_pairs.sort(key=lambda x: x['code'])

            # Build available_coins dictionary
            coin_colors = self.get_default_colors()
            for pair in usdt_pairs:
                code = pair['code']
                self.available_coins[code] = {
                    'name': pair['name'],
                    'symbol': pair['symbol'],
                    'color': coin_colors.get(code, '#ffffff')
                }
                self.all_coin_list.append(f"{code} - {pair['name']}")

            print(f"Loaded {len(self.available_coins)} coins from Binance")
            self.coins_loaded = True

        except Exception as e:
            print(f"Error loading coins from Binance: {e}")
            # Fallback to default popular coins
            self.load_default_coins()

    def get_default_colors(self):
        """Tra ve mau mac dinh cho cac coin pho bien"""
        return {
            "BTC": "#f7931a",
            "ETH": "#627eea",
            "BNB": "#f3ba2f",
            "XRP": "#23292f",
            "SOL": "#14f195",
            "ADA": "#0033ad",
            "DOGE": "#c2a633",
            "TRX": "#ff0013",
            "AVAX": "#e84142",
            "SHIB": "#ffa409",
            "DOT": "#e6007a",
            "MATIC": "#8247e5",
            "LTC": "#345d9d",
            "UNI": "#ff007a",
            "LINK": "#2a5ada",
            "ATOM": "#2e3148",
            "XLM": "#14b6e7",
            "ETC": "#328332",
            "BCH": "#8dc351",
            "PAXG": "#FFD700",
        }

    def load_default_coins(self):
        """Load danh sach coin mac dinh neu API loi"""
        default_coins = {
            "BTC": {"name": "Bitcoin", "symbol": "BTCUSDT", "color": "#f7931a"},
            "ETH": {"name": "Ethereum", "symbol": "ETHUSDT", "color": "#627eea"},
            "BNB": {"name": "Binance Coin", "symbol": "BNBUSDT", "color": "#f3ba2f"},
        }
        self.available_coins = default_coins
        self.all_coin_list = [f"{code} - {info['name']}" for code, info in default_coins.items()]

    def setup_ui(self):
        """Thiet lap giao dien"""
        # Title with asset selector
        title_frame = tk.Frame(self.root, bg='#2d2d2d', pady=15)
        title_frame.pack(fill='x', padx=10, pady=10)

        self.title_label = tk.Label(
            title_frame,
            text="BITCOIN REAL-TIME TRACKER",
            font=('Arial', 20, 'bold'),
            bg='#2d2d2d',
            fg='#f7931a'
        )
        self.title_label.pack()

        # Asset and Currency selector frame
        selector_frame = tk.Frame(self.root, bg='#2d2d2d', pady=10)
        selector_frame.pack(fill='x', padx=10)

        # Asset selector with search
        asset_label = tk.Label(
            selector_frame,
            text="Coin:",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        )
        asset_label.pack(side='left', padx=(20, 10))

        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)

        self.search_entry = tk.Entry(
            selector_frame,
            textvariable=self.search_var,
            font=('Arial', 10),
            width=15,
            bg='#ffffff',
            fg='#000000'
        )
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.insert(0, "BTC")

        # Search button
        search_btn = tk.Button(
            selector_frame,
            text="🔍 Search",
            command=self.show_coin_list,
            font=('Arial', 9),
            bg='#555555',
            fg='#ffffff',
            padx=10,
            pady=4,
            cursor='hand2'
        )
        search_btn.pack(side='left', padx=5)

        # Selected coin label
        self.selected_coin_label = tk.Label(
            selector_frame,
            text="Bitcoin (BTC)",
            font=('Arial', 10, 'bold'),
            bg='#2d2d2d',
            fg='#f7931a'
        )
        self.selected_coin_label.pack(side='left', padx=10)

        # Currency selector
        currency_label = tk.Label(
            selector_frame,
            text="Currency:",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        )
        currency_label.pack(side='left', padx=(40, 10))

        self.usd_btn = tk.Button(
            selector_frame,
            text="USD",
            command=self.switch_to_usd,
            font=('Arial', 10, 'bold'),
            bg='#00aa00',
            fg='#ffffff',
            padx=15,
            pady=5,
            relief='sunken',
            bd=2,
            cursor='hand2'
        )
        self.usd_btn.pack(side='left', padx=5)

        self.vnd_btn = tk.Button(
            selector_frame,
            text="VND",
            command=self.switch_to_vnd,
            font=('Arial', 10, 'bold'),
            bg='#444444',
            fg='#ffffff',
            padx=15,
            pady=5,
            relief='raised',
            bd=2,
            cursor='hand2'
        )
        self.vnd_btn.pack(side='left', padx=5)

        # Main price display
        self.price_frame = tk.Frame(self.root, bg='#2d2d2d', pady=20)
        self.price_frame.pack(fill='x', padx=10, pady=10)

        # Price label
        self.price_label = tk.Label(
            self.price_frame,
            text="$0.00",
            font=('Arial', 48, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.price_label.pack()

        # Change indicator
        self.change_label = tk.Label(
            self.price_frame,
            text="UP +0.00",
            font=('Arial', 14),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.change_label.pack(pady=5)

        # Info frame
        info_frame = tk.Frame(self.root, bg='#2d2d2d', pady=15)
        info_frame.pack(fill='x', padx=10, pady=10)

        # Grid layout for info - 2 columns
        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)

        # 24H High
        high_title = tk.Label(
            info_frame,
            text="24H HIGH",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        )
        high_title.grid(row=0, column=0, sticky='n', padx=20)

        self.high_label = tk.Label(
            info_frame,
            text="$0.00",
            font=('Arial', 18, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.high_label.grid(row=1, column=0, sticky='n', padx=20, pady=5)

        # 24H Low
        low_title = tk.Label(
            info_frame,
            text="24H LOW",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        )
        low_title.grid(row=0, column=1, sticky='n', padx=20)

        self.low_label = tk.Label(
            info_frame,
            text="$0.00",
            font=('Arial', 18, 'bold'),
            bg='#2d2d2d',
            fg='#ff0000'
        )
        self.low_label.grid(row=1, column=1, sticky='n', padx=20, pady=5)

        # Status bar
        status_frame = tk.Frame(self.root, bg='#1a1a1a', pady=10)
        status_frame.pack(side='bottom', fill='x')

        self.status_label = tk.Label(
            status_frame,
            text="[*] Disconnected",
            font=('Arial', 10),
            bg='#1a1a1a',
            fg='#ff0000'
        )
        self.status_label.pack(side='left', padx=20)

        # Control buttons
        button_frame = tk.Frame(self.root, bg='#1e1e1e')
        button_frame.pack(side='bottom', pady=15)

        self.start_btn = tk.Button(
            button_frame,
            text="▶ START",
            command=self.start_tracking,
            font=('Arial', 14, 'bold'),
            bg='#00cc00',
            fg='#ffffff',
            activebackground='#00ff00',
            activeforeground='#000000',
            padx=40,
            pady=12,
            relief='raised',
            bd=3,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=10)

        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ STOP",
            command=self.stop_tracking,
            font=('Arial', 14, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            activebackground='#ff0000',
            activeforeground='#ffffff',
            padx=40,
            pady=12,
            relief='raised',
            bd=3,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)

        # Coin list popup (hidden by default)
        self.coin_list_window = None

    def on_search_change(self, *args):
        """Callback khi search text thay doi"""
        # Auto search khi go
        pass

    def show_coin_list(self):
        """Hien thi popup list cac coin"""
        if not self.coins_loaded or len(self.all_coin_list) == 0:
            # Show loading message
            tk.messagebox.showinfo("Loading", "Coins are still loading. Please wait...")
            return

        if self.coin_list_window is not None:
            self.coin_list_window.destroy()

        # Create popup window
        self.coin_list_window = tk.Toplevel(self.root)
        self.coin_list_window.title("Select Coin")
        self.coin_list_window.geometry("400x500")
        self.coin_list_window.configure(bg='#2d2d2d')

        # Search frame in popup
        search_frame = tk.Frame(self.coin_list_window, bg='#2d2d2d', pady=10)
        search_frame.pack(fill='x', padx=10)

        tk.Label(
            search_frame,
            text="Search:",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left', padx=5)

        popup_search_var = tk.StringVar()
        popup_search_entry = tk.Entry(
            search_frame,
            textvariable=popup_search_var,
            font=('Arial', 10),
            width=30
        )
        popup_search_entry.pack(side='left', padx=5, fill='x', expand=True)

        # Listbox with scrollbar
        list_frame = tk.Frame(self.coin_list_window, bg='#2d2d2d')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        coin_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 10),
            bg='#1e1e1e',
            fg='#ffffff',
            selectbackground='#f7931a',
            selectforeground='#000000',
            yscrollcommand=scrollbar.set,
            height=20
        )
        coin_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=coin_listbox.yview)

        # Populate list
        def update_coin_list(search_text=""):
            coin_listbox.delete(0, tk.END)
            search_text = search_text.upper()

            for coin_str in self.all_coin_list:
                if search_text in coin_str.upper():
                    coin_listbox.insert(tk.END, coin_str)

        # Initial population
        update_coin_list()

        # Update list on search
        def on_popup_search(*args):
            update_coin_list(popup_search_var.get())

        popup_search_var.trace('w', on_popup_search)

        # Select coin on double click
        def on_coin_select(event):
            selection = coin_listbox.curselection()
            if selection:
                selected_text = coin_listbox.get(selection[0])
                coin_code = selected_text.split(" - ")[0]
                self.select_coin(coin_code)
                self.coin_list_window.destroy()

        coin_listbox.bind('<Double-Button-1>', on_coin_select)

        # Select button
        btn_frame = tk.Frame(self.coin_list_window, bg='#2d2d2d', pady=10)
        btn_frame.pack(fill='x', padx=10)

        def on_select_btn():
            selection = coin_listbox.curselection()
            if selection:
                selected_text = coin_listbox.get(selection[0])
                coin_code = selected_text.split(" - ")[0]
                self.select_coin(coin_code)
                self.coin_list_window.destroy()

        tk.Button(
            btn_frame,
            text="Select",
            command=on_select_btn,
            font=('Arial', 10, 'bold'),
            bg='#00aa00',
            fg='#ffffff',
            padx=20,
            pady=5
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=self.coin_list_window.destroy,
            font=('Arial', 10, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            padx=20,
            pady=5
        ).pack(side='left', padx=5)

    def select_coin(self, coin_code):
        """Chon coin va cap nhat UI"""
        if coin_code in self.available_coins:
            self.current_asset = coin_code
            coin_info = self.available_coins[coin_code]

            # Update search entry
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, coin_code)

            # Update selected label
            self.selected_coin_label.config(
                text=f"{coin_info['name']} ({coin_code})",
                fg=coin_info['color']
            )

            # Update title
            self.title_label.config(
                text=f"{coin_info['name'].upper()} REAL-TIME TRACKER",
                fg=coin_info['color']
            )

            # Restart WebSocket if running
            if self.running:
                self.stop_tracking()
                self.root.after(500, self.start_tracking)


    def switch_to_usd(self):
        """Chuyen sang USD"""
        if self.current_currency != "USD":
            self.current_currency = "USD"
            self.usd_btn.config(bg='#00aa00', relief='sunken')
            self.vnd_btn.config(bg='#444444', relief='raised')
            self.refresh_display()

    def switch_to_vnd(self):
        """Chuyen sang VND"""
        if self.current_currency != "VND":
            self.current_currency = "VND"
            self.vnd_btn.config(bg='#00aa00', relief='sunken')
            self.usd_btn.config(bg='#444444', relief='raised')
            self.refresh_display()

    def refresh_display(self):
        """Refresh lai hien thi voi currency moi"""
        if self.current_price > 0:
            self.update_price_display(self.current_price, 0)
            if self.high_24h > 0:
                self.update_24h_stats(self.high_24h, self.low_24h)

    def start_tracking(self):
        """Bat dau theo doi gia"""
        if not self.running:
            self.running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.update_status("[*] Connecting...", '#ffaa00')

            # Start WebSocket in separate thread
            ws_thread = threading.Thread(target=self.connect_websocket, daemon=True)
            ws_thread.start()

    def stop_tracking(self):
        """Dung theo doi gia"""
        self.running = False
        if self.ws:
            self.ws.close()
        if self.ws_ticker:
            self.ws_ticker.close()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_status("[*] Disconnected", '#ff0000')

    def connect_websocket(self):
        """Ket noi WebSocket"""
        try:
            # Lay symbol cua coin hien tai
            coin_info = self.available_coins[self.current_asset]
            symbol = coin_info['symbol'].lower()

            # Build WebSocket URLs
            trade_url = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
            ticker_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"

            # Connect to trade stream for real-time price
            self.ws = websocket.WebSocketApp(
                trade_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )

            # Connect to ticker stream for 24h high/low
            self.ws_ticker = websocket.WebSocketApp(
                ticker_url,
                on_message=self.on_ticker_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            # Run both websockets in separate threads
            trade_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            ticker_thread = threading.Thread(target=self.ws_ticker.run_forever, daemon=True)

            trade_thread.start()
            ticker_thread.start()

            trade_thread.join()
        except Exception as e:
            self.update_status("[!] Error: " + str(e), '#ff0000')

    def on_open(self, ws):
        """Callback khi WebSocket connected"""
        self.update_status("[+] Connected - Live", '#00ff00')

    def on_message(self, ws, message):
        """Callback khi nhan message"""
        try:
            data = json.loads(message)
            price = float(data['p'])
            volume = float(data['q'])

            # Update UI trong main thread
            self.root.after(0, self.update_price_display, price, volume)
        except Exception as e:
            print("Error processing message:", e)

    def on_ticker_message(self, ws, message):
        """Callback khi nhan ticker message (24h stats)"""
        try:
            data = json.loads(message)
            high_24h = float(data['h'])
            low_24h = float(data['l'])

            # Update 24h high/low
            self.root.after(0, self.update_24h_stats, high_24h, low_24h)
        except Exception as e:
            print("Error processing ticker message:", e)

    def on_error(self, ws, error):
        """Callback khi co loi"""
        self.update_status("[!] Error: " + str(error), '#ff0000')

    def on_close(self, ws, close_status_code, close_msg):
        """Callback khi WebSocket dong"""
        if self.running:
            self.update_status("[*] Reconnecting...", '#ffaa00')

    def update_price_display(self, price, volume):
        """Cap nhat hien thi gia"""
        # Luu gia tri cu
        self.previous_price = self.current_price
        self.current_price = price

        # Add to history
        self.price_history.append(price)
        if len(self.price_history) > self.max_history:
            self.price_history.pop(0)

        # Convert price if needed
        display_price = price
        currency_symbol = "$"
        if self.current_currency == "VND":
            display_price = price * self.usd_to_vnd
            currency_symbol = ""

        # Update price label
        if self.current_currency == "VND":
            self.price_label.config(text=f"{display_price:,.0f} VND")
        else:
            self.price_label.config(text=f"${display_price:,.2f}")

        # Update price color based on change
        if price > self.previous_price:
            self.price_label.config(fg='#00ff00')
            change_symbol = "UP"
            change_color = '#00ff00'
        elif price < self.previous_price:
            self.price_label.config(fg='#ff0000')
            change_symbol = "DOWN"
            change_color = '#ff0000'
        else:
            change_symbol = "---"
            change_color = '#ffaa00'

        # Calculate change
        if self.previous_price > 0:
            change_value = price - self.previous_price

            # Convert change if VND
            if self.current_currency == "VND":
                change_value_display = change_value * self.usd_to_vnd
                self.change_label.config(
                    text=f"{change_symbol} {change_value_display:+,.0f} VND",
                    fg=change_color
                )
            else:
                self.change_label.config(
                    text=f"{change_symbol} {change_value:+,.2f} USD",
                    fg=change_color
                )


    def update_24h_stats(self, high_24h, low_24h):
        """Cap nhat 24h high/low"""
        self.high_24h = high_24h
        self.low_24h = low_24h

        # Convert if VND
        if self.current_currency == "VND":
            high_display = high_24h * self.usd_to_vnd
            low_display = low_24h * self.usd_to_vnd
            self.high_label.config(text=f"{high_display:,.0f} VND")
            self.low_label.config(text=f"{low_display:,.0f} VND")
        else:
            self.high_label.config(text=f"${high_24h:,.2f}")
            self.low_label.config(text=f"${low_24h:,.2f}")


    def update_status(self, text, color):
        """Cap nhat trang thai"""
        self.status_label.config(text=text, fg=color)

    def on_closing(self):
        """Xu ly khi dong cua so"""
        self.stop_tracking()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = BTCRealtimeGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
