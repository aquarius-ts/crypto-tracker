# -*- coding: utf-8 -*-
import websocket
import json
from datetime import datetime
import sys

class BTCRealTimePrice:
    """Class de lay gia Bitcoin real-time tu WebSocket"""

    def __init__(self):
        self.binance_ws = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        self.latest_prices = {
            'binance': None,
        }
        self.ws_binance = None
        self.running = False
        self.first_display = True

    def on_message_binance(self, ws, message):
        """Xu ly message tu Binance WebSocket"""
        try:
            data = json.loads(message)
            price = float(data['p'])
            self.latest_prices['binance'] = {
                'source': 'Binance',
                'price': price,
                'currency': 'USDT',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'volume': float(data['q'])
            }
            self.display_price(self.latest_prices['binance'])
        except Exception as e:
            print(f"Loi xu ly du lieu Binance: {e}")

    def on_error(self, ws, error):
        """Xu ly loi WebSocket"""
        print(f"Loi WebSocket: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Xu ly khi dong WebSocket"""
        if self.running:
            print("WebSocket da dong. Dang thu ket noi lai...")

    def on_open(self, ws):
        """Xu ly khi mo WebSocket"""
        print("Da ket noi WebSocket thanh cong!")

    def display_price(self, price_info):
        """Hien thi gia BTC real-time"""
        if self.first_display:
            # In header lan dau tien
            print("\n" + "="*70)
            print(f"{'BTC REAL-TIME PRICE (WEBSOCKET)':^70}")
            print("="*70)
            print("\nNguon: Binance")
            print(f"Gia: ${price_info['price']:,.2f} {price_info['currency']}")
            print(f"Volume: {price_info['volume']:.6f} BTC")
            print(f"Thoi gian: {price_info['timestamp']}")
            print("\n" + "="*70)
            print("Nhan Ctrl+C de dung")
            print("="*70)
            self.first_display = False
        else:
            # Chi cap nhat 3 dong gia tri (Gia, Volume, Thoi gian)
            # Di chuyen cursor len 6 dong (3 dong gia tri + 3 dong footer)
            sys.stdout.write('\033[6A')  # Move up 6 lines

            # Cap nhat dong Gia
            sys.stdout.write('\033[K')  # Clear line
            sys.stdout.write(f"Gia: ${price_info['price']:,.2f} {price_info['currency']}\n")

            # Cap nhat dong Volume
            sys.stdout.write('\033[K')  # Clear line
            sys.stdout.write(f"Volume: {price_info['volume']:.6f} BTC\n")

            # Cap nhat dong Thoi gian
            sys.stdout.write('\033[K')  # Clear line
            sys.stdout.write(f"Thoi gian: {price_info['timestamp']}\n")

            # In lai cac dong footer (khong thay doi)
            sys.stdout.write("\n" + "="*70 + "\n")
            sys.stdout.write("Nhan Ctrl+C de dung\n")
            sys.stdout.write("="*70 + "\n")

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

            # Chay WebSocket trong thread rieng
            self.ws_binance.run_forever()

        except KeyboardInterrupt:
            print("\n\nDang dung ket noi...")
            self.running = False
            if self.ws_binance:
                self.ws_binance.close()
            print("Da dung theo doi gia Bitcoin.")
        except Exception as e:
            print(f"Loi: {e}")
            self.running = False


def main():
    """Ham main de chay chuong trinh"""
    btc_tracker = BTCRealTimePrice()

    print("\n" + "="*70)
    print(f"{'CHUONG TRINH THEO DOI GIA BITCOIN REAL-TIME (WEBSOCKET)':^70}")
    print("="*70)
    print("\nChuong trinh su dung WebSocket de nhan du lieu real-time")
    print("Du lieu duoc cap nhat ngay lap tuc khi co giao dich moi")
    print("\n")

    input("Nhan Enter de bat dau...")

    btc_tracker.monitor_realtime_binance()


if __name__ == "__main__":
    main()
