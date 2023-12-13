<?php
    include_once "../../config/db_connect.php";
    
    $p_id=$_POST['record'];
    $query="DELETE FROM pest where pest_id='$p_id'";

    $data=mysqli_query($conn,$query);

    if($data){
        echo"Pest Data Deleted";
    }
    else{
        echo"Not able to delete pest data";
    }
    
?>