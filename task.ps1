<#
PrivIMU Windows task runner.

Usage examples from PowerShell:
  .\task.ps1 install
  .\task.ps1 test
  .\task.ps1 download
  .\task.ps1 train-rf
  .\task.ps1 demo

This file is the Windows-friendly equivalent of the Makefile.
#>

param(
    [Parameter(Position = 0)]
    [ValidateSet('help', 'install', 'test', 'download', 'download-force', 'train-rf', 'train-cnn', 'evaluate', 'demo', 'clean')]
    [string]$Task = 'help'
)

$ErrorActionPreference = 'Stop'

function Invoke-PrivIMUCommand {
    param([Parameter(Mandatory = $true)][string]$Command)
    Write-Host "`n[PrivIMU] $Command" -ForegroundColor Cyan
    Invoke-Expression $Command
}

function Show-Help {
    Write-Host @'
PrivIMU task runner for Windows PowerShell

Usage:
  .\task.ps1 install         Install/update dependencies
  .\task.ps1 test            Run unit tests
  .\task.ps1 download        Download MotionSense into data/raw/motionsense
  .\task.ps1 download-force  Re-download and overwrite MotionSense
  .\task.ps1 train-rf        Train/evaluate Random Forest and write reports/metrics.json
  .\task.ps1 train-cnn       Train/evaluate 1D-CNN and write reports/metrics.json
  .\task.ps1 evaluate        Print the current metrics summary
  .\task.ps1 demo            Launch Streamlit demo
  .\task.ps1 clean           Remove local caches

Recommended sequence:
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  .\task.ps1 install
  .\task.ps1 test
  .\task.ps1 download
  .\task.ps1 train-rf
  .\task.ps1 demo
'@
}

switch ($Task) {
    'help' { Show-Help }
    'install' {
        Invoke-PrivIMUCommand 'python -m pip install --upgrade pip'
        Invoke-PrivIMUCommand 'python -m pip install -e ".[dev,app]"'
    }
    'test' { Invoke-PrivIMUCommand 'pytest -q' }
    'download' { Invoke-PrivIMUCommand 'python data/download.py --dest data/raw/motionsense' }
    'download-force' { Invoke-PrivIMUCommand 'python data/download.py --dest data/raw/motionsense --force' }
    'train-rf' { Invoke-PrivIMUCommand 'python -m privimu.train --data-root data/raw/motionsense --model rf --output-dir . --window-size 50 --step-size 25 --n-splits 5' }
    'train-cnn' { Invoke-PrivIMUCommand 'python -m privimu.train --data-root data/raw/motionsense --model cnn --output-dir . --window-size 50 --step-size 25 --n-splits 5' }
    'evaluate' { Invoke-PrivIMUCommand 'python -m privimu.evaluate --metrics reports/metrics.json' }
    'demo' { Invoke-PrivIMUCommand 'streamlit run streamlit_app.py' }
    'clean' {
        Write-Host '[PrivIMU] Cleaning local caches' -ForegroundColor Cyan
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue .pytest_cache, .ruff_cache, build, dist
        Get-ChildItem -Recurse -Directory -Filter '__pycache__' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Recurse -Directory -Filter '*.egg-info' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}
