# 🎸 Trabajo Individual — Multimedia
**Jonathan Gutierrez Condori · UMSA 2026**

Repositorio del trabajo individual de la materia **Multimedia**, que cubre tres actividades principales:
- **Actividad A:** Clasificación de texturas por análisis de píxeles en espacio HSV
- **Actividad B:** Filtro de suavizado 3×3 implementado manualmente (píxel a píxel)
- **Actividad C:** Producción multimedia — cover animado en HD 720p de "La Vaca Lola" versión rockera con escenario, luces, guitarra y karaoke sincronizado

---

## 🗂 Estructura del Proyecto

```
ProyectoMultimedia/
├── procesamiento/
│   ├── a_clasificacion_texturas.py   ← Clasificar superficies por color/textura (HSV)
│   ├── b_filtro_suavizado.py         ← Filtro de promedio 3×3 manual (píxel a píxel)
│   └── c_vaca_lola_animacion.py      ← Cover HD 720p "La Vaca Lola" rockera
├── web/
│   ├── index.html                    ← Plataforma web principal
│   ├── style.css                     ← Estilos modernos (dark mode, glassmorphism)
│   ├── app.js                        ← Canvas API + Three.js + lógica de actividades
│   ├── mascara_texturas.jpg          ← Resultado demo Actividad A
│   ├── resultado_suavizado.jpg       ← Resultado demo Actividad B
│   ├── resultado_texturas.jpg        ← Resultado demo Actividad A (comparativa)
│   └── modelo/GutierrezCondori_modelo.obj ← Modelo 3D
├── generar_informe.py                ← Genera el informe Word técnico
├── Informe_Tecnico_JonathanGutierrez.docx
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

### c) Cover "La Vaca Lola" 🐄🎸
Pipeline multimedia completo de producción de videoclip rockero en **HD 720p**:
1. Generación de audio con `edge-tts` (voz neural boliviana `es-BO-MarceloNeural`)
2. Animación frame a frame con **OpenCV** (30 FPS, 1280×720):
   - Escenario de rock: fondo oscuro, estructura de truss metálica, tablas en perspectiva
   - 4 focos de luz animados con haces semitransparentes oscilantes (magenta, naranja, cyan, verde)
   - Vaca rockera dibujada vectorialmente con manchas, ubre, cola con meneo animado
   - Guitarra eléctrica roja de doble cuerno con animación de rasgueo sincronizado
   - Collar de púas, mohawk punk negro, gafas de sol de aviador
   - Karaoke sincronizado efecto máquina de escribir, notas musicales flotantes
3. Combinación de video + audio con **FFmpeg** → H.264/AAC compatible HTML5
4. Archivo final: `GutierrezCondori_vaca_lola_final.mp4`

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

## 🌐 Demo en Línea

La plataforma web está publicada en **GitHub Pages** y puede visitarse directamente en el navegador sin instalación:

> 🔗 [Ver plataforma multimedia en GitHub Pages](https://github.com/JonathanGutierrez1/ProyectoMultimedia)

---

## 👤 Autor

**Jonathan Gutierrez Condori**  
Carrera de Informática · UMSA  
Materia: Multimedia I · 2026  
Docente: Moises Silva
