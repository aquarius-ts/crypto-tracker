# -*- coding: utf-8 -*-
"""
Crypto Real-Time Price Tracker - Simplified Version
Supports ALL coins on Binance by entering coin code directly
+ Vietnamese Stock Market Information Tab
"""
import tkinter as tk
from tkinter import messagebox, ttk
import websocket
import json
import threading
import requests
import urllib3
from datetime import datetime

# Disable SSL warnings for stock APIs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CryptoTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto & Stock Tracker - All Binance Coins + Vietnam Stocks")
        self.root.geometry("700x600")
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
        self.usd_to_vnd = 25000  # Default fallback value
        self.exchange_rate_label = None  # Will be created in UI

        # Load popular coins
        self.popular_coins = self.get_popular_coins()

        # All available coins from Binance
        self.all_coins = []
        self.coins_loaded = False

        # Suggestion listbox
        self.suggestion_listbox = None

        # Stock market variables
        self.stock_running = False
        self.current_stock = "VNM"
        self.stock_data = {}
        self.stock_update_timer = None

        self.setup_ui()

        # Load all coins in background
        load_thread = threading.Thread(target=self.load_all_coins, daemon=True)
        load_thread.start()

        # Load exchange rate in background
        exchange_thread = threading.Thread(target=self.load_exchange_rate, daemon=True)
        exchange_thread.start()

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

    def load_exchange_rate(self):
        """Load USD to VND exchange rate from API"""
        try:
            # Try exchangerate-api.com (free, no key required for basic usage)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if 'rates' in data and 'VND' in data['rates']:
                    self.usd_to_vnd = data['rates']['VND']
                    print(f"Exchange rate loaded: 1 USD = {self.usd_to_vnd:,.0f} VND")

                    # Update UI if exchange rate label exists
                    if self.exchange_rate_label:
                        self.root.after(0, lambda: self.exchange_rate_label.config(
                            text=f"Tỉ giá: 1 USD = {self.usd_to_vnd:,.0f} VND"))

                    # Refresh display if showing VND
                    if self.current_currency == "VND" and self.current_price > 0:
                        self.root.after(0, self.refresh_display)
                    return

            # Fallback: Try another API (fixer.io alternative - free tier)
            print("Primary exchange API failed, using fallback...")
            url2 = "https://open.er-api.com/v6/latest/USD"
            response2 = requests.get(url2, timeout=10)

            if response2.status_code == 200:
                data2 = response2.json()
                if 'rates' in data2 and 'VND' in data2['rates']:
                    self.usd_to_vnd = data2['rates']['VND']
                    print(f"Exchange rate loaded (fallback): 1 USD = {self.usd_to_vnd:,.0f} VND")

                    if self.exchange_rate_label:
                        self.root.after(0, lambda: self.exchange_rate_label.config(
                            text=f"Tỉ giá: 1 USD = {self.usd_to_vnd:,.0f} VND"))

                    if self.current_currency == "VND" and self.current_price > 0:
                        self.root.after(0, self.refresh_display)
                    return

            print(f"Could not load exchange rate, using default: {self.usd_to_vnd}")

        except Exception as e:
            print(f"Error loading exchange rate: {e}")
            print(f"Using default exchange rate: {self.usd_to_vnd}")

    def setup_ui(self):
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1e1e1e', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2d2d2d', foreground='#ffffff',
                        padding=[20, 10], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#f7931a')],
                  foreground=[('selected', '#000000')])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Crypto Tab
        self.crypto_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.crypto_tab, text='  Cryptocurrency  ')

        # Stock Tab
        self.stock_tab = tk.Frame(self.notebook, bg='#1e1e1e')
        self.notebook.add(self.stock_tab, text='  Vietnam Stocks  ')

        # Setup crypto tab
        self.setup_crypto_tab()

        # Setup stock tab
        self.setup_stock_tab()

    def setup_crypto_tab(self):
        """Setup cryptocurrency tracking interface"""
        # Title
        title_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=15)
        title_frame.pack(fill='x', padx=10, pady=10)

        self.title_label = tk.Label(
            title_frame,
            text="BITCOIN REAL-TIME TRACKER",
            font=('Arial', 20, 'bold'),
            bg='#2d2d2d',
            fg='#f7931a'
        )
        self.title_label.pack()

        # Input frame - First row
        input_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=10)
        input_frame.pack(fill='x', padx=10)

        # Center the input elements
        input_center = tk.Frame(input_frame, bg='#2d2d2d')
        input_center.pack()

        tk.Label(
            input_center,
            text="Enter Coin Code:",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left', padx=(10, 10))

        self.coin_entry = tk.Entry(
            input_center,
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
            input_center,
            text="Load Coin",
            command=self.load_coin,
            font=('Arial', 10, 'bold'),
            bg='#f7931a',
            fg='#000000',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)

        # Popular coins - Second row (always visible)
        popular_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=5)
        popular_frame.pack(fill='x', padx=10)

        # Center the popular buttons
        popular_center = tk.Frame(popular_frame, bg='#2d2d2d')
        popular_center.pack()

        tk.Label(
            popular_center,
            text="Popular:",
            font=('Arial', 9, 'bold'),
            bg='#2d2d2d',
            fg='#888888'
        ).pack(side='left', padx=(5, 10))

        popular_list = ['BTC', 'ETH', 'BNB', 'DOGE', 'SOL', 'PAXG']
        for code in popular_list:
            display_text = code if code != 'PAXG' else 'GOLD'
            tk.Button(
                popular_center,
                text=display_text,
                command=lambda c=code: self.quick_select(c),
                font=('Arial', 9),
                bg='#444444',
                fg='#ffffff',
                padx=10,
                pady=3,
                cursor='hand2'
            ).pack(side='left', padx=3)

        # Currency selector
        currency_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=5)
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

        # Exchange rate display
        self.exchange_rate_label = tk.Label(
            currency_frame,
            text=f"Tỉ giá: 1 USD = {self.usd_to_vnd:,.0f} VND",
            font=('Arial', 8),
            bg='#2d2d2d',
            fg='#ffaa00'
        )
        self.exchange_rate_label.pack(side='left', padx=20)

        # Price display
        price_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=20)
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
        stats_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=15)
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

        # Control buttons inside crypto tab
        btn_frame = tk.Frame(self.crypto_tab, bg='#2d2d2d', pady=15)
        btn_frame.pack(fill='x', padx=10, pady=10)

        # Center the buttons
        btn_center = tk.Frame(btn_frame, bg='#2d2d2d')
        btn_center.pack()

        self.start_btn = tk.Button(
            btn_center,
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
            btn_center,
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

        # Status bar at bottom of crypto tab
        status_frame = tk.Frame(self.crypto_tab, bg='#1a1a1a', pady=10)
        status_frame.pack(side='bottom', fill='x')

        self.status_label = tk.Label(
            status_frame,
            text="[*] Enter a coin code and click Load Coin or START",
            font=('Arial', 9),
            bg='#1a1a1a',
            fg='#888888'
        )
        self.status_label.pack(side='left', padx=20)

    def setup_stock_tab(self):
        """Setup Vietnam stock market interface"""
        # Title
        title_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=15)
        title_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            title_frame,
            text="VIETNAM STOCK MARKET TRACKER",
            font=('Arial', 20, 'bold'),
            bg='#2d2d2d',
            fg='#00aaff'
        ).pack()

        # Input frame - First row
        input_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=10)
        input_frame.pack(fill='x', padx=10)

        # Center the input elements
        input_center = tk.Frame(input_frame, bg='#2d2d2d')
        input_center.pack()

        tk.Label(
            input_center,
            text="Mã Cổ Phiếu:",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left', padx=(10, 10))

        self.stock_entry = tk.Entry(
            input_center,
            font=('Arial', 12),
            width=10,
            bg='#ffffff',
            fg='#000000'
        )
        self.stock_entry.pack(side='left', padx=5)
        self.stock_entry.insert(0, "VNM")
        self.stock_entry.bind('<Return>', lambda e: self.load_stock())

        tk.Button(
            input_center,
            text="Tải Cổ Phiếu",
            command=self.load_stock,
            font=('Arial', 10, 'bold'),
            bg='#00aaff',
            fg='#000000',
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side='left', padx=5)

        # Popular stocks - Second row (always visible)
        popular_stock_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=5)
        popular_stock_frame.pack(fill='x', padx=10)

        # Center the popular buttons
        popular_stock_center = tk.Frame(popular_stock_frame, bg='#2d2d2d')
        popular_stock_center.pack()

        tk.Label(
            popular_stock_center,
            text="Phổ biến:",
            font=('Arial', 9, 'bold'),
            bg='#2d2d2d',
            fg='#888888'
        ).pack(side='left', padx=(5, 10))

        popular_stocks = ['VNM', 'VIC', 'HPG', 'FPT', 'VCB', 'MSN']
        for stock in popular_stocks:
            tk.Button(
                popular_stock_center,
                text=stock,
                command=lambda s=stock: self.quick_select_stock(s),
                font=('Arial', 9),
                bg='#444444',
                fg='#ffffff',
                padx=10,
                pady=3,
                cursor='hand2'
            ).pack(side='left', padx=3)

        # Stock info display
        info_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=20)
        info_frame.pack(fill='x', padx=10, pady=10)

        # Stock name
        self.stock_name_label = tk.Label(
            info_frame,
            text="---",
            font=('Arial', 16, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff'
        )
        self.stock_name_label.pack(pady=10)

        # Price display
        self.stock_price_label = tk.Label(
            info_frame,
            text="0,000 VND",
            font=('Arial', 48, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        self.stock_price_label.pack()

        self.stock_change_label = tk.Label(
            info_frame,
            text="---",
            font=('Arial', 14),
            bg='#2d2d2d',
            fg='#ffaa00'
        )
        self.stock_change_label.pack(pady=5)

        # Stock details grid
        details_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=15)
        details_frame.pack(fill='x', padx=10)

        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)
        details_frame.columnconfigure(2, weight=1)

        # Row 1
        tk.Label(details_frame, text="Trần", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=0, column=0)
        tk.Label(details_frame, text="Sàn", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=0, column=1)
        tk.Label(details_frame, text="Tham chiếu", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=0, column=2)

        self.stock_ceiling_label = tk.Label(details_frame, text="---", font=('Arial', 14, 'bold'), bg='#2d2d2d', fg='#ff00ff')
        self.stock_ceiling_label.grid(row=1, column=0, pady=5)

        self.stock_floor_label = tk.Label(details_frame, text="---", font=('Arial', 14, 'bold'), bg='#2d2d2d', fg='#00ffff')
        self.stock_floor_label.grid(row=1, column=1, pady=5)

        self.stock_ref_label = tk.Label(details_frame, text="---", font=('Arial', 14, 'bold'), bg='#2d2d2d', fg='#ffff00')
        self.stock_ref_label.grid(row=1, column=2, pady=5)

        # Row 2
        tk.Label(details_frame, text="Khối lượng", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=2, column=0, pady=(10, 0))
        tk.Label(details_frame, text="Cao nhất", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=2, column=1, pady=(10, 0))
        tk.Label(details_frame, text="Thấp nhất", font=('Arial', 9), bg='#2d2d2d', fg='#888888').grid(row=2, column=2, pady=(10, 0))

        self.stock_volume_label = tk.Label(details_frame, text="---", font=('Arial', 12), bg='#2d2d2d', fg='#ffffff')
        self.stock_volume_label.grid(row=3, column=0, pady=5)

        self.stock_high_label = tk.Label(details_frame, text="---", font=('Arial', 12), bg='#2d2d2d', fg='#00ff00')
        self.stock_high_label.grid(row=3, column=1, pady=5)

        self.stock_low_label = tk.Label(details_frame, text="---", font=('Arial', 12), bg='#2d2d2d', fg='#ff0000')
        self.stock_low_label.grid(row=3, column=2, pady=5)

        # Stock control buttons
        stock_btn_frame = tk.Frame(self.stock_tab, bg='#2d2d2d', pady=15)
        stock_btn_frame.pack(fill='x', padx=10, pady=10)

        # Center the buttons
        stock_btn_center = tk.Frame(stock_btn_frame, bg='#2d2d2d')
        stock_btn_center.pack()

        self.stock_start_btn = tk.Button(
            stock_btn_center,
            text="▶ BẮT ĐẦU",
            command=self.start_stock_tracking,
            font=('Arial', 12, 'bold'),
            bg='#00cc00',
            fg='#ffffff',
            padx=30,
            pady=10,
            relief='raised',
            bd=3,
            cursor='hand2'
        )
        self.stock_start_btn.pack(side='left', padx=10)

        self.stock_stop_btn = tk.Button(
            stock_btn_center,
            text="⏹ DỪNG",
            command=self.stop_stock_tracking,
            font=('Arial', 12, 'bold'),
            bg='#cc0000',
            fg='#ffffff',
            padx=30,
            pady=10,
            relief='raised',
            bd=3,
            cursor='hand2',
            state='disabled'
        )
        self.stock_stop_btn.pack(side='left', padx=10)

        # Stock status
        self.stock_status_label = tk.Label(
            self.stock_tab,
            text="[*] Nhập mã cổ phiếu và nhấn Tải hoặc Bắt đầu",
            font=('Arial', 9),
            bg='#2d2d2d',
            fg='#888888'
        )
        self.stock_status_label.pack(pady=5)

        # Last update time
        self.stock_update_time_label = tk.Label(
            self.stock_tab,
            text="",
            font=('Arial', 8),
            bg='#2d2d2d',
            fg='#666666'
        )
        self.stock_update_time_label.pack(pady=5)

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

    # ========== STOCK MARKET METHODS ==========

    def quick_select_stock(self, stock_code):
        """Quick select popular stock"""
        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, stock_code)
        self.load_stock()

    def load_stock(self):
        """Load stock info from API"""
        stock_code = self.stock_entry.get().strip().upper()
        if not stock_code:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã cổ phiếu!")
            return

        self.current_stock = stock_code
        self.stock_status_label.config(text=f"[*] Đang tải dữ liệu {stock_code}...", fg='#ffaa00')

        # Fetch stock data in background
        fetch_thread = threading.Thread(target=self.fetch_stock_data, args=(stock_code, True), daemon=True)
        fetch_thread.start()

    def fetch_stock_data(self, stock_code, auto_start=False):
        """Fetch stock data from Vietnam stock API"""
        try:
            # Try Cafef API - works well for Vietnam stocks
            url = f"https://s.cafef.vn/Ajax/PageNew/DataHistory/PriceHistory.ashx?Symbol={stock_code}&StartDate=&EndDate=&PageIndex=1&PageSize=2"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data and 'Data' in data and 'Data' in data['Data'] and len(data['Data']['Data']) > 0:
                    # Get latest data
                    latest = data['Data']['Data'][0]

                    # Parse price (format: "70.6")
                    price_str = str(latest.get('GiaDongCua', '0')).replace(',', '')
                    current_price = float(price_str) * 1000  # Convert to VND

                    # Parse change (format: "-0.5(-0.70 %)")
                    change_str = latest.get('ThayDoi', '0(0 %)')
                    change = 0
                    change_percent = 0

                    try:
                        if '(' in change_str:
                            parts = change_str.split('(')
                            change = float(parts[0].strip()) * 1000
                            change_percent = float(parts[1].replace('%', '').replace(')', '').strip())
                    except:
                        pass

                    # Calculate reference price
                    reference_price = current_price - change
                    ceiling_price = reference_price * 1.07  # +7%
                    floor_price = reference_price * 0.93    # -7%

                    # Parse volume (already a number)
                    volume = latest.get('KhoiLuongKhopLenh', 0)

                    # Get high/low from previous day if we have 2 days data
                    high_price = current_price
                    low_price = current_price
                    if len(data['Data']['Data']) > 1:
                        prev_day = data['Data']['Data'][1]
                        prev_price_str = str(prev_day.get('GiaDongCua', '0')).replace(',', '')
                        prev_price = float(prev_price_str) * 1000
                        high_price = max(current_price, prev_price)
                        low_price = min(current_price, prev_price)

                    stock_info = {
                        'code': stock_code,
                        'close': current_price,
                        'high': high_price,
                        'low': low_price,
                        'volume': volume,
                        'change': change,
                        'pctChange': change_percent,
                        'ceiling': ceiling_price,
                        'floor': floor_price,
                        'reference': reference_price
                    }

                    self.stock_data = stock_info
                    self.root.after(0, self.update_stock_display, stock_info)

                    # Update last refresh time
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.root.after(0, lambda: self.stock_update_time_label.config(
                        text=f"Cập nhật lần cuối: {current_time}"))

                    self.root.after(0, lambda code=stock_code: self.stock_status_label.config(
                        text=f"[+] Đã tải dữ liệu {code} từ Cafef", fg='#00ff00'))

                    # Auto-start tracking after first load
                    if auto_start and not self.stock_running:
                        self.root.after(500, self.start_stock_tracking)

                    return

            # If Cafef fails, try backup API
            self.try_ssi_price_api(stock_code, auto_start)

        except Exception as e:
            print(f"Error with Cafef API: {e}")
            self.try_ssi_price_api(stock_code, auto_start)

    def try_ssi_price_api(self, stock_code, auto_start=False):
        """Try SSI price API"""
        try:
            url = f"https://fc-data.ssi.com.vn/api/v2/Market/Securities/{stock_code}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)

            if response.status_code == 200:
                data = response.json()
                if data and 'data' in data:
                    info = data['data']
                    stock_info = {
                        'code': stock_code,
                        'close': info.get('lastPrice', 0),
                        'high': info.get('highestPrice', 0),
                        'low': info.get('lowestPrice', 0),
                        'volume': info.get('totalVolume', 0),
                        'change': info.get('changePoint', 0),
                        'pctChange': info.get('changePercent', 0),
                        'ceiling': info.get('ceilingPrice', 0),
                        'floor': info.get('floorPrice', 0),
                        'reference': info.get('referencePrice', 0)
                    }

                    self.stock_data = stock_info
                    self.root.after(0, self.update_stock_display, stock_info)

                    # Update last refresh time
                    current_time = datetime.now().strftime("%H:%M:%S")
                    self.root.after(0, lambda: self.stock_update_time_label.config(
                        text=f"Cập nhật lần cuối: {current_time}"))

                    self.root.after(0, lambda code=stock_code: self.stock_status_label.config(
                        text=f"[+] Đã tải dữ liệu {code}", fg='#00ff00'))

                    # Auto-start tracking after first load
                    if auto_start and not self.stock_running:
                        self.root.after(500, self.start_stock_tracking)

                    return

            # Try simple price display as last resort
            self.try_simple_display(stock_code)

        except Exception as e:
            print(f"Error with SSI API: {e}")
            self.try_simple_display(stock_code)

    def try_simple_display(self, stock_code):
        """Display simple mock data when all APIs fail"""
        try:
            # Show message that we're using demo data
            stock_info = {
                'code': stock_code,
                'close': 0,
                'high': 0,
                'low': 0,
                'volume': 0,
                'change': 0,
                'pctChange': 0
            }

            self.stock_data = stock_info
            self.root.after(0, self.update_stock_display, stock_info)
            self.root.after(0, lambda code=stock_code: self.stock_status_label.config(
                text=f"[!] Không thể kết nối API cho {code}. Vui lòng thử lại sau.", fg='#ff0000'))
        except Exception as e:
            print(f"Final fallback error: {e}")
            error_msg = str(e)[:50]
            self.root.after(0, lambda msg=error_msg: self.stock_status_label.config(
                text=f"[!] Lỗi: {msg}", fg='#ff0000'))

    def update_stock_display(self, stock_info):
        """Update stock display with fetched data"""
        try:
            # Stock name
            stock_code = stock_info.get('code', stock_info.get('symbol', self.current_stock))
            self.stock_name_label.config(text=f"{stock_code}")

            # Current price - try different field names
            current_price = stock_info.get('close', stock_info.get('lastPrice', stock_info.get('c', 0)))
            if current_price:
                self.stock_price_label.config(text=f"{current_price:,.1f} VND")

            # Change
            change = stock_info.get('change', stock_info.get('priceChange', 0))
            change_percent = stock_info.get('pctChange', stock_info.get('percentPriceChange', 0))

            if change > 0:
                color = '#00ff00'
                symbol = "▲"
            elif change < 0:
                color = '#ff0000'
                symbol = "▼"
            else:
                color = '#ffaa00'
                symbol = "─"

            self.stock_price_label.config(fg=color)
            self.stock_change_label.config(
                text=f"{symbol} {change:+,.1f} ({change_percent:+.2f}%)",
                fg=color
            )

            # Ceiling, floor, reference
            ceiling = stock_info.get('ceiling', stock_info.get('ceilingPrice', 0))
            floor = stock_info.get('floor', stock_info.get('floorPrice', 0))
            reference = stock_info.get('reference', stock_info.get('refPrice', 0))

            if ceiling:
                self.stock_ceiling_label.config(text=f"{ceiling:,.1f}")
            if floor:
                self.stock_floor_label.config(text=f"{floor:,.1f}")
            if reference:
                self.stock_ref_label.config(text=f"{reference:,.1f}")

            # High, low, volume
            high = stock_info.get('high', stock_info.get('h', 0))
            low = stock_info.get('low', stock_info.get('l', 0))
            volume = stock_info.get('nmVolume', stock_info.get('totalVolume', stock_info.get('v', 0)))

            if high:
                self.stock_high_label.config(text=f"{high:,.1f}")
            if low:
                self.stock_low_label.config(text=f"{low:,.1f}")
            if volume:
                if volume >= 1000000:
                    self.stock_volume_label.config(text=f"{volume/1000000:.2f}M")
                elif volume >= 1000:
                    self.stock_volume_label.config(text=f"{volume/1000:.2f}K")
                else:
                    self.stock_volume_label.config(text=f"{volume:,.0f}")

        except Exception as e:
            print(f"Error updating stock display: {e}")

    def update_stock_display_alt(self, stock_info):
        """Update stock display with alternative API data structure"""
        try:
            # Alternative API structure
            stock_code = self.current_stock
            self.stock_name_label.config(text=f"{stock_code}")

            # Try to extract price from various possible fields
            current_price = stock_info.get('Price', stock_info.get('LastPrice', 0))
            if current_price:
                self.stock_price_label.config(text=f"{current_price:,.1f} VND")

            # Change
            change = stock_info.get('Change', 0)
            change_percent = stock_info.get('ChangePercent', 0)

            if change > 0:
                color = '#00ff00'
                symbol = "▲"
            elif change < 0:
                color = '#ff0000'
                symbol = "▼"
            else:
                color = '#ffaa00'
                symbol = "─"

            self.stock_price_label.config(fg=color)
            if change != 0 or change_percent != 0:
                self.stock_change_label.config(
                    text=f"{symbol} {change:+,.1f} ({change_percent:+.2f}%)",
                    fg=color
                )

            # Other fields
            ceiling = stock_info.get('Ceiling', 0)
            floor = stock_info.get('Floor', 0)
            reference = stock_info.get('Reference', 0)

            if ceiling:
                self.stock_ceiling_label.config(text=f"{ceiling:,.1f}")
            if floor:
                self.stock_floor_label.config(text=f"{floor:,.1f}")
            if reference:
                self.stock_ref_label.config(text=f"{reference:,.1f}")

            high = stock_info.get('High', 0)
            low = stock_info.get('Low', 0)
            volume = stock_info.get('TotalVolume', 0)

            if high:
                self.stock_high_label.config(text=f"{high:,.1f}")
            if low:
                self.stock_low_label.config(text=f"{low:,.1f}")
            if volume:
                if volume >= 1000000:
                    self.stock_volume_label.config(text=f"{volume/1000000:.2f}M")
                elif volume >= 1000:
                    self.stock_volume_label.config(text=f"{volume/1000:.2f}K")
                else:
                    self.stock_volume_label.config(text=f"{volume:,.0f}")

        except Exception as e:
            print(f"Error updating alternative stock display: {e}")

    def start_stock_tracking(self):
        """Start automatic stock tracking (refresh every 10 seconds)"""
        if not self.stock_running:
            self.stock_running = True
            self.stock_start_btn.config(state='disabled')
            self.stock_stop_btn.config(state='normal')
            self.stock_status_label.config(text="[*] Đang theo dõi (refresh mỗi 10s)...", fg='#00ff00')
            self.auto_update_stock()

    def stop_stock_tracking(self):
        """Stop automatic stock tracking"""
        self.stock_running = False
        if self.stock_update_timer:
            self.root.after_cancel(self.stock_update_timer)
            self.stock_update_timer = None
        self.stock_start_btn.config(state='normal')
        self.stock_stop_btn.config(state='disabled')
        self.stock_status_label.config(text="[*] Đã dừng", fg='#ff0000')

    def auto_update_stock(self):
        """Auto update stock data every 10 seconds"""
        if self.stock_running:
            self.fetch_stock_data(self.current_stock)
            # Schedule next update in 10 seconds (faster refresh)
            self.stock_update_timer = self.root.after(10000, self.auto_update_stock)

    def on_closing(self):
        self.stop_tracking()
        self.stop_stock_tracking()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CryptoTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
