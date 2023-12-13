<?php
    include_once "../../config/db_connect.php";
    
    $d_id=$_POST['record'];
    $query="DELETE FROM disease where dis_id='$d_id'";

    $data=mysqli_query($conn,$query);

    if($data){
        echo"Corn Data Deleted";
    }
    else{
        echo"Not able to delete corn data";
    }
    
?>