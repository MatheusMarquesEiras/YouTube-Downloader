@echo off
title Executando Meu Projeto Python
echo Iniciando o script com uv...
echo -----------------------------------

:: Garante que o script rode na pasta onde o arquivo .bat está
cd /d "%~dp0"

:: Executa o comando
uv run main.py

:: Verifica se o Python retornou algum erro (Exit Code diferente de 0)
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERRO] Ocorreu um problema ao executar o script.
    pause
) else (
    echo.
    echo [OK] Execução finalizada com sucesso.
    timeout /t 5
)