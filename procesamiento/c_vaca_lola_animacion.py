import cv2
import numpy as np
import asyncio
import os
import subprocess
from pathlib import Path

LETRA = """Looooooola
la vaca Loooolaaaa
en el silencio del campo
su alma se asomaaaa

Tiene cabeza
y tiene cola
pero hay tristeza en sus ojos
ay mi vaca Lola

Camina sola entre el viento
sobre la tierra dorada
nadie comprende su canto
ni su mirada cansada

Dicen que es solo una vaca
pero yo siento en su voz
que hay un latido profundo
que tambien conoce el amor"""

LINEAS = [l for l in LETRA.strip().split('\n') if l.strip()]

# ── Generar audio con edge-tts ─────────────────────────────────
async def generar_audio():
    import edge_tts
    # Usamos voz neural en español de Bolivia para el acento solicitado
    comunica = edge_tts.Communicate(
        LETRA,
        voice="es-BO-MarceloNeural",
        rate="+5%",
        pitch="+3Hz"
    )
    await comunica.save("vaca_lola.mp3")
    print("[+] Audio generado: vaca_lola.mp3")

# ── Dibujar la vaca con formas vectoriales avanzadas y animación ──
def dibujar_vaca(frame, t, texto_linea="", linea_completa=""):
    h, w = frame.shape[:2]  # 720, 1280
    
    # 1. Escenario de Rock (Fondo oscuro y luces de show)
    # Fondo gris ultra oscuro
    frame[:, :] = (15, 12, 10)  # Casi negro
    
    # Líneas verticales de paneles de escenario
    for x in range(0, w, 160):
        cv2.line(frame, (x, 0), (x, h - 140), (25, 20, 18), 2)
        
    # Estructura metálica superior para las luces (Truss)
    cv2.rectangle(frame, (0, 0), (w, 25), (40, 40, 45), -1)
    for tx in range(0, w, 40):
        cv2.line(frame, (tx, 0), (tx + 20, 25), (70, 70, 75), 2)
        cv2.line(frame, (tx + 20, 0), (tx, 25), (70, 70, 75), 2)

    # 2. Piso de la Tarima (Madera oscura o metal)
    # Piso gris oscuro
    cv2.rectangle(frame, (0, h - 140), (w, h), (35, 30, 28), -1)
    cv2.line(frame, (0, h - 140), (w, h - 140), (80, 70, 65), 4) # Borde de la tarima
    
    # Tablas del escenario en perspectiva
    for px in range(-200, w + 400, 150):
        cv2.line(frame, (px, h - 140), (px + int((px - w//2)*0.4), h), (22, 18, 16), 2)

    # 3. Focos de Luces de Colores (Spotlights) Animados
    # Crearemos un overlay para los haces de luces semitransparentes
    overlay = frame.copy()
    
    # Focos fijos en el truss (lámparas)
    focos = [
        {"pos": (150, 25), "color": (255, 0, 180), "offset": 0},      # Magenta
        {"pos": (450, 25), "color": (255, 150, 0), "offset": 2},      # Cian (Celeste)
        {"pos": (830, 25), "color": (0, 255, 255), "offset": 4},      # Amarillo
        {"pos": (1130, 25), "color": (0, 255, 0), "offset": 6}        # Verde
    ]
    
    for f in focos:
        fx, fy = f["pos"]
        fcol = f["color"]
        foff = f["offset"]
        
        # Oscilación angular del haz de luz
        ang_osc = 0.5 * np.sin(t * 0.05 + foff)
        target_x = int(fx + 300 * np.sin(ang_osc))
        
        # Dibujar haz (trapecio/triángulo) en el overlay
        pt1 = (fx - 15, fy)
        pt2 = (fx + 15, fy)
        pt3 = (target_x + 250, h)
        pt4 = (target_x - 250, h)
        
        pts = np.array([pt1, pt2, pt3, pt4], dtype=np.int32)
        cv2.fillPoly(overlay, [pts], fcol)
        
        # Dibujar el foco físico brillante
        cv2.circle(frame, (fx, fy), 18, (230, 230, 230), -1)
        cv2.circle(frame, (fx, fy), 24, fcol, 3)

    # Mezclar haces de luces con el escenario (transparencia)
    cv2.addWeighted(overlay, 0.22, frame, 0.78, 0, frame)

    # 4. Parámetros de animación de la vaca
    es_linea_cabeza_cola = "cabeza" in linea_completa.lower() or "cola" in linea_completa.lower()
    
    # Ritmo más acelerado en el coro
    if es_linea_cabeza_cola:
        bob_y = int(22 * np.sin(t * 0.45))
        wag_speed = 0.6
        rock_offset = int(10 * np.sin(t * 0.45))
    else:
        bob_y = int(10 * np.sin(t * 0.25))
        wag_speed = 0.35
        rock_offset = int(4 * np.sin(t * 0.25))
        
    cx, cy = w // 2 + 80, h // 2 + 40
    
    # 5. Patas Traseras (Lejanas, detrás del cuerpo)
    cv2.rectangle(frame, (cx + 70, cy + 20), (cx + 105, cy + 180), (200, 200, 200), -1)
    cv2.rectangle(frame, (cx + 70, cy + 160), (cx + 105, cy + 180), (45, 45, 45), -1) # Pezuña
    
    # Patas Delanteras (Lejanas, detrás del cuerpo)
    cv2.rectangle(frame, (cx - 95, cy + 20), (cx - 60, cy + 180), (200, 200, 200), -1)
    cv2.rectangle(frame, (cx - 95, cy + 160), (cx - 60, cy + 180), (45, 45, 45), -1) # Pezuña

    # 6. Ubre
    cv2.ellipse(frame, (cx + 10, cy + 70), (40, 25), 0, 0, 360, (255, 180, 195), -1)
    cv2.circle(frame, (cx - 15, cy + 85), 6, (255, 180, 195), -1)
    cv2.circle(frame, (cx, cy + 88), 6, (255, 180, 195), -1)
    cv2.circle(frame, (cx + 15, cy + 85), 6, (255, 180, 195), -1)

    # 7. Cuerpo de la vaca (blanco)
    cv2.ellipse(frame, (cx, cy), (165, 115), 0, 0, 360, (255, 255, 255), -1)
    
    # Patas Delanteras/Traseras Cercanas (Delante del cuerpo)
    # Pata trasera cercana
    cv2.rectangle(frame, (cx + 105, cy + 20), (cx + 140, cy + 180), (255, 255, 255), -1)
    cv2.rectangle(frame, (cx + 105, cy + 160), (cx + 140, cy + 180), (25, 25, 25), -1)
    
    # Manchas negras en el cuerpo
    cv2.circle(frame, (cx - 70, cy - 35), 45, (25, 25, 25), -1)
    cv2.circle(frame, (cx + 30, cy + 20), 55, (25, 25, 25), -1)
    cv2.circle(frame, (cx + 90, cy - 45), 32, (25, 25, 25), -1)

    # 8. Cola de la vaca (meneo rockero)
    wag_angle = np.sin(t * wag_speed) * 0.45
    tail_start = (cx + 145, cy - 35)
    tail_end = (
        int(cx + 205 + 30 * np.cos(wag_angle)),
        int(cy + 40 + 40 * np.sin(wag_angle))
    )
    cv2.line(frame, tail_start, tail_end, (245, 245, 245), 8)
    cv2.circle(frame, tail_end, 15, (25, 25, 25), -1) # Pincel negro

    # 9. GUITARRA ELÉCTRICA ROJA ROCKERA
    # Posición base de la guitarra cruzada en el pecho
    gx, gy = cx - 20, cy + 20
    
    # Mástil (Neck) de la guitarra (va hacia arriba a la izquierda)
    cv2.line(frame, (gx, gy), (gx - 220, gy - 160), (42, 24, 18), 12) # Madera
    cv2.line(frame, (gx, gy), (gx - 220, gy - 160), (180, 180, 180), 2) # Cuerdas
    
    # Clavijero (Headstock) de la guitarra
    cv2.circle(frame, (gx - 230, gy - 168), 12, (200, 20, 20), -1)
    for p_offset in range(-8, 16, 8):
        cv2.circle(frame, (gx - 230 + p_offset, gy - 176), 3, (150, 150, 150), -1) # clavijas
    
    # Cuerpo de la guitarra (forma de doble cuerno rockera)
    cv2.circle(frame, (gx - 35, gy + 15), 45, (200, 20, 20), -1)  # Lóbulo izquierdo rojo
    cv2.circle(frame, (gx + 15, gy + 10), 38, (200, 20, 20), -1)  # Lóbulo derecho rojo
    # Cuernos rockeros superiores
    poly_horn1 = np.array([[gx - 55, gy - 25], [gx - 30, gy - 15], [gx - 20, gy + 5]], dtype=np.int32)
    poly_horn2 = np.array([[gx - 15, gy - 45], [gx + 5, gy - 20], [gx - 5, gy + 5]], dtype=np.int32)
    cv2.fillPoly(frame, [poly_horn1, poly_horn2], (200, 20, 20))
    
    # Golpeador (Pickguard) blanco
    cv2.circle(frame, (gx - 15, gy + 10), 22, (245, 245, 245), -1)
    # Pastillas (Pickups) y puente
    cv2.rectangle(frame, (gx - 25, gy), (gx - 5, gy + 10), (50, 50, 50), -1)
    cv2.rectangle(frame, (gx - 25, gy + 15), (gx - 5, gy + 22), (50, 50, 50), -1)

    # 10. Pata delantera izquierda (Sosteniendo el mástil de la guitarra)
    cv2.line(frame, (cx - 70, cy), (gx - 120, gy - 90), (255, 255, 255), 18)
    cv2.circle(frame, (gx - 120, gy - 90), 10, (25, 25, 25), -1) # mano
    
    # Pata delantera derecha (¡ANIMACIÓN DE RASGUEO!)
    strum_y = gy + 5 + int(30 * np.sin(t * 0.45))
    cv2.line(frame, (cx - 30, cy - 20), (gx - 15, strum_y), (255, 255, 255), 18)
    cv2.circle(frame, (gx - 15, strum_y), 10, (25, 25, 25), -1) # Mano tocando

    # 11. Cuello de la Vaca + Collar de Púas
    cuello_pts = np.array([
        [cx - 110, cy - 50],
        [cx - 150, cy - 130 + bob_y],
        [cx - 95, cy - 145 + bob_y],
        [cx - 70, cy - 40]
    ], dtype=np.int32)
    cv2.fillPoly(frame, [cuello_pts], (255, 255, 255))
    
    # Gargantilla rockera negra con púas blancas
    col_pt1 = (cx - 133, cy - 96 + bob_y // 2)
    col_pt2 = (cx - 100, cy - 106 + bob_y // 2)
    cv2.line(frame, col_pt1, col_pt2, (20, 20, 20), 14) # Correa negra
    
    # Dibujar púas
    for p_i in range(4):
        f_val = p_i / 3.0
        px_spk = int(col_pt1[0] + (col_pt2[0] - col_pt1[0]) * f_val)
        py_spk = int(col_pt1[1] + (col_pt2[1] - col_pt1[1]) * f_val)
        spike_poly = np.array([
            [px_spk, py_spk],
            [px_spk - 12, py_spk - 12],
            [px_spk - 18, py_spk + 2]
        ], dtype=np.int32)
        cv2.fillPoly(frame, [spike_poly], (250, 250, 250))

    # 12. Cabeza de la vaca (con bobbing vertical de rockero)
    hx, hy = cx - 150, cy - 130 + bob_y
    cv2.circle(frame, (hx, hy), 55, (255, 255, 255), -1) # Cráneo
    
    # Cabello Punk Mohicano Negro
    hair_pts = np.array([
        [hx - 40, hy - 40],
        [hx - 35, hy - 85],
        [hx - 15, hy - 50],
        [hx, hy - 95],
        [hx + 15, hy - 50],
        [hx + 35, hy - 85],
        [hx + 40, hy - 40]
    ], dtype=np.int32)
    cv2.fillPoly(frame, [hair_pts], (10, 10, 10))

    # Cuernos metálicos (grises)
    cv2.line(frame, (hx - 20, hy - 48), (hx - 35, hy - 78), (140, 140, 145), 8)
    cv2.line(frame, (hx + 20, hy - 48), (hx + 35, hy - 78), (140, 140, 145), 8)
    
    # Orejas
    cv2.ellipse(frame, (hx - 48, hy - 20), (28, 11), -25, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(frame, (hx - 48, hy - 20), (20, 7), -25, 0, 360, (255, 180, 195), -1) # oreja izq
    cv2.ellipse(frame, (hx + 48, hy - 20), (28, 11), 25, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(frame, (hx + 48, hy - 20), (20, 7), 25, 0, 360, (255, 180, 195), -1) # oreja der

    # Hocico rosa rockero
    cv2.ellipse(frame, (hx - 15, hy + 28), (42, 30), 12, 0, 360, (255, 180, 195), -1)
    cv2.circle(frame, (hx - 25, hy + 22), 4, (35, 35, 35), -1)
    cv2.circle(frame, (hx - 8, hy + 30), 4, (35, 35, 35), -1)

    # Animación de boca abierta cantando rockero
    if texto_linea:
        boca_h = int(6 + 18 * abs(np.sin(t * 0.6)))
        cv2.ellipse(frame, (hx - 18, hy + 32), (16, boca_h), 12, 0, 360, (30, 30, 30), -1)
    else:
        cv2.line(frame, (hx - 28, hy + 36), (hx - 12, hy + 32), (30, 30, 30), 3)

    # GAFAS DE SOL NEGRAS COOL DE AVIADOR (Efecto rock)
    # Ojo Izquierdo Gafa
    cv2.ellipse(frame, (hx - 26, hy - 14), (18, 14), 10, 0, 360, (20, 20, 20), -1)
    cv2.ellipse(frame, (hx - 26, hy - 14), (18, 14), 10, 0, 360, (200, 200, 200), 2)
    # Ojo Derecho Gafa
    cv2.ellipse(frame, (hx + 8, hy - 17), (18, 14), 10, 0, 360, (20, 20, 20), -1)
    cv2.ellipse(frame, (hx + 8, hy - 17), (18, 14), 10, 0, 360, (200, 200, 200), 2)
    # Puente de las gafas
    cv2.line(frame, (hx - 10, hy - 16), (hx - 4, hy - 17), (200, 200, 200), 3)
    # Brillo diagonal
    cv2.line(frame, (hx - 32, hy - 8), (hx - 20, hy - 20), (255, 255, 255), 2)
    cv2.line(frame, (hx + 2, hy - 11), (hx + 14, hy - 23), (255, 255, 255), 2)

    # 13. Notas musicales flotantes en colores de luces
    nota1_y = int(140 + 35 * np.cos(t * 0.15))
    nota1_x = int(hx - 110 + 20 * np.sin(t * 0.2))
    nota2_y = int(160 + 30 * np.sin(t * 0.2))
    nota2_x = int(hx + 220 + 15 * np.cos(t * 0.25))
    
    if texto_linea:
        cv2.putText(frame, "♪", (nota1_x, nota1_y), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 0, 200), 4) # Magenta
        cv2.putText(frame, "♫", (nota2_x, nota2_y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 200, 0), 4) # Cian
        cv2.putText(frame, "🎸", (nota1_x + 50, nota1_y - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 255), 3) # Amarillo

    # 14. Títulos principales superiores
    cv2.putText(frame, "La Vaca Lola (ROCK COVER)", (40, 70),
                cv2.FONT_HERSHEY_DUPLEX, 1.4, (255, 255, 255), 3)
    cv2.putText(frame, "Banda Virtual: Marcelo Neural & The Pixel Rockers", (40, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 200, 200), 2)

    # 15. Caja de texto para karaoke inferior (más grande para HD 720p)
    if texto_linea:
        rect_y = h - 90
        # Fondo translúcido oscuro
        sub_img = frame[rect_y - 15:rect_y + 55, 60:w - 60]
        rect_negro = np.zeros_like(sub_img)
        cv2.addWeighted(sub_img, 0.45, rect_negro, 0.55, 0, sub_img)
        
        cv2.putText(frame, texto_linea, (90, rect_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3) # Amarillo

# ── Generar video frame a frame ───────────────────────────────
def generar_video():
    ancho, alto = 1280, 720
    fps = 30
    duracion_total = 30  # segundos
    total_frames = fps * duracion_total

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('vaca_lola_video.mp4', codec, fps, (ancho, alto))

    frames_por_linea = total_frames // max(len(LINEAS), 1)
    
    print(f"[*] Generando {total_frames} frames de video para La Vaca Lola (HD 720p Rocker)...")

    for t in range(total_frames):
        frame = np.zeros((alto, ancho, 3), dtype=np.uint8)
        
        linea_idx = min(t // frames_por_linea, len(LINEAS) - 1)
        linea_completa = LINEAS[linea_idx]
        
        # Efecto maquina de escribir dentro de cada linea
        progreso_en_linea = t % frames_por_linea
        chars_visibles = min(progreso_en_linea // 3 + 1, len(linea_completa))
        texto_visible = linea_completa[:chars_visibles]
        
        dibujar_vaca(frame, t, texto_visible, linea_completa)
        video.write(frame)

        if t % (fps * 5) == 0:
            print(f"    Progreso: {t}/{total_frames} frames ({t*100//total_frames}%)")

    video.release()
    print("[+] Video crudo generado: vaca_lola_video.mp4")

# ── Combinar video + audio con FFmpeg (Formato Web HTML5 H264) ──
def combinar():
    # Buscar el ejecutable de ffmpeg descargado localmente
    ffmpeg_path = "ffmpeg"
    posibles_rutas = [
        "ffmpeg.exe",
        "procesamiento/ffmpeg.exe",
        "../ffmpeg.exe",
        "../procesamiento/ffmpeg.exe"
    ]
    for ruta in posibles_rutas:
        if os.path.exists(ruta):
            ffmpeg_path = os.path.abspath(ruta)
            break
            
    print(f"[*] Usando ffmpeg en: {ffmpeg_path}")
    
    # Convertimos a H264 y AAC de forma explícita para que pueda transmitirse en navegadores web (HTML5)
    # Usamos pix_fmt yuv420p que es mandatorio para reproductores web y dispositivos móviles
    cmd = [
        ffmpeg_path, "-y",
        "-i", "vaca_lola_video.mp4",
        "-i", "vaca_lola.mp3",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        "GutierrezCondori_vaca_lola_final.mp4"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("[+] Video compatible Web H264 generado: GutierrezCondori_vaca_lola_final.mp4")
        
        # Copiar automáticamente el video a la carpeta web/ para el visor html
        web_dir = Path("web")
        if web_dir.exists():
            dest = web_dir / "vaca_lola_video.mp4"
            import shutil
            shutil.copy2("GutierrezCondori_vaca_lola_final.mp4", dest)
            print(f"[+] Video copiado a visor web en: {dest}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("[!] Error al ejecutar FFmpeg. Asegúrese de tener FFmpeg en su PATH para la mezcla de audio.")
        if hasattr(e, 'stderr') and e.stderr:
            print("Detalle:", e.stderr.decode(errors='ignore'))

# ── Ejecucion ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== COVER LA VACA LOLA OPTIMIZADA Y CANTANDO — Jonathan Gutierrez ===\n")

    # Asegurar que el audio exista
    if not os.path.exists("vaca_lola.mp3"):
        try:
            import edge_tts
            asyncio.run(generar_audio())
        except ImportError:
            print("[!] edge-tts no disponible. Se requiere 'pip install edge-tts'")
    else:
        print("[*] Usando audio existente vaca_lola.mp3")

    generar_video()
    combinar()
    print("\n[+] Produccion multimedia finalizada.")
