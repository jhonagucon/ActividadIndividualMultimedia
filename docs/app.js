/* ═══════════════════════════════════════════════════════════
   app.js — Trabajo Individual Multimedia · Jonathan Gutierrez
   ═══════════════════════════════════════════════════════════ */

// ══════════════════════════════════════════════════════════
// TEXTURA DE PARTÍCULA CIRCULAR GLOWING
// ══════════════════════════════════════════════════════════
function createCircleTexture(colorStr = '#ffffff', size = 64) {
  const canvas = document.createElement('canvas');
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0, colorStr);
  grad.addColorStop(0.25, colorStr);
  grad.addColorStop(0.65, 'rgba(255, 255, 255, 0.2)');
  grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(size/2, size/2, size/2, 0, Math.PI*2);
  ctx.fill();
  return new THREE.CanvasTexture(canvas);
}

// ══════════════════════════════════════════════════════════
// THREE.JS — HERO CANVAS (partículas flotantes verde esmeralda)
// ══════════════════════════════════════════════════════════
(function initHero() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas || typeof THREE === 'undefined') return;
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  const w = canvas.clientWidth || 500, h = canvas.clientHeight || 420;
  renderer.setSize(w, h, false);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 100);
  camera.position.z = 5;

  const geo = new THREE.BufferGeometry();
  const N = 800;
  const pos = new Float32Array(N * 3);
  const col = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    pos[i*3]   = (Math.random()-0.5)*12;
    pos[i*3+1] = (Math.random()-0.5)*9;
    pos[i*3+2] = (Math.random()-0.5)*6;
    const t = Math.random();
    // Paleta verde oscuro → verde menta
    col[i*3]   = 0.05 + t*0.15;  // R
    col[i*3+1] = 0.55 + t*0.35;  // G
    col[i*3+2] = 0.15 + t*0.25;  // B
  }
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color',    new THREE.BufferAttribute(col, 3));

  const circleTexture = createCircleTexture('#34d399', 64);
  const mat = new THREE.PointsMaterial({
    size: 0.12, vertexColors: true, map: circleTexture,
    transparent: true, opacity: 0.8, depthWrite: false,
    blending: THREE.AdditiveBlending
  });
  scene.add(new THREE.Points(geo, mat));

  // Anillo decorativo verde
  const ringGeo = new THREE.TorusGeometry(2.2, 0.025, 16, 100);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x16a34a, transparent: true, opacity: 0.5, wireframe: true });
  const ring = new THREE.Mesh(ringGeo, ringMat);
  ring.rotation.x = 0.6;
  scene.add(ring);

  let t = 0;
  (function animate() {
    requestAnimationFrame(animate);
    t += 0.004;
    ring.rotation.z = t * 0.2;
    ring.rotation.y = t * 0.08;
    const positions = geo.attributes.position.array;
    for (let i = 0; i < N; i++) {
      positions[i*3+1] += Math.sin(t + i*0.08) * 0.0006;
    }
    geo.attributes.position.needsUpdate = true;
    renderer.render(scene, camera);
  })();
})();

// ══════════════════════════════════════════════════════════
// PROCESAMIENTO DE IMÁGENES — Estados globales independientes
// ══════════════════════════════════════════════════════════
let imageDataA_original = null; // Datos originales Sección A
let currentImageSrcA = null;    // Fuente actual Sección A

let imageDataB_original = null; // Datos originales Sección B
let currentImageSrcB = null;    // Fuente actual Sección B

// Mostrar/Ocultar elementos de canvas vacíos
function mostrarCanvas(canvasId, emptyId, show) {
  const canvas = document.getElementById(canvasId);
  const empty = document.getElementById(emptyId);
  if (canvas) canvas.style.display = show ? 'block' : 'none';
  if (empty) empty.style.display = show ? 'none' : 'block';
}

