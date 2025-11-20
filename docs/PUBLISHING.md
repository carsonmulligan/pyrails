# Publishing PyRails to PyPI

## Current Status

✅ Package builds successfully
✅ Can be installed via `pip install dist/pyrails-0.1.0-py3-none-any.whl`
✅ All functionality works when pip installed
❌ Not yet published to PyPI

## Local Installation (Works Now)

```bash
# From source
pip install -e .

# From built package
pip install dist/pyrails-0.1.0-py3-none-any.whl

# From tarball
pip install dist/pyrails-0.1.0.tar.gz

# From GitHub (after pushing)
pip install git+https://github.com/yourusername/pyrails.git
```

## Publishing to PyPI (Future)

### 1. Prerequisites

```bash
# Install twine
pip install twine

# Create PyPI account
# Visit https://pypi.org/account/register/
```

### 2. Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build
```

### 3. Test on TestPyPI First

```bash
# Upload to test.pypi.org
twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ pyrails
```

### 4. Publish to Real PyPI

```bash
# Upload to pypi.org
twine upload dist/*

# Users can now install with:
pip install pyrails
```

### 5. Update Version

Edit `pyproject.toml`:
```toml
version = "0.1.1"  # Increment version
```

Then rebuild and re-upload.

## What Users Will Be Able to Do (After PyPI Publish)

```bash
# Install globally
pip install pyrails

# Use anywhere
cd ~/projects
pyrails new myapp
cd myapp
pyrails server
```

## Current Options (Before PyPI)

### Option 1: Install from GitHub

```bash
pip install git+https://github.com/yourusername/pyrails.git
```

### Option 2: Download and Install

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install .
```

### Option 3: Development Install

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e .
# Changes to code take effect immediately
```

## Verification

Test your installation works:

```bash
# Run automated test
./test_pip_install.sh

# Or manually
pyrails --help
cd /tmp
pyrails new testapp
```

## GitHub Release Workflow

1. **Tag a release**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create GitHub Release**
   - Go to GitHub > Releases > New Release
   - Choose tag v0.1.0
   - Add release notes
   - Attach `dist/pyrails-0.1.0-py3-none-any.whl`

3. **Users can install from release**
   ```bash
   pip install https://github.com/user/pyrails/releases/download/v0.1.0/pyrails-0.1.0-py3-none-any.whl
   ```

## Next Steps

1. ✅ Fix remaining bugs (controller generator - DONE)
2. ✅ Add `.env` to gitignore (DONE)
3. ✅ Test pip install works (DONE)
4. Push to GitHub
5. Create first release
6. (Optional) Publish to TestPyPI
7. (When ready) Publish to PyPI

## Package Info

- **Name**: pyrails
- **Version**: 0.1.0
- **License**: MIT
- **Python**: >=3.11
- **Homepage**: https://github.com/pyrails/pyrails
