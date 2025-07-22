# Módulo de Análisis de Textos Largos con Ollama

Este módulo extiende el workshop de extracción de información con capacidades especializadas para analizar textos largos y transcripciones de entrevistas usando modelos LLM locales con Ollama.

## 🚀 Características

### Analizador General (`long_text_analyzer.py`)
- **Procesamiento de textos largos**: Maneja documentos extensos dividiendo el contenido en chunks manejables
- **Extracción de palabras clave**: Identifica términos y frases más relevantes
- **Resumen detallado**: Genera síntesis comprehensivas manteniendo información crucial
- **Análisis temático**: Identifica temas principales y estructura del contenido
- **Análisis de sentimientos**: Evalúa el tono emocional general
- **Detección de hablantes**: Identifica participantes en transcripciones
- **Estadísticas**: Conteo de palabras y tiempo de lectura estimado

### Analizador Especializado de Entrevistas (`interview_analyzer.py`)
- **Clasificación de entrevistas**: Identifica el tipo (laboral, periodística, académica, etc.)
- **Extracción de insights**: Encuentra revelaciones y puntos clave
- **Citas destacadas**: Identifica declaraciones impactantes y memorables
- **Análisis de preguntas**: Categoriza temas de las preguntas realizadas
- **Estilo de interacción**: Evalúa dinámicas comunicacionales
- **Estimación de duración**: Calcula tiempo aproximado de la entrevista

## 📋 Requisitos

### Prerequisitos del Sistema
- Python 3.8+
- Ollama instalado y ejecutándose
- Modelo LLM descargado (recomendado: `llama3.1`, `llama3.2`, o `mixtral`)

### Dependencias Python

1. Usando pip:

```bash
# a. con pip
pip install -r requirements.txt
```

2. Usando poetry:

- Se han aplicado cambios en el archivo `pyproject.toml`.
    - añadido `dependencies = [..., "requests>=2.28.0"]`
- Se puede eliminar el archivo `requirements.txt`.
- Ejecutando el comando de Poetry en tu terminal se instalarán las dependencias correctas:

```bash
poetry install
```

## 🔧 Instalación

1. **Instalar Ollama** 

2. **Comprobar que tienes descargado un modelo**

    - para este ejemplo se sugiere `llama3.1`, `llama3.2` o `mixtral`


<!-- REVISAR 

1. **Instalar Ollama** (si no lo tienes):
```bash
# En macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# En Windows, descargar desde https://ollama.ai
```

2. **Descargar un modelo**:

```bash
ollama pull llama3.1
# o
ollama pull llama3.2
# o 
ollama pull mixtral
```

Ya está explicado como descargar gemma3

-->

3. **Clonar los archivos del módulo** en tu directorio del workshop:
```
llm-information-extraction-workshop/
├── modules/
│   ├── long_text_analyzer.py
│   ├── interview_analyzer.py
│   └── requirements.txt
└── examples/
    └── sample_interview.txt
```

4. **Instalar dependencias**:
```bash
cd modules
pip install -r requirements.txt
```

## 🎯 Uso

### Análisis General de Textos Largos

```bash
# Análisis básico
python long_text_analyzer.py mi_documento.txt

# Especificar archivo de salida
python long_text_analyzer.py transcripcion.txt -o reporte_analisis.md

# Usar modelo específico
python long_text_analyzer.py documento.txt -m mixtral

# Servidor Ollama personalizado
python long_text_analyzer.py texto.txt --url http://192.168.1.100:11434
```

### Análisis Especializado de Entrevistas

```bash
# Análisis de entrevista
python interview_analyzer.py entrevista.txt

# Con archivo de salida personalizado
python interview_analyzer.py transcripcion_entrevista.txt -o analisis_entrevista.md
```

## 📄 Formatos de Entrada

### Texto Plano
```
Este es un documento largo que queremos analizar...
El contenido puede incluir múltiples párrafos...
```

### Transcripción de Entrevista
```
ENTREVISTADOR: ¿Cuál es tu experiencia en el campo?

ENTREVISTADO: Bueno, he trabajado durante más de 10 años...

ENTREVISTADOR: Interesante, ¿podrías contarme más sobre...
```

## 📊 Ejemplo de Salida

