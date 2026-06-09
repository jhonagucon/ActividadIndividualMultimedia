<?php
// Pantalla C3 — Emitir Certificado (Rol: decano)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>🏅 Emisión de Certificado</h3>
        <p>La solicitud fue <strong>aprobada por secretaría</strong>. Como Decano, confirma y emite el certificado.</p>
    </div>
    <div class="card-body">

        <div class="alert alert-success">
            ✅ Aprobado por Secretaría — listo para firma y emisión del Decano.
        </div>

        <!-- Vista previa del certificado -->
        <div class="certificado-preview">
            <div class="cert-header">
                <div class="cert-logo">🎓</div>
                <h4>UNIVERSIDAD AUTÓNOMA</h4>
                <p>Facultad de Ingeniería</p>
            </div>
            <div class="cert-titulo">
                CERTIFICA QUE:
            </div>
            <div class="cert-nombre">
                <?= strtoupper(htmlspecialchars($datos_ticket['nombre_est'] ?? 'NOMBRE DEL ESTUDIANTE')) ?>
            </div>
            <div class="cert-body">
                con Registro Universitario <strong><?= htmlspecialchars($datos_ticket['ru'] ?? '—') ?></strong>,
                estudiante de la carrera de <strong><?= htmlspecialchars($datos_ticket['carrera'] ?? '—') ?></strong>,
                ha solicitado el siguiente documento:
                <br><br>
                <span class="cert-tipo"><?= htmlspecialchars($datos_ticket['tipo_cert'] ?? '—') ?></span>
                <br><br>
                Motivo: <em><?= htmlspecialchars($datos_ticket['motivo'] ?? '—') ?></em>
                &nbsp;|&nbsp; Copias: <strong><?= htmlspecialchars($datos_ticket['copias'] ?? '1') ?></strong>
            </div>
            <div class="cert-fecha">
                <?= date('d \d\e F \d\e Y') ?>
            </div>
            <div class="cert-firma">
                ____________________________<br>
                DECANO / DIRECTOR
            </div>
        </div>

        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">
            <div class="form-group">
                <label for="nro_certificado">Número de certificado emitido</label>
                <input type="text" id="nro_certificado" name="nro_certificado"
                       placeholder="Ej: CERT-2026-001" required>
            </div>
            <div class="form-group">
                <label for="observaciones_decano">Observaciones del Decano (opcional)</label>
                <textarea id="observaciones_decano" name="observaciones_decano" rows="2"
                          placeholder="Alguna nota adicional..."></textarea>
            </div>
            <div class="form-actions">
                <button type="submit" class="btn btn-success btn-lg">
                    🏅 Emitir y Cerrar Trámite ✔
                </button>
            </div>
        </form>

    </div>
</div>
