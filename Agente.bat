@echo off
REM ---------------------------------------------------------------
REM  Con Interes - lanzador del agente local
REM  Doble clic aca y arranca. No hace falta escribir ningun comando.
REM ---------------------------------------------------------------
title Con Interes - Agente
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0agente\local\agente.ps1"
if errorlevel 1 (
  echo.
  echo  El agente termino con un error. La ventana queda abierta para que puedas leerlo.
  pause
)
