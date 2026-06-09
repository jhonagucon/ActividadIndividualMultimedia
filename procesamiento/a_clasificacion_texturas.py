import cv2
import numpy as np
import urllib.request
import os

# ── Descargar imagen de prueba con las 4 texturas ──────────────
URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/1200px-Camponotus_flavomarginatus_ant.jpg"
ruta_img = "imagen_prueba.jpg"

if not os.path.exists(ruta_img):
    print("Descargando imagen de prueba...")
    urllib.request.urlretrieve(URL, ruta_img)

imagen = cv2.imread(ruta_img)
if imagen is None:
    print("No se pudo cargar imagen. Generando imagen sintetica...")
    imagen = np.zeros((400, 400, 3), dtype=np.uint8)
    imagen[0:100, :] = [34, 139, 34]    # verde cesped arriba
    imagen[100:200, :] = [101, 67, 33]  # marron tierra
    imagen[200:300, :] = [169, 169, 169] # gris cemento
    imagen[300:400, :] = [60, 60, 60]   # gris oscuro asfalto
    cv2.imwrite(ruta_img, imagen)
    print("Imagen sintetica generada.")

print(f"Imagen cargada: {imagen.shape}")
original = imagen.copy()

# ── Convertir a HSV para clasificar por color ──────────────────
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
h = hsv[:, :, 0]
s = hsv[:, :, 1]
v = hsv[:, :, 2]

# ── Calcular textura local (varianza en ventana 5x5) ──────────
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY).astype(np.float32)
altura, ancho = gray.shape
textura = np.zeros_like(gray)
radio = 2

for y in range(radio, altura - radio):
    for x in range(radio, ancho - radio):
        ventana = gray[y-radio:y+radio+1, x-radio:x+radio+1]
        textura[y, x] = np.var(ventana)

textura_norm = (textura / textura.max() * 255).astype(np.uint8)

# ── Clasificación por rangos de color ─────────────────────────
# Inicializar mascara con -1 (sin clasificar)
mascara = np.full((altura, ancho), -1, dtype=np.int8)

# CESPED: verde (H entre 35-85, S alto)
m_cesped  = (h >= 35) & (h <= 85) & (s >= 40)

# TIERRA: marron/naranja (H entre 10-30, S medio, V bajo-medio)
m_tierra  = (h >= 8) & (h <= 30) & (s >= 30) & (v <= 180)

# CEMENTO: gris claro (S bajo, V alto)
m_cemento = (s < 30) & (v >= 120)

# ASFALTO: gris oscuro (S bajo, V bajo)
m_asfalto = (s < 35) & (v < 120)

mascara[m_cesped]  = 0
mascara[m_tierra]  = 1
mascara[m_cemento] = 2
mascara[m_asfalto] = 3

# ── Imagen de salida coloreada ─────────────────────────────────
COLORES = {
    0: (34, 180, 34),     # Verde  — Cesped
    1: (42, 90, 160),     # Marron — Tierra
    2: (200, 200, 200),   # Gris claro — Cemento
    3: (50, 50, 50),      # Gris oscuro — Asfalto
    -1: (128, 0, 128),    # Morado — Sin clasificar
}
ETIQUETAS = {0: "Cesped", 1: "Tierra", 2: "Cemento", 3: "Asfalto", -1: "Otro"}

resultado = np.zeros_like(imagen)
for clase, color in COLORES.items():
    resultado[mascara == clase] = color

# ── Estadísticas ───────────────────────────────────────────────
total_px = altura * ancho
print("\n=== RESULTADOS DE CLASIFICACION ===")
for clase in [0, 1, 2, 3, -1]:
    n = np.sum(mascara == clase)
    pct = n / total_px * 100
    print(f"  {ETIQUETAS[clase]:<12}: {n:7d} pixeles ({pct:.1f}%)")

# ── Imagen comparativa antes/despues ──────────────────────────
alto_cmp = max(original.shape[0], resultado.shape[0])
separador = np.ones((alto_cmp, 10, 3), dtype=np.uint8) * 255

# Etiquetas sobre las imagenes
orig_label = original.copy()
res_label  = resultado.copy()
cv2.putText(orig_label, "ORIGINAL",     (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)
cv2.putText(res_label,  "CLASIFICACION",(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)

# Leyenda de colores
y_ley = 60
for clase in [0, 1, 2, 3]:
    c = COLORES[clase]
    cv2.rectangle(res_label, (10, y_ley), (30, y_ley+20), c, -1)
    cv2.putText(res_label, ETIQUETAS[clase], (35, y_ley+15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    y_ley += 28

comparativa = np.hstack([orig_label, separador, res_label])
cv2.imwrite("resultado_texturas.jpg", comparativa)
cv2.imwrite("mascara_texturas.jpg", resultado)
print("\nArchivos guardados:")
print("  resultado_texturas.jpg  (antes/despues)")
print("  mascara_texturas.jpg    (mascara de segmentacion)")
