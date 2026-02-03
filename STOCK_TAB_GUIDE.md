# Vietnam Stock Market Tab - Implementation Guide

## Overview
Added a new tab to the Crypto Tracker application for tracking Vietnamese stock market information in real-time.

## Features Added

### 1. **Tabbed Interface**
- Used `ttk.Notebook` to create a modern tabbed interface
- Tab 1: Cryptocurrency tracking (original functionality)
- Tab 2: Vietnam Stock Market tracking (new feature)

### 2. **Vietnam Stock Tab Components**

#### Input Section
- Stock code entry field (e.g., VNM, VIC, HPG)
- "Tải Cổ Phiếu" button to load stock data
- Quick select buttons for popular stocks: VNM, VIC, HPG, FPT, VCB, MSN

#### Display Section
- **Stock Name**: Displays the stock code
- **Current Price**: Large display showing current price in VND
- **Price Change**: Shows change amount and percentage with color coding:
  - Green (▲) for positive
  - Red (▼) for negative
  - Yellow (─) for no change

#### Stock Details Grid
Shows key trading information:
- **Trần (Ceiling)**: Maximum price allowed for the day
- **Sàn (Floor)**: Minimum price allowed for the day
- **Tham chiếu (Reference)**: Reference price
- **Khối lượng (Volume)**: Trading volume (formatted as M/K)
- **Cao nhất (High)**: Highest price of the day
- **Thấp nhất (Low)**: Lowest price of the day

#### Control Buttons
- **▶ BẮT ĐẦU**: Start automatic tracking (refreshes every 30 seconds)
- **⏹ DỪNG**: Stop automatic tracking

### 3. **API Integration**
Uses VNDirect API to fetch real-time stock data:
```
https://finfo-api.vndirect.com.vn/v4/stock_prices/{stock_code}
```

### 4. **Auto-refresh Feature**
- When tracking is started, the stock data refreshes automatically every 30 seconds
- Can be stopped at any time using the DỪNG button

## Technical Implementation

### New Variables Added
```python
self.stock_running = False          # Tracking state
self.current_stock = "VNM"          # Current stock code
self.stock_data = {}                # Stock data cache
self.stock_update_timer = None      # Timer for auto-refresh
```

### New Methods Added
1. `setup_stock_tab()` - Creates the stock market UI
2. `quick_select_stock()` - Quick selection of popular stocks
3. `load_stock()` - Loads stock data when user clicks button
4. `fetch_stock_data()` - Fetches data from API in background thread
5. `update_stock_display()` - Updates UI with fetched stock data
6. `start_stock_tracking()` - Starts auto-refresh tracking
7. `stop_stock_tracking()` - Stops auto-refresh tracking
8. `auto_update_stock()` - Recursive method for periodic updates

### UI Color Scheme
- Background: Dark theme (#1e1e1e, #2d2d2d)
- Title: Blue (#00aaff)
- Price colors:
  - Green (#00ff00) for positive/high
  - Red (#ff0000) for negative/low
  - Magenta (#ff00ff) for ceiling
  - Cyan (#00ffff) for floor
  - Yellow (#ffff00) for reference

## Usage

### For End Users
1. Launch the application
2. Click on "Vietnam Stocks" tab
3. Enter a stock code (e.g., VNM) or click a popular stock button
4. Click "Tải Cổ Phiếu" to load current data
5. Optionally click "BẮT ĐẦU" to enable auto-refresh every 30 seconds

### Popular Vietnamese Stocks Included
- **VNM**: Vietnam Dairy Products (Vinamilk)
- **VIC**: Vingroup
- **HPG**: Hoa Phat Group
- **FPT**: FPT Corporation
- **VCB**: Vietcombank
- **MSN**: Masan Group

## Notes
- Stock data is fetched from VNDirect's public API
- All prices are displayed in VND
- The application handles API errors gracefully with status messages
- The original crypto tracking functionality remains unchanged and fully functional

## Future Enhancements
Potential improvements:
- Add stock search with autocomplete
- Add more detailed company information
- Add price charts/history
- Add watchlist functionality
- Add alerts for price thresholds
- Support for multiple exchanges (HOSE, HNX, UPCOM)
