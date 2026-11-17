@echo off
setlocal
cd /d "%~dp0"
echo =========================================
echo     Projeto de IA - Instalacao e inicio
 echo =========================================
if not exist ".venv\Scripts\python.exe" (
  echo Criando ambiente virtual Python...
  py -3.13 -m venv .venv
  if errorlevel 1 (
    echo Nao foi possivel criar o ambiente. Verifique se o Python 3.13 esta instalado.
    pause
    exit /b 1
  )
)
echo Instalando dependencias...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Erro ao instalar bibliotecas. Consulte a mensagem acima.
  pause
  exit /b 1
)
echo Inicializando banco de dados e treinando modelo...
".venv\Scripts\python.exe" -m app_core.cli init
".venv\Scripts\python.exe" -m app_core.cli train
if errorlevel 1 (pause & exit /b 1)
echo Iniciando API e dashboard em terminais separados...
start "Projeto de IA - API" /D "%~dp0" cmd /k ".venv\Scripts\python.exe -m uvicorn app_core.api:app --host 127.0.0.1 --port 8000"
timeout /t 4 /nobreak >nul
start "Projeto de IA - Dashboard" /D "%~dp0" cmd /k ".venv\Scripts\python.exe -m streamlit run dashboard\app.py --server.port 8501"
echo.
echo Acesse: http://localhost:8501
 echo API docs: http://127.0.0.1:8000/docs
pause
