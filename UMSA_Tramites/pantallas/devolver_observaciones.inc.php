<?php
// Pantalla P5 — Devolver con observaciones (Rol: asesor)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>🔄 Devolver con Observaciones</h3>
        <p>La solicitud regresará al estudiante para que corrija su formulario.</p>
    </div>
    <div class="card-body">

        <div class="alert alert-warning">
            ⚠️ Esta solicitud fue <strong>rechazada</strong> por el asesor y regresa al estudiante.
        </div>

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
            </div>
        </div>

        <?php if (!empty($datos_ticket['motivo_devolucion'])): ?>
        <div class="info-block">
            <h4>💬 Motivo de Devolución (registrado por el asesor)</h4>
            <p class="text-warning"><?= htmlspecialchars($datos_ticket['motivo_devolucion']) ?></p>
        </div>
        <?php endif; ?>

        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">
            <div class="form-group">
                <label for="observaciones_devolucion">Instrucciones adicionales para el estudiante</label>
                <textarea id="observaciones_devolucion" name="observaciones_devolucion" rows="3"
                          placeholder="Especifica qué debe corregir el estudiante..."
                          required><?= htmlspecialchars($datos_ticket['motivo_devolucion'] ?? '') ?></textarea>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-warning btn-lg">
                    🔄 Devolver al Estudiante
                </button>
            </div>
        </form>

    </div>
</div>
