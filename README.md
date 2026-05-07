# Ruta para Data Analyst con Python

Este proyecto es una guía práctica para aprender análisis de datos usando Python, siguiendo un enfoque progresivo: desde fundamentos estadísticos hasta análisis completos con visualización y modelado.

## Nota sobre el entorno

Este repositorio utiliza el gestor de paquetes **uv** para la gestión de dependencias y entornos.

Si prefieres usar **pip**, no hay problema: puedes instalar las dependencias manualmente sin afectar el funcionamiento del proyecto.

---

## Objetivo

Desarrollar las habilidades necesarias para trabajar como analista de datos, combinando:

- Fundamentos de estadística
- Análisis exploratorio de datos (EDA)
- Visualización
- Modelado básico

---

## Tecnologías

- Python 3.12
- uv (gestor de paquetes y entornos)
- numpy
- pandas
- matplotlib
- seaborn
- scipy
- sqlalchemy
- requests
- pyarrow
- scikit-learn
- openpyxl
---

## Instalación

### Pasos para ejecutar el proyecto desde cero

```bash
uv init
uv venv --python 3.12.10
. .venv/Scripts/activate
uv sync
uv pip list