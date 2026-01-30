# 📦 Build Executable Guide

## Build File EXE/Binary cho Crypto Tracker

### ✅ Build Thành Công!

File executable đã được build tại: `dist/CryptoTracker`
- **Size**: ~17MB
- **Platform**: Linux (hoặc tùy theo OS bạn build)

---

## 🚀 Quick Build

### Linux/Mac:
```bash
./build.sh
```

### Windows:
```batch
build.bat
```

Hoặc:
```bash
python -m PyInstaller crypto_tracker.spec
```

---

## 📋 Build Requirements

```bash
pip install pyinstaller
pip install -r requirements.txt
```

---

## 🔧 Build Options

### 1. Using Spec File (Recommended)
```bash
pyinstaller crypto_tracker.spec
```

**Ưu điểm:**
- ✅ Cấu hình chi tiết
- ✅ Hidden imports được xử lý
- ✅ Reproducible builds
- ✅ No console window

### 2. Direct Build (Simple)
```bash
pyinstaller --onefile --windowed --name CryptoTracker crypto_tracker_simple.py
```

**Tùy chọn:**
- `--onefile`: Single executable file
- `--windowed`: No console window
- `--name`: Output filename
- `--icon=icon.ico`: Add custom icon (nếu có)

---

## 📦 Build Outputs

```
dist/
  └── CryptoTracker          # Executable file
build/                       # Temporary build files (có thể xóa)
__pycache__/                 # Python cache (có thể xóa)
```

### Clean Build:
```bash
rm -rf build dist __pycache__ *.spec.bak
```

---

## 🌐 Multi-Platform Builds

### Build cho từng platform:

#### Linux:
```bash
# Build trên Linux machine
./build.sh
# Output: dist/CryptoTracker
```

#### Windows:
```batch
# Build trên Windows machine
build.bat
# Output: dist\CryptoTracker.exe
```

#### macOS:
```bash
# Build trên macOS machine
./build.sh
# Output: dist/CryptoTracker
```

**Lưu ý:** Phải build trên từng platform để có executable tương ứng.

---

## 🤖 CI/CD Auto Build

CI/CD đã được cấu hình để tự động build executables!

### Khi Push lên Main:
```bash
git push origin main
```
→ CI/CD sẽ build cho Linux, Windows, macOS và upload artifacts.

### Khi Tạo Release Tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

→ CI/CD sẽ:
1. ✅ Build executables cho 3 platforms
2. ✅ Tạo GitHub Release
3. ✅ Upload files để download

**Download từ**: https://github.com/aquarius-ts/crypto-tracker/releases

---

## 🧪 Test Executable

### Linux/Mac:
```bash
./dist/CryptoTracker
```

### Windows:
```batch
dist\CryptoTracker.exe
```

---

## 🐛 Troubleshooting

### Issue 1: ModuleNotFoundError
**Solution:** Thêm module vào `hiddenimports` trong `crypto_tracker.spec`

```python
hiddenimports=[
    'websocket',
    'requests',
    'your_missing_module',
],
```

### Issue 2: Tkinter not found
**Linux:**
```bash
sudo apt-get install python3-tk
```

**Windows/Mac:** Tkinter có sẵn trong Python installation.

### Issue 3: File too large
**Solution:** Exclude unused modules:

```python
excludes=[
    'matplotlib',
    'pandas',
    'numpy',
],
```

### Issue 4: SSL/HTTPS errors
**Solution:** Đã bao gồm certifi trong spec file.

### Issue 5: Missing DLLs (Windows)
**Solution:** PyInstaller tự động include, nhưng nếu thiếu:
- Cài Visual C++ Redistributable
- Hoặc copy DLLs vào thư mục dist/

---

## 📊 Build Size Optimization

### Current size: ~17MB

### Để giảm size:

1. **Exclude unused modules:**
```python
excludes=['matplotlib', 'pandas', 'numpy', 'scipy'],
```

2. **Use UPX compression:**
```python
upx=True,
upx_exclude=[],
```

3. **Strip debug symbols:**
```python
strip=True,
```

4. **Remove test/dev files:**
```bash
# Không include trong build
excludes=['pytest', 'unittest'],
```

---

## 🎯 Distribution

### Chia sẻ executable:

1. **Direct file share:**
   - Zip file và gửi
   - Upload lên Google Drive/Dropbox

2. **GitHub Releases:**
   - Tạo tag → Tự động build
   - Users download từ Releases page

3. **Website/Server:**
   - Host files để download
   - Provide checksums cho security

---

## 📝 Build Checklist

- [ ] Cài đặt PyInstaller
- [ ] Cài đặt dependencies (requirements.txt)
- [ ] Test app chạy bình thường
- [ ] Chạy build script
- [ ] Test executable
- [ ] Check file size
- [ ] Verify no console window
- [ ] Test trên target platform
- [ ] Create release tag (optional)

---

## 🔒 Security Notes

- Executables không obfuscated hoàn toàn
- Source code có thể được decompile (khó nhưng có thể)
- Không hardcode sensitive data (API keys, passwords)
- Use environment variables hoặc config files

---

## 📚 Advanced Topics

### Custom Icon:
```bash
pyinstaller --icon=icon.ico crypto_tracker_simple.py
```

### Version Info (Windows):
```bash
pyinstaller --version-file=version.txt crypto_tracker_simple.py
```

### One Directory Mode:
```bash
pyinstaller --onedir crypto_tracker_simple.py
# Output: dist/CryptoTracker/ (folder with multiple files)
```

---

## 🎉 Success!

Build thành công! File executable:
- ✅ Standalone (không cần Python installed)
- ✅ No console window
- ✅ Double-click to run
- ✅ ~17MB size
- ✅ Multi-platform support (via CI/CD)

**Run it:**
```bash
./dist/CryptoTracker
```

---

## 🔗 Links

- **Repository**: https://github.com/aquarius-ts/crypto-tracker
- **Releases**: https://github.com/aquarius-ts/crypto-tracker/releases
- **Actions**: https://github.com/aquarius-ts/crypto-tracker/actions
- **PyInstaller Docs**: https://pyinstaller.org/

---

**Happy Building! 🚀**
