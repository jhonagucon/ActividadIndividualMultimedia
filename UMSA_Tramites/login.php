<?php
session_start();

// ─── Usuarios del sistema (en producción vendría de BD) ───────────────────────
$usuarios = [
    'juan'      => ['password' => '123', 'rol' => 'estudiante', 'nombre' => 'Juan Pérez'],
    'lic_garcia'=> ['password' => '123', 'rol' => 'asesor',     'nombre' => 'Lic. García'],
    'kardex1'   => ['password' => '123', 'rol' => 'kardex',     'nombre' => 'Personal Kardex'],
    'sec_rosa'  => ['password' => '123', 'rol' => 'secretaria', 'nombre' => 'Secretaria Rosa'],
    'decano'    => ['password' => '123', 'rol' => 'decano',     'nombre' => 'Decano Quispe'],
];

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $user = trim($_POST['usuario'] ?? '');
    $pass = trim($_POST['password'] ?? '');

    if (isset($usuarios[$user]) && $usuarios[$user]['password'] === $pass) {
        $_SESSION['usuario'] = $user;
        $_SESSION['rol']     = $usuarios[$user]['rol'];
        $_SESSION['nombre']  = $usuarios[$user]['nombre'];
        header('Location: bandeja.php');
        exit();
    } else {
        $error = 'Usuario o contraseña incorrectos.';
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UMSA — Iniciar Sesión</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="login-body">

<div class="login-card">
    <div class="login-logo">
        <div class="logo-icon">🎓</div>
        <h1>UMSA Trámites</h1>
        <p>Digitalización de Trámites Universitarios</p>
    </div>

    <?php if ($error): ?>
        <div class="alert alert-error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>

    <form method="POST" action="login.php">
        <div class="form-group">
            <label for="usuario">Usuario</label>
            <input type="text" id="usuario" name="usuario" placeholder="Ej: juan, lic_garcia…"
                   value="<?= htmlspecialchars($_POST['usuario'] ?? '') ?>" required>
        </div>
        <div class="form-group">
            <label for="password">Contraseña</label>
            <input type="password" id="password" name="password" placeholder="••••••••" required>
        </div>
        <button type="submit" class="btn btn-primary btn-block">Ingresar</button>
    </form>

    <div class="login-hint">
        <p><strong>Usuarios de prueba</strong> (contraseña: <code>123</code>)</p>
        <table class="hint-table">
            <tr><td><code>juan</code></td><td>Estudiante</td></tr>
            <tr><td><code>lic_garcia</code></td><td>Asesor</td></tr>
            <tr><td><code>kardex1</code></td><td>Kardex</td></tr>
            <tr><td><code>sec_rosa</code></td><td>Secretaria</td></tr>
            <tr><td><code>decano</code></td><td>Decano</td></tr>
        </table>
    </div>
</div>

</body>
</html>
