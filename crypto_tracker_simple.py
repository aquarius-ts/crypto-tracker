# -*- coding: utf-8 -*-
"""
Crypto Real-Time Price Tracker - Simplified Version
Supports ALL coins on Binance by entering coin code directly
"""
import tkinter as tk
from tkinter import messagebox
import websocket
import json
import threading
import requests

class CryptoTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Real-Time Price Tracker - All Binance Coins")
        self.root.geometry("650x550")
        self.root.configure(bg='#1e1e1e')

        self.ws = None
        self.ws_ticker = None
        self.running = False

        self.current_price = 0
        self.previous_price = 0
        self.high_24h = 0
        self.low_24h = 0

        self.current_asset = "BTC"
        self.current_currency = "USD"
        self.usd_to_vnd = 25000

        # Load popular coins
        self.popular_coins = self.get_popular_coins()

        # All available coins from Binance
        self.all_coins = []
        self.coins_loaded = False

        # Suggestion listbox
        self.suggestion_listbox = None

        self.setup_ui()

        # Load all coins in background
        load_thread = threading.Thread(target=self.load_all_coins, daemon=True)
        load_thread.start()

    def get_popular_coins(self):
        """Danh sach coin pho bien"""
        return {
            "BTC": {"name": "Bitcoin", "color": "#f7931a"},
            "ETH": {"name": "Ethereum", "color": "#627eea"},
            "BNB": {"name": "Binance Coin", "color": "#f3ba2f"},
            "XRP": {"name": "Ripple", "color": "#23292f"},
            "SOL": {"name": "Solana", "color": "#14f195"},
            "ADA": {"name": "Cardano", "color": "#0033ad"},
            "DOGE": {"name": "Dogecoin", "color": "#c2a633"},
            "MATIC": {"name": "Polygon", "color": "#8247e5"},
            "DOT": {"name": "Polkadot", "color": "#e6007a"},
            "AVAX": {"name": "Avalanche", "color": "#e84142"},
            "PAXG": {"name": "Gold", "color": "#FFD700"},  # Vang tokenized
        }

    def load_all_coins(self):
        """Load tat ca coins tu Binance API"""
        try:
            url = "https://api.binance.com/api/v3/exchangeInfo"
            response = requests.get(url, timeout=10)
            data = response.json()

            for symbol_info in data['symbols']:
                if (symbol_info['symbol'].endswith('USDT') and
                    symbol_info['status'] == 'TRADING' and
                    symbol_info['quoteAsset'] == 'USDT'):

                    base_asset = symbol_info['baseAsset']

                    # Skip leveraged tokens
                    if any(x in base_asset for x in ['UP', 'DOWN', 'BULL', 'BEAR']):
                        continue

                    self.all_coins.append(base_asset)

            self.all_coins.sort()
            self.coins_loaded = True
            print(f"Loaded {len(self.all_coins)} coins from Binance")

        except Exception as e:
            print(f"Error loading coins: {e}")
            # Fallback to popular coins
            self.all_coins = list(self.popular_coins.keys())
            self.coins_loaded = True

    def setup_ui(self):
        # Title
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

        # Input frame
        input_frame = tk.Frame(self.root, bg='#2d2d2d', pady=10)
        input_frame.pack(fill='x', padx=10)

        tk.Label(
            input_frame,
            text="Enter Coin Code:",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left', padx=(20, 10))

        self.coin_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=10,
            bg='#ffffff',
            fg='#000000'
        )
        self.coin_entry.pack(side='left', padx=5)
        self.coin_entry.insert(0, "BTC")
        self.coin_entry.bind('<Return>', lambda e: self.load_coin())
        self.coin_entry.bind('<KeyRelease>', self.on_coin_entry_change)
        self.coin_entry.bind('<FocusOut>', lambda e: self.hide_suggestions())

        tk.Button(
            input_frame,
            text="Load Coin",
            command=self.load_coin,
            font=('Arial', 10, 'bold'),
            bg='#f7931a',
            fg='#000000',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)

        # Popular coins - Hien thi 6 coins pho bien nhat
        tk.Label(
            input_frame,
            text="Popular:",
            font=('Arial', 9),
            bg='#2d2d2d',
            fg='#888888'
        ).pack(side='left', padx=(20, 5))
        popular_list = ['BTC', 'ETH', 'BNB', 'DOGE', 'SOL', 'PAXG']
        for code in popular_list:
            display_text = code if code != 'PAXG' else 'GOLD'
            tk.Button(
                input_frame,
                text=display_text,
                command=lambda c=code: self.quick_select(c),
                font=('Arial', 8),
                bg='#444444',
                fg='#ffffff',
                padx=8,
                pady=2,
                cursor='hand2'
            ).pack(side='left', padx=2)

        # Currency selector
        currency_frame = tk.Frame(self.root, bg='#2d2d2d', pady=5)
        currency_frame.pack(fill='x', padx=10)

        tk.Label(
            currency_frame,
            text="Currency:",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        ).pack(side='left', padx=20)

        self.usd_btn = tk.Button(
            currency_frame,
            text="USD",
            command=self.switch_to_usd,
            font=('Arial', 9, 'bold'),
            bg='#00aa00',
            fg='#ffffff',
            padx=15,
            pady=4,
            relief='sunken',
            cursor='hand2'
        )
        self.usd_btn.pack(side='left', padx=5)

        self.vnd_btn = tk.Button(
            currency_frame,
            text="VND",
            command=self.switch_to_vnd,
            font=('Arial', 9, 'bold'),
            bg='#444444',
            fg='#ffffff',
            padx=15,
            pady=4,
            relief='raised',
            cursor='hand2'
        )
        self.vnd_btn.pack(side='left', padx=5)

        # Price display
        price_frame = tk.Frame(self.root, bg='#2d2d2d', pady=20)
        price_frame.pack(fill='x', padx=10, pady=10)

        self.price_label = tk.Label(
            price_frame,
            text="$0.00",
            font=('Arial', 48, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.price_label.pack()

        self.change_label = tk.Label(
            price_frame,
            text="---",
            font=('Arial', 14),
            bg='#2d2d2d',
            fg='#ffaa00'
        )
        self.change_label.pack(pady=5)

        # 24H stats
        stats_frame = tk.Frame(self.root, bg='#2d2d2d', pady=15)
        stats_frame.pack(fill='x', padx=10)

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        tk.Label(
            stats_frame,
            text="24H HIGH",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        ).grid(row=0, column=0)

        self.high_label = tk.Label(
            stats_frame,
            text="$0.00",
            font=('Arial', 18, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.high_label.grid(row=1, column=0, pady=5)

        tk.Label(
            stats_frame,
            text="24H LOW",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#888888'
        ).grid(row=0, column=1)

        self.low_label = tk.Label(
            stats_frame,
            text="$0.00",
            font=('Arial', 18, 'bold'),
            bg='#2d2d2d',
            fg='#ff0000'
        )
        self.low_label.grid(row=1, column=1, pady=5)

        # Status bar
        status_frame = tk.Frame(self.root, bg='#1a1a1a', pady=10)
        status_frame.pack(side='bottom', fill='x')

        self.status_label = tk.Label(
            status_frame,
            text="[*] Enter a coin code and click Load Coin or START",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#888888'
        )
        self.status_label.pack(side='left', padx=20)

        # Control buttons
        btn_frame = tk.Frame(self.root, bg='#1e1e1e')
        btn_frame.pack(side='bottom', pady=15)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ START",
            command=self.start_tracking,
            font=('Arial', 14, 'bold'),
            bg='#00cc00',
            fg='#ffffff',
            padx=40,
            pady=12,
            relief='raised',
            bd=3,
            cursor='hand2'
        )
        self.start_btn.pack(side='left', padx=10)

        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹ STOP",
            command=self.stop_tracking,
            font=('Arial', 14, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            padx=40,
            pady=12,
            relief='raised',
            bd=3,
            cursor='hand2',
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=10)

    def quick_select(self, code):
        """Quick select popular coin"""
        self.coin_entry.delete(0, tk.END)
        self.coin_entry.insert(0, code)
        self.load_coin()

    def on_coin_entry_change(self, event):
        """Xu ly khi thay doi text trong coin entry"""
        if event.keysym in ['Return', 'Up', 'Down', 'Escape']:
            return

        typed_text = self.coin_entry.get().strip().upper()

        if not typed_text or not self.coins_loaded:
            self.hide_suggestions()
            return

        # Tim cac coin phu hop
        matching_coins = [coin for coin in self.all_coins if coin.startswith(typed_text)]

        if matching_coins and len(matching_coins) > 0:
            self.show_suggestions(matching_coins[:10])  # Hien thi toi da 10 goi y
        else:
            self.hide_suggestions()

    def show_suggestions(self, suggestions):
        """Hien thi danh sach goi y"""
        # Destroy old listbox if exists
        if self.suggestion_listbox:
            try:
                self.suggestion_listbox.master.destroy()
            except:
                pass

        # Get entry position
        entry_x = self.coin_entry.winfo_rootx() - self.root.winfo_rootx()
        entry_y = self.coin_entry.winfo_rooty() - self.root.winfo_rooty()
        entry_height = self.coin_entry.winfo_height()

        # Create listbox frame
        list_frame = tk.Frame(self.root, bg='#ffffff', relief='solid', bd=1)
        list_frame.place(x=entry_x, y=entry_y + entry_height, width=150)

        # Create listbox
        self.suggestion_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 10),
            bg='#ffffff',
            fg='#000000',
            selectbackground='#f7931a',
            selectforeground='#000000',
            height=min(len(suggestions), 10),
            relief='flat',
            exportselection=False
        )
        self.suggestion_listbox.pack(fill='both', expand=True)

        # Add suggestions
        for coin in suggestions:
            self.suggestion_listbox.insert(tk.END, coin)

        # Bind selection - Use ButtonRelease instead of Button-1
        self.suggestion_listbox.bind('<ButtonRelease-1>', self.on_suggestion_click)
        self.suggestion_listbox.bind('<Return>', self.on_suggestion_select)

        # Bind keyboard navigation
        self.coin_entry.bind('<Down>', lambda e: self.focus_suggestions())
        self.coin_entry.bind('<Escape>', lambda e: self.hide_suggestions())

    def hide_suggestions(self):
        """An danh sach goi y"""
        if self.suggestion_listbox:
            try:
                self.suggestion_listbox.master.destroy()
            except:
                pass
            self.suggestion_listbox = None

    def focus_suggestions(self):
        """Focus vao listbox suggestions"""
        if self.suggestion_listbox:
            self.suggestion_listbox.focus()
            self.suggestion_listbox.select_set(0)

    def on_suggestion_click(self, event):
        """Xu ly khi click vao suggestion"""
        if self.suggestion_listbox:
            # Get clicked item index
            index = self.suggestion_listbox.nearest(event.y)
            if index >= 0:
                self.suggestion_listbox.selection_clear(0, tk.END)
                self.suggestion_listbox.selection_set(index)
                self.suggestion_listbox.activate(index)
                # Select the coin
                self.on_suggestion_select(None)

    def on_suggestion_select(self, event):
        """Xu ly khi chon suggestion"""
        if self.suggestion_listbox:
            selection = self.suggestion_listbox.curselection()
            if selection:
                selected_coin = self.suggestion_listbox.get(selection[0])
                # Hide suggestions first
                self.hide_suggestions()
                # Update entry
                self.coin_entry.delete(0, tk.END)
                self.coin_entry.insert(0, selected_coin)
                self.coin_entry.focus()
                # Auto load coin
                self.load_coin()

    def load_coin(self):
        """Load coin info"""
        coin_code = self.coin_entry.get().strip().upper()
        if not coin_code:
            messagebox.showwarning("Warning", "Please enter a coin code!")
            return

        self.current_asset = coin_code

        # Update title
        coin_info = self.popular_coins.get(coin_code, {"name": coin_code, "color": "#ffffff"})
        self.title_label.config(
            text=f"{coin_info['name'].upper()} REAL-TIME TRACKER",
            fg=coin_info['color']
        )

        if self.running:
            self.stop_tracking()
            self.root.after(500, self.start_tracking)

    def switch_to_usd(self):
        if self.current_currency != "USD":
            self.current_currency = "USD"
            self.usd_btn.config(bg='#00aa00', relief='sunken')
            self.vnd_btn.config(bg='#444444', relief='raised')
            self.refresh_display()

    def switch_to_vnd(self):
        if self.current_currency != "VND":
            self.current_currency = "VND"
            self.vnd_btn.config(bg='#00aa00', relief='sunken')
            self.usd_btn.config(bg='#444444', relief='raised')
            self.refresh_display()

    def refresh_display(self):
        if self.current_price > 0:
            self.update_price_display(self.current_price, 0)
            if self.high_24h > 0:
                self.update_24h_stats(self.high_24h, self.low_24h)

    def start_tracking(self):
        if not self.running:
            self.running = True
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.update_status("[*] Connecting...", '#ffaa00')

            ws_thread = threading.Thread(target=self.connect_websocket, daemon=True)
            ws_thread.start()

    def stop_tracking(self):
        self.running = False
        if self.ws:
            self.ws.close()
        if self.ws_ticker:
            self.ws_ticker.close()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_status("[*] Disconnected", '#ff0000')

    def connect_websocket(self):
        try:
            symbol = f"{self.current_asset}USDT".lower()
            trade_url = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
            ticker_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"

            self.ws = websocket.WebSocketApp(
                trade_url,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )

            self.ws_ticker = websocket.WebSocketApp(
                ticker_url,
                on_message=self.on_ticker_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            trade_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            ticker_thread = threading.Thread(target=self.ws_ticker.run_forever, daemon=True)

            trade_thread.start()
            ticker_thread.start()

            trade_thread.join()
        except Exception as e:
            self.update_status(f"[!] Error: {e}", '#ff0000')

    def on_open(self, ws):
        self.update_status("[+] Connected - Live", '#00ff00')

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            price = float(data['p'])
            self.root.after(0, self.update_price_display, price, 0)
        except Exception as e:
            print(f"Error: {e}")

    def on_ticker_message(self, ws, message):
        try:
            data = json.loads(message)
            high_24h = float(data['h'])
            low_24h = float(data['l'])
            self.root.after(0, self.update_24h_stats, high_24h, low_24h)
        except Exception as e:
            print(f"Error: {e}")

    def on_error(self, ws, error):
        self.update_status(f"[!] Error: {error}", '#ff0000')

    def on_close(self, ws, close_status_code, close_msg):
        if self.running:
            self.update_status("[*] Reconnecting...", '#ffaa00')

    def update_price_display(self, price, volume):
        self.previous_price = self.current_price
        self.current_price = price

        display_price = price * self.usd_to_vnd if self.current_currency == "VND" else price

        if self.current_currency == "VND":
            self.price_label.config(text=f"{display_price:,.0f} VND")
        else:
            self.price_label.config(text=f"${display_price:,.2f}")

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

        if self.previous_price > 0:
            change_value = price - self.previous_price

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
        self.high_24h = high_24h
        self.low_24h = low_24h

        if self.current_currency == "VND":
            high_display = high_24h * self.usd_to_vnd
            low_display = low_24h * self.usd_to_vnd
            self.high_label.config(text=f"{high_display:,.0f} VND")
            self.low_label.config(text=f"{low_display:,.0f} VND")
        else:
            self.high_label.config(text=f"${high_24h:,.2f}")
            self.low_label.config(text=f"${low_24h:,.2f}")

    def update_status(self, text, color):
        self.status_label.config(text=text, fg=color)

    def on_closing(self):
        self.stop_tracking()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CryptoTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
