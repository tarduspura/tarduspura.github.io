@echo off
setlocal

powershell -ExecutionPolicy Bypass -File "%~dp0quickpush.ps1" %*

endlocal
