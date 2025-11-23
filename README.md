# Jornadas de Calidad de Software y Agilidad (JCSA) - Edición 2025

## 🧪 Taller: Testing para calidad de datos

Taller desarrollado en el marco de la edición 2025 de las [JCSA](https://jcsa2025.frre.utn.edu.ar/index.html).

### 📖 Descripción
El taller está diseñado para brindar una introducción a la aplicación de conceptos de testing de software y su automatización en contextos diferentes, como el de un proyecto de ciencia de datos o de una iniciativa de revisión de calidad de datos de un proyecto de software.
Se presentarán casos para evaluar aspectos tanto de la estructura de los datos como de los rangos de valores de estos, además de reglas propias del negocio que podrían aplicarse.
El objetivo es que los participantes puedan incorporar estrategias de testing de datos como parte habitual de su flujo de trabajo, incluso en flujos de Integración Continua (CI) mediante la definición de pipelines para automatizar estas revisiones.

### 🎙️ Disertante
Mgter. Lic. Martín Rey | FCEQyN - UNaM. Docente e investigador en las áreas de ingeniería de software y de ciencia de datos por la FCEQyN - UNaM. Integrante del equipo de la Dirección de Tecnologías para la Gestión de la FCE - UNaM.

### 📝 Temario
Se van a abordar los siguientes temas:

1. Conceptos fundamentales relacionados con la calidad de los datos.
2. Revisión de conceptos relacionados con pruebas de software.
3. Generación de tests para la validación de esquemas de datos y la revisión de cumplimiento de rangos de valores aceptables en los datos.
4. Generación de casos de prueba para la validación de reglas de negocio y el perfilado de datos.
5. Integración de estas herramientas en un flujo de trabajo de Integración Continua (CI/CD).

### 📦 Materiales
Desde este repositorio se presentan todos materiales a utilizar en el desarrollo del taller:

- Presentación utilizada en el directorio `/docs`.
- Dataset de e-commerce en el directorio `/data` (ver [data/README.md](data/README.md) para detalles).
- Código de ejemplo y ejercicios en el directorio `/src`.

## 🚀 Configuración del Entorno

Este proyecto utiliza Python 3.12+ y requiere las siguientes dependencias:
- `pandas` - Manipulación de datos
- `great-expectations` - Framework de validación de datos
- `pandera` - Validación de esquemas con Pandas
- `pytest` - Framework de testing
- `pytest-html` - Reportes HTML de tests

### Opción 1: Usando uv (Recomendado)

[uv](https://docs.astral.sh/uv/) es un gestor de paquetes y proyectos Python extremadamente rápido, escrito en Rust. Es la opción recomendada para este proyecto.

**Instalación de uv:**
```bash
# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# En Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Configurar el proyecto:**
```bash
# Clonar el repositorio
git clone https://github.com/tinxo/taller-jcsa25-testing-datos.git
cd taller-jcsa25-testing-datos

# Alternativa con GitHub CLI
# (requiere https://cli.github.com/)
gh repo clone tinxo/taller-jcsa25-testing-datos
cd taller-jcsa25-testing-datos

# Alternativa con GitHub CLI
# (requiere https://cli.github.com/)
gh repo clone tinxo/taller-jcsa25-testing-datos
cd taller-jcsa25-testing-datos

# uv sincronizará automáticamente las dependencias y creará el entorno virtual
uv sync

# Activar el entorno virtual
source .venv/bin/activate  # En Linux/macOS
# o
.venv\Scripts\activate     # En Windows
```

**Ejecutar tests:**
```bash
uv run pytest                    # Ejecutar todos los tests
uv run pytest --html=report.html  # Generar reporte HTML
```

### Opción 2: Usando pip y venv

Si prefieres usar las herramientas estándar de Python:

```bash
# Clonar el repositorio
git clone https://github.com/tinxo/taller-jcsa25-testing-datos.git
cd taller-jcsa25-testing-datos

# Crear entorno virtual
python3.12 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate  # En Linux/macOS
# o
.venv\Scripts\activate     # En Windows

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# Ejecutar tests
pytest
pytest --html=report.html  # Generar reporte HTML
```

**Nota:** Se tiene que contar con una instalación de Python 3.12 o superior para ejecutar las instrucciones anteriores. Esto se puede verificar con:
```bash
python --version
```

## 📚 Recursos Adicionales

- [Documentación de uv](https://docs.astral.sh/uv/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [Pandera Documentation](https://pandera.readthedocs.io/)

