<?php
// Database connection configuration
$dsn = "mysql:host=localhost;dbname=ourdata";
$dbusername = "root";
$dbpassword = "qsdfg123@gfdsq";

// Connect to the database using PDO
try {
    $pdo = new PDO($dsn, $dbusername, $dbpassword);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
    exit();
}
