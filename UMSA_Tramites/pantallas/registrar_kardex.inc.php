<?php
// Pantalla P3 — Registrar en Kardex (Rol: kardex)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket

$materias_map = [
    'INF-111' => 'Programación I',
    'INF-272' => 'Programación II',
    'MAT-101' => 'Matemáticas I',
    'MAT-202' => 'Matemáticas II',
    'ETN-201' => 'Estadística',
    'IND-112' => 'Ingeniería Industrial I',
    'SIS-301' => 'Sistemas Operativos',
    'RED-401' => 'Redes de Computadoras',
];
$materias_sel = !empty($datos_ticket['materias'])
    ? explode(',', $datos_ticket['materias']) : [];
?>
<div class="card">
    <div class="card-header">
        <h3>🗂️ Registro en Kardex</h3>
        <p>La inscripción fue <strong>aprobada por el asesor</strong>. Registra las materias en el sistema Kardex.</p>
    </div>
    <div class="card-body">

        <div class="alert alert-success">
            ✅ Esta solicitud fue <strong>aprobada</strong> por el asesor académico.
        </div>

        <!-- Resumen del estudiante -->
        <div class="info-block">
            <h4>👨‍🎓 Datos del Estudiante</h4>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">RU</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['ru'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Nombre</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['nombre_est'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Carrera</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['carrera'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Semestre</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['semestre'] ?? '—') ?>°</span>
                </div>
            </div>
        </div>

        <!-- Materias a registrar -->
        <div class="info-block">
            <h4>📚 Materias a Registrar</h4>
            <table class="table">
                <thead>
                    <tr><th>Código</th><th>Materia</th><th>Estado</th></tr>
                </thead>
                <tbody>
                    <?php foreach ($materias_sel as $cod): ?>
                    <tr>
                        <td><span class="badge badge-mat"><?= htmlspecialchars($cod) ?></span></td>
                        <td><?= htmlspecialchars($materias_map[$cod] ?? $cod) ?></td>
                        <td><span class="badge badge-success">Para registrar</span></td>
                    </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>

        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">
            <div class="form-group">
                <label for="nro_registro_kardex">Número de registro en Kardex</label>
                <input type="text" id="nro_registro_kardex" name="nro_registro_kardex"
                       placeholder="Ej: KDX-2026-001" required>
            </div>
            <div class="form-group">
                <label for="fecha_registro">Fecha de registro</label>
                <input type="date" id="fecha_registro" name="fecha_registro"
                       value="<?= date('Y-m-d') ?>" required>
            </div>
            <div class="form-group">
                <label for="observaciones_kardex">Observaciones (opcional)</label>
                <textarea id="observaciones_kardex" name="observaciones_kardex" rows="2"
                          placeholder="Alguna nota del registro..."></textarea>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-lg">
                    ✔ Confirmar Registro en Kardex →
                </button>
            </div>
        </form>

    </div>
</div>
