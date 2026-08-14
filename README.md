# Dashboard de la Paradoja de Simpson con Python

Este dashboard está basado en el dashboard realizado por [Bach and Tan](https://github.com/DigitalCausalityLab/simpsonsparadox) para demostrar el mismo fenómeno. El ejemplo fue tomado de Glymour et al. (2016).

---

# 🚀 Guía de Instalación Rápida / Quick Start Guide

Este proyecto está configurado para ejecutarse en cualquier entorno local de manera sencilla utilizando el módulo nativo de Python (`venv`), por lo que **no es necesario instalar Anaconda**.

## ⚠️ Acerca de la compatibilidad: `requirements.txt`
Para asegurar que el proyecto funcione en distintas computadoras y sistemas operativos (Windows, Linux, MacOS), las dependencias del archivo `requirements.txt` utilizan el enfoque de **versiones flexibles (`>=`)**. Esto le da libertad a `pip` para descargar los paquetes pre-ensamblados más recientes que sean compatibles con tu máquina, evitando errores de compilación.

## 🛠️ Paso a paso para ejecutar el proyecto

Asegúrate de tener Python instalado y en tu `PATH`. Abre la terminal en la carpeta principal de este repositorio y sigue estos pasos:

**1. Crear el entorno virtual**
Crea un entorno aislado para el proyecto:
```bash
python -m venv streamlit
```
*(Nota: Esto creará una carpeta oculta llamada `streamlit`).*

**2. Activar el entorno virtual**
Dependiendo de tu sistema operativo, ejecuta el comando correspondiente:

**Windows:**
```bash
.\streamlit\Scripts\activate
```
> **Nota para usuarios de PowerShell en Windows:** Si recibes un error indicando que "la ejecución de scripts está deshabilitada", quita el seguro temporalmente en tu ventana actual ejecutando:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y luego vuelve a intentar el comando de activación.

**Linux / MacOS:**
```bash
source streamlit/bin/activate
```

**3. Instalar las dependencias**
Una vez activado el entorno, instala las librerías necesarias (esto puede tomar unos minutos):
```bash
pip install -r requirements.txt
```

**4. Generar los datos e imágenes iniciales**
Antes de lanzar el dashboard, debes procesar los datos simulados y generar los gráficos estáticos ejecutando este script:
```bash
python src/plots.py
```

**5. Ejecutar la aplicación web**
Finalmente, levanta el servidor local de Streamlit:
```bash
streamlit run src/streamlit_app.py
```
Esto abrirá automáticamente una pestaña en tu navegador web mostrando el dashboard interactivo.

---

### References

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016.