// ── Utilidades RGB ↔ HSV ──────────────────────────────────
function rgbToHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  const d = max - min;
  let h = 0, s = max === 0 ? 0 : d / max, v = max;
  if (d !== 0) {
    if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6;
    else if (max === g) h = ((b - r) / d + 2) / 6;
    else h = ((r - g) / d + 4) / 6;
  }
  return { h: h * 360, s: s * 100, v: v * 255 };
}

// ── Varianza local 5×5 ────────────────────────────────────
function calcVarianza5x5(x, y, imgData) {
  const W = imgData.width, d = imgData.data;
  let sum = 0, sum2 = 0, count = 0;
  for (let ky = -2; ky <= 2; ky++) {
    for (let kx = -2; kx <= 2; kx++) {
      const nx = x + kx, ny = y + ky;
      if (nx < 0 || ny < 0 || nx >= W || ny >= imgData.height) continue;
      const idx = (ny * W + nx) * 4;
      const gray = 0.299 * d[idx] + 0.587 * d[idx+1] + 0.114 * d[idx+2];
      sum += gray; sum2 += gray * gray; count++;
    }
  }
  const mean = sum / count;
  return (sum2 / count) - mean * mean;
}

// ── Cargar imagen en canvas parametrizado ───────────────────
function cargarImagenEnCanvas(src, destino) {
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    const MAX = 500;
    let W = img.width, H = img.height;
    if (W > MAX) { H = Math.round(H * MAX / W); W = MAX; }
    if (H > MAX) { W = Math.round(W * MAX / H); H = MAX; }

    if (destino === 'A') {
      const cinA = document.getElementById('canvasIn');
      const coutA = document.getElementById('canvasOut');
      if (cinA) { cinA.width = W; cinA.height = H; }
      if (coutA) { coutA.width = W; coutA.height = H; }

      const ctxA = cinA.getContext('2d');
      ctxA.drawImage(img, 0, 0, W, H);
      imageDataA_original = ctxA.getImageData(0, 0, W, H);
      currentImageSrcA = src;

      // Limpiar y mostrar canvases
      mostrarCanvas('canvasIn', 'emptyIn', true);
      mostrarCanvas('canvasOut', 'emptyOut', false);
      const ctxOutA = coutA.getContext('2d');
      ctxOutA.clearRect(0, 0, W, H);
      // El de salida inicia como copia de la original antes de procesar
      ctxOutA.drawImage(img, 0, 0, W, H);
    } else if (destino === 'B') {
      const cinB = document.getElementById('canvasInSmooth');
      const coutB = document.getElementById('canvasOutSmooth');
      if (cinB) { cinB.width = W; cinB.height = H; }
      if (coutB) { coutB.width = W; coutB.height = H; }

      const ctxB = cinB.getContext('2d');
      ctxB.drawImage(img, 0, 0, W, H);
      imageDataB_original = ctxB.getImageData(0, 0, W, H);
      currentImageSrcB = src;

      // Limpiar y mostrar canvases
      mostrarCanvas('canvasInSmooth', 'emptyInSmooth', true);
      mostrarCanvas('canvasOutSmooth', 'emptyOutSmooth', false);
      const ctxOutB = coutB.getContext('2d');
      ctxOutB.clearRect(0, 0, W, H);
      ctxOutB.drawImage(img, 0, 0, W, H);
    }
  };
  img.onerror = () => {
    generarImagenSintetica(src, destino);
  };
  img.src = src;
}

