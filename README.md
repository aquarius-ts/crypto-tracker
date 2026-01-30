# Crypto Real-Time Price Tracker 🚀

[![CI - Continuous Integration](https://github.com/aquarius-ts/crypto-tracker/workflows/CI%20-%20Continuous%20Integration/badge.svg)](https://github.com/aquarius-ts/crypto-tracker/actions)
[![CD - Continuous Deployment](https://github.com/aquarius-ts/crypto-tracker/workflows/CD%20-%20Continuous%20Deployment/badge.svg)](https://github.com/aquarius-ts/crypto-tracker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Mô tả
Chương trình theo dõi giá Bitcoin real-time sử dụng WebSocket từ Binance với 2 giao diện:
- **GUI (Khuyên dùng)**: Giao diện đồ họa hiện đại, mượt mà
- **Terminal**: Giao diện dòng lệnh đơn giản

## Tính năng
- ✅ Kết nối WebSocket đến Binance để nhận dữ liệu real-time
- ✅ Hiển thị giá Bitcoin (BTC/USDT) cập nhật liên tục
- ✅ Hiển thị volume của mỗi giao dịch
- ✅ Timestamp chính xác đến mili giây
- ✅ Hiển thị thay đổi giá (UP/DOWN) với màu sắc
- ✅ Theo dõi giá cao nhất và thấp nhất trong phiên
- ✅ Giao diện đẹp mắt, không spam text

## Cài đặt

### 1. Cài đặt thư viện cần thiết
```bash
# Cài đặt WebSocket client
pip install websocket-client

# Cài đặt tkinter cho GUI (Ubuntu/Debian)
sudo apt-get install python3-tk
```

### 2. Chạy chương trình

#### GUI (Khuyên dùng) ⭐
```bash
python3 btc_gui.py
```

**Hướng dẫn sử dụng GUI:**
1. Mở ứng dụng
2. Nhấn nút **START** để bắt đầu theo dõi
3. Giá sẽ tự động cập nhật real-time
4. Nhấn nút **STOP** để dừng
5. Đóng cửa sổ để thoát

**Tính năng GUI:**
- 🎨 Giao diện hiện đại với theme tối
- 💰 Hiển thị giá lớn, dễ nhìn
- 📊 Màu xanh khi giá tăng, đỏ khi giá giảm
- 📈 Theo dõi HIGH/LOW trong phiên
- ⏱️ Cập nhật mượt mà, không giật lag
- 🔄 Tự động reconnect khi mất kết nối

#### Terminal
```bash
python3 btcrealtime.py
```

## Demo

### GUI Interface
```
┌─────────────────────────────────────────────────────┐
│         BITCOIN REAL-TIME TRACKER                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│                 $83,125.50                          │
│            UP +15.25 (+0.02%)                       │
│                                                     │
├─────────────────────────────────────────────────────┤
│  VOLUME              │  LAST UPDATE                 │
│  0.125000 BTC        │  14:25:32.156                │
│                                                     │
│  SESSION HIGH        │  SESSION LOW                 │
│  $83,250.00          │  $82,980.50                  │
├─────────────────────────────────────────────────────┤
│  [+] Connected - Live                               │
│                                                     │
│      [START]              [STOP]                    │
└─────────────────────────────────────────────────────┘
```

## So sánh 2 giao diện

| Tính năng | GUI | Terminal |
|-----------|-----|----------|
| Cập nhật mượt mà | ✅ | ⚠️ |
| Dễ sử dụng | ✅ | ❌ |
| Giao diện đẹp | ✅ | ❌ |
| Không spam text | ✅ | ⚠️ |
| Chạy trên server | ❌ | ✅ |
| Nhẹ tài nguyên | ⚠️ | ✅ |

## Ưu điểm của WebSocket so với REST API
- ⚡ **Real-time thực sự**: Dữ liệu được push ngay lập tức, không cần polling
- 🚀 **Hiệu quả hơn**: Chỉ duy trì 1 kết nối, không gọi API liên tục
- 📊 **Độ trễ thấp**: Nhận dữ liệu ngay khi có giao dịch mới
- 💪 **Ít tải hơn**: Không bị giới hạn rate limit như REST API

## Kỹ thuật sử dụng
- **WebSocket**: Kết nối 2 chiều giữa client và server
- **Binance Stream API**: `wss://stream.binance.com:9443/ws/btcusdt@trade`
- **Event-driven**: Sử dụng callback để xử lý message real-time
- **Threading**: WebSocket chạy trong thread riêng để không block UI
- **Tkinter**: Thư viện GUI tích hợp sẵn trong Python

## Lưu ý
- Cần kết nối internet ổn định
- WebSocket sẽ tự động reconnect nếu bị ngắt kết nối
- Dữ liệu cập nhật liên tục, có thể thay đổi rất nhanh
- GUI yêu cầu môi trường đồ họa (X11/Wayland)
- Terminal version hoạt động tốt hơn qua SSH