### Reporte General
```markdown
# REPORTE DE ANÁLISIS DE TEXTO LARGO

## 📊 ESTADÍSTICAS GENERALES
- **Número de palabras**: 2,547
- **Tiempo de lectura estimado**: 13 minutos
- **Sentimiento general**: Neutral

## 🎯 PALABRAS CLAVE
inteligencia artificial, machine learning, datos, algoritmos, tecnología

## 🏷️ TEMAS PRINCIPALES
• Desarrollo de inteligencia artificial
• Impacto en la industria tecnológica
• Desafíos éticos y regulatorios
• Futuro de la automatización

## 📋 RESUMEN DETALLADO
El documento aborda los avances recientes en inteligencia artificial...
```

### Reporte de Entrevista
```markdown
# REPORTE DE ANÁLISIS DE ENTREVISTA

## 📊 INFORMACIÓN GENERAL
- **Tipo de entrevista**: Entrevista laboral
- **Duración estimada**: 25 minutos
- **Estilo de interacción**: Formal colaborativo

## 💡 INSIGHTS PRINCIPALES
• El candidato tiene experiencia sólida en desarrollo backend
• Muestra interés genuino por el aprendizaje continuo
• Destaca su capacidad de trabajo en equipo

## 💬 CITAS DESTACADAS
• "Mi pasión por la tecnología me impulsa a estar siempre actualizado"
• "Creo que la colaboración es clave para el éxito de cualquier proyecto"
```

## ⚙️ Configuración Avanzada

### Personalizar Parámetros del Modelo
Puedes modificar los parámetros en el código:

```python
analyzer = LongTextAnalyzer(
    model_name="llama3.1",
    ollama_url="http://localhost:11434"
)

# Personalizar parámetros de la llamada
payload = {
    "model": self.model_name,
    "prompt": prompt,
    "options": {
        "temperature": 0.1,      # Creatividad (0.0-1.0)
        "top_p": 0.9,           # Diversidad de tokens
        "num_ctx": 8192         # Ventana de contexto
    }
}
```

### Ajustar Tamaño de Chunks
```python
# En la clase LongTextAnalyzer
self.max_chunk_size = 4000  # Ajustar según el modelo
```

## 🚨 Solución de Problemas

### Error de Conexión con Ollama
```bash
# Verificar que Ollama está ejecutándose
ollama list

# Iniciar Ollama si está detenido
ollama serve
```

### Modelo No Encontrado
```bash
# Listar modelos disponibles
ollama list

# Descargar modelo necesario
ollama pull llama3.1
```

### Memoria Insuficiente
- Usar modelos más pequeños: `llama3.2:1b`
- Reducir `max_chunk_size` en el código
- Procesar textos más cortos

### Análisis Lento
- Usar modelos más rápidos pero menos precisos
- Reducir el tamaño de los chunks
- Procesar en paralelo (modificación avanzada)

## 🔄 Integración con el Workshop

Este módulo se integra perfectamente con el workshop existente:

```python
# Ejemplo de uso en un script personalizado
from long_text_analyzer import LongTextAnalyzer
from interview_analyzer import InterviewAnalyzer

# Análisis general
analyzer = LongTextAnalyzer(model_name="llama3.1")
analysis = analyzer.analyze_text(texto_largo)

# Análisis especializado
interview_analyzer = InterviewAnalyzer(model_name="llama3.1")
interview_analysis = interview_analyzer.analyze_interview(transcripcion)
```

## 🎨 Casos de Uso

### Investigación Académica
- Análisis de transcripciones de focus groups
- Resumen de documentos de investigación largos
- Extracción de temas de entrevistas cualitativas

### Periodismo y Medios
- Análisis de entrevistas periodísticas
- Resumen de conferencias de prensa
- Extracción de quotes destacados

### Recursos Humanos
- Análisis de entrevistas laborales
- Evaluación de feedback de empleados
- Procesamiento de encuestas abiertas

### Consultoría y Negocios
- Análisis de transcripciones de reuniones
- Procesamiento de feedback de clientes
- Resumen de documentos corporativos

## 🛠️ Extensibilidad

El módulo está diseñado para ser extensible:

```python
# Crear un analizador personalizado
class CustomAnalyzer(LongTextAnalyzer):
    def custom_analysis(self, text: str):
        # Implementar análisis específico
        pass
```

## 📈 Mejoras Futuras

- [ ] Soporte para múltiples idiomas
- [ ] Análisis de emociones más granular
- [ ] Detección automática de temas emergentes
- [ ] Integración con bases de datos
- [ ] API REST para uso remoto
- [ ] Interfaz web para análisis interactivo

## 🤝 Contribuciones

Este módulo es parte del workshop de extracción de información. Para contribuir:

1. Fork del repositorio principal
2. Crear branch para tu feature
3. Añadir tests si es necesario
4. Enviar pull request

## 📝 Licencia

Mantiene la misma licencia que el workshop principal.