<?php
include_once "../../config/db_connect.php";

$dis_id = $_POST['dis_id'];
$dis_name = $_POST['dis_name'];
$dis_symptoms = $_POST['dis_symptoms'];
$dis_stage = $_POST['dis_stage'];
$dis_alt_host = $_POST['dis_alt_host'];
$dis_mgmt = $_POST['dis_mgmt'];

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
        $updateItem = mysqli_query($conn, "UPDATE disease SET 
            dis_name='$dis_name', 
            dis_symptoms='$dis_symptoms', 
            dis_stage='$dis_stage',
            dis_alt_host='$dis_alt_host',
            dis_mgmt='$dis_mgmt',
            dis_photo='$final_image' 
            WHERE dis_id=$dis_id");

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
    $updateItem = mysqli_query($conn, "UPDATE disease SET 
        dis_name='$dis_name', 
        dis_symptoms='$dis_symptoms', 
        dis_stage='$dis_stage',
        dis_alt_host='$dis_alt_host', 
        dis_mgmt='$dis_mgmt' 
        WHERE pest_id=$pest_id");

    if ($updateItem) {
        echo "true";
    } else {
        echo mysqli_error($conn);
    }
}
?>
