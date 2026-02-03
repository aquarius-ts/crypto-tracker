# 🚀 Quick Start - Push to GitHub & Setup CI/CD

## Cách Nhanh Nhất (Chỉ 3 Bước)

### Bước 1: Tạo Repository Trên GitHub
1. Vào https://github.com/new
2. Đặt tên repository: `crypto-tracker`
3. **KHÔNG** tick "Initialize this repository with a README"
4. Click "Create repository"
5. Copy URL repository (vd: `https://github.com/username/crypto-tracker.git`)

### Bước 2: Chạy Script Tự Động
```bash
./push_to_github.sh
```

Script sẽ hỏi:
- GitHub repository URL → paste URL vừa copy
- Tên và email (nếu chưa config)
- Commit message → Enter để dùng mặc định
- Confirm push → nhập `y`

### Bước 3: Xem CI/CD Chạy
1. Vào repository trên GitHub
2. Click tab **Actions**
3. Xem CI/CD đang chạy! ✅

---

## Hoặc Làm Thủ Công

```bash
# 1. Khởi tạo git (nếu chưa có)
git init

# 2. Config user
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Thêm remote (thay YOUR_USERNAME và YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 4. Add, commit, push
git add .
git commit -m "Initial commit with CI/CD"
git branch -M main
git push -u origin main
```

---

## Files CI/CD Đã Tạo

✅ `.github/workflows/ci.yml` - Continuous Integration
- Chạy tests tự động
- Kiểm tra code quality (flake8)
- Security scan (safety, bandit)
- Chạy trên: Ubuntu, Windows, macOS
- Python: 3.8, 3.9, 3.10, 3.11

✅ `.github/workflows/cd.yml` - Continuous Deployment
- Build executables tự động
- Tạo GitHub releases
- Build Docker images (nếu config)

✅ `Dockerfile` - Docker containerization

✅ `.gitignore` - Loại trừ files không cần

✅ `LICENSE` - MIT License

✅ `CONTRIBUTING.md` - Hướng dẫn contribute

✅ `test_crypto_tracker.py` - Unit tests

✅ `README_GITHUB.md` - README cho GitHub (đổi tên thành README.md)

---

## CI/CD Sẽ Chạy Khi Nào?

### CI (Tests & Quality Checks)
- ✅ Mỗi khi push lên `main` hoặc `develop`
- ✅ Mỗi khi tạo Pull Request
- ✅ Chạy tests trên nhiều OS và Python versions

### CD (Build & Deploy)
- ✅ Khi push lên `main`
- ✅ Khi tạo tag version (vd: `v1.0.0`)
- ✅ Build executables cho Windows, Linux, macOS

---

## Tạo Release (Tùy Chọn)

### Cách 1: Qua GitHub UI
1. Vào repository → Releases → "Create a new release"
2. Tag: `v1.0.0`, Title: `v1.0.0 - Initial Release`
3. Click "Publish release"

### Cách 2: Qua Command Line
```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

CI/CD sẽ tự động build executables và upload vào release!

---

## Cấu Hình Docker Hub (Tùy Chọn)

Nếu muốn tự động push Docker image:

1. Tạo account tại https://hub.docker.com
2. Tạo Access Token: Account Settings → Security → New Access Token
3. Thêm vào GitHub Secrets:
   - Repository → Settings → Secrets → Actions
   - Thêm `DOCKER_USERNAME` và `DOCKER_PASSWORD`

---

## Test Local Trước Khi Push

```bash
# Chạy tests
pytest

# Kiểm tra code style
flake8 .

# Security scan (cài trước nếu chưa có)
pip install safety bandit
safety check
bandit -r .
```

---

## Badges Cho README

Cập nhật `README_GITHUB.md` (đổi YOUR_USERNAME và YOUR_REPO):

```markdown
[![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
[![CD](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CD/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPO/actions)
```

---

## Troubleshooting

### "Authentication failed"
- Dùng **Personal Access Token** thay password
- GitHub → Settings → Developer settings → Personal access tokens
- Tạo token với scope `repo`
- Dùng token làm password khi push

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin YOUR_URL
```

### Xem logs CI/CD
- GitHub → Actions → Click vào workflow run

---

## Workflow Hàng Ngày

```bash
# Pull latest changes
git pull

# Tạo branch cho feature mới
git checkout -b feature/ten-feature

# Code...

# Commit và push
git add .
git commit -m "Add: mô tả feature"
git push origin feature/ten-feature

# Tạo Pull Request trên GitHub
# CI sẽ tự động chạy!
```

---

## Tài Liệu Chi Tiết

- 📖 **GITHUB_GUIDE.md** - Hướng dẫn đầy đủ
- 📖 **CONTRIBUTING.md** - Quy tắc contribute
- 📖 **README_GITHUB.md** - README mẫu cho GitHub

---

## Kết Quả Sau Khi Setup

✅ Code được version control
✅ Tests tự động mỗi khi push
✅ Code quality checks tự động
✅ Security scans tự động
✅ Build executables tự động
✅ Professional project structure

**Happy Coding! 🎉**
