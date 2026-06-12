/* ═══════════════════════════════════════════════════════════
   app.js — Proyecto Multimedia I · Jonathan Gutierrez Condori
   Three.js: Hero, Animación 3D, Visor Fotogramétrico
   Formularios dinámicos desde JSON
   ═══════════════════════════════════════════════════════════ */

// ══════════════════════════════════════════════════════════
// FLUJOS JSON (inline para evitar CORS en file://)
// ══════════════════════════════════════════════════════════
const FLUJOS = {
  inscripcion: {
    flujo: "inscripcion",
    nombre: "Inscripción de Materias",
    descripcion: "Formulario para inscribirse a materias del siguiente semestre.",
    campos: [
      { id:"nombre",    label:"Nombre completo",     tipo:"text",   requerido:true  },
      { id:"carnet",    label:"Número de carnet",    tipo:"text",   requerido:true  },
      { id:"carrera",   label:"Carrera",             tipo:"select", opciones:["Informática","Matemáticas","Física","Química"], requerido:true },
      { id:"semestre",  label:"Semestre actual",     tipo:"select", opciones:["1ro","2do","3ro","4to","5to","6to","7mo","8vo","9no","10mo"] },
      { id:"materias",  label:"Materias a inscribir",tipo:"textarea",requerido:true },
      { id:"email",     label:"Correo electrónico",  tipo:"email",  requerido:true  }
    ],
    procesos: [
      { id:"P1", nombre:"Completar formulario",      rol:"estudiante" },
      { id:"P2", nombre:"Revisar y aprobar",          rol:"asesor"     },
      { id:"P3", nombre:"Registrar en Kardex",        rol:"kardex"     },
      { id:"P4", nombre:"Notificar al estudiante",    rol:"asesor"     }
    ]
  },
  certificado: {
    flujo: "certificado",
    nombre: "Certificado de Notas",
    descripcion: "Solicitud de certificado académico de notas por gestión.",
    campos: [
      { id:"nombre",   label:"Nombre completo",   tipo:"text",   requerido:true },
      { id:"carnet",   label:"Número de carnet",  tipo:"text",   requerido:true },
      { id:"gestion",  label:"Gestión solicitada",tipo:"select", opciones:["2024-I","2024-II","2025-I","2025-II","2026-I"] },
      { id:"motivo",   label:"Motivo de la solicitud", tipo:"textarea" },
      { id:"urgente",  label:"¿Es urgente?",      tipo:"select", opciones:["No","Sí — necesito en 24h"] }
    ],
    procesos: [
      { id:"P1", nombre:"Completar solicitud",    rol:"estudiante" },
      { id:"P2", nombre:"Verificar datos",         rol:"secretaria" },
      { id:"P3", nombre:"Generar certificado",     rol:"sistemas"   },
      { id:"P4", nombre:"Entregar al estudiante",  rol:"secretaria" }
    ]
  }
};

// ══════════════════════════════════════════════════════════
// FORMULARIOS DINÁMICOS
// ══════════════════════════════════════════════════════════
function cargarFlujo(nombre) {
  const flujo = FLUJOS[nombre];
  if (!flujo) return;

  // Activar botón
  document.querySelectorAll('.btn-tramite').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.btn-tramite').forEach(b => {
    if (b.textContent.toLowerCase().includes(nombre === 'inscripcion' ? 'inscripción' : 'certificado'))
      b.classList.add('active');
  });

  // Info del formulario
  document.getElementById('formInfo').innerHTML = `
    <h3>${flujo.nombre}</h3>
    <p>${flujo.descripcion}</p>
  `;

  // Campos dinámicos
  const form = document.getElementById('tramiteForm');
  form.innerHTML = '';
  flujo.campos.forEach(campo => {
    const grupo = document.createElement('div');
    grupo.className = 'form-group';
    let inputHTML = '';
    if (campo.tipo === 'select') {
      inputHTML = `<select id="${campo.id}" ${campo.requerido ? 'required' : ''}>
        ${campo.opciones.map(o => `<option value="${o}">${o}</option>`).join('')}
      </select>`;
    } else if (campo.tipo === 'textarea') {
      inputHTML = `<textarea id="${campo.id}" rows="3" placeholder="Ingrese aquí..." ${campo.requerido ? 'required' : ''}></textarea>`;
    } else {
      inputHTML = `<input type="${campo.tipo}" id="${campo.id}" placeholder="${campo.label}" ${campo.requerido ? 'required' : ''}>`;
    }
    grupo.innerHTML = `<label for="${campo.id}">${campo.label}${campo.requerido ? ' <span style="color:#ef4444">*</span>' : ''}</label>${inputHTML}`;
    form.appendChild(grupo);
  });

  // Botón enviar
  const btn = document.createElement('button');
  btn.type = 'submit';
  btn.className = 'btn-submit';
  btn.textContent = '📤 Enviar solicitud';
  form.appendChild(btn);

  form.onsubmit = (e) => {
    e.preventDefault();
    btn.textContent = '✅ Solicitud enviada con éxito';
    btn.style.background = 'linear-gradient(135deg,#10b981,#059669)';
    setTimeout(() => {
      btn.textContent = '📤 Enviar solicitud';
      btn.style.background = '';
    }, 3000);
  };

  // Pasos del flujo
  const stepsDiv = document.getElementById('formSteps');
  stepsDiv.innerHTML = `<h4>Flujo del trámite</h4><div class="steps-list">
    ${flujo.procesos.map((p, i) => `
      <div class="step-badge">
        <span style="color:#94a3b8">${p.id}</span>
        ${p.nombre}
        <span class="step-role">[${p.rol}]</span>
        ${i < flujo.procesos.length - 1 ? '<span style="color:#6366f1">→</span>' : ''}
      </div>
    `).join('')}
  </div>`;
}

