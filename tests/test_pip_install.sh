#!/bin/bash
set -e

echo "Testing pip install of PyRails..."
echo ""

# Create temp venv
VENV_DIR="/tmp/pyrails-pip-test-$$"
echo "Creating test virtualenv at $VENV_DIR"
python -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "✅ Virtual environment created"

# Install from wheel
echo ""
echo "Installing PyRails from wheel..."
pip install dist/pyrails-0.1.0-py3-none-any.whl --quiet

echo "✅ Package installed"

# Test CLI
echo ""
echo "Testing CLI accessibility..."
pyrails --help > /dev/null
echo "✅ pyrails command works"

# Test in temp directory
echo ""
echo "Testing app creation..."
cd /tmp
rm -rf pip-test-app 2>/dev/null || true
pyrails new pip-test-app << 'INPUT'
1
1
n
n
INPUT

cd pip-test-app
echo "✅ App created successfully"

# Test generators
echo ""
echo "Testing model generator..."
pyrails generate model Product name:str price:float
test -f app/models/product.py || (echo "❌ Model not created" && exit 1)
echo "✅ Model generator works"

echo ""
echo "Testing controller generator..."
pyrails generate controller Products
test -f app/controllers/products_controller.py || (echo "❌ Controller not created" && exit 1)
echo "✅ Controller generator works"

# Cleanup
deactivate
rm -rf "$VENV_DIR"
cd /tmp && rm -rf pip-test-app

echo ""
echo "🎉 All pip install tests passed!"
echo ""
echo "PyRails can be installed via:"
echo "  pip install dist/pyrails-0.1.0-py3-none-any.whl"
echo "  pip install dist/pyrails-0.1.0.tar.gz"
echo "  pip install pyrails (once published to PyPI)"
