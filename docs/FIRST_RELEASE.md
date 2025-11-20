# First PyPI Release - Quick Guide

## Do This First (Manual Upload to Claim Name)

You need to upload once manually to claim the `pyrails` package name on PyPI.

### 1. Build the package

```bash
python -m build
```

This creates `dist/pyrails-0.1.0-py3-none-any.whl`

### 2. Upload to PyPI

```bash
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your PyPI token from your account)

Or if you have `.pypirc` configured:
```bash
twine upload dist/* --config-file ~/.pypirc
```

### 3. Verify it worked

```bash
# Check PyPI
open https://pypi.org/project/pyrails/

# Test install
pip install pyrails
pyrails --help
```

## Set Up GitHub Automation (After First Upload)

### 1. Create Project-Scoped Token

1. Go to https://pypi.org/manage/account/
2. Click "Add API token"
3. Name: `pyrails-github-actions`
4. **Scope: Project** → Select `pyrails`
5. Copy the token (starts with `pypi-`)

### 2. Add Token to GitHub

1. Go to your repo: `https://github.com/youruser/pyrails/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: (paste your token)
5. Click "Add secret"

## Future Releases (Automatic)

Now every time you create a GitHub release, it auto-publishes to PyPI!

```bash
# 1. Update version
vim pyproject.toml  # Change version = "0.1.1"

# 2. Commit
git add pyproject.toml
git commit -m "Bump version to 0.1.1"
git push

# 3. Tag
git tag v0.1.1
git push origin v0.1.1

# 4. Create GitHub Release
# Go to: https://github.com/youruser/pyrails/releases/new
# - Choose tag: v0.1.1
# - Title: PyRails v0.1.1
# - Description: Bug fixes and improvements
# - Click "Publish release"

# 5. GitHub Actions automatically publishes to PyPI! ✨
```

## Quick Commands

```bash
# First release
python -m build && twine upload dist/*

# Future releases
git tag v0.1.1 && git push origin v0.1.1
# Then create GitHub release

# Test
pip install pyrails
pyrails new test
```

## Troubleshooting

**"Package already exists"**
- PyPI doesn't allow re-uploading the same version
- Increment version in `pyproject.toml` first

**"Invalid credentials"**
- Username must be `__token__` exactly
- Password is your full token including `pypi-` prefix

**GitHub Action fails**
- Check `PYPI_API_TOKEN` secret is set
- Make sure token scope is "Project: pyrails" not "All projects"

## You're Done!

After the first manual upload + GitHub secret setup:
1. Push changes
2. Create GitHub release
3. Package publishes automatically
4. Users can `pip install pyrails`
