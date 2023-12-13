<?php
    include_once "../../config/db_connect.php";
    
    if(isset($_POST['upload']))
    {       
        echo "Reached here!"; // Add this line for debugging
        echo '<pre>';
        print_r($_POST);
        print_r($_FILES);
        echo '</pre>';
    

        $Pestname = $_POST['pest_name'];
        $life_cycle = $_POST['life_cycle'];
        $pest_damage = $_POST['pest_damage'];
        $pest_control = $_POST['pest_control'];

       
        $name = $_FILES['file']['name'];
        $temp = $_FILES['file']['tmp_name'];
    
        $location="./upload/";
        $image=$location.$name;

        $target_dir="../upload/";
        $finalImage=$target_dir.$name;

        move_uploaded_file($temp,$finalImage);

        $insert = mysqli_query($conn, "INSERT INTO pest 
        (pest_name, pest_photo, life_cycle, pest_damage, pest_control)
        VALUES ('$Pestname', '$image', '$life_cycle', '$pest_damage', '$pest_control')");
        // echo $insertQuery; // Add this line for debugging
        // $insert = mysqli_query($conn, $insertQuery);

        if (!$insert) {
            echo mysqli_error($conn);
        } else {
            echo "Records added successfully.";
        }
    }  
?>
