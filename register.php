<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = $_POST['name'];
    $password = $_POST['password'];

    if (!empty($name) && !empty($password)) {
        $user = $name . ':' . $password . "\n";
        file_put_contents('users.txt', $user, FILE_APPEND | LOCK_EX);
        echo 'User registered successfully.';
    } else {
        echo 'Please fill in all fields.';
    }
}
?>
