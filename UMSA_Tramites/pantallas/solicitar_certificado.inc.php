<?php
// Pantalla C1 — Solicitar Certificado (Rol: estudiante)
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket

$tipos_cert = [
    'Certificado de Estudios',
    'Certificado de Notas',
    'Carta de Presentación',
    'Certificado de Egreso',
    'Solicitud de Título',
];
?>
<div class="card">
    <div class="card-header">
        <h3>📄 Solicitud de Certificado</h3>
        <p>Completa el formulario para solicitar tu certificado académico.</p>
    </div>
    <div class="card-body">
        <form method="POST"
              action="controlador.php?flujo=<?= urlencode($flujo_id) ?>&proceso=<?= urlencode($proceso_id) ?>&ticket=<?= $ticket_id ?>&Siguiente=1">

            <div class="form-row">
                <div class="form-group">
                    <label for="ru">Registro Universitario (RU)</label>
                    <input type="text" id="ru" name="ru" placeholder="Ej: 12345"
                           value="<?= htmlspecialchars($datos_ticket['ru'] ?? '') ?>" required>
                </div>
                <div class="form-group">
                    <label for="nombre_est">Nombre completo</label>
                    <input type="text" id="nombre_est" name="nombre_est"
                           placeholder="Tu nombre completo"
                           value="<?= htmlspecialchars($datos_ticket['nombre_est'] ?? '') ?>" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="carrera">Carrera</label>
                    <select id="carrera" name="carrera" required>
                        <option value="">— Selecciona tu carrera —</option>
                        <?php
                        $carreras = [
                            'Ingeniería de Sistemas',
                            'Informática',
                            'Telecomunicaciones',
                            'Ingeniería Industrial',
                            'Ingeniería Civil',
                            'Ingeniería Química',
                        ];
                        foreach ($carreras as $c):
                            $sel = ($datos_ticket['carrera'] ?? '') === $c ? 'selected' : '';
                        ?>
                        <option value="<?= htmlspecialchars($c) ?>" <?= $sel ?>><?= htmlspecialchars($c) ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
                <div class="form-group">
                    <label for="tipo_cert">Tipo de Certificado</label>
                    <select id="tipo_cert" name="tipo_cert" required>
                        <option value="">— Selecciona el tipo —</option>
                        <?php foreach ($tipos_cert as $tc):
                            $sel = ($datos_ticket['tipo_cert'] ?? '') === $tc ? 'selected' : '';
                        ?>
                        <option value="<?= htmlspecialchars($tc) ?>" <?= $sel ?>><?= htmlspecialchars($tc) ?></option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="motivo">Motivo / Destino del certificado</label>
                <input type="text" id="motivo" name="motivo"
                       placeholder="Ej: Postulación a pasantía, trámite de beca, visa..."
                       value="<?= htmlspecialchars($datos_ticket['motivo'] ?? '') ?>" required>
            </div>

            <div class="form-group">
                <label for="copias">Número de copias solicitadas</label>
                <select id="copias" name="copias" required>
                    <?php for ($n = 1; $n <= 5; $n++):
                        $sel = ($datos_ticket['copias'] ?? 1) == $n ? 'selected' : '';
                    ?>
                    <option value="<?= $n ?>" <?= $sel ?>><?= $n ?> copia(s)</option>
                    <?php endfor; ?>
                </select>
            </div>

            <div class="form-group">
                <label for="observaciones_est">Observaciones adicionales (opcional)</label>
                <textarea id="observaciones_est" name="observaciones_est" rows="3"
                          placeholder="Alguna indicación especial..."><?= htmlspecialchars($datos_ticket['observaciones_est'] ?? '') ?></textarea>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-lg">
                    Enviar Solicitud a Secretaría →
                </button>
                <a href="bandeja.php" class="btn btn-secondary btn-lg">Cancelar</a>
            </div>
        </form>
    </div>
</div>
