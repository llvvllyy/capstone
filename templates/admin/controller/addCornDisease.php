<?php
    include_once "../../config/db_connect.php";
    
    if(isset($_POST['upload']))
    {       
        echo "Reached here!"; // Add this line for debugging
        echo '<pre>';
        print_r($_POST);
        print_r($_FILES);
        echo '</pre>';
    

        $dis_name = $_POST['dis_name'];
        $dis_symptoms = $_POST['dis_symptoms'];
        $dis_stage = $_POST['dis_stage'];
        $dis_alt_host = $_POST['dis_alt_host'];
        $dis_mgmt = $_POST['dis_mgmt'];

       
        $name = $_FILES['file']['name'];
        $temp = $_FILES['file']['tmp_name'];
    
        $location="./upload/";
        $image=$location.$name;

        $target_dir="../upload/";
        $finalImage=$target_dir.$name;

        move_uploaded_file($temp,$finalImage);

        $insert = mysqli_query($conn, "INSERT INTO disease 
        (dis_name, dis_photo, dis_symptoms, dis_stage, dis_alt_host, dis_mgmt)
        VALUES ('$dis_name', '$image', '$dis_symptoms', '$dis_stage', '$dis_alt_hos', '$dis_mgmt')");

        if (!$insert) {
            echo mysqli_error($conn);
        } else {
            echo "Records added successfully.";
        }
    }  
?>
