#!/bin/bash
set -e

echo "Testing PyRails installation..."

# Test CLI is accessible
python -m pyrails.cli --help > /dev/null
echo "✅ CLI accessible"

# Test in temp directory
cd /tmp
rm -rf pyrails-install-test 2>/dev/null || true

echo "Creating test app..."
python -m pyrails.cli new pyrails-install-test << 'INPUT'
1
1
y
n
INPUT

cd pyrails-install-test
echo "✅ App created"

# Test model generation
python -m pyrails.cli generate model Article title:str body:text
echo "✅ Model generated"

# Check files exist
test -f app/models/article.py || (echo "❌ Model file missing" && exit 1)
echo "✅ Model file exists"

# Test controller generation  
python -m pyrails.cli generate controller Articles index
echo "✅ Controller generated"

test -f app/controllers/articles_controller.py || (echo "❌ Controller file missing" && exit 1)
echo "✅ Controller file exists"

echo ""
echo "🎉 All installation tests passed!"
echo "PyRails is ready to use"

# Cleanup
cd /tmp
rm -rf pyrails-install-test
