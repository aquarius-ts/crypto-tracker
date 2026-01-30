# Crypto & Gold Real-Time Price Tracker - Hướng Dẫn Sử Dụng

## 🎯 Tính Năng Mới (Version 3.0)

### ✅ **Đã hoàn thành:**

1. **Dropdown Menu với 20+ Cryptocurrencies** 🪙
   - Không còn chỉ 2 nút Bitcoin/Gold
   - Sử dụng **Combobox** với tính năng search/filter
   - Chỉ cần gõ tên coin để tìm kiếm nhanh
   - Danh sách 20 coin phổ biến nhất trên Binance

2. **20 Cryptocurrencies hỗ trợ:**
   - 🟠 **BTC** - Bitcoin
   - 🔷 **ETH** - Ethereum
   - 🟡 **BNB** - Binance Coin
   - ⚫ **XRP** - Ripple
   - 🟢 **SOL** - Solana
   - 🔵 **ADA** - Cardano
   - 🟤 **DOGE** - Dogecoin
   - 🔴 **TRX** - Tron
   - 🔺 **AVAX** - Avalanche
   - 🟠 **SHIB** - Shiba Inu
   - 🟣 **DOT** - Polkadot
   - 🟣 **MATIC** - Polygon
   - ⚪ **LTC** - Litecoin
   - 🩷 **UNI** - Uniswap
   - 🔵 **LINK** - Chainlink
   - ⚫ **ATOM** - Cosmos
   - 🔷 **XLM** - Stellar
   - 🟢 **ETC** - Ethereum Classic
   - 🟢 **BCH** - Bitcoin Cash
   - 🟡 **PAXG** - Gold (tokenized)

3. **Chuyển đổi USD ↔ VNĐ** 💱
   - Nút USD/VND đã được sửa lỗi
   - Tỷ giá: 1 USD = 25,000 VND
   - Tất cả số liệu tự động chuyển đổi

4. **Tự động cập nhật màu sắc** 🎨
   - Mỗi coin có màu riêng biệt
   - Title tự động đổi màu theo coin đang xem
   - UI chuyên nghiệp và dễ nhận biết

## 🎨 Giao Diện Mới

```
┌────────────────────────────────────────────────────────────┐
│           BITCOIN REAL-TIME TRACKER                        │
├────────────────────────────────────────────────────────────┤
│ Coin: [BTC - Bitcoin         ▼]                           │
│ Currency: [USD] [VND]                                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│                   $83,125.50                              │
│                UP +15.25 USD                              │
│                                                            │
├────────────────────────────────────────────────────────────┤
│       24H HIGH              24H LOW                        │
│      $83,250.00           $82,980.50                      │
├────────────────────────────────────────────────────────────┤
│  [+] Connected - Live                                     │
│                                                            │
│      [▶ START]              [⏹ STOP]                      │
└────────────────────────────────────────────────────────────┘
```

## 🚀 Cách Sử Dụng

### 1. **Khởi động**
```bash
python3 btc_gui.py
```

### 2. **Chọn Coin**
Có 2 cách:
- **Click dropdown** → Chọn coin từ danh sách
- **Gõ tìm kiếm**: Click vào dropdown → Gõ "ETH", "DOGE", v.v.
  - Combobox có tính năng filter tự động!

### 3. **Chọn Currency**
- Click **USD** để hiển thị bằng đô la
- Click **VND** để hiển thị bằng Việt Nam Đồng

### 4. **Bắt đầu theo dõi**
- Click **▶ START** để kết nối
- Giá sẽ cập nhật real-time
- Click **⏹ STOP** để dừng

### 5. **Chuyển đổi coin**
- Chọn coin khác từ dropdown
- Nếu đang chạy: Tự động reconnect WebSocket
- Title và màu sắc tự động cập nhật

## 📊 Ví Dụ Hiển Thị

### **Ethereum (ETH) + USD**:
```
ETHEREUM REAL-TIME TRACKER
$2,850.75
UP +25.30 USD

24H HIGH: $2,890.00
24H LOW: $2,780.50
```

### **Dogecoin (DOGE) + VND**:
```
DOGECOIN REAL-TIME TRACKER
2,250 VND
DOWN -125 VND

24H HIGH: 2,500 VND
24H LOW: 2,150 VND
```

