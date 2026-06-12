import cv2
import numpy as np
import os

# ── Generar una imagen de prueba sintética con textura realista (Mayor resolución) ──
# Subimos la resolución a 800x800 píxeles para visualización detallada de alta calidad
ruta_img = "imagen_prueba.jpg"

def generar_imagen_sintetica_con_textura(ruta):
    h, w = 800, 800
    imagen = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Colores base (BGR)
    color_cesped = np.array([34, 139, 34])     # verde
    color_tierra = np.array([33, 67, 101])     # marron
    color_cemento = np.array([180, 180, 180])   # gris claro
    color_asfalto = np.array([55, 55, 55])      # gris oscuro
    
    h_half, w_half = h // 2, w // 2
    np.random.seed(42)
    
    # 1. Cesped (Top-Left): verde + ruido de alta frecuencia + briznas
    quad_cesped = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_cesped
    noise = np.random.randint(-15, 15, (h_half, w_half, 3))
    quad_cesped = np.clip(quad_cesped.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    for _ in range(300): # Más briznas para mayor resolución
        x = np.random.randint(2, w_half - 2)
        y = np.random.randint(5, h_half - 5)
        cv2.line(quad_cesped, (x, y), (x + np.random.randint(-2, 3), y - np.random.randint(4, 10)), (20, 95, 20), 1)
        
    # 2. Tierra (Top-Right): marron + ruido de varianza media + piedras
    quad_tierra = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_tierra
    noise = np.random.randint(-25, 25, (h_half, w_half, 3))
    quad_tierra = np.clip(quad_tierra.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    for _ in range(60): # Más piedras
        x = np.random.randint(5, w_half - 5)
        y = np.random.randint(5, h_half - 5)
        cv2.circle(quad_tierra, (x, y), np.random.randint(3, 7), (20, 40, 60), -1)

    # 3. Cemento (Bottom-Left): gris claro + ruido muy suave (baja varianza)
    quad_cemento = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_cemento
    noise = np.random.randint(-4, 5, (h_half, w_half, 3))
    quad_cemento = np.clip(quad_cemento.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # 4. Asfalto (Bottom-Right): gris oscuro + ruido de alta varianza (rugosidad granular)
    quad_asfalto = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_asfalto
    noise = np.random.randint(-35, 35, (h_half, w_half, 3))
    quad_asfalto = np.clip(quad_asfalto.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Consolidar imagen
    imagen[0:h_half, 0:w_half] = quad_cesped
    imagen[0:h_half, w_half:w] = quad_tierra
    imagen[h_half:h, 0:w_half] = quad_cemento
    imagen[h_half:h, w_half:w] = quad_asfalto
    
    cv2.imwrite(ruta, imagen)
    print(f"[+] Imagen sintetica texturizada generada a {w}x{h} píxeles.")

# Regenerar la imagen de prueba para tener la versión de alta resolución
generar_imagen_sintetica_con_textura(ruta_img)

imagen = cv2.imread(ruta_img)
if imagen is None:
    raise FileNotFoundError("Error al cargar la imagen.")

original = imagen.copy()
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
h = hsv[:, :, 0]
s = hsv[:, :, 1]
v = hsv[:, :, 2]

# ── Calcular textura local (varianza en ventana 5x5) ──────────
# Principio a nivel de píxel: Para cada píxel, calculamos la varianza de los valores de brillo (gris)
# en su vecindario de 5x5. Para lograr alta velocidad en imágenes de 800x800, vectorizamos la suma
# de los 25 píxeles de la ventana usando corrimientos de matriz en NumPy.
# Esto equivale exactamente al doble bucle iterativo pero corre 1000 veces más rápido.
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY).astype(np.float32)
altura, ancho = gray.shape

# Suma y suma de cuadrados en vecindario 5x5 (radio = 2)
sum_x = np.zeros_like(gray)
sum_x2 = np.zeros_like(gray)

for dy in range(-2, 3):
    for dx in range(-2, 3):
        # Desplazar la imagen y sumarla
        sum_x += np.roll(np.roll(gray, dy, axis=0), dx, axis=1)
        sum_x2 += np.roll(np.roll(gray, dy, axis=0), dx, axis=1)**2

mean_x = sum_x / 25.0
mean_x2 = sum_x2 / 25.0
textura = np.clip(mean_x2 - mean_x**2, 0, None)

# Anular bordes para evitar artefactos del np.roll (radio de 2 píxeles)
textura[0:2, :] = 0
textura[-2:, :] = 0
textura[:, 0:2] = 0
textura[:, -2:] = 0

# ── Clasificación Híbrida: Color (HSV) + Varianza de Textura ──
mascara = np.full((altura, ancho), -1, dtype=np.int8)

# CESPED: verde + varianza moderada (debido a las briznas)
m_cesped  = (h >= 30) & (h <= 90) & (s >= 40) & (textura > 5)

# TIERRA: marron/naranja + varianza media-alta
m_tierra  = (h >= 5) & (h <= 30) & (s >= 30) & (textura > 15)

# CEMENTO: gris claro + varianza extremadamente baja (superficie lisa)
m_cemento = (s < 30) & (v >= 100) & (textura <= 15)

# ASFALTO: gris oscuro + varianza alta (granularidad de piedras)
m_asfalto = (s < 35) & (v < 100) & (textura > 15)

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
print("\n=== RESULTADOS DE CLASIFICACION HIBRIDA ===")
for clase in [0, 1, 2, 3, -1]:
    n = np.sum(mascara == clase)
    pct = n / total_px * 100
    print(f"  {ETIQUETAS[clase]:<12}: {n:7d} pixeles ({pct:.1f}%)")

# ── Imagen comparativa antes/despues (Alta Calidad) ──────────
alto_cmp = max(original.shape[0], resultado.shape[0])
separador = np.ones((alto_cmp, 15, 3), dtype=np.uint8) * 255 # Separador blanco más grueso

# Etiquetas sobre las imagenes
orig_label = original.copy()
res_label  = resultado.copy()
cv2.putText(orig_label, "IMAGEN ORIGINAL (800x800)", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
cv2.putText(res_label,  "CLASIFICACION DE TEXTURAS", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

# Leyenda de colores incrustada
y_ley = 90
for clase in [0, 1, 2, 3]:
    c = COLORES[clase]
    cv2.rectangle(res_label, (20, y_ley), (55, y_ley+30), c, -1)
    cv2.rectangle(res_label, (20, y_ley), (55, y_ley+30), (255,255,255), 1)
    cv2.putText(res_label, ETIQUETAS[clase], (65, y_ley+22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    y_ley += 45

comparativa = np.hstack([orig_label, separador, res_label])

# Guardar en raíz para reporte docx
cv2.imwrite("resultado_texturas.jpg", comparativa, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
cv2.imwrite("mascara_texturas.jpg", resultado, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

# Guardar en web/ para visualización en navegador
web_dir = "web"
if os.path.exists(web_dir):
    cv2.imwrite(os.path.join(web_dir, "resultado_texturas.jpg"), comparativa, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    cv2.imwrite(os.path.join(web_dir, "mascara_texturas.jpg"), resultado, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

print("\nArchivos guardados en alta calidad (CWD y web/):")
print("  resultado_texturas.jpg")
print("  mascara_texturas.jpg")
