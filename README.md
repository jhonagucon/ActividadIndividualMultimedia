# Multimedia I — Proyecto Final
**Jonathan Gutierrez Condori · UMSA 2026**

Repositorio del proyecto final de la materia **Multimedia I**, que incluye procesamiento de imágenes a nivel de píxel, producción multimedia con audio y animación, plataforma web 3D interactiva y reconstrucción fotogramétrica.

---

## 🗂 Estructura del Proyecto

```
ProyectoMultimedia/
├── procesamiento/
│   ├── a_clasificacion_texturas.py   ← Clasificar superficies por color/textura
│   ├── b_filtro_suavizado.py         ← Filtro de promedio 3×3 manual (píxel a píxel)
│   └── c_vaca_lola_animacion.py      ← Cover multimedia "La Vaca Lola"
├── web/
│   ├── index.html                    ← Plataforma web principal
│   ├── style.css                     ← Estilos modernos (dark mode)
│   └── app.js                        ← Three.js + formularios dinámicos
├── examen/
│   └── reconstruccion_3d.ipynb       ← Pipeline fotogramétrico
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

La web incluye 4 secciones interactivas:

| Sección | Descripción |
|---|---|
| **Formularios Dinámicos** | Trámites UMSA cargados desde JSON (inscripción, certificado) |
| **Animación 3D** | Geometrías Three.js con controles de órbita (mouse drag) |
| **Modelo Fotogramétrico** | Nube de puntos 3D del objeto reconstruido (5,920 vértices) |
| **Procesamiento** | Visualización del código de clasificación y filtros |

---

## 🛠 Tecnologías Utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.13 | Procesamiento de imágenes y multimedia |
| OpenCV 4.13 | Manipulación de imágenes y video a nivel de píxel |
| NumPy 2.4 | Operaciones matriciales sobre arrays de píxeles |
| edge-tts | Síntesis de voz neural (Microsoft Azure) |
| FFmpeg | Combinación de video y audio |
| Three.js r128 | Gráficos 3D WebGL en el navegador |
| GitHub Pages | Hosting estático de la plataforma web |

---

## 📷 Fotogrametría

El modelo 3D fue generado mediante el siguiente pipeline:
1. Captura de video del objeto (28.6s, 867 frames, 30.3 FPS)
2. Extracción de fotogramas útiles (74 frames, filtrado por varianza del Laplaciano < 15)
3. Generación de nube de puntos con coordenadas angulares y color RGB por vértice
4. Exportación en formato estándar **OBJ** (5,920 vértices, 303 KB)

---

## 👤 Autor

**Jonathan Gutierrez Condori**  
Carrera de Informática · UMSA  
Materia: Multimedia I · 2026  
Docente: Moises Silva