// ── Imagen sintética si no existe el archivo o por presets ────
function generarImagenSintetica(tipo, destino) {
  const W = 400, H = 400;
  const tmpCanvas = document.createElement('canvas');
  tmpCanvas.width = W; tmpCanvas.height = H;
  const ctx = tmpCanvas.getContext('2d');

  // Crear imagen por cuadrantes según el tipo
  const palettes = {
    cesped:  [[34,139,34],[46,160,40],[22,100,22],[60,180,60]],
    tierra:  [[139,90,43],[160,110,60],[120,75,35],[170,120,70]],
    cemento: [[180,180,180],[195,195,195],[165,165,165],[200,200,200]],
    asfalto: [[60,60,60],[45,45,45],[70,70,70],[55,55,55]],
    paisaje: null // cuadrantes mixtos
  };

  if (tipo.includes('cesped') || tipo.includes('tierra') || tipo.includes('cemento') || tipo.includes('asfalto')) {
    const key = Object.keys(palettes).find(k => tipo.includes(k)) || 'cesped';
    const pal = palettes[key] || palettes.cesped;
    for (let y = 0; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const qi = (Math.floor(x/(W/2)) + Math.floor(y/(H/2))*2);
        const [r,g,b] = pal[qi % pal.length];
        const noise = (Math.random()-0.5)*30;
        ctx.fillStyle = `rgb(${r+noise},${g+noise},${b+noise})`;
        ctx.fillRect(x, y, 1, 1);
      }
    }
  } else {
    // Paisaje: 4 cuadrantes (cesped, tierra, cemento, asfalto)
    const regiones = [
      { x:0,   y:0,   w:W/2, h:H/2, r:34,  g:139, b:34  }, // Césped
      { x:W/2, y:0,   w:W/2, h:H/2, r:139, g:90,  b:43  }, // Tierra
      { x:0,   y:H/2, w:W/2, h:H/2, r:180, g:180, b:180 }, // Cemento
      { x:W/2, y:H/2, w:W/2, h:H/2, r:60,  g:60,  b:60  }  // Asfalto
    ];
    regiones.forEach(reg => {
      const imgD = ctx.createImageData(reg.w, reg.h);
      for (let i = 0; i < imgD.data.length; i += 4) {
        const n = (Math.random()-0.5)*40;
        imgD.data[i]   = reg.r + n;
        imgD.data[i+1] = reg.g + n;
        imgD.data[i+2] = reg.b + n;
        imgD.data[i+3] = 255;
      }
      ctx.putImageData(imgD, reg.x, reg.y);
    });
    // Etiquetas
    ctx.font = 'bold 16px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#fff';
    ctx.shadowColor = '#000'; ctx.shadowBlur = 4;
    ctx.fillText('Césped', W/4, H/4);
    ctx.fillText('Tierra', 3*W/4, H/4);
    ctx.fillText('Cemento', W/4, 3*H/4);
    ctx.fillText('Asfalto', 3*W/4, 3*H/4);
  }

  const src = tmpCanvas.toDataURL('image/png');
  cargarImagenEnCanvas(src, destino);
}

// ══════════════════════════════════════════════════════════
// ACTIVIDAD A: CLASIFICACIÓN DE TEXTURAS
// ══════════════════════════════════════════════════════════
function aplicarClasificacionTexturas() {
  const cinA = document.getElementById('canvasIn');
  const coutA = document.getElementById('canvasOut');
  if (!cinA || !coutA) return;
  if (!imageDataA_original) {
    alert("Por favor, sube una imagen o selecciona una muestra rápida primero.");
    return;
  }
  const ctxIn  = cinA.getContext('2d');
  const ctxOut = coutA.getContext('2d');
  const W = cinA.width, H = cinA.height;
  const src = ctxIn.getImageData(0, 0, W, H);
  const out = ctxOut.createImageData(W, H);

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 4;
      const r = src.data[i], g = src.data[i+1], b = src.data[i+2];
      const {h, s, v} = rgbToHsv(r, g, b);
      const variance = calcVarianza5x5(x, y, src);

      let nr = 128, ng = 0, nb = 128; // default: Otros (morado)

      if (h >= 30 && h <= 90 && s >= 40 && variance > 5) {
        // Césped — verde
        nr = 34; ng = 180; nb = 34;
      } else if (h >= 5 && h < 30 && s >= 30 && variance > 15) {
        // Tierra — marrón
        nr = 160; ng = 90; nb = 42;
      } else if (s < 30 && v >= 100 && variance <= 15) {
        // Cemento — gris claro
        nr = 200; ng = 200; nb = 200;
      } else if (s < 35 && v < 100 && variance > 15) {
        // Asfalto — gris oscuro
        nr = 72; ng = 72; nb = 72;
      }

      out.data[i]   = nr;
      out.data[i+1] = ng;
      out.data[i+2] = nb;
      out.data[i+3] = 255;
    }
  }
  ctxOut.putImageData(out, 0, 0);
  mostrarCanvas('canvasOut', 'emptyOut', true);
}

