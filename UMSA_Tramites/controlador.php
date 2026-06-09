<?php
session_start();
include 'json_helper.php';

// ─── Verificar sesión ─────────────────────────────────────────────────────────
if (!isset($_SESSION['usuario'])) {
    header('Location: login.php'); exit();
}

$flujo_id   = $_GET['flujo']   ?? '';
$proceso_id = $_GET['proceso'] ?? '';
$ticket_id  = (int)($_GET['ticket'] ?? 0);
$usuario    = $_SESSION['usuario'];
$rol        = $_SESSION['rol'];
$nombre_usr = $_SESSION['nombre'];

// ─── Cargar el flujo ──────────────────────────────────────────────────────────
$flujo = leer_flujo($flujo_id);
if (!$flujo) {
    echo '<div style="padding:2rem;font-family:sans-serif;color:red;">Error: flujo no encontrado.</div>';
    exit();
}

$proceso = buscar_proceso($flujo, $proceso_id);
if (!$proceso) {
    echo '<div style="padding:2rem;font-family:sans-serif;color:red;">Error: proceso no encontrado.</div>';
    exit();
}

// ─── Verificar que el rol del usuario coincida con el proceso ─────────────────
if ($proceso['rol'] !== $rol) {
    echo '<div style="padding:2rem;font-family:sans-serif;color:red;">
        ⛔ No tienes permisos para este paso. Tu rol es <strong>' .
        htmlspecialchars($rol) . '</strong> pero este paso requiere <strong>' .
        htmlspecialchars($proceso['rol']) . '</strong>.</div>';
    exit();
}

