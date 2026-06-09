<?php
// Pantalla P1 — Formulario de Inscripción (Rol: estudiante)
// Incluida por controlador.php
// Variables disponibles: $ticket_id, $flujo_id, $proceso_id, $datos_ticket
?>
<div class="card">
    <div class="card-header">
        <h3>📋 Formulario de Inscripción de Materias</h3>
        <p>Completa tus datos y selecciona las materias que deseas inscribir.</p>
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
                    <label for="semestre">Semestre</label>
                    <select id="semestre" name="semestre" required>
                        <option value="">— Semestre —</option>
                        <?php for ($s = 1; $s <= 10; $s++):
                            $sel = ($datos_ticket['semestre'] ?? '') == $s ? 'selected' : '';
                        ?>
                        <option value="<?= $s ?>" <?= $sel ?>><?= $s ?>° Semestre</option>
                        <?php endfor; ?>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label>Materias a inscribir</label>
                <div class="materias-grid">
                    <?php
                    $materias_disponibles = [
                        'INF-111' => 'Programación I',
                        'INF-272' => 'Programación II',
                        'MAT-101' => 'Matemáticas I',
                        'MAT-202' => 'Matemáticas II',
                        'ETN-201' => 'Estadística',
                        'IND-112' => 'Ingeniería Industrial I',
                        'SIS-301' => 'Sistemas Operativos',
                        'RED-401' => 'Redes de Computadoras',
                    ];
                    $seleccionadas = isset($datos_ticket['materias'])
                        ? explode(',', $datos_ticket['materias']) : [];
                    foreach ($materias_disponibles as $cod => $nom):
                        $chk = in_array($cod, $seleccionadas) ? 'checked' : '';
                    ?>
                    <label class="materia-item">
                        <input type="checkbox" name="materias_arr[]"
                               value="<?= htmlspecialchars($cod) ?>" <?= $chk ?>>
                        <span class="materia-cod"><?= htmlspecialchars($cod) ?></span>
                        <span class="materia-nom"><?= htmlspecialchars($nom) ?></span>
                    </label>
                    <?php endforeach; ?>
                </div>
                <!-- Campo oculto para enviar las materias como string -->
                <input type="hidden" id="materias_hidden" name="materias">
            </div>

            <div class="form-group">
                <label for="observaciones_est">Observaciones (opcional)</label>
                <textarea id="observaciones_est" name="observaciones_est" rows="3"
                          placeholder="Alguna nota para el asesor..."><?= htmlspecialchars($datos_ticket['observaciones_est'] ?? '') ?></textarea>
            </div>

            <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-lg">
                    Enviar al Asesor →
                </button>
                <a href="bandeja.php" class="btn btn-secondary btn-lg">Cancelar</a>
            </div>
        </form>
    </div>
</div>

<script>
// Combinar checkboxes de materias en un campo hidden antes de enviar
document.querySelector('form').addEventListener('submit', function() {
    const checks = document.querySelectorAll('input[name="materias_arr[]"]:checked');
    const valores = Array.from(checks).map(c => c.value);
    document.getElementById('materias_hidden').value = valores.join(',');
});
</script>