// ══════════════════════════════════════════════════════════
// TEXTURA DE PARTÍCULA CIRCULAR GLOWING (Elimina cuadrados feos)
// ══════════════════════════════════════════════════════════
function createCircleTexture(colorStr = '#ffffff', size = 64) {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  
  // Gradiente radial para difuminar bordes y dar efecto de luz suave
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
// THREE.JS — HERO CANVAS (partículas flotantes de alta calidad)
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

  // Nube de partículas circulares suaves
  const geo = new THREE.BufferGeometry();
  const N = 800;
  const pos = new Float32Array(N * 3);
  const col = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    pos[i*3]   = (Math.random()-0.5)*12;
    pos[i*3+1] = (Math.random()-0.5)*9;
    pos[i*3+2] = (Math.random()-0.5)*6;
    const t = Math.random();
    col[i*3]   = 0.38 + t*0.2; // R
    col[i*3+1] = 0.4  + t*0.3; // G (mezcla de indigo a cian)
    col[i*3+2] = 0.95;         // B
  }
  geo.setAttribute('position', new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color',    new THREE.BufferAttribute(col,3));
  
  const circleTexture = createCircleTexture('#ffffff', 64);
  const mat = new THREE.PointsMaterial({ 
    size: 0.12, 
    vertexColors: true, 
    map: circleTexture,
    transparent: true, 
    opacity: 0.75,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  });
  scene.add(new THREE.Points(geo, mat));

  // Anillo decorativo futurista
  const ringGeo = new THREE.TorusGeometry(2.2, 0.03, 16, 100);
  const ringMat = new THREE.MeshBasicMaterial({ 
    color: 0x06b6d4, 
    transparent: true, 
    opacity: 0.45,
    wireframe: true 
  });
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
// THREE.JS — ANIMACIÓN 3D INTERACTIVA (Upgrade Materiales y Luces)
// ══════════════════════════════════════════════════════════
let threeScene, threeCamera, threeRenderer, meshPrincipal, isWireframe = false;
let orbitLight; // Luz en órbita para reflejos dinámicos

(function initThree() {
  const canvas = document.getElementById('threeCanvas');
  if (!canvas || typeof THREE === 'undefined') return;
  threeRenderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  threeRenderer.setClearColor(0x03050b);
  const w = canvas.clientWidth || 700, h = 520;
  threeRenderer.setSize(w, h, false);

  threeScene  = new THREE.Scene();
  threeCamera = new THREE.PerspectiveCamera(50, w/h, 0.1, 100);
  threeCamera.position.set(0, 0, 4.2);

  // Luces premium
  threeScene.add(new THREE.AmbientLight(0x131930, 2.0));
  
  const dirLight = new THREE.DirectionalLight(0x06b6d4, 3.5); // Luz cian
  dirLight.position.set(4, 4, 4);
  threeScene.add(dirLight);
  
  const fillLight = new THREE.DirectionalLight(0x6366f1, 2.5); // Luz índigo
  fillLight.position.set(-4, -2, -3);
  threeScene.add(fillLight);

  // Luz puntual giratoria de color rosa caliente para crear reflejos especulares de ensueño
  orbitLight = new THREE.PointLight(0xec4899, 4, 12);
  threeScene.add(orbitLight);

  // Geometría y material avanzado MeshPhysicalMaterial (Transparencia, brillo, laca clara)
  const geo = new THREE.SphereGeometry(1.25, 64, 64);
  const mat = new THREE.MeshPhysicalMaterial({
    color: 0x6366f1,
    roughness: 0.12,
    metalness: 0.85,
    clearcoat: 1.0,
    clearcoatRoughness: 0.05,
    reflectivity: 1.0,
    transparent: true,
    opacity: 0.92,
    flatShading: false
  });
  meshPrincipal = new THREE.Mesh(geo, mat);
  threeScene.add(meshPrincipal);

  // Grid de fondo estilizado
  const grid = new THREE.GridHelper(20, 30, 0x1e293b, 0x1e293b);
  grid.position.y = -2.1;
  threeScene.add(grid);

  // Partículas flotantes de fondo
  const pgeo = new THREE.BufferGeometry();
  const pp = new Float32Array(500*3);
  for (let i=0;i<500;i++){
    pp[i*3]=(Math.random()-0.5)*20;
    pp[i*3+1]=(Math.random()-0.5)*20;
    pp[i*3+2]=(Math.random()-0.5)*20;
  }
  pgeo.setAttribute('position', new THREE.BufferAttribute(pp,3));
  
  const starTexture = createCircleTexture('#06b6d4', 64);
  const pointsMat = new THREE.PointsMaterial({
    size: 0.15,
    color: 0x06b6d4,
    map: starTexture,
    transparent: true,
    opacity: 0.45,
    depthWrite: false,
    blending: THREE.AdditiveBlending
  });
  threeScene.add(new THREE.Points(pgeo, pointsMat));

  // Controles de órbita manual
  let isDragging=false, prevX=0, prevY=0, rotX=0, rotY=0;
  canvas.addEventListener('mousedown',e=>{isDragging=true;prevX=e.clientX;prevY=e.clientY;});
  window.addEventListener('mouseup',()=>isDragging=false);
  window.addEventListener('mousemove',e=>{
    if(!isDragging)return;
    rotY+=(e.clientX-prevX)*0.007;
    rotX+=(e.clientY-prevY)*0.007;
    prevX=e.clientX;prevY=e.clientY;
  });
  canvas.addEventListener('wheel',e=>{
    if (e.ctrlKey) {
      e.preventDefault();
      threeCamera.position.z=Math.max(2,Math.min(8,threeCamera.position.z+e.deltaY*0.005));
    }
  }, { passive: false });

  let t=0;
  (function animate(){
    requestAnimationFrame(animate);
    t+=0.01;
    meshPrincipal.rotation.y = rotY + t*0.35;
    meshPrincipal.rotation.x = rotX + Math.sin(t*0.25)*0.08;
    meshPrincipal.position.y = Math.sin(t*0.75)*0.12;
    
    // Mover la luz de órbita en círculo tridimensional
    if (orbitLight) {
      orbitLight.position.x = Math.cos(t * 1.5) * 2.8;
      orbitLight.position.z = Math.sin(t * 1.5) * 2.8;
      orbitLight.position.y = Math.sin(t * 0.7) * 1.5;
    }
    
    threeRenderer.render(threeScene,threeCamera);
  })();
})();

function cambiarGeometria(tipo) {
  if (!threeScene || !meshPrincipal) return;
  threeScene.remove(meshPrincipal);
  let geo;
  if (tipo==='esfera')    geo = new THREE.SphereGeometry(1.25,64,64);
  else if(tipo==='toroide') geo = new THREE.TorusGeometry(1.05,0.42,32,100);
  else                    geo = new THREE.IcosahedronGeometry(1.35,1);
  meshPrincipal = new THREE.Mesh(geo, meshPrincipal.material);
  threeScene.add(meshPrincipal);
}

function toggleWireframe() {
  if (!meshPrincipal) return;
  isWireframe = !isWireframe;
  meshPrincipal.material.wireframe = isWireframe;
}

// ══════════════════════════════════════════════════════════
// THREE.JS — VISOR FOTOGRAMÉTRICO (Nube de Puntos Holográfica Glow)
// ══════════════════════════════════════════════════════════
(function initObjViewer() {
  const canvas = document.getElementById('objCanvas');
  if (!canvas || typeof THREE === 'undefined') return;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x03050b);
  const w = canvas.clientWidth || 500, h = 520;
  renderer.setSize(w, h, false);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(50, w/h, 0.01, 100);
  camera.position.set(0, 0, 3.5);

  // Ejes 3D de referencia
  const axes = new THREE.AxesHelper(0.6);
  axes.material.opacity = 0.35;
  axes.material.transparent = true;
  scene.add(axes);

  // Luces de ambientación
  scene.add(new THREE.AmbientLight(0x131930, 2.5));

  // Inicializar geometría y material de partículas circulares suaves (Holograma Glow)
  const geo = new THREE.BufferGeometry();
  
  const particleTexture = createCircleTexture('#ffffff', 64);
  const pointsMaterial = new THREE.PointsMaterial({ 
    size: 0.045, // Tamaño perfecto de partícula
    vertexColors: true,
    map: particleTexture,
    transparent: true,
    alphaTest: 0.001,
    depthWrite: false,
    blending: THREE.AdditiveBlending // Glow holográfico en aditivo
  });
  
  const pts = new THREE.Points(geo, pointsMaterial);
  scene.add(pts);

  // Cargar modelo real (con fallback a simulación por CORS en file://)
  fetch('modelo/GutierrezCondori_modelo.obj')
    .then(response => {
      if (!response.ok) throw new Error('Error al cargar archivo');
      return response.text();
    })
    .then(text => {
      const posArray = [];
      const colArray = [];
      const lines = text.split('\n');
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('v ')) {
          const parts = line.split(/\s+/);
          if (parts.length >= 4) {
            posArray.push(parseFloat(parts[1]), parseFloat(parts[2]), parseFloat(parts[3]));
            if (parts.length >= 7) {
              colArray.push(parseFloat(parts[4]), parseFloat(parts[5]), parseFloat(parts[6]));
            } else {
              colArray.push(0.06, 0.71, 0.83); // Color cian por defecto
            }
          }
        }
      }
      
      if (posArray.length === 0) throw new Error('No se encontraron vértices');
      
      geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(posArray), 3));
      geo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(colArray), 3));
      
      // Actualizar badge con info real
      const badge = canvas.parentElement.querySelector('.canvas-badge');
      if (badge) {
        badge.textContent = `${(posArray.length / 3).toLocaleString()} vértices · Modelo Real`;
      }
      
      console.log('Modelo real OBJ cargado exitosamente:', posArray.length/3, 'vértices');
    })
    .catch(err => {
      console.warn('Usando fallback de simulación de nube de puntos:', err.message);
      // Simular nube de puntos igual a la real pero con colores premium (cian/rosa)
      const N = 5920;
      const positions = new Float32Array(N*3);
      const colors    = new Float32Array(N*3);
      const ptsPerFrame = 80;
      const nFrames = N / ptsPerFrame;

      for (let i = 0; i < N; i++) {
        const frameIdx = Math.floor(i / ptsPerFrame);
        const angle = (frameIdx / nFrames) * Math.PI * 2;
        const r = 1.0;
        const noise = () => (Math.random()-0.5)*0.1;
        positions[i*3]   = r*Math.cos(angle) + noise();
        positions[i*3+1] = (Math.random()-0.5)*1.3 + noise();
        positions[i*3+2] = r*Math.sin(angle) + noise();
        
        // Color premium (Gradiente de rosa a cian)
        const t = Math.random();
        colors[i*3]   = 0.38 * t + 0.92 * (1-t); // Mezcla R
        colors[i*3+1] = 0.4  * t + 0.28 * (1-t); // Mezcla G
        colors[i*3+2] = 0.95;                    // B
      }
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geo.setAttribute('color',    new THREE.BufferAttribute(colors, 3));
      
      const badge = canvas.parentElement.querySelector('.canvas-badge');
      if (badge) {
        badge.textContent = `5,920 vértices · Simulación (CORS Fallback)`;
      }
    });

  // Mouse drag
  let drag=false,px=0,py=0,rx=0,ry=0;
  canvas.addEventListener('mousedown',e=>{drag=true;px=e.clientX;py=e.clientY;});
  window.addEventListener('mouseup',()=>drag=false);
  window.addEventListener('mousemove',e=>{
    if(!drag)return;
    ry+=(e.clientX-px)*0.007; rx+=(e.clientY-py)*0.007;
    px=e.clientX;py=e.clientY;
  });
  
  canvas.addEventListener('wheel',e=>{
    if (e.ctrlKey) {
      e.preventDefault();
      camera.position.z=Math.max(1.5,Math.min(6,camera.position.z+e.deltaY*0.005));
    }
  }, { passive: false });

  let t=0;
  (function animate(){
    requestAnimationFrame(animate);
    t+=0.003;
    pts.rotation.y = ry + t;
    pts.rotation.x = rx;
    renderer.render(scene,camera);
  })();
})();

// ══════════════════════════════════════════════════════════
// TABS DE PROCESAMIENTO
// ══════════════════════════════════════════════════════════
function mostrarTab(id) {
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  event.target.classList.add('active');
}

// ══════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  cargarFlujo('inscripcion');
});
