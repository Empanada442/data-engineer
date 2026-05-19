# Proyecto de Análisis de Ventas

Análisis completo de datos de ventas 2023 utilizando Python, Pandas y visualizaciones.

## 📊 Descripción

Este proyecto analiza datos de ventas de una empresa retail para identificar:
- Productos más vendidos
- Tendencias temporales
- Regiones con mejor desempeño
- KPIs clave del negocio

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/usuario/proyecto-ventas.git
cd proyecto-ventas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 📁 Estructura del Proyecto

```
proyecto-ventas/
├── data/
│   ├── raw/              # Datos originales
│   └── processed/        # Datos procesados
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_limpieza.ipynb
│   └── 03_analisis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── visualization.py
├── tests/
│   └── test_preprocessing.py
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

## 🛠️ Uso

```python
# Cargar datos
from src.data_loader import load_data
df = load_data('data/raw/ventas.csv')

# Procesar datos
from src.preprocessing import clean_data
df_clean = clean_data(df)

# Visualizar
from src.visualization import plot_ventas_mensuales
plot_ventas_mensuales(df_clean)
```

## 📈 Resultados

- **Total de ventas**: $1,250,000
- **Producto más vendido**: Laptop (35% del total)
- **Mejor mes**: Diciembre (20% del total anual)
- **Región líder**: Norte (28% del total)

Ver análisis completo en `notebooks/03_analisis.ipynb`

## 🔧 Tecnologías

- Python 3.9+
- Pandas 2.0
- NumPy 1.24
- Matplotlib 3.7
- Seaborn 0.12
- Jupyter Notebook

## 📝 Licencia

MIT License - ver archivo [LICENSE](LICENSE)

## 👥 Autores

- **Tu Nombre** - [@tu-usuario](https://github.com/tu-usuario)

## 🤝 Contribuir

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Contacto

Email: tu@email.com  
LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---
⭐️ Si este proyecto te fue útil, dale una estrella en GitHub
