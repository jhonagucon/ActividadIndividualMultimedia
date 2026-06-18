# Trabajo Individual — Multimedia
**Jonathan Gutierrez Condori · UMSA 2026**

Repositorio del trabajo individual de la materia **Multimedia**, que incluye procesamiento de imágenes a nivel de píxel (clasificación de texturas e implementación de un filtro de suavizado) y producción multimedia (cover animado de "La Vaca Lola" versión rockera).

---

## 🗂 Estructura del Proyecto

```
ProyectoMultimedia/
├── procesamiento/
│   ├── a_clasificacion_texturas.py   ← Clasificar superficies por color/textura
│   ├── b_filtro_suavizado.py         ← Filtro de promedio 3×3 manual (píxel a píxel)
│   └── c_vaca_lola_animacion.py      ← Cover multimedia "La Vaca Lola"
├── web/
│   ├── index.html                    ← Plataforma web principal (GitHub Pages)
│   ├── style.css                     ← Estilos modernos (dark mode)
│   └── app.js                        ← Three.js + formularios dinámicos
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

### Requisitos
- Python 3.10+
- pip

### Instalar dependencias
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución

### a) Clasificación de Texturas
```bash
cd procesamiento
python a_clasificacion_texturas.py
```
**Genera:** `resultado_texturas.jpg` (comparativa antes/después)

### b) Filtro de Suavizado 3×3
```bash
cd procesamiento
python b_filtro_suavizado.py
```
**Genera:** `resultado_suavizado.jpg` (imagen con ruido vs imagen suavizada)

### c) Cover La Vaca Lola
```bash
cd procesamiento
python c_vaca_lola_animacion.py
```
**Genera:** `GutierrezCondori_vaca_lola_final.mp4` (video con audio sincronizado)

> Requiere `ffmpeg` instalado: https://ffmpeg.org/download.html

### Plataforma Web
Abrir directamente en el navegador:
```bash
# Windows
start web/index.html

# O simplemente doble clic en web/index.html
```

---

## 📌 Actividades Implementadas

### a) Clasificación de Texturas
Análisis de píxeles en espacio de color **HSV** para clasificar superficies:
- 🟢 **Césped** — Tono verde (H: 35–85°, saturación alta)
- 🟤 **Tierra** — Tono marrón/naranja (H: 8–30°, saturación media)
- ⬜ **Cemento** — Saturación baja, brillo alto (V ≥ 120)
- ⬛ **Asfalto** — Saturación baja, brillo bajo (V < 120)

Adicionalmente se calcula la **varianza local en ventana 5×5** como descriptor de textura.

### b) Filtro de Suavizado 3×3
Implementación manual del filtro de promedio sin usar funciones de suavizado de OpenCV:
```
Para cada píxel (x, y):
  P'(x,y) = Σ P(x+i, y+j) / 9   donde i,j ∈ {-1, 0, 1}
```
Se compara el resultado contra `cv2.blur()` como referencia.

### c) Cover "La Vaca Lola"
Pipeline multimedia completo:
1. Generación de audio con `edge-tts` (voz neural boliviana `es-BO-MarceloNeural`)
2. Animación frame a frame con **OpenCV**: modelo 3D rotando con texto sincronizado
3. Combinación de video + audio con **FFmpeg**

---

## 🌐 Plataforma Web

La plataforma web incluye las tres actividades principales organizadas en una interfaz responsiva y estilizada con un tema verde esmeralda oscuro:

| Sección | Descripción |
|---|---|
| **Clasificación de Texturas** | Subida de imágenes y presets con ejecución del algoritmo en vivo mediante Canvas API. |
| **Filtro de Suavizado** | Carga independiente de imágenes y presets para aplicar el filtro de promedio 3×3 píxel a píxel. |
| **Cover La Vaca Lola** | Reproductor multimedia customizado con el videoclip de la vaca rockera y el pipeline de producción detallado. |

---

## 🛠 Tecnologías Utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Procesamiento de imágenes y renderizado de la animación |
| OpenCV | Manipulación matricial de imágenes y dibujo de fotogramas |
| NumPy | Optimización vectorizada de cálculos de píxeles en Python |
| edge-tts | Síntesis de voz neural realista con el modelo MarceloNeural |
| FFmpeg | Acoplamiento final de audio H.264 y video AAC para la web |
| Three.js r128 | Animación interactiva de partículas verdes flotantes de fondo |
| Canvas API | Procesamiento digital de imágenes directamente en el navegador |

---

## 👤 Autor

**Jonathan Gutierrez Condori**  
Carrera de Informática · UMSA  
Materia: Multimedia I · 2026  
Docente: Moises Silva
