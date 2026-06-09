<?php
// Pantalla P2 — Revisar y aprobar materias (Rol: asesor)
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
        <h3>🔍 Revisión de Solicitud de Inscripción</h3>
        <p>Revisa la información del estudiante y decide si <strong>aprobar</strong> o <strong>devolver</strong> la solicitud.</p>
    </div>
    <div class="card-body">

        <!-- Datos del estudiante (solo lectura) -->
        <div class="info-block">
            <h4>📌 Datos del Estudiante</h4>
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

        <!-- Materias solicitadas -->
        <div class="info-block">
            <h4>📚 Materias Solicitadas</h4>
            <?php if (empty($materias_sel)): ?>
                <p class="text-muted">No se seleccionaron materias.</p>
            <?php else: ?>
                <ul class="materias-list">
                    <?php foreach ($materias_sel as $cod): ?>
                    <li>
                        <span class="badge badge-mat"><?= htmlspecialchars($cod) ?></span>
                        <?= htmlspecialchars($materias_map[$cod] ?? $cod) ?>
                    </li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>
        </div>

        <?php if (!empty($datos_ticket['observaciones_est'])): ?>
        <div class="info-block">
            <h4>💬 Observaciones del Estudiante</h4>
            <p><?= htmlspecialchars($datos_ticket['observaciones_est']) ?></p>
        </div>
        <?php endif; ?>

        <!-- Botones de decisión -->
        <div class="decision-panel">
            <h4>⚖️ Decisión del Asesor</h4>
            <div class="decision-btns">
                <form method="POST"
                      action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1&decision=verdad">
                    <input type="hidden" name="decision_asesor" value="Aprobado">
                    <button type="submit" class="btn btn-success btn-lg">
                        ✅ Aprobar — enviar a Kardex
                    </button>
                </form>
                <form method="POST"
                      action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1&decision=falso">
                    <div class="form-group">
                        <label for="motivo_devolucion">Motivo de devolución (requerido)</label>
                        <textarea id="motivo_devolucion" name="motivo_devolucion" rows="3"
                                  placeholder="Explica por qué se devuelve al estudiante..."
                                  required></textarea>
                    </div>
                    <button type="submit" class="btn btn-warning btn-lg">
                        🔄 Devolver con Observaciones
                    </button>
                </form>
            </div>
        </div>

    </div>
</div>
