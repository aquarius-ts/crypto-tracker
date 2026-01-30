#!/bin/bash

echo "=========================================="
echo "  Building Crypto Tracker Executable"
echo "=========================================="
echo ""

# Check if pyinstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "⚠️  PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist __pycache__ *.spec.bak

# Build executable
echo "🔨 Building executable..."
pyinstaller crypto_tracker.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Build successful!"
    echo "=========================================="
    echo ""
    echo "📦 Executable location: dist/CryptoTracker"
    echo ""

    # Check file size
    if [ -f "dist/CryptoTracker" ]; then
        SIZE=$(du -h dist/CryptoTracker | cut -f1)
        echo "📊 File size: $SIZE"
    fi

    echo ""
    echo "🚀 To run: ./dist/CryptoTracker"
else
    echo ""
    echo "=========================================="
    echo "❌ Build failed!"
    echo "=========================================="
    exit 1
fi
