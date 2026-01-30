# 🚀 Crypto Real-Time Price Tracker - FINAL VERSION

## ✅ **ĐÃ HOÀN THÀNH**

### **Tính năng chính:**
1. ✅ **TẤT CẢ coins trên Binance** (400+ coins!)
2. ✅ **Không giới hạn** - Chỉ cần nhập coin code
3. ✅ **Search đơn giản** - Gõ code và nhấn Load
4. ✅ **Nút quick select** - 5 coin phổ biến nhất
5. ✅ **Chuyển đổi USD/VND** - Tỷ giá 1:25,000
6. ✅ **Real-time WebSocket** - Cập nhật tức thì
7. ✅ **24H HIGH/LOW** - Thống kê 24 giờ
8. ✅ **Không spam** - Chỉ cập nhật giá trị thay đổi

## 🎮 **CÁCH SỬ DỤNG**

### **File chạy: `crypto_tracker_simple.py`**

```bash
python3 crypto_tracker_simple.py
```

### **Hướng dẫn sử dụng:**

1. **Nhập coin code vào ô "Enter Coin Code"**
   - Ví dụ: BTC, ETH, DOGE, SHIB, PEPE, v.v.
   - Coin code KHÔNG phân biệt hoa thường

2. **Click "Load Coin" hoặc nhấn Enter**
   - Hệ thống sẽ tải thông tin coin

3. **Click nút quick select (nếu muốn)**
   - BTC, ETH, BNB, XRP, SOL - Click để chọn nhanh

4. **Chọn currency: USD hoặc VND**
   - Click nút USD: Hiển thị bằng đô la
   - Click nút VND: Hiển thị bằng Việt Nam Đồng

5. **Click ▶ START**
   - Kết nối WebSocket
   - Bắt đầu nhận dữ liệu real-time

6. **Xem giá real-time!**
   - Giá tự động cập nhật
   - UP (xanh) khi tăng
   - DOWN (đỏ) khi giảm

7. **Click ⏹ STOP để dừng**

## 📊 **VÍ DỤ SỬ DỤNG**

### **Xem giá Bitcoin:**
```
1. Nhập: BTC
2. Click: Load Coin
3. Click: ▶ START
```

### **Xem giá Dogecoin bằng VND:**
```
1. Nhập: DOGE
2. Click: Load Coin
3. Click: VND
4. Click: ▶ START
```

### **Xem giá Shiba Inu:**
```
1. Nhập: SHIB
2. Click: Load Coin
3. Click: ▶ START
```

### **Xem giá PEPE coin:**
```
1. Nhập: PEPE
2. Click: Load Coin
3. Click: ▶ START
```

## 💡 **COIN CODES PHỔ BIẾN**

| Code | Coin Name | Code | Coin Name |
|------|-----------|------|-----------|
| BTC | Bitcoin | ETH | Ethereum |
| BNB | Binance Coin | XRP | Ripple |
| SOL | Solana | ADA | Cardano |
| DOGE | Dogecoin | MATIC | Polygon |
| DOT | Polkadot | AVAX | Avalanche |
| SHIB | Shiba Inu | LINK | Chainlink |
| UNI | Uniswap | ATOM | Cosmos |
| LTC | Litecoin | ETC | Ethereum Classic |
| TRX | Tron | XLM | Stellar |
| PEPE | Pepe | FLOKI | Floki |

**Và hơn 400+ coins khác!**

## 🔍 **LÀM SAO BIẾT COIN CODE?**

Các cách tìm coin code:

1. **CoinMarketCap**: Xem trang coin → Tìm "Symbol"
2. **Binance**: Vào Markets → Xem cột Symbol
3. **Google**: Gõ "tên coin symbol binance"

Ví dụ:
- Bitcoin → BTC
- Ethereum → ETH
- Shiba Inu → SHIB
- Pepe → PEPE

## 🎨 **GIAO DIỆN**

```
┌──────────────────────────────────────────────────────┐
│        BITCOIN REAL-TIME TRACKER                     │
├──────────────────────────────────────────────────────┤
│ Enter Coin Code: [BTC    ] [Load Coin]              │
│ Popular: [BTC] [ETH] [BNB] [XRP] [SOL]              │
│                                                      │
│ Currency: [USD] [VND]                                │
├──────────────────────────────────────────────────────┤
│                                                      │
│                  $83,125.50                         │
│               UP +15.25 USD                         │
│                                                      │
├──────────────────────────────────────────────────────┤
│      24H HIGH           24H LOW                      │
│     $83,250.00         $82,980.50                   │
├──────────────────────────────────────────────────────┤
│ [+] Connected - Live                                │
│                                                      │
│     [▶ START]           [⏹ STOP]                    │
└──────────────────────────────────────────────────────┘
```

## ⚙️ **KỸ THUẬT**

### **WebSocket Streams:**
- Trade stream: `wss://stream.binance.com:9443/ws/{symbol}@trade`
- Ticker stream: `wss://stream.binance.com:9443/ws/{symbol}@ticker`

### **Hỗ trợ:**
- ✅ Tất cả USDT pairs trên Binance
- ✅ Real-time price updates
- ✅ 24h statistics
- ✅ USD/VND conversion
- ✅ Thread-safe
- ✅ Auto-reconnect

## 🎯 **TẠI SAO DÙNG VERSION NÀY?**

### **Ưu điểm:**

1. **Đơn giản** ✅
   - Không phức tạp
   - Không popup window
   - Chỉ nhập code và go!

2. **Hỗ trợ TẤT CẢ coins** ✅
   - Không giới hạn 20 coins
   - Hơn 400+ coins
   - Binance liên tục thêm coin mới? Không vấn đề!

3. **Nhanh** ✅
   - Không load danh sách coins
   - Không popup crash
   - Ổn định

4. **Linh hoạt** ✅
   - Nhập bất kỳ coin code nào
   - Quick select cho coin phổ biến
   - USD hoặc VND

## 🐛 **TROUBLESHOOTING**

### **Lỗi "Error: 400"**
→ Coin code không tồn tại trên Binance
→ Kiểm tra lại spelling

### **Không kết nối được**
→ Kiểm tra internet
→ Thử coin khác (BTC, ETH)

### **GUI không mở**
→ Cài đặt: `sudo apt-get install python3-tk`

## 📝 **LƯU Ý**

- Chỉ hỗ trợ coins có pair USDT trên Binance
- Tỷ giá USD/VND: 1 = 25,000 (cố định)
- Coin code không phân biệt hoa/thường
- Data real-time từ Binance
- Miễn phí 100%

## 🎉 **KẾT LUẬN**

Version này là **tốt nhất** vì:
- ✅ Hỗ trợ TẤT CẢ coins
- ✅ Đơn giản, dễ dùng
- ✅ Không bị crash
- ✅ Không giới hạn
- ✅ Ổn định

**Enjoy tracking your crypto! 🚀**
