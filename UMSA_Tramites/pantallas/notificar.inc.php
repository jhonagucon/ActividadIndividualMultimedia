<?php
// Pantalla P4 — Notificar al estudiante (Rol: asesor)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>📢 Notificar al Estudiante</h3>
        <p>La inscripción ya fue registrada en Kardex. Envía la notificación final al estudiante.</p>
    </div>
    <div class="card-body">

        <div class="alert alert-success">
            ✅ Las materias del estudiante <strong><?= htmlspecialchars($datos_ticket['nombre_est'] ?? '—') ?></strong>
            ya están registradas en Kardex (Ref: <strong><?= htmlspecialchars($datos_ticket['nro_registro_kardex'] ?? 'N/D') ?></strong>).
        </div>

        <!-- Resumen completo -->
        <div class="info-block">
            <h4>📋 Resumen del Trámite</h4>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">RU</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['ru'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Estudiante</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['nombre_est'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Materias inscritas</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['materias'] ?? '—') ?></span>
                </div>
                <div class="info-item">
                    <span class="info-label">Nro. Kardex</span>
                    <span class="info-val"><?= htmlspecialchars($datos_ticket['nro_registro_kardex'] ?? '—') ?></span>
                </div>
            </div>
        </div>

        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">
            <div class="form-group">
                <label for="mensaje_notificacion">Mensaje de notificación al estudiante</label>
                <textarea id="mensaje_notificacion" name="mensaje_notificacion" rows="4"
                          required><?php
                $nombre = htmlspecialchars($datos_ticket['nombre_est'] ?? 'Estimado/a estudiante');
                $mats   = htmlspecialchars($datos_ticket['materias'] ?? '');
                echo "Estimado/a $nombre,\n\nNos complace informarte que tu inscripción de materias ($mats) ha sido aprobada y registrada exitosamente.\n\nSaludos,\nAsesoría Académica";
                ?></textarea>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-lg">
                    📨 Enviar Notificación y Cerrar Trámite ✔
                </button>
            </div>
        </form>

    </div>
</div>
