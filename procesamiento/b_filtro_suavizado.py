import cv2
import numpy as np
import os

def filtro_promedio_manual(imagen):
    """
    Filtro de suavizado 3x3 implementado a nivel de pixel sin usar cv2.blur.
    Para cada pixel se calcula el promedio de su vecindad de 3x3.
    Los bordes se ignoran (se dejan sin modificar).
    Optimizado en NumPy para mantener alta velocidad en 800x800 píxeles.
    """
    alto, ancho, canales = imagen.shape
    resultado = imagen.copy()

    # Vectorización en NumPy para velocidad extrema:
    # Suma las 9 posiciones del vecindario 3x3 para toda la matriz simultáneamente
    img_f = imagen.astype(np.float32)
    suma = np.zeros_like(img_f)
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            suma += np.roll(np.roll(img_f, dy, axis=0), dx, axis=1)

    # El promedio de los 9 píxeles (se divide entre 9)
    # Solo aplicamos en los píxeles interiores, dejando los bordes intactos (1:-1)
    resultado[1:-1, 1:-1] = (suma[1:-1, 1:-1] / 9.0).astype(np.uint8)

    return resultado

ruta_img = "imagen_prueba.jpg"
if not os.path.exists(ruta_img):
    print("[!] Generando imagen sintetica con textura...")
    # Generar fallback de imagen si no existiese
    base = np.zeros((800, 800, 3), dtype=np.uint8)
    base[0:400, :] = [80, 160, 80]
    base[400:800, :] = [160, 160, 160]
    ruido = np.random.randint(0, 35, base.shape, dtype=np.uint8)
    base = cv2.add(base, ruido)
    cv2.imwrite(ruta_img, base)

imagen_original = cv2.imread(ruta_img)
if imagen_original is None:
    raise FileNotFoundError(f"No se encontro: {ruta_img}")

print(f"Imagen original cargada: {imagen_original.shape}")

# Agregar ruido gaussiano moderado para demostrar el efecto del filtro
np.random.seed(42)
ruido = np.random.normal(0, 20, imagen_original.shape).astype(np.int16)
imagen_con_ruido = np.clip(imagen_original.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

print("Aplicando filtro de suavizado 3x3 manual vectorizado en resolucion de alta fidelidad (800x800)...")
suavizada_manual = filtro_promedio_manual(imagen_con_ruido)
suavizada_cv2 = cv2.blur(imagen_con_ruido, (3, 3))

print("Filtro aplicado correctamente.")

# Calcular diferencia de ruido (MSE) para verificar la exactitud matemática
mse_manual = np.mean((imagen_original.astype(np.float32) - suavizada_manual.astype(np.float32))**2)
mse_ruido  = np.mean((imagen_original.astype(np.float32) - imagen_con_ruido.astype(np.float32))**2)
mse_cv2    = np.mean((imagen_original.astype(np.float32) - suavizada_cv2.astype(np.float32))**2)

print(f"\n=== COMPARACION DE ERROR (MSE — menor es mejor) ===")
print(f"  Imagen con ruido  : MSE = {mse_ruido:.2f}")
print(f"  Filtro manual 3x3 : MSE = {mse_manual:.2f}")
print(f"  cv2.blur (ref.)   : MSE = {mse_cv2:.2f}")

alto = imagen_original.shape[0]
sep = np.ones((alto, 15, 3), dtype=np.uint8) * 255 # Separador blanco grueso

def agregar_etiqueta(img, texto):
    copia = img.copy()
    # Pinta una barra de titulo superior semitransparente
    cv2.rectangle(copia, (0,0), (copia.shape[1], 60), (0,0,0), -1)
    cv2.putText(copia, texto, (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255,255,255), 3)
    return copia

col1 = agregar_etiqueta(imagen_con_ruido, "IMAGEN DE ENTRADA CON RUIDO")
col2 = agregar_etiqueta(suavizada_manual, "SUAVIZADO MANUAL VECINDARIO 3x3")

comparativa = np.hstack([col1, sep, col2])

# Guardar en raíz para reporte docx
cv2.imwrite("resultado_suavizado.jpg", comparativa, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

# Guardar en web/ para navegador
web_dir = "web"
if os.path.exists(web_dir):
    cv2.imwrite(os.path.join(web_dir, "resultado_suavizado.jpg"), comparativa, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

print("\nGuardado en alta calidad: resultado_suavizado.jpg (CWD y web/)")
