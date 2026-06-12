import cv2
import numpy as np
import os

# ── Generar una imagen de prueba sintética con textura realista ──
ruta_img = "imagen_prueba.jpg"

def generar_imagen_sintetica_con_textura(ruta):
    h, w = 400, 400
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
    for _ in range(120):
        x = np.random.randint(2, w_half - 2)
        y = np.random.randint(5, h_half - 5)
        cv2.line(quad_cesped, (x, y), (x + np.random.randint(-1, 2), y - np.random.randint(3, 7)), (20, 95, 20), 1)
        
    # 2. Tierra (Top-Right): marron + ruido de varianza media + piedras
    quad_tierra = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_tierra
    noise = np.random.randint(-25, 25, (h_half, w_half, 3))
    quad_tierra = np.clip(quad_tierra.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    for _ in range(25):
        x = np.random.randint(5, w_half - 5)
        y = np.random.randint(5, h_half - 5)
        cv2.circle(quad_tierra, (x, y), np.random.randint(2, 4), (20, 40, 60), -1)

    # 3. Cemento (Bottom-Left): gris claro + ruido muy suave (baja varianza)
    quad_cemento = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_cemento
    noise = np.random.randint(-4, 5, (h_half, w_half, 3))
    quad_cemento = np.clip(quad_cemento.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # 4. Asfalto (Bottom-Right): gris oscuro + ruido de alta varianza (rugosidad)
    quad_asfalto = np.ones((h_half, w_half, 3), dtype=np.uint8) * color_asfalto
    noise = np.random.randint(-35, 35, (h_half, w_half, 3))
    quad_asfalto = np.clip(quad_asfalto.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Consolidar imagen
    imagen[0:h_half, 0:w_half] = quad_cesped
    imagen[0:h_half, w_half:w] = quad_tierra
    imagen[h_half:h, 0:w_half] = quad_cemento
    imagen[h_half:h, w_half:w] = quad_asfalto
    
    cv2.imwrite(ruta, imagen)
    print("[+] Imagen sintetica texturizada de alta fidelidad generada.")

# Forzar la regeneración de la imagen de prueba para tener la versión texturizada
generar_imagen_sintetica_con_textura(ruta_img)

imagen = cv2.imread(ruta_img)
if imagen is None:
    raise FileNotFoundError("Error al cargar la imagen.")

print(f"Imagen cargada correctamente: {imagen.shape}")
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
