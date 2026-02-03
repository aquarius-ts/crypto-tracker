# Hướng Dẫn Push Lên GitHub và Cài Đặt CI/CD

## Bước 1: Chuẩn Bị Repository

### 1.1 Tạo Repository Mới Trên GitHub

1. Đăng nhập vào GitHub (https://github.com)
2. Click nút "+" ở góc trên bên phải, chọn "New repository"
3. Điền thông tin:
   - **Repository name**: `crypto-tracker` (hoặc tên bạn muốn)
   - **Description**: "Real-time cryptocurrency price tracker"
   - **Public** hoặc **Private**: Tùy chọn
   - **KHÔNG** chọn "Initialize this repository with a README" (vì đã có sẵn)
4. Click "Create repository"

### 1.2 Cấu Hình Git Local

```bash
# Di chuyển vào thư mục project
cd /home/anhtuan/PycharmProjects/PythonProject7

# Khởi tạo git (nếu chưa có)
git init

# Cấu hình user (thay thế bằng thông tin của bạn)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Thêm remote repository (thay YOUR_USERNAME và YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Hoặc dùng SSH (nếu đã cấu hình SSH key)
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

## Bước 2: Push Code Lên GitHub

### 2.1 Staging và Commit

```bash
# Thêm tất cả files
git add .

# Kiểm tra status
git status

# Commit
git commit -m "Initial commit: Crypto Real-Time Price Tracker with CI/CD"

# Đổi branch sang main (nếu đang ở master)
git branch -M main

# Push lên GitHub
git push -u origin main
```

### 2.2 Push Lần Sau (sau khi đã push lần đầu)

```bash
# Thêm files mới hoặc thay đổi
git add .

# Commit với message mô tả thay đổi
git commit -m "Mô tả thay đổi của bạn"

# Push
git push
```

## Bước 3: Cấu Hình CI/CD

### 3.1 GitHub Actions (Đã Tự Động)

CI/CD đã được cấu hình sẵn trong folder `.github/workflows/`:
- **ci.yml**: Chạy tests, linting, security scan
- **cd.yml**: Build executables, tạo releases

GitHub Actions sẽ tự động chạy khi:
- Push code lên branch `main` hoặc `develop`
- Tạo Pull Request
- Tạo tag version (vd: `v1.0.0`)

### 3.2 Xem CI/CD Chạy

1. Vào repository trên GitHub
2. Click tab "Actions"
3. Xem các workflow đang chạy hoặc đã chạy

### 3.3 Badges (Tùy Chọn)

Cập nhật badges trong `README_GITHUB.md`:
- Thay `YOUR_USERNAME` và `YOUR_REPO` bằng thông tin thực của bạn

## Bước 4: Cấu Hình Docker Hub (Tùy Chọn)

Nếu muốn tự động push Docker image lên Docker Hub:

### 4.1 Tạo Docker Hub Account
1. Đăng ký tại https://hub.docker.com
2. Tạo Access Token:
   - Vào Account Settings → Security → New Access Token
   - Copy token

### 4.2 Thêm Secrets Vào GitHub

1. Vào repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Thêm 2 secrets:
   - **Name**: `DOCKER_USERNAME`, **Value**: username Docker Hub của bạn
   - **Name**: `DOCKER_PASSWORD`, **Value**: access token vừa tạo

## Bước 5: Tạo Release

### 5.1 Tạo Release Qua GitHub UI

1. Vào repository → Releases → "Create a new release"
2. Click "Choose a tag" → Nhập `v1.0.0` → Create new tag
3. **Release title**: `v1.0.0 - Initial Release`
4. **Description**: Mô tả các tính năng
5. Click "Publish release"

### 5.2 Tạo Release Qua Command Line

```bash
# Tạo tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial Release"

# Push tag
git push origin v1.0.0
```

CI/CD sẽ tự động:
- Build executables cho Windows, Linux, macOS
- Upload vào GitHub Release

## Bước 6: Kiểm Tra CI/CD

### 6.1 Kiểm Tra Tests

```bash
# Chạy tests local trước khi push
pytest

# Kiểm tra code style
flake8 .

# Security scan
pip install safety bandit
safety check
bandit -r .
```

### 6.2 Xem Logs CI/CD

1. Vào GitHub → Actions
2. Click vào workflow run
3. Xem logs chi tiết

## Bước 7: Workflow Làm Việc Hàng Ngày

### 7.1 Feature Branch Workflow

```bash
# Tạo branch mới cho feature
git checkout -b feature/ten-tinh-nang

# Code và commit
git add .
git commit -m "Add: mô tả feature"

# Push branch
git push origin feature/ten-tinh-nang

# Tạo Pull Request trên GitHub
# CI sẽ tự động chạy tests

# Sau khi PR được merge, pull về main
git checkout main
git pull origin main
```

### 7.2 Hotfix Workflow

```bash
# Tạo branch hotfix
git checkout -b hotfix/fix-bug

# Fix bug và commit
git add .
git commit -m "Fix: mô tả bug fix"

# Push và tạo PR
git push origin hotfix/fix-bug
```

## Các Lệnh Git Hữu Ích

```bash
# Xem history
git log --oneline

# Xem thay đổi chưa commit
git diff

# Xem remote repository
git remote -v

# Pull latest changes
git pull

# Xem branches
git branch -a

# Chuyển branch
git checkout branch-name

# Xóa branch local
git branch -d branch-name

# Xóa branch remote
git push origin --delete branch-name

# Revert commit
git revert commit-hash

# Reset về commit trước (cẩn thận!)
git reset --hard HEAD~1

# Stash changes (lưu tạm)
git stash

# Apply stash
git stash pop
```

## Troubleshooting

### Lỗi: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Lỗi: Authentication failed
```bash
# Dùng Personal Access Token thay vì password
# Hoặc cấu hình SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Thêm SSH key vào GitHub: Settings → SSH and GPG keys
```

### Lỗi: Conflict khi merge
```bash
# Pull trước khi push
git pull origin main

# Resolve conflicts trong file
# Sau đó:
git add .
git commit -m "Resolve merge conflicts"
git push
```

## Best Practices

1. **Commit thường xuyên** với messages rõ ràng
2. **Pull trước khi push** để tránh conflicts
3. **Dùng branches** cho features mới
4. **Review code** qua Pull Requests
5. **Chạy tests** trước khi push
6. **Không commit** files nhạy cảm (keys, passwords)
7. **Dùng .gitignore** để loại trừ files không cần thiết
8. **Tag versions** cho releases quan trọng

## Monitoring CI/CD

### GitHub Actions Status
- Green ✅: All checks passed
- Red ❌: Some checks failed
- Yellow 🟡: Checks running

### Email Notifications
- GitHub sẽ gửi email khi CI/CD fail
- Cấu hình: Settings → Notifications

## Kết Luận

Bạn đã hoàn thành việc setup CI/CD! Giờ đây:
- ✅ Mỗi khi push code, tests sẽ tự động chạy
- ✅ Code sẽ được kiểm tra quality và security
- ✅ Có thể tạo releases tự động
- ✅ Build executables cho nhiều platforms

Happy coding! 🚀
