<?php
// Database connection configuration
include('connection.php');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Debugging: Inspect POST and FILES data (remove in production)
    var_dump($_POST);
    var_dump($_FILES);

    // Retrieve form data
    $user_type = trim($_POST['usertype']);
    $first_name = trim($_POST['username']);
    $last_name = trim($_POST['userLname']);
    $email = filter_var(trim($_POST['userEmail']), FILTER_VALIDATE_EMAIL);
    $phone = trim($_POST['usertel']);
    $password = $_POST['userpassword'];
    $hashed_password = password_hash($password, PASSWORD_BCRYPT);

    if (!$email) {
        echo "Invalid email address.";
        exit();
    }

    try {
        // Check if email or phone already exists
        $sql = "SELECT * FROM users WHERE email = :email OR phone = :phone";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':email' => $email, ':phone' => $phone]);
        $existingUser = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($existingUser) {
            header("Location: process.html?error=L'email ou le téléphone est déjà utilisé. Veuillez essayer avec des informations différentes");
            exit();
        }

        // Insert into users table
        $sql = "INSERT INTO users (user_type, first_name, last_name, email, phone, password)
                VALUES (:user_type, :first_name, :last_name, :email, :phone, :password)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':user_type' => $user_type,
            ':first_name' => $first_name,
            ':last_name' => $last_name,
            ':email' => $email,
            ':phone' => $phone,
            ':password' => $hashed_password
        ]);

        $user_id = $pdo->lastInsertId();

        // Handle Patient user type
        if ($user_type === 'Patient') {
            $age = intval($_POST['age']);
            $gender = $_POST['gender'];
            $pconsent = isset($_POST['patient_consent']) ? 1 : 0; // Convert to integer

            // Validate age
            if ($age < 0 || $age > 120) {
                echo "Please enter a valid age.";
                exit();
            }

            $sql = "INSERT INTO patients (user_id, age, gender, consent_data) 
                    VALUES (:user_id, :age, :gender, :consent)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([
                ':user_id' => $user_id,
                ':age' => $age,
                ':gender' => $gender,
                ':consent' => $pconsent
            ]);
        } elseif ($user_type === 'Clinician') {
            $specialization = trim($_POST['specialization'] ?? null);
            $years_experience = intval($_POST['years_of_experience'] ?? 0);
            $institution = trim($_POST['establishment'] ?? null);
            $consent = isset($_POST['consent_data']) ? 1 : 0; // Convert to integer

            // Handle file upload
            if ($_FILES['certification']['error'] === UPLOAD_ERR_NO_FILE) {
                echo "No file uploaded for certification.";
                exit();
            } elseif ($_FILES['certification']['error'] !== UPLOAD_ERR_OK) {
                echo "File upload error: " . $_FILES['certification']['error'];
                exit();
            } else {
                $upload_dir = 'uploads/';
                if (!is_dir($upload_dir)) {
                    mkdir($upload_dir, 0777, true);
                }

                $certification = basename($_FILES['certification']['name']);
                $certification = preg_replace("/[^a-zA-Z0-9\._-]/", "", $certification); // Sanitize file name
                $upload_file = $upload_dir . $certification;

                // Validate file type
                $allowed_types = ['pdf', 'jpg', 'jpeg', 'png'];
                $file_ext = strtolower(pathinfo($certification, PATHINFO_EXTENSION));
                if (!in_array($file_ext, $allowed_types)) {
                    echo "Invalid file type. Allowed types: " . implode(", ", $allowed_types);
                    exit();
                }

                // Validate file size (max 2MB)
                if ($_FILES['certification']['size'] > 2 * 1024 * 1024) {
                    echo "File size exceeds the 2MB limit.";
                    exit();
                }

                // Move the uploaded file
                if (!move_uploaded_file($_FILES['certification']['tmp_name'], $upload_file)) {
                    throw new Exception("Failed to upload the certification file.");
                }

                // Insert into clinicians table
                $sql = "INSERT INTO clinicians (user_id, certification, specialty, years_experience, institution, consent_data)
                        VALUES (:user_id, :certification, :specialty, :years_experience, :institution, :consent)";
                $stmt = $pdo->prepare($sql);
                $stmt->execute([
                    ':user_id' => $user_id,
                    ':certification' => $upload_file,
                    ':specialty' => $specialization,
                    ':years_experience' => $years_experience,
                    ':institution' => $institution,
                    ':consent' => $consent
                ]);
            }
        }

        // Redirect on success
        header('Location: chatbot.html?done');
    } catch (Exception $e) {
        echo "Erreur : " . $e->getMessage();
    }
}
