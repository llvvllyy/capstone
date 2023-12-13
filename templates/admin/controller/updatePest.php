<?php
include_once "../../config/db_connect.php";

$pest_id = $_POST['pest_id'];
$pest_name = $_POST['pest_name'];
$life_cycle = $_POST['life_cycle'];
$pest_damage = $_POST['pest_damage'];
$pest_control = $_POST['pest_control'];

if (isset($_FILES['new_Image']) && $_FILES['new_Image']['error'] == 0) {
    $location = "./upload/";
    $img = $_FILES['new_Image']['name'];
    $tmp = $_FILES['new_Image']['tmp_name'];
    $dir = '../upload/';
    $ext = strtolower(pathinfo($img, PATHINFO_EXTENSION));
    $valid_extensions = array('jpeg', 'jpg', 'png', 'gif', 'webp');
    $image = rand(1000, 1000000) . "." . $ext;
    $final_image = $location . $image;

    if (in_array($ext, $valid_extensions)) {
        move_uploaded_file($tmp, $dir . $image);

        // Update the database record with the new file path
        $updateItem = mysqli_query($conn, "UPDATE pest SET 
            pest_name='$pest_name', 
            life_cycle='$life_cycle', 
            pest_damage='$pest_damage',
            pest_control='$pest_control',
            pest_photo='$final_image' 
            WHERE pest_id=$pest_id");

        if ($updateItem) {
            echo "true";
        } else {
            echo mysqli_error($conn);
        }
    } else {
        echo "Invalid file format";
    }
} else {
    // If no new image is provided, update only text fields
    $updateItem = mysqli_query($conn, "UPDATE pest SET 
        pest_name='$pest_name', 
        life_cycle='$life_cycle', 
        pest_damage='$pest_damage',
        pest_control='$pest_control' 
        WHERE pest_id=$pest_id");

    if ($updateItem) {
        echo "true";
    } else {
        echo mysqli_error($conn);
    }
}
?>
