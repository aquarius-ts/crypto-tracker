#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script to test real-time Bitcoin price display
Run this directly in your terminal: python demo.py
"""
import websocket
import json
from datetime import datetime
import sys
import time

class BTCRealTimePrice:
    """Class de lay gia Bitcoin real-time tu WebSocket"""

    def __init__(self):
        self.binance_ws = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        self.ws_binance = None
        self.running = False
        self.first_display = True

    def on_message_binance(self, ws, message):
        """Xu ly message tu Binance WebSocket"""
        try:
            data = json.loads(message)
            price = float(data['p'])
            price_info = {
                'price': price,
                'volume': float(data['q']),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            }
            self.display_price(price_info)
        except Exception as e:
            print(f"\nLoi xu ly du lieu: {e}")

    def on_error(self, ws, error):
        """Xu ly loi WebSocket"""
        print(f"\nLoi WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Xu ly khi dong WebSocket"""
        if self.running:
            print("\nWebSocket da dong. Dang thu ket noi lai...")

    def on_open(self, ws):
        """Xu ly khi mo WebSocket"""
        print("Da ket noi WebSocket thanh cong!\n")

    def display_price(self, price_info):
        """Hien thi gia BTC real-time"""
        if self.first_display:
            # In header lan dau tien
            print("="*70)
            print(f"{'BTC REAL-TIME PRICE (WEBSOCKET)':^70}")
            print("="*70)
            print("\nNguon: Binance")
            print(f"Gia: ${price_info['price']:,.2f} USDT")
            print(f"Volume: {price_info['volume']:.6f} BTC")
            print(f"Thoi gian: {price_info['timestamp']}")
            print("\n" + "="*70)
            print("Nhan Ctrl+C de dung")
            print("="*70)
            self.first_display = False
        else:
            # Di chuyen cursor len 6 dong va cap nhat
            sys.stdout.write('\033[6A')  # Move up 6 lines

            # Xoa va cap nhat dong Gia
            sys.stdout.write('\r\033[K')  # Carriage return + clear line
            sys.stdout.write(f"Gia: ${price_info['price']:,.2f} USDT\n")

            # Xoa va cap nhat dong Volume
            sys.stdout.write('\r\033[K')
            sys.stdout.write(f"Volume: {price_info['volume']:.6f} BTC\n")

            # Xoa va cap nhat dong Thoi gian
            sys.stdout.write('\r\033[K')
            sys.stdout.write(f"Thoi gian: {price_info['timestamp']}\n")

            # Ghi lai cac dong footer
            sys.stdout.write("\n" + "="*70 + "\n")
            sys.stdout.write("Nhan Ctrl+C de dung\n")
            sys.stdout.write("="*70)

            sys.stdout.flush()

    def monitor_realtime_binance(self):
        """Theo doi gia BTC real-time tu Binance WebSocket"""
        self.running = True

        print("\nDang ket noi toi Binance WebSocket...")
        print("Cho du lieu real-time...\n")

        try:
            self.ws_binance = websocket.WebSocketApp(
                self.binance_ws,
                on_message=self.on_message_binance,
                on_error=self.on_error,
                on_close=self.on_close,
                on_open=self.on_open
            )

            self.ws_binance.run_forever()

        except KeyboardInterrupt:
            print("\n\nDang dung ket noi...")
            self.running = False
            if self.ws_binance:
                self.ws_binance.close()
            print("Da dung theo doi gia Bitcoin.")
        except Exception as e:
            print(f"\nLoi: {e}")
            self.running = False


if __name__ == "__main__":
    print("\n" + "="*70)
    print(f"{'DEMO - THEO DOI GIA BITCOIN REAL-TIME':^70}")
    print("="*70)
    print("\nChuong trinh se cap nhat gia real-time ma KHONG spam text!")
    print("Chi cap nhat 3 dong: Gia, Volume, Thoi gian")
    print("\n")

    input("Nhan Enter de bat dau...")

    btc_tracker = BTCRealTimePrice()
    btc_tracker.monitor_realtime_binance()
