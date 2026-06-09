<?php
// Pantalla C2 — Revisar solicitud de certificado (Rol: secretaria)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>📝 Revisión de Solicitud de Certificado</h3>
        <p>Revisa la solicitud del estudiante y decide si <strong>aprobar</strong> (enviar al Decano) o <strong>rechazar</strong>.</p>
    </div>
    <div class="card-body">

        <!-- Datos del estudiante -->
        <div class="info-block">
            <h4>👨‍🎓 Datos del Solicitante</h4>
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
                    <span class="info-label">Tipo de Certificado</span>
                    <span class="info-val">
                        <strong><?= htmlspecialchars($datos_ticket['tipo_cert'] ?? '—') ?></strong>
                    </span>
                </div>
                <div class="info-item">
                    <span class="info-label">Motivo</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['motivo'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Copias</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['copias'] ?? '1') ?></span>
                </div>
            </div>
            <?php if (!empty($datos_ticket['observaciones_est'])): ?>
            <p class="mt-2"><strong>Obs. del estudiante:</strong>
                <?= htmlspecialchars($datos_ticket['observaciones_est']) ?></p>
            <?php endif; ?>
        </div>

        <!-- Panel de decisión -->
        <div class="decision-panel">
            <h4>⚖️ Decisión de Secretaría</h4>
            <div class="decision-btns">
                <!-- APROBAR → enviar al Decano (verdad → C3) -->
                <form method="POST"
                      action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1&decision=verdad">
                    <input type="hidden" name="decision_secretaria" value="Aprobado por secretaría">
                    <button type="submit" class="btn btn-success btn-lg">
                        ✅ Aprobar — Enviar al Decano
                    </button>
                </form>

                <!-- RECHAZAR (falso → C4) -->
                <form method="POST"
                      action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1&decision=falso">
                    <div class="form-group">
                        <label for="motivo_rechazo">Motivo de rechazo (requerido)</label>
                        <textarea id="motivo_rechazo" name="motivo_rechazo" rows="3"
                                  placeholder="Indica por qué se rechaza la solicitud..."
                                  required></textarea>
                    </div>
                    <button type="submit" class="btn btn-danger btn-lg">
                        ❌ Rechazar Solicitud
                    </button>
                </form>
            </div>
        </div>

    </div>
</div>
