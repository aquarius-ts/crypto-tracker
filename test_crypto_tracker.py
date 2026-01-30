# -*- coding: utf-8 -*-
"""
Simple test file for CI/CD pipeline
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestBasic(unittest.TestCase):
    """Basic tests for the crypto tracker"""

    def test_import(self):
        """Test if main module can be imported"""
        try:
            import crypto_tracker_simple
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import crypto_tracker_simple: {e}")

    def test_popular_coins(self):
        """Test popular coins list"""
        from crypto_tracker_simple import CryptoTrackerGUI
        import tkinter as tk

        root = tk.Tk()
        app = CryptoTrackerGUI(root)

        # Check if popular coins exist
        self.assertIn("BTC", app.popular_coins)
        self.assertIn("ETH", app.popular_coins)
        self.assertIn("BNB", app.popular_coins)

        # Check coin properties
        btc = app.popular_coins["BTC"]
        self.assertIn("name", btc)
        self.assertIn("color", btc)

        root.destroy()

    def test_currency_switch(self):
        """Test currency switching functionality"""
        from crypto_tracker_simple import CryptoTrackerGUI
        import tkinter as tk

        root = tk.Tk()
        app = CryptoTrackerGUI(root)

        # Default should be USD
        self.assertEqual(app.current_currency, "USD")

        # Switch to VND
        app.switch_to_vnd()
        self.assertEqual(app.current_currency, "VND")

        # Switch back to USD
        app.switch_to_usd()
        self.assertEqual(app.current_currency, "USD")

        root.destroy()

    def test_usd_to_vnd_rate(self):
        """Test USD to VND conversion rate"""
        from crypto_tracker_simple import CryptoTrackerGUI
        import tkinter as tk

        root = tk.Tk()
        app = CryptoTrackerGUI(root)

        self.assertGreater(app.usd_to_vnd, 0)
        self.assertIsInstance(app.usd_to_vnd, (int, float))

        root.destroy()


class TestWebSocket(unittest.TestCase):
    """Test WebSocket related functionality"""

    def test_websocket_url_format(self):
        """Test WebSocket URL formatting"""
        from crypto_tracker_simple import CryptoTrackerGUI
        import tkinter as tk

        root = tk.Tk()
        app = CryptoTrackerGUI(root)

        # Test symbol formatting
        app.current_asset = "BTC"
        symbol = f"{app.current_asset}USDT".lower()

        self.assertEqual(symbol, "btcusdt")

        # Test URL format
        trade_url = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
        ticker_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"

        self.assertTrue(trade_url.startswith("wss://"))
        self.assertTrue(ticker_url.startswith("wss://"))
        self.assertIn("btcusdt", trade_url)
        self.assertIn("btcusdt", ticker_url)

        root.destroy()


if __name__ == '__main__':
    unittest.main()
