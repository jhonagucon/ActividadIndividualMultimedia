<?php
// Directorio base donde están los archivos de datos
define('DATA_DIR', __DIR__ . '/data/');
define('FLUJOS_DIR', __DIR__ . '/flujos/');

// ─── Leer JSON ────────────────────────────────────────────────────────────────
function leer_json($archivo) {
    $ruta = DATA_DIR . $archivo;
    if (!file_exists($ruta)) return [];
    $contenido = file_get_contents($ruta);
    return json_decode($contenido, true) ?? [];
}

// ─── Guardar JSON ─────────────────────────────────────────────────────────────
function guardar_json($archivo, $datos) {
    $ruta = DATA_DIR . $archivo;
    // CORRECCIÓN: json_encode (no json_decode) y pasar $datos (array)
    $json = json_encode($datos, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    file_put_contents($ruta, $json);
}

// ─── Leer flujo JSON ──────────────────────────────────────────────────────────
function leer_flujo($flujo_id) {
    $ruta = FLUJOS_DIR . $flujo_id . '.json';
    if (!file_exists($ruta)) return null;
    $contenido = file_get_contents($ruta);
    return json_decode($contenido, true) ?? null;
}

// ─── Buscar proceso dentro del flujo ─────────────────────────────────────────
function buscar_proceso($flujo, $proceso_id) {
    foreach ($flujo['procesos'] as $p) {
        if ($p['id'] == $proceso_id) return $p;
    }
    return null;
}

// ─── Buscar condición dentro del flujo ───────────────────────────────────────
// CORRECCIÓN: nombre en español, argumento correcto ($c['proceso'] no $c['proceso_id'])
function buscar_condicion($flujo, $proceso_id) {
    if (!isset($flujo['condiciones'])) return null;
    foreach ($flujo['condiciones'] as $c) {
        if ($c['proceso'] == $proceso_id) return $c;
    }
    return null;
}

// ─── Generar número de ticket nuevo ──────────────────────────────────────────
function generar_ticket_id() {
    $tickets = leer_json('ticket.json');
    if (empty($tickets)) return 1;
    $ids = array_column($tickets, 'ticket');
    return max($ids) + 1;
}
?>
