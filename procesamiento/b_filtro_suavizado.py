import cv2
import numpy as np
import os

def filtro_promedio_manual(imagen):
    """
    Filtro de suavizado 3x3 implementado a nivel de pixel sin usar cv2.blur.
    Para cada pixel se calcula el promedio de su vecindad de 3x3.
    Los bordes se ignoran (se dejan sin modificar).
    """
    alto, ancho, canales = imagen.shape
    resultado = imagen.copy().astype(np.float32)

    for y in range(1, alto - 1):
        for x in range(1, ancho - 1):
            for c in range(canales):
                ventana = imagen[y-1:y+2, x-1:x+2, c]
                resultado[y, x, c] = np.sum(ventana) / 9.0

    return resultado.astype(np.uint8)

ruta_img = "imagen_prueba.jpg"
if not os.path.exists(ruta_img):
    print("Generando imagen sintetica con ruido...")
    base = np.zeros((300, 400, 3), dtype=np.uint8)
    base[0:150, :] = [80, 160, 80]
    base[150:300, :] = [160, 160, 160]
    ruido = np.random.randint(0, 50, base.shape, dtype=np.uint8)
    base = cv2.add(base, ruido)
    cv2.imwrite(ruta_img, base)

imagen_original = cv2.imread(ruta_img)
if imagen_original is None:
    raise FileNotFoundError(f"No se encontro: {ruta_img}")

print(f"Imagen cargada: {imagen_original.shape}")

# Agregar ruido gaussiano para demostrar el efecto del filtro
ruido = np.random.normal(0, 25, imagen_original.shape).astype(np.int16)
imagen_con_ruido = np.clip(imagen_original.astype(np.int16) + ruido, 0, 255).astype(np.uint8)

print("Aplicando filtro de suavizado 3x3 manual...")
print("(Puede tardar unos segundos en imagenes grandes...)")

# Aplicar en imagen pequeña para mayor velocidad
factor = 0.25
pequena = cv2.resize(imagen_con_ruido,
                     (int(imagen_con_ruido.shape[1]*factor),
                      int(imagen_con_ruido.shape[0]*factor)))

suavizada_manual = filtro_promedio_manual(pequena)

suavizada_manual = cv2.resize(suavizada_manual,
                              (imagen_con_ruido.shape[1], imagen_con_ruido.shape[0]))

suavizada_cv2 = cv2.blur(imagen_con_ruido, (3, 3))

print("Filtro aplicado correctamente.")

# Calcular diferencia de ruido (MSE) para comparar
mse_manual = np.mean((imagen_original.astype(np.float32) - suavizada_manual.astype(np.float32))**2)
mse_ruido  = np.mean((imagen_original.astype(np.float32) - imagen_con_ruido.astype(np.float32))**2)
mse_cv2    = np.mean((imagen_original.astype(np.float32) - suavizada_cv2.astype(np.float32))**2)

print(f"\n=== COMPARACION DE ERROR (MSE — menor es mejor) ===")
print(f"  Imagen con ruido  : MSE = {mse_ruido:.2f}")
print(f"  Filtro manual 3x3 : MSE = {mse_manual:.2f}")
print(f"  cv2.blur (ref.)   : MSE = {mse_cv2:.2f}")

alto = imagen_original.shape[0]
sep = np.ones((alto, 8, 3), dtype=np.uint8) * 200

def agregar_etiqueta(img, texto):
    copia = img.copy()
    cv2.rectangle(copia, (0,0), (copia.shape[1], 45), (0,0,0), -1)
    cv2.putText(copia, texto, (8, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    return copia

col1 = agregar_etiqueta(imagen_con_ruido, "CON RUIDO")
col2 = agregar_etiqueta(suavizada_manual, "FILTRO 3x3 MANUAL")
col3 = agregar_etiqueta(suavizada_cv2,    "cv2.blur (referencia)")

comparativa = np.hstack([col1, sep, col2, sep, col3])
cv2.imwrite("resultado_suavizado.jpg", comparativa)
print("\nGuardado: resultado_suavizado.jpg")
