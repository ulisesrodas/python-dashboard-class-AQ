# Dashboard de la Paradoja de Simpson con Python

Este dashboard está basado en el dashboard realizado por [Bach and Tan](https://github.com/DigitalCausalityLab/simpsonsparadox) para demostrar el mismo fenómeno. El ejemplo fue tomado de Glymour et al. (2016).

---

## Guía de Instalación Rápida

Este proyecto está configurado para ejecutarse en cualquier entorno local de manera sencilla utilizando el módulo nativo de Python para crear **entornos virtuales** (`venv`), por lo que no es necesario instalar Anaconda. Seguimos estos pasos:
* Nos aseguramos de tener desactivado (o no tener) Anaconda.
* Los archivos clave están en la carpeta `src`, pero la Terminal del VS Code debe estar en la carpeta base
* En el Terminal, creamos un entorno virtual llamado streamlit:  `-m venv streamlit`
* Activarlo:
  * Windows: `.\streamlit\Scripts\activate`
  * Mac/Linux: `source streamlit/bin/activate`
* Instalar las librerías: `pip install -r requirements.txt`    

## Acerca de la compatibilidad: `requirements.txt`
Para asegurar que el proyecto funcione en distintas computadoras y sistemas operativos (Windows, Linux, MacOS), las librerías del archivo `requirements.txt` utilizan el enfoque de **versiones flexibles (`>=`)**. Esto le da libertad a `pip` para descargar los paquetes pre-ensamblados más recientes que sean compatibles con tu máquina, evitando errores de compilación.

## Paso a paso para ejecutar el proyecto

Una vez instaladas las librerías, ejecutamos los siguientes comandos en la terminal de VS Code:
* `python src\plots.py` (o con `/` si estás en Mac/Linux): Procesará los datos iniciales y construirá la carpeta assets con las imágenes para que el dashboard no se quede ciego.
* `streamlit run src\streamlit_app.py`: Comando final que levanta el servidor y abre la interfaz web en tu navegador.
---

## Referencias

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016.
