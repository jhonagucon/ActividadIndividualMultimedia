import os
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

def crear_informe():
    doc = Document()

    # ── Márgenes ──────────────────────────────────────────────
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3)
        section.right_margin  = Cm(2.5)

    # ── Helpers Estilos ───────────────────────────────────────
    def titulo(doc, texto, nivel=1):
        p = doc.add_heading(texto, level=nivel)
        run = p.runs[0]
        run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
        run.font.name = 'Calibri'
        run.bold = True
        return p

    def parrafo(doc, texto, negrita=False, cursiva=False, centrado=False):
        p = doc.add_paragraph()
        run = p.add_run(texto)
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        run.bold = negrita
        run.italic = cursiva
        if centrado:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return p

    def linea_tabla(table, etiqueta, valor):
        row = table.add_row()
        row.cells[0].text = etiqueta
        row.cells[1].text = valor
        row.cells[0].paragraphs[0].runs[0].bold = True
        row.cells[0].paragraphs[0].runs[0].font.name = 'Calibri'
        row.cells[1].paragraphs[0].runs[0].font.name = 'Calibri'

    # ════════════════════════════════════════════════════════
    # PORTADA
    # ════════════════════════════════════════════════════════
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('\n\n\nUNIVERSIDAD MAYOR DE SAN ANDRÉS')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run('Facultad de Ciencias Puras y Naturales\nCarrera de Informática')
    r2.font.size = Pt(12)
    r2.font.name = 'Calibri'

    doc.add_paragraph()

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r3 = p3.add_run('INFORME TÉCNICO - ACTIVIDADES INDIVIDUALES')
    r3.bold = True
    r3.font.size = Pt(16)
    r3.font.name = 'Calibri'
    r3.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r4 = p4.add_run('Procesamiento de Imágenes, Animación Multimedia y Plataforma Web 3D')
    r4.font.size = Pt(12)
    r4.font.name = 'Calibri'

    doc.add_paragraph()
    doc.add_paragraph()

    tabla_portada = doc.add_table(rows=0, cols=2)
    tabla_portada.style = 'Table Grid'
    linea_tabla(tabla_portada, 'Nombre Completo:', 'Jonathan Gutierrez Condori')
    linea_tabla(tabla_portada, 'Materia:', 'Multimedia I')
    linea_tabla(tabla_portada, 'Docente:', 'Moises Silva')
    linea_tabla(tabla_portada, 'Fecha de Entrega:', datetime.now().strftime('%d de junio de %Y'))
    linea_tabla(tabla_portada, 'Ciudad:', 'La Paz, Bolivia')

    for row in tabla_portada.rows:
        for cell in row.cells:
            for prg in cell.paragraphs:
                for rn in prg.runs:
                    rn.font.name = 'Calibri'
                    rn.font.size = Pt(11)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    # 1. INTRODUCCIÓN
    # ════════════════════════════════════════════════════════
    titulo(doc, '1. Introducción')
    parrafo(doc,
        'Este informe técnico presenta los resultados y metodologías empleadas en el desarrollo de las '
        'actividades individuales para la asignatura de Multimedia I. El proyecto abarca tres áreas principales: '
        'el procesamiento digital de imágenes a nivel de píxel en Python, la producción de contenido multimedia '
        'sincronizado (voz neural + video generado), y el diseño de una plataforma web tridimensional interactiva '
        'que integra modelos fotogramétricos, controles de interacción personalizados y formularios dinámicos.')

    # ════════════════════════════════════════════════════════
    # 2. ACTIVIDADES INDIVIDUALES — PROCESAMIENTO
    # ════════════════════════════════════════════════════════
    titulo(doc, '2. Procesamiento de Imágenes a Nivel de Píxel')
    
    titulo(doc, '2.1 Clasificación de Texturas', nivel=2)
    parrafo(doc,
        'La clasificación de texturas consiste en categorizar superficies dentro de una imagen utilizando '
        'análisis a nivel de píxel en base a características de color y variabilidad espacial. '
        'Se implementó un clasificador robusto con la siguiente metodología:')
    
    bullets_txt = [
        'Espacio de color HSV: Se convierte la imagen de entrada a HSV para aislar la información de tono (Hue) del brillo (Value), permitiendo una calibración de color estable.',
        'Varianza Local (Ventana 5x5): Para cuantificar la rugosidad de la superficie, se calcula la varianza local de los valores de brillo en el vecindario de cada píxel.',
        'Reglas de Decisión: Se establecieron rangos de color y límites de varianza para segmentar en 4 categorías: Césped (Tono verde, saturación alta), Tierra (Tono marrón, saturación media), Cemento (Saturación baja, brillo alto) y Asfalto (Saturación baja, brillo bajo).',
        'Visualización: Se asigna una máscara coloreada en base a la clase asignada: Verde para Césped, Marrón para Tierra, Gris claro para Cemento y Gris oscuro para Asfalto.'
    ]
    for b in bullets_txt:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(b.split(':')[0] + ':').bold = True
        p.add_run(b.split(':')[1])
        p.runs[0].font.name = 'Calibri'
        p.runs[1].font.name = 'Calibri'

    # Insertar imagen de texturas
    img_texturas = 'resultado_texturas.jpg'
    if os.path.exists(img_texturas):
        doc.add_paragraph()
        doc.add_picture(img_texturas, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig1 = doc.add_paragraph('Figura 1: Comparativa antes (izquierda) y después (derecha) de la clasificación de texturas.')
        p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig1.runs[0].font.size = Pt(10)
        p_fig1.runs[0].italic = True

    titulo(doc, '2.2 Implementación de un Filtro de Suavizado 3x3', nivel=2)
    parrafo(doc,
        'Se diseñó e implementó manualmente (sin usar funciones predefinidas de OpenCV como cv2.blur) '
        'un filtro de suavizado espacial de promedio aritmético utilizando una ventana deslizante de 3x3 píxeles.')
    
    parrafo(doc,
        'La ventana recorre la imagen píxel por píxel. Para cada canal de color (R, G, B), se calcula el promedio '
        'de los 9 valores correspondientes al píxel y sus 8 vecinos más cercanos. Los bordes de la imagen se mantienen '
        'inalterados para evitar efectos colaterales de desbordamiento. Este filtro permite reducir de forma efectiva '
        'ruidos Gaussianos de alta frecuencia y suavizar transiciones de contorno.')

    # Insertar imagen de suavizado
    img_suavizado = 'resultado_suavizado.jpg'
    if os.path.exists(img_suavizado):
        doc.add_paragraph()
        doc.add_picture(img_suavizado, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig2 = doc.add_paragraph('Figura 2: Comparativa de la imagen original con ruido y el resultado tras aplicar el filtro de suavizado.')
        p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig2.runs[0].font.size = Pt(10)
        p_fig2.runs[0].italic = True

    doc.add_page_break()

    # ════════════════════════════════════════════════════════
    # 3. PRODUCCIÓN MULTIMEDIA
    # ════════════════════════════════════════════════════════
    titulo(doc, '3. Producción Multimedia: Cover de "La Vaca Lola"')
    parrafo(doc,
        'La producción multimedia consiste en sincronizar y acoplar audio neural con una animación automatizada '
        'para dar vida a una recreación lúdica de la canción infantil "La Vaca Lola".')
    
    parrafo(doc, 'El proceso se estructuró en tres fases de desarrollo:', negrita=True)
    bullets_mult = [
        'Voz Neural Artificial: Se generó la narración de la letra utilizando la biblioteca edge-tts, empleando una voz neural adaptada (es-BO-MarceloNeural) de Microsoft Azure, que provee una entonación boliviana fluida.',
        'Animación con OpenCV: Se creó una animación frame a frame dibujando la silueta de una vaca con formas geométricas vectoriales simples que se mueven al ritmo del compás y mostrando el texto sincronizado en tiempo de ejecución.',
        'Fusión de Medios (FFmpeg): Se utilizó la herramienta FFmpeg para acoplar la pista de audio sintética (.mp3) con la secuencia de vídeo vectorial (.mp4) generada por Python, sincronizando de forma precisa el audio y el movimiento.'
    ]
    for b in bullets_mult:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(b.split(':')[0] + ':').bold = True
        p.add_run(b.split(':')[1])
        p.runs[0].font.name = 'Calibri'
        p.runs[1].font.name = 'Calibri'

    # ════════════════════════════════════════════════════════
    # 4. PLATAFORMA WEB FUNCIONAL
    # ════════════════════════════════════════════════════════
    titulo(doc, '4. Plataforma Web Funcional')
    parrafo(doc,
        'Se diseñó una plataforma web moderna con visualización e interacción de objetos. '
        'La interfaz de usuario implementa las siguientes características premium:')
    
    bullets_web = [
        'Formularios Dinámicos: Lee flujos de procesos en formato JSON y renderiza campos de formulario automáticamente (para los flujos de inscripción de materias y certificado de notas).',
        'Animación 3D Interactiva (Three.js): Renderiza geometrías procedurales (esferas, toroides e icosaedros) en tiempo real con texturas metálicas, iluminación direccional y vista de malla (wireframe).',
        'Modelo Fotogramétrico Real: Visualiza la nube de puntos 3D reconstruida mediante fotogrametría (5,920 vértices) cargando directamente el archivo OBJ de forma asíncrona mediante fetch, con soporte de simulación local como respaldo ante problemas de CORS.',
        'Mejora de Usabilidad en Canvas: Se limitó el zoom con rueda del ratón en ambos visores 3D para que requieran presionar la tecla "Ctrl" (Ctrl + Scroll). Esto previene que los visores capturen el scroll general y congelen la navegación vertical de la página.'
    ]
    for b in bullets_web:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(b.split(':')[0] + ':').bold = True
        p.add_run(b.split(':')[1])
        p.runs[0].font.name = 'Calibri'
        p.runs[1].font.name = 'Calibri'

    # ════════════════════════════════════════════════════════
    # 5. CONCLUSIONES Y TECNOLOGÍAS EMPLEADAS
    # ════════════════════════════════════════════════════════
    titulo(doc, '5. Conclusiones y Tecnologías Empleadas')
    
    tabla_tech = doc.add_table(rows=0, cols=2)
    tabla_tech.style = 'Table Grid'
    linea_tabla(tabla_tech, 'Python 3.13 / NumPy', 'Cálculos de matrices de píxeles para clasificación y filtro de suavizado.')
    linea_tabla(tabla_tech, 'OpenCV 4.13', 'Lectura de imágenes y generación del video vectorial de la vaca animada.')
    linea_tabla(tabla_tech, 'edge-tts', 'Síntesis de voz neural de alta calidad en español boliviano.')
    linea_tabla(tabla_tech, 'FFmpeg', 'Combinación del video generado con el archivo MP3 sintético.')
    linea_tabla(tabla_tech, 'Three.js r128', 'Visualización de geometrías interactivas y visor de nube de puntos OBJ en web.')
    linea_tabla(tabla_tech, 'HTML5 / CSS3 / JS', 'Estructura semántica, formularios dinámicos y estilos premium oscuros.')

    for row in tabla_tech.rows:
        for cell in row.cells:
            for prg in cell.paragraphs:
                for rn in prg.runs:
                    rn.font.name = 'Calibri'
                    rn.font.size = Pt(10)

    doc.add_paragraph()
    parrafo(doc,
        'En conclusión, el desarrollo del proyecto demuestra la viabilidad de implementar algoritmos de '
        'bajo nivel a nivel de píxel en Python de forma eficiente. La combinación de Three.js y APIs '
        'de front-end web proveen una experiencia inmersiva e interactiva sin necesidad de software propietario.')

    # ── Guardar Documento ─────────────────────────────────────
    salida = 'Informe_Tecnico_JonathanGutierrez.docx'
    doc.save(salida)
    print(f'[OK] Word generado: {salida}')
    print(f'     Tamaño: {os.path.getsize(salida)/1024:.1f} KB')

if __name__ == '__main__':
    crear_informe()
