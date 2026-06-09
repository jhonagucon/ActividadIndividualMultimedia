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
    comunica = edge_tts.Communicate(
        LETRA,
        voice="es-BO-MarceloNeural",
        rate="+5%",
        pitch="+3Hz"
    )
    await comunica.save("vaca_lola.mp3")
    print("[+] Audio generado: vaca_lola.mp3")

# ── Dibujar la vaca con formas geometricas ─────────────────────
def dibujar_vaca(frame, t, texto_linea=""):
    h, w = frame.shape[:2]
    
    # Fondo con degradado animado
    color_fondo = (
        int(30 + 20 * np.sin(t * 0.05)),
        int(60 + 20 * np.sin(t * 0.03)),
        int(90 + 30 * np.sin(t * 0.04))
    )
    frame[:] = color_fondo
    
    # Suelo con cesped
    cv2.rectangle(frame, (0, h-80), (w, h), (30, 100, 30), -1)
    for gx in range(0, w, 15):
        offset = int(5 * np.sin(t * 0.1 + gx * 0.3))
        cv2.ellipse(frame, (gx, h-80+offset), (6,12), 0, 180, 360, (20,140,20), 2)
    
    # Modelo 3D del examen rotando — representado como OBJ viewer simplificado
    # (elipse que simula rotacion del objeto)
    cx, cy = w//2, h//2 - 20
    angulo_rot = t * 3.0
    radio_x = int(100 + 20 * np.sin(np.radians(angulo_rot)))
    radio_y = 70
    
    # Sombra
    cv2.ellipse(frame, (cx, h-85), (radio_x//2, 15), 0, 0, 360, (10,60,10), -1)
    
    # Cuerpo del objeto (simula modelo 3D rotando)
    cv2.ellipse(frame, (cx, cy), (radio_x, radio_y), 0, 0, 360, (220, 200, 180), -1)
    cv2.ellipse(frame, (cx, cy), (radio_x, radio_y), 0, 0, 360, (180, 160, 140), 3)
    
    # Manchas animadas (giran con el objeto)
    for i in range(4):
        ang = np.radians(angulo_rot + i * 90)
        mx = int(cx + radio_x * 0.5 * np.cos(ang))
        my = int(cy + radio_y * 0.4 * np.sin(ang))
        tamaño = int(15 + 5 * np.sin(ang))
        cv2.ellipse(frame, (mx, my), (tamaño, tamaño//2), 0, 0, 360, (80, 60, 40), -1)
    
    # Etiqueta "Modelo 3D"
    cv2.putText(frame, "Modelo 3D (OBJ)", (cx - 70, cy + radio_y + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Nota musical animada
    nota_x = int(50 + 30 * np.sin(t * 0.2))
    nota_y = int(100 + 20 * np.cos(t * 0.15))
    cv2.putText(frame, "♪", (nota_x, nota_y),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 220, 50), 2)
    cv2.putText(frame, "♫", (w - nota_x - 30, nota_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 220, 50), 2)
    
    # Titulo
    cv2.putText(frame, "La Vaca Lola", (w//2 - 120, 50),
                cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 240, 100), 2)
    cv2.putText(frame, "Cover - Jonathan Gutierrez Condori", (w//2 - 180, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Texto de la cancion (efecto maquina de escribir)
    if texto_linea:
        rect_y = h - 60
        cv2.rectangle(frame, (0, rect_y - 10), (w, h - 30), (0,0,0), -1)
        cv2.putText(frame, texto_linea, (30, rect_y + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 200), 2)

# ── Generar video frame a frame ───────────────────────────────
def generar_video():
    ancho, alto = 800, 480
    fps = 30
    duracion_total = 30  # segundos
    total_frames = fps * duracion_total

    codec = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('vaca_lola_video.mp4', codec, fps, (ancho, alto))

    frames_por_linea = total_frames // max(len(LINEAS), 1)
    
    print(f"[*] Generando {total_frames} frames de video...")

    for t in range(total_frames):
        frame = np.zeros((alto, ancho, 3), dtype=np.uint8)
        
        linea_idx = min(t // frames_por_linea, len(LINEAS) - 1)
        linea_completa = LINEAS[linea_idx]
        
        # Efecto maquina de escribir dentro de cada linea
        progreso_en_linea = t % frames_por_linea
        chars_visibles = min(progreso_en_linea // 3 + 1, len(linea_completa))
        texto_visible = linea_completa[:chars_visibles]
        
        dibujar_vaca(frame, t, texto_visible)
        video.write(frame)

        if t % (fps * 5) == 0:
            print(f"    Progreso: {t}/{total_frames} frames ({t*100//total_frames}%)")

    video.release()
    print("[+] Video generado: vaca_lola_video.mp4")

# ── Combinar video + audio con FFmpeg ─────────────────────────
def combinar():
    cmd = [
        "ffmpeg", "-y",
        "-i", "vaca_lola_video.mp4",
        "-i", "vaca_lola.mp3",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "GutierrezCondori_vaca_lola_final.mp4"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("[+] Video final: GutierrezCondori_vaca_lola_final.mp4")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] FFmpeg no disponible. El video sin audio esta en vaca_lola_video.mp4")

# ── Ejecucion ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== COVER LA VACA LOLA — Jonathan Gutierrez Condori ===\n")

    try:
        import edge_tts
        asyncio.run(generar_audio())
    except ImportError:
        print("[!] edge-tts no disponible. Instalar con: pip install edge-tts")

    generar_video()
    combinar()
    print("\n[+] Produccion multimedia completada.")
