<?php
session_start();
include 'json_helper.php';

if (!isset($_SESSION['usuario'])) {
    header('Location: login.php'); exit();
}

$usuario = $_SESSION['usuario'];
$rol     = $_SESSION['rol'];
$nombre  = $_SESSION['nombre'];

// ─── Leer todos los tickets y filtrar por rol y sin fecha final ───────────────
$todos      = leer_json('ticket.json');
$pendientes = array_filter($todos, function($t) use ($rol) {
    return $t['usuario'] === $rol && $t['fechafinal'] == null;
});

// ─── Estadísticas del usuario ─────────────────────────────────────────────────
$completados = array_filter($todos, function($t) use ($rol) {
    return $t['usuario'] === $rol && $t['fechafinal'] != null;
});

// ─── Nombres de flujo para mostrar amigablemente ──────────────────────────────
$nombres_flujo = [
    'inscripcion'  => 'Inscripción de Materias',
    'certificado'  => 'Emisión de Certificados',
];
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bandeja — UMSA Trámites</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<!-- ─── NAVBAR ─────────────────────────────────────────────────────────────── -->
<nav class="navbar">
    <div class="nav-brand">🎓 UMSA Trámites</div>
    <div class="nav-links">
        <span class="nav-user">👤 <?= htmlspecialchars($nombre) ?>
            <span class="badge badge-rol"><?= htmlspecialchars($rol) ?></span>
        </span>
        <?php if (in_array($rol, ['estudiante'])): ?>
            <a href="nuevo_tramite.php" class="btn btn-sm btn-primary">+ Nuevo Trámite</a>
        <?php endif; ?>
        <a href="logout.php" class="btn btn-sm btn-danger">Salir</a>
    </div>
</nav>

<div class="container">

    <!-- ─── ENCABEZADO ──────────────────────────────────────────────────────── -->
    <div class="page-header">
        <h2>📥 Mi Bandeja</h2>
        <p>Aquí están las tareas pendientes asignadas a tu rol: <strong><?= htmlspecialchars($rol) ?></strong></p>
    </div>

    <!-- ─── ESTADÍSTICAS ────────────────────────────────────────────────────── -->
    <div class="stats-row">
        <div class="stat-card stat-pending">
            <div class="stat-num"><?= count($pendientes) ?></div>
            <div class="stat-label">Pendientes</div>
        </div>
        <div class="stat-card stat-done">
            <div class="stat-num"><?= count($completados) ?></div>
            <div class="stat-label">Completados</div>
        </div>
        <div class="stat-card stat-total">
            <div class="stat-num"><?= count($todos) ?></div>
            <div class="stat-label">Total del sistema</div>
        </div>
    </div>

    <!-- ─── TABLA DE PENDIENTES ─────────────────────────────────────────────── -->
    <?php if (empty($pendientes)): ?>
        <div class="empty-state">
            <div class="empty-icon">✅</div>
            <h3>¡Sin tareas pendientes!</h3>
            <p>No tienes ninguna tarea asignada en este momento.</p>
            <?php if (in_array($rol, ['estudiante'])): ?>
                <a href="nuevo_tramite.php" class="btn btn-primary">Iniciar un nuevo trámite</a>
            <?php endif; ?>
        </div>
    <?php else: ?>
        <div class="card">
            <div class="card-header">
                <h3>Tareas pendientes (<?= count($pendientes) ?>)</h3>
            </div>
            <div class="table-wrapper">
                <table class="table">
                    <thead>
                        <tr>
                            <th>#Ticket</th>
                            <th>Trámite</th>
                            <th>Proceso actual</th>
                            <th>Datos del solicitante</th>
                            <th>Fecha de ingreso</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($pendientes as $t):
                            $flujo   = leer_flujo($t['flujo']);
                            $proceso = $flujo ? buscar_proceso($flujo, $t['proceso']) : null;
                            $nombre_flujo = $nombres_flujo[$t['flujo']] ?? $t['flujo'];
                        ?>
                        <tr>
                            <td><span class="ticket-badge">#<?= $t['ticket'] ?></span></td>
                            <td><?= htmlspecialchars($nombre_flujo) ?></td>
                            <td>
                                <span class="proceso-nombre">
                                    <?= htmlspecialchars($proceso['nombre'] ?? $t['proceso']) ?>
                                </span>
                            </td>
                            <td>
                                <?php if (!empty($t['datos'])): ?>
                                    <?php foreach ($t['datos'] as $k => $v): ?>
                                        <small><strong><?= htmlspecialchars($k) ?>:</strong>
                                        <?= htmlspecialchars($v) ?></small><br>
                                    <?php endforeach; ?>
                                <?php else: ?>
                                    <small class="text-muted">—</small>
                                <?php endif; ?>
                            </td>
                            <td><?= htmlspecialchars($t['fechainicial']) ?></td>
                            <td>
                                <a href="controlador.php?flujo=<?= urlencode($t['flujo']) ?>&proceso=<?= urlencode($t['proceso']) ?>&ticket=<?= (int)$t['ticket'] ?>"
                                   class="btn btn-sm btn-primary">
                                    ▶ Atender
                                </a>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    <?php endif; ?>

    <!-- ─── HISTORIAL ───────────────────────────────────────────────────────── -->
    <?php if (!empty($completados)): ?>
    <div class="card mt-4">
        <div class="card-header">
            <h3>Historial de tareas completadas</h3>
        </div>
        <div class="table-wrapper">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>#Ticket</th>
                        <th>Trámite</th>
                        <th>Proceso</th>
                        <th>Inicio</th>
                        <th>Fin</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach (array_reverse(array_values($completados)) as $t):
                        $nombre_flujo = $nombres_flujo[$t['flujo']] ?? $t['flujo'];
                    ?>
                    <tr class="row-done">
                        <td><span class="ticket-badge badge-done">#<?= $t['ticket'] ?></span></td>
                        <td><?= htmlspecialchars($nombre_flujo) ?></td>
                        <td><?= htmlspecialchars($t['proceso']) ?></td>
                        <td><?= htmlspecialchars($t['fechainicial']) ?></td>
                        <td><?= htmlspecialchars($t['fechafinal']) ?></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
    <?php endif; ?>

</div><!-- /container -->
</body>
</html>
