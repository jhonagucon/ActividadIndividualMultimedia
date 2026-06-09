<?php
// Pantalla C4 — Rechazar con motivo (Rol: secretaria)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>❌ Rechazo de Solicitud de Certificado</h3>
        <p>La solicitud ha sido <strong>rechazada</strong>. Completa los detalles del rechazo para cerrar el trámite.</p>
    </div>
    <div class="card-body">

        <div class="alert alert-error">
            ❌ Esta solicitud fue <strong>rechazada</strong> por la Secretaría. El trámite se cerrará.
        </div>

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
                    <span class="info-label">Tipo solicitado</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['tipo_cert'] ?? '—') ?></span>
                </div>
            </div>
        </div>

        <?php if (!empty($datos_ticket['motivo_rechazo'])): ?>
        <div class="info-block">
            <h4>💬 Motivo de Rechazo</h4>
            <p class="text-danger"><?= htmlspecialchars($datos_ticket['motivo_rechazo']) ?></p>
        </div>
        <?php endif; ?>

        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">
            <div class="form-group">
                <label for="comunicado_rechazo">Comunicado oficial de rechazo</label>
                <textarea id="comunicado_rechazo" name="comunicado_rechazo" rows="4"
                          required><?php
$nombre = htmlspecialchars($datos_ticket['nombre_est'] ?? 'Estimado/a estudiante');
$motivo = htmlspecialchars($datos_ticket['motivo_rechazo'] ?? 'no cumple con los requisitos establecidos');
echo "Estimado/a $nombre,\n\nLamentamos informarte que tu solicitud de certificado ha sido rechazada. Motivo: $motivo.\n\nPuedes volver a presentar tu solicitud una vez que corrijas la situación indicada.\n\nAtentamente,\nSecretaría";
                ?></textarea>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-danger btn-lg">
                    ❌ Confirmar Rechazo y Cerrar Trámite
                </button>
            </div>
        </form>

    </div>
</div>