// ══════════════════════════════════════════════════════════
// ACTIVIDAD B: FILTRO DE SUAVIZADO 3×3 (Promedio)
// ══════════════════════════════════════════════════════════
function aplicarFiltroPromedio() {
  const cinB = document.getElementById('canvasInSmooth');
  const coutB = document.getElementById('canvasOutSmooth');
  if (!cinB || !coutB) return;
  if (!imageDataB_original) {
    alert("Por favor, sube una imagen o selecciona una muestra rápida primero.");
    return;
  }
  const ctxIn  = cinB.getContext('2d');
  const ctxOut = coutB.getContext('2d');
  const W = cinB.width, H = cinB.height;
  const src = ctxIn.getImageData(0, 0, W, H);
  const out = ctxOut.createImageData(W, H);
  const s = src.data;
  const o = out.data;

  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      let sumR = 0, sumG = 0, sumB = 0, count = 0;

      // Ventana 3×3
      for (let ky = -1; ky <= 1; ky++) {
        for (let kx = -1; kx <= 1; kx++) {
          const nx = x + kx, ny = y + ky;
          if (nx < 0 || ny < 0 || nx >= W || ny >= H) continue;
          const idx = (ny * W + nx) * 4;
          sumR += s[idx]; sumG += s[idx+1]; sumB += s[idx+2];
          count++;
        }
      }

      const i = (y * W + x) * 4;
      o[i]   = sumR / count;
      o[i+1] = sumG / count;
      o[i+2] = sumB / count;
      o[i+3] = 255;
    }
  }
  ctxOut.putImageData(out, 0, 0);
  mostrarCanvas('canvasOutSmooth', 'emptyOutSmooth', true);
}

// ══════════════════════════════════════════════════════════
// CONTROLES DE CARGA / MUESTRAS INDEPENDIENTES
// ══════════════════════════════════════════════════════════

// ── Sección A: Clasificación de Texturas ───────────────────
function triggerUpload() {
  document.getElementById('imageLoader').click();
}

function handleImage(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => cargarImagenEnCanvas(e.target.result, 'A');
  reader.readAsDataURL(file);
  document.querySelectorAll('#texturas .preset-btn').forEach(b => b.classList.remove('active'));
}

function cargarMuestra(tipo) {
  document.querySelectorAll('#texturas .preset-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('preset' + tipo.charAt(0).toUpperCase() + tipo.slice(1));
  if (btn) btn.classList.add('active');

  generarImagenSintetica(tipo, 'A');
}

function restaurarOriginal() {
  if (!imageDataA_original) return;
  const cinA = document.getElementById('canvasIn');
  const coutA = document.getElementById('canvasOut');
  if (cinA) cinA.getContext('2d').putImageData(imageDataA_original, 0, 0);
  if (coutA) coutA.getContext('2d').putImageData(imageDataA_original, 0, 0);
}

// ── Sección B: Filtro de Suavizado ─────────────────────────
function triggerUploadSmooth() {
  document.getElementById('imageLoaderSmooth').click();
}

function handleImageSmooth(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => cargarImagenEnCanvas(e.target.result, 'B');
  reader.readAsDataURL(file);
  document.querySelectorAll('#suavizado .preset-btn').forEach(b => b.classList.remove('active'));
}

function cargarMuestraSmooth(tipo) {
  document.querySelectorAll('#suavizado .preset-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('presetSmooth' + tipo.charAt(0).toUpperCase() + tipo.slice(1));
  if (btn) btn.classList.add('active');

  generarImagenSintetica(tipo, 'B');
}

function restaurarOriginalSmooth() {
  if (!imageDataB_original) return;
  const cinB = document.getElementById('canvasInSmooth');
  const coutB = document.getElementById('canvasOutSmooth');
  if (cinB) cinB.getContext('2d').putImageData(imageDataB_original, 0, 0);
  if (coutB) coutB.getContext('2d').putImageData(imageDataB_original, 0, 0);
}

// ══════════════════════════════════════════════════════════
// INICIO: Configurar canvases como vacíos al iniciar
// ══════════════════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  mostrarCanvas('canvasIn', 'emptyIn', false);
  mostrarCanvas('canvasOut', 'emptyOut', false);
  mostrarCanvas('canvasInSmooth', 'emptyInSmooth', false);
  mostrarCanvas('canvasOutSmooth', 'emptyOutSmooth', false);
});

