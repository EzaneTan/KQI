<#
.SYNOPSIS
  Bootstraps the Python environment and runs lint + tests on Windows.

.DESCRIPTION
  - Creates (or re-uses) a venv in .venv\
  - Activates it
  - Installs requirements/dev.txt
  - Runs isort, black --check, mypy, then pytest

.EXAMPLE
  PS> .\run-ci.ps1
#>

# Ensure script is running from repo root:
Set-Location -Path $PSScriptRoot\..

# Create venv if needed
if (-Not (Test-Path .venv\Scripts\Activate.ps1)) {
    python -m venv .venv
}

# Activate venv
. .\venv\Scripts\Activate.ps1

# Upgrade pip + install dev dependencies
python -m pip install --upgrade pip
pip install -r requirements/dev.txt

# Run linters & types
Write-Host "→ Running isort..."
isort .

Write-Host "→ Running black..."
black --check .

Write-Host "→ Running mypy..."
mypy src/

# Run tests
Write-Host "→ Running pytest..."
pytest --maxfail=1 --disable-warnings -q

Write-Host "✅ All checks passed."
