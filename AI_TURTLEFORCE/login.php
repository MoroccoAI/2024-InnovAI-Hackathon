<?php
include('connection.php');

// Si l'utilisateur soumet le formulaire de connexion
if (isset($_POST['logEmail']) && isset($_POST['logPassword'])) {
    $logEmail = $_POST['logEmail'];
    $logPassword = $_POST['logPassword'];

    $sql = "SELECT * FROM users WHERE email = :email";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':email' => $logEmail]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($user && password_verify($logPassword, $user['password'])) {
        header("Location: chatbot.html?logindone");
        exit(); // Ajoutez exit pour s'assurer que le script s'arrête après la redirection
    } else {
        header("Location: process.html?loginNotDone");
        exit();
    }
}