### **Gold (PAXG) + USD**:
```
GOLD REAL-TIME TRACKER
$2,725.80
UP +12.50 USD

24H HIGH: $2,750.00
24H LOW: $2,698.20
```

## 🔧 Kỹ Thuật

### **WebSocket Dynamic URLs:**
Tự động build URL dựa trên coin được chọn:
```python
symbol = coin_info['symbol'].lower()  # Ví dụ: "ethusdt"
trade_url = f"wss://stream.binance.com:9443/ws/{symbol}@trade"
ticker_url = f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
```

### **Tính năng:**
- ✅ Dropdown menu với ttk.Combobox
- ✅ 20 cryptocurrencies phổ biến
- ✅ Tìm kiếm nhanh trong dropdown
- ✅ Dynamic WebSocket connection
- ✅ Tự động đổi màu theo coin
- ✅ Currency converter (USD/VND)
- ✅ Thread-safe UI updates
- ✅ Auto-reconnect khi đổi coin

## 💡 Mẹo Sử Dụng

1. **Tìm kiếm nhanh**: 
   - Click dropdown → Gõ vài chữ cái đầu
   - Ví dụ: Gõ "DO" → Tìm thấy "DOGE - Dogecoin"

2. **Chuyển đổi nhanh**:
   - Có thể chuyển coin khi đang chạy
   - Hệ thống tự động reconnect trong 0.5s

3. **Theo dõi nhiều coin**:
   - Mở nhiều cửa sổ để theo dõi nhiều coin cùng lúc
   - Mỗi cửa sổ độc lập với nhau

## 📝 Coin List & Colors

| Code | Name | Color | Symbol |
|------|------|-------|--------|
| BTC | Bitcoin | #f7931a | BTCUSDT |
| ETH | Ethereum | #627eea | ETHUSDT |
| BNB | Binance Coin | #f3ba2f | BNBUSDT |
| XRP | Ripple | #23292f | XRPUSDT |
| SOL | Solana | #14f195 | SOLUSDT |
| ADA | Cardano | #0033ad | ADAUSDT |
| DOGE | Dogecoin | #c2a633 | DOGEUSDT |
| TRX | Tron | #ff0013 | TRXUSDT |
| AVAX | Avalanche | #e84142 | AVAXUSDT |
| SHIB | Shiba Inu | #ffa409 | SHIBUSDT |
| DOT | Polkadot | #e6007a | DOTUSDT |
| MATIC | Polygon | #8247e5 | MATICUSDT |
| LTC | Litecoin | #345d9d | LTCUSDT |
| UNI | Uniswap | #ff007a | UNIUSDT |
| LINK | Chainlink | #2a5ada | LINKUSDT |
| ATOM | Cosmos | #2e3148 | ATOMUSDT |
| XLM | Stellar | #14b6e7 | XLMUSDT |
| ETC | Ethereum Classic | #328332 | ETCUSDT |
| BCH | Bitcoin Cash | #8dc351 | BCHUSDT |
| PAXG | Gold | #FFD700 | PAXGUSDT |

## 📝 Changelog

### Version 3.0 (Latest - 30/01/2026)
- ✅ Thay thế nút Bitcoin/Gold bằng Dropdown menu
- ✅ Thêm 20 cryptocurrencies
- ✅ Tính năng search/filter trong dropdown
- ✅ Sửa lỗi button USD/VND
- ✅ Dynamic WebSocket URL generation
- ✅ Tự động đổi màu title theo coin
- ✅ Improved UI/UX

### Version 2.0
- Bỏ Volume display
- Bỏ % thay đổi
- Thêm option Bitcoin/Gold (2 nút)
- Thêm chuyển đổi USD/VND

### Version 1.0
- WebSocket real-time data
- 24H HIGH/LOW display
- START/STOP controls

## 🎓 Muốn thêm coin khác?

Rất dễ! Chỉ cần thêm vào dictionary `available_coins`:

```python
"COIN_CODE": {
    "name": "Coin Name",
    "symbol": "COINUSDT",  # Symbol trên Binance
    "color": "#hexcolor"    # Màu hiển thị
}
```

Ví dụ thêm Pepe coin:
```python
"PEPE": {
    "name": "Pepe",
    "symbol": "PEPEUSDT",
    "color": "#00ff00"
}
```

Hệ thống sẽ tự động:
- Thêm vào dropdown
- Tạo WebSocket connection
- Cập nhật title và màu sắc

