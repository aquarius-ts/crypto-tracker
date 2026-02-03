#!/bin/bash

# Script tự động push lên GitHub
# Sử dụng: ./push_to_github.sh

echo "=========================================="
echo "  GitHub Push Script"
echo "=========================================="
echo ""

# Kiểm tra git đã được cài đặt chưa
if ! command -v git &> /dev/null
then
    echo "❌ Git chưa được cài đặt. Vui lòng cài đặt git trước."
    exit 1
fi

# Kiểm tra đã có remote origin chưa
if git remote | grep -q "origin"; then
    echo "✅ Remote origin đã tồn tại"
    git remote -v
else
    echo "⚠️  Chưa có remote origin"
    echo -n "Nhập GitHub repository URL (https hoặc SSH): "
    read REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "❌ URL không được để trống"
        exit 1
    fi

    git remote add origin "$REPO_URL"
    echo "✅ Đã thêm remote origin: $REPO_URL"
fi

echo ""
echo "=========================================="
echo "  Chuẩn bị commit và push"
echo "=========================================="
echo ""

# Kiểm tra branch hiện tại
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    echo "⚠️  Chưa có branch, tạo branch main..."
    git checkout -b main
    CURRENT_BRANCH="main"
fi

echo "📌 Branch hiện tại: $CURRENT_BRANCH"
echo ""

# Kiểm tra git config
GIT_NAME=$(git config user.name)
GIT_EMAIL=$(git config user.email)

if [ -z "$GIT_NAME" ] || [ -z "$GIT_EMAIL" ]; then
    echo "⚠️  Cần cấu hình git user"
    echo -n "Nhập tên của bạn: "
    read USER_NAME
    echo -n "Nhập email của bạn: "
    read USER_EMAIL

    git config user.name "$USER_NAME"
    git config user.email "$USER_EMAIL"
    echo "✅ Đã cấu hình git user"
fi

echo "👤 Git User: $GIT_NAME <$GIT_EMAIL>"
echo ""

# Hiển thị trạng thái
echo "📋 Git status:"
git status --short
echo ""

# Xác nhận trước khi commit
echo -n "Bạn có muốn commit và push các thay đổi này? (y/n): "
read CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ Hủy bỏ"
    exit 0
fi

# Commit message
echo -n "Nhập commit message (Enter để dùng mặc định): "
read COMMIT_MSG

if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo ""
echo "🔄 Đang commit và push..."
echo ""

# Add all files
git add .

# Commit
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo "⚠️  Không có gì để commit hoặc có lỗi xảy ra"
    echo "Thử push code hiện tại..."
fi

# Push
git push -u origin "$CURRENT_BRANCH"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Push thành công!"
    echo "=========================================="
    echo ""
    echo "🔗 Kiểm tra repository của bạn trên GitHub"
    echo "📊 Xem CI/CD status tại tab 'Actions'"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Push thất bại!"
    echo "=========================================="
    echo ""
    echo "Một số lý do có thể:"
    echo "  - Chưa xác thực GitHub (cần Personal Access Token hoặc SSH key)"
    echo "  - Remote URL không đúng"
    echo "  - Không có quyền push vào repository"
    echo ""
    echo "Hướng dẫn chi tiết: đọc file GITHUB_GUIDE.md"
fi
