@echo off
echo ========================================
echo    ANALIZADOR POETICO PRO - v1.0.0
echo ========================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor:
    echo 1. Descarga Python desde https://python.org
    echo 2. Durante la instalacion, marca "Add Python to PATH"
    echo 3. Reinicia este script
    echo.
    pause
    exit /b 1
)

echo ✓ Python detectado correctamente
echo.

:: Verificar si pip está disponible
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: pip no está disponible
    echo Reinstala Python con la opción "Add to PATH"
    pause
    exit /b 1
)

echo ✓ pip detectado correctamente
echo.

:: Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
    echo.
)

:: Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo ERROR: No se pudo activar el entorno virtual
    pause
    exit /b 1
)

echo ✓ Entorno virtual activado
echo.

:: Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip --quiet

:: Instalar dependencias
echo Instalando dependencias necesarias...
echo (Esto puede tomar unos minutos la primera vez)
echo.

pip install -r requirements.txt --quiet
if %ERRORLEVEL% neq 0 (
    echo.
    echo ERROR: Error instalando dependencias
    echo Intentando instalación individual...
    echo.
    
    :: Instalar paquetes uno por uno si falla la instalación masiva
    pip install streamlit --quiet
    pip install pandas --quiet
    pip install plotly --quiet
    pip install pyttsx3 --quiet
    pip install reportlab --quiet
    pip install requests --quiet
    pip install python-dateutil --quiet
    pip install pyyaml --quiet
    pip install colorlog --quiet
    pip install cerberus --quiet
)

echo ✓ Dependencias instaladas correctamente
echo.

:: Verificar que Streamlit está instalado
streamlit --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Streamlit no se instaló correctamente
    echo Intentando reinstalación...
    pip install streamlit --force-reinstall --quiet
)

:: Buscar puerto disponible
set PORT=8501
echo Verificando puerto %PORT%...

:: Verificar si el puerto está ocupado
netstat -an | find ":%PORT% " >nul
if %ERRORLEVEL% equ 0 (
    echo Puerto %PORT% ocupado, probando alternativas...
    set PORT=8502
    netstat -an | find ":8502 " >nul
    if %ERRORLEVEL% equ 0 (
        set PORT=8503
        netstat -an | find ":8503 " >nul
        if %ERRORLEVEL% equ 0 (
            set PORT=8504
        )
    )
)

echo ✓ Usando puerto %PORT%
echo.

:: Crear directorio utils si no existe
if not exist "utils" (
    mkdir utils
)

:: Crear __init__.py si no existe
if not exist "utils\__init__.py" (
    echo. > utils\__init__.py
)

:: Verificar que app.py existe
if not exist "app.py" (
    echo ERROR: app.py no encontrado
    echo Asegúrate de que todos los archivos estén en la carpeta correcta
    pause
    exit /b 1
)

:: Abrir navegador automáticamente después de 3 segundos
echo Iniciando aplicación en puerto %PORT%...
echo.
echo La aplicación se abrirá automáticamente en tu navegador
echo Si no se abre, ve manualmente a: http://localhost:%PORT%
echo.
echo ========================================
echo    PRESIONA CTRL+C PARA CERRAR
echo ========================================
echo.

:: Abrir navegador en segundo plano
start "" http://localhost:%PORT%

:: Ejecutar aplicación Streamlit
streamlit run app.py --server.port %PORT% --server.headless true --browser.gatherUsageStats false

:: Si llegamos aquí, la aplicación se cerró
echo.
echo ========================================
echo  Aplicación cerrada correctamente
echo ========================================
echo.
pause