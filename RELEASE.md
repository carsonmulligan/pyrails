# PyRails Release Process

## Setup (One Time)

### 1. Add PyPI Token to GitHub Secrets

1. Go to your PyPI account: https://pypi.org/manage/account/
2. Create API token (Settings → API tokens → Add API token)
   - Name: `pyrails-github-actions`
   - Scope: Project (select `pyrails` after first manual upload)
3. Copy the token (starts with `pypi-`)
4. Go to GitHub repository → Settings → Secrets and variables → Actions
5. Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: (paste your token)

## Release Process

### Option 1: Automatic (Recommended)

**Via GitHub Release:**

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.1"  # Increment version
   ```

2. Commit and push:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.1.1"
   git push
   ```

3. Create and push tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

4. Create GitHub Release:
   - Go to: https://github.com/youruser/pyrails/releases/new
   - Choose tag: `v0.1.1`
   - Title: `PyRails v0.1.1`
   - Description: (list changes)
   - Click "Publish release"

5. **GitHub Actions will automatically publish to PyPI!** ✨

6. Verify at: https://pypi.org/project/pyrails/

### Option 2: Manual Trigger

1. Go to: https://github.com/youruser/pyrails/actions
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow"

### Option 3: Manual Upload

**First time only (to claim package name):**

```bash
# Update version
vim pyproject.toml  # Change version = "0.1.0"

# Build
rm -rf dist/
python -m build

# Upload to PyPI
twine upload dist/*
# Enter: __token__
# Password: pypi-your-token-here

# Or use .pypirc
twine upload dist/* --config-file ~/.pypirc
```

## First Release Checklist

- [ ] Update version to `0.1.0` in `pyproject.toml`
- [ ] Run tests: `pytest`
- [ ] Build package: `python -m build`
- [ ] Test install: `pip install dist/*.whl`
- [ ] Manual upload to claim name: `twine upload dist/*`
- [ ] Add PyPI token to GitHub secrets
- [ ] Create GitHub release (auto-publishes future versions)

## Versioning

Use semantic versioning:
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features
- `1.0.0` - Stable release

## After First Manual Upload

Once you've manually uploaded once to claim the package name:

1. Create a **Project-scoped** token on PyPI for just `pyrails`
2. Update GitHub secret `PYPI_API_TOKEN` with new token
3. All future releases happen automatically via GitHub

## Testing Before Release

```bash
# Test install from built package
pip install dist/pyrails-*.whl

# Test in clean environment
./test_pip_install.sh

# Test all commands work
cd /tmp
pyrails new testrelease
cd testrelease
pyrails g model Test name:str
```

## Verification After Release

```bash
# Install from PyPI
pip install pyrails

# Or specific version
pip install pyrails==0.1.1

# Verify
pyrails --version
pyrails new test
```

## Troubleshooting

**Upload fails with "package already exists":**
- Increment version in `pyproject.toml`
- Can't re-upload same version

**GitHub Action fails:**
- Check `PYPI_API_TOKEN` secret is set
- Check token hasn't expired
- Check token scope includes `pyrails` project

**Package not found on PyPI:**
- Wait a few minutes for indexing
- Check package name: https://pypi.org/project/pyrails/
