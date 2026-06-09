<?php
// Punto de entrada — redirigir según estado de sesión
session_start();
if (isset($_SESSION['usuario'])) {
    header('Location: bandeja.php');
} else {
    header('Location: login.php');
}
exit();
?>