// ══════════════════════════════════════════════════════════
// REPRODUCTOR MULTIMEDIA CUSTOM
// ══════════════════════════════════════════════════════════
const video = document.getElementById('mainVideo');
const playPauseBtn = document.getElementById('playPauseBtn');
const progressBarWrapper = document.querySelector('.progress-bar-wrapper');
const progressFill = document.getElementById('progressFill');
const progressThumb = document.getElementById('progressThumb');
const currentTimeSpan = document.getElementById('currentTime');
const totalTimeSpan = document.getElementById('totalTime');
const volumeSlider = document.getElementById('volumeSlider');
const muteBtn = document.getElementById('muteBtn');
const videoError = document.getElementById('videoError');

if (video) {
  // Ocultar controles nativos si la carga es exitosa para usar los personalizados
  video.removeAttribute('controls');

  // Detectar error de carga
  video.addEventListener('error', () => {
    if (videoError) videoError.style.display = 'flex';
  });

  // Play / Pause
  window.togglePlayPause = function() {
    if (video.paused || video.ended) {
      video.play().catch(e => console.log("Auto-play blocked or error: ", e));
      if (playPauseBtn) playPauseBtn.textContent = '⏸';
    } else {
      video.pause();
      if (playPauseBtn) playPauseBtn.textContent = '▶';
    }
  };

  // Click en el video para play/pause
  video.addEventListener('click', window.togglePlayPause);

  // Actualizar barra de progreso
  video.addEventListener('timeupdate', () => {
    if (video.duration) {
      const pct = (video.currentTime / video.duration) * 100;
      if (progressFill) progressFill.style.width = pct + '%';
      if (progressThumb) progressThumb.style.left = pct + '%';
      if (currentTimeSpan) currentTimeSpan.textContent = formatTime(video.currentTime);
    }
  });

  // Cargar metadatos (duración total)
  video.addEventListener('loadedmetadata', () => {
    if (totalTimeSpan) totalTimeSpan.textContent = formatTime(video.duration);
  });

  // Si ya están los metadatos cargados
  if (video.readyState >= 1) {
    if (totalTimeSpan) totalTimeSpan.textContent = formatTime(video.duration);
  }

  // Click / Arrastrar barra de progreso
  if (progressBarWrapper) {
    progressBarWrapper.addEventListener('click', (e) => {
      const rect = progressBarWrapper.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width;
      video.currentTime = pos * video.duration;
    });
  }

  // Cambiar volumen
  window.cambiarVolumen = function(val) {
    video.volume = val;
    video.muted = (val == 0);
    actualizarIconoMute();
  };

  // Mute / Unmute
  window.toggleMute = function() {
    video.muted = !video.muted;
    actualizarIconoMute();
  };

  function actualizarIconoMute() {
    if (video.muted || video.volume === 0) {
      if (muteBtn) muteBtn.textContent = '🔇';
      if (volumeSlider) volumeSlider.value = 0;
    } else {
      if (muteBtn) muteBtn.textContent = '🔊';
      if (volumeSlider) volumeSlider.value = video.volume;
    }
  }

  function formatTime(sec) {
    if (isNaN(sec)) return '0:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  // Al terminar, resetear botón
  video.addEventListener('ended', () => {
    if (playPauseBtn) playPauseBtn.textContent = '▶';
  });
}