// ─── Manejar el botón "Siguiente" ─────────────────────────────────────────────
if (isset($_GET['Siguiente'])) {

    // PASO 1: Cerrar el paso actual (escribir fechafinal)
    $tickets  = leer_json('ticket.json');
    $decision = $_GET['decision'] ?? null;

    // Guardar datos del formulario si vienen por POST
    $datos_formulario = [];
    foreach ($_POST as $k => $v) {
        // Si el valor es un array (ej: checkboxes materias_arr[]), unirlo como string
        if (is_array($v)) {
            $datos_formulario[$k] = implode(',', $v);
        } else {
            $datos_formulario[$k] = trim($v);
        }
    }

    $tickets = array_map(function($t) use ($ticket_id, $proceso_id, $datos_formulario) {
        if ($t['ticket'] == $ticket_id
            && $t['proceso'] == $proceso_id
            && $t['fechafinal'] == null) {
            $t['fechafinal'] = date('Y-m-d H:i:s');
            // Combinar datos del formulario con los datos existentes
            if (!empty($datos_formulario)) {
                $t['datos'] = array_merge($t['datos'] ?? [], $datos_formulario);
            }
        }
        return $t;
    }, $tickets);

    // PASO 2: Determinar el siguiente proceso (con o sin condición)
    $condicion = buscar_condicion($flujo, $proceso_id);
    if ($condicion) {
        $siguiente_id = ($decision === 'verdad')
            ? $condicion['verdad']
            : $condicion['falso'];
    } else {
        $siguiente_id = $proceso['siguiente'];
    }

    // ─── ¿El trámite ha terminado? ────────────────────────────────────────────
    if ($siguiente_id === null) {
        guardar_json('ticket.json', $tickets);
        ?>
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Trámite Completado</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
        <nav class="navbar">
            <div class="nav-brand">🎓 UMSA Trámites</div>
            <div class="nav-links">
                <a href="bandeja.php" class="btn btn-sm btn-secondary">← Bandeja</a>
                <a href="logout.php" class="btn btn-sm btn-danger">Salir</a>
            </div>
        </nav>
        <div class="container">
            <div class="success-screen">
                <div class="success-icon">🎉</div>
                <h2>¡Trámite Completado!</h2>
                <p>El ticket <strong>#<?= $ticket_id ?></strong> ha concluido exitosamente.</p>
                <p class="text-muted">Flujo: <strong><?= htmlspecialchars($flujo['nombre']) ?></strong></p>
                <a href="bandeja.php" class="btn btn-primary btn-lg">Ir a mi Bandeja</a>
            </div>
        </div>
        </body>
        </html>
        <?php
        exit();
    }

    // PASO 3: Crear el ticket del siguiente proceso
    $proc_sig  = buscar_proceso($flujo, $siguiente_id);

    // Obtener datos acumulados del ticket actual para pasarlos al siguiente
    $datos_acumulados = [];
    foreach ($tickets as $t) {
        if ($t['ticket'] == $ticket_id && !empty($t['datos'])) {
            $datos_acumulados = array_merge($datos_acumulados, $t['datos']);
        }
    }

    $tickets[] = [
        'ticket'      => $ticket_id,
        'flujo'       => $flujo_id,
        'proceso'     => $siguiente_id,
        'usuario'     => $proc_sig['rol'],
        'datos'       => $datos_acumulados,
        'fechainicial'=> date('Y-m-d H:i:s'),
        'fechafinal'  => null,
    ];

    guardar_json('ticket.json', $tickets);
    header('Location: bandeja.php');
    exit();

} else {
    // ─── Mostrar la pantalla del proceso actual ───────────────────────────────
    $pantalla = 'pantallas/' . $proceso['pantalla'] . '.inc.php';

    // Recuperar datos guardados de este ticket
    $tickets      = leer_json('ticket.json');
    $datos_ticket = [];
    foreach ($tickets as $t) {
        if ($t['ticket'] == $ticket_id && $t['proceso'] == $proceso_id) {
            $datos_ticket = $t['datos'] ?? [];
        }
    }
    // También buscar datos de pasos anteriores
    foreach ($tickets as $t) {
        if ($t['ticket'] == $ticket_id && !empty($t['datos'])) {
            $datos_ticket = array_merge($t['datos'], $datos_ticket);
        }
    }
    $datos_ticket = array_unique($datos_ticket);
    ?>
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?= htmlspecialchars($proceso['nombre']) ?> — UMSA Trámites</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
    <nav class="navbar">
        <div class="nav-brand">🎓 UMSA Trámites</div>
        <div class="nav-links">
            <span class="nav-user">👤 <?= htmlspecialchars($nombre_usr) ?>
                <span class="badge badge-rol"><?= htmlspecialchars($rol) ?></span>
            </span>
            <a href="bandeja.php" class="btn btn-sm btn-secondary">← Bandeja</a>
            <a href="logout.php" class="btn btn-sm btn-danger">Salir</a>
        </div>
    </nav>
    <div class="container">

        <!-- Encabezado del proceso -->
        <div class="proceso-header">
            <div class="proceso-meta">
                <span class="ticket-badge">#<?= $ticket_id ?></span>
                <span class="flujo-nombre"><?= htmlspecialchars($flujo['nombre']) ?></span>
            </div>
            <h2><?= htmlspecialchars($proceso['nombre']) ?></h2>

            <!-- Barra de progreso del flujo -->
            <div class="progreso-flujo">
                <?php
                $total_proc = count($flujo['procesos']);
                $idx_actual = 0;
                foreach ($flujo['procesos'] as $i => $p) {
                    if ($p['id'] == $proceso_id) { $idx_actual = $i; break; }
                }
                ?>
                <?php foreach ($flujo['procesos'] as $i => $p): ?>
                <div class="paso <?= $i < $idx_actual ? 'paso-done' : ($i == $idx_actual ? 'paso-active' : 'paso-pending') ?>">
                    <div class="paso-num"><?= $i + 1 ?></div>
                    <div class="paso-label"><?= htmlspecialchars($p['nombre']) ?></div>
                </div>
                <?php if ($i < $total_proc - 1): ?>
                    <div class="paso-linea <?= $i < $idx_actual ? 'linea-done' : '' ?>"></div>
                <?php endif; ?>
                <?php endforeach; ?>
            </div>
        </div>

        <!-- Pantalla del proceso -->
        <?php
        if (file_exists($pantalla)) {
            include $pantalla;
        } else {
            echo '<div class="alert alert-error">⚠️ Pantalla no encontrada: ' .
                 htmlspecialchars($pantalla) . '</div>';
        }
        ?>
    </div>
    </body>
    </html>
    <?php
}
?>
