<?php
session_start();
include 'json_helper.php';

if (!isset($_SESSION['usuario'])) {
    header('Location: login.php'); exit();
}

$rol    = $_SESSION['rol'];
$nombre = $_SESSION['nombre'];

// Solo los estudiantes pueden iniciar trámites
if ($rol !== 'estudiante') {
    header('Location: bandeja.php'); exit();
}

$mensaje = '';
$error   = '';

// Flujos disponibles para iniciar
$flujos_disponibles = [
    'inscripcion'  => [
        'nombre'      => 'Inscripción de Materias',
        'descripcion' => 'Selección y aprobación de materias para el semestre.',
        'icono'       => '📋',
        'primer_proceso' => 'P1',
    ],
    'certificado'  => [
        'nombre'      => 'Emisión de Certificados',
        'descripcion' => 'Solicitud de certificados de estudios, notas, egreso, etc.',
        'icono'       => '📄',
        'primer_proceso' => 'C1',
    ],
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $flujo_id = $_POST['flujo'] ?? '';

    if (!isset($flujos_disponibles[$flujo_id])) {
        $error = 'Trámite no válido.';
    } else {
        $info_flujo  = $flujos_disponibles[$flujo_id];
        $flujo       = leer_flujo($flujo_id);
        $primer_proc = buscar_proceso($flujo, $info_flujo['primer_proceso']);

        // Crear el primer ticket
        $ticket_id = generar_ticket_id();
        $tickets   = leer_json('ticket.json');

        $tickets[] = [
            'ticket'      => $ticket_id,
            'flujo'       => $flujo_id,
            'proceso'     => $info_flujo['primer_proceso'],
            'usuario'     => $primer_proc['rol'],
            'datos'       => [],
            'fechainicial'=> date('Y-m-d H:i:s'),
            'fechafinal'  => null,
        ];

        guardar_json('ticket.json', $tickets);
        $mensaje = "Trámite #{$ticket_id} creado exitosamente. ¡Ya aparece en tu bandeja!";
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuevo Trámite — UMSA Trámites</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<nav class="navbar">
    <div class="nav-brand">🎓 UMSA Trámites</div>
    <div class="nav-links">
        <span class="nav-user">👤 <?= htmlspecialchars($nombre) ?>
            <span class="badge badge-rol"><?= htmlspecialchars($rol) ?></span>
        </span>
        <a href="bandeja.php" class="btn btn-sm btn-secondary">← Bandeja</a>
        <a href="logout.php" class="btn btn-sm btn-danger">Salir</a>
    </div>
</nav>

<div class="container">
    <div class="page-header">
        <h2>📂 Iniciar Nuevo Trámite</h2>
        <p>Selecciona el tipo de trámite que deseas iniciar.</p>
    </div>

    <?php if ($mensaje): ?>
        <div class="alert alert-success">
            ✅ <?= htmlspecialchars($mensaje) ?>
            <a href="bandeja.php" class="btn btn-sm btn-primary ml-2">Ir a mi Bandeja</a>
        </div>
    <?php endif; ?>
    <?php if ($error): ?>
        <div class="alert alert-error">❌ <?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="POST" action="nuevo_tramite.php" id="form-nuevo-tramite">
        <div class="tramite-grid">
            <?php foreach ($flujos_disponibles as $fid => $finfo): ?>
            <label class="tramite-card" for="flujo_<?= $fid ?>">
                <input type="radio" id="flujo_<?= $fid ?>" name="flujo"
                       value="<?= $fid ?>" required>
                <div class="tramite-icon"><?= $finfo['icono'] ?></div>
                <div class="tramite-titulo"><?= htmlspecialchars($finfo['nombre']) ?></div>
                <div class="tramite-desc"><?= htmlspecialchars($finfo['descripcion']) ?></div>
                <div class="tramite-check">✔</div>
            </label>
            <?php endforeach; ?>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary btn-lg">Iniciar Trámite</button>
            <a href="bandeja.php" class="btn btn-secondary btn-lg">Cancelar</a>
        </div>
    </form>
</div>

</body>
</html>
