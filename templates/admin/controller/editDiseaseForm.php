<div class="container p-5">
    <h4>Edit Corn Disease Data</h4>

    <?php
        include_once "../../config/db_connect.php";
        $ID = $_POST['record'];
        $qry = mysqli_query($conn, "SELECT * FROM disease WHERE dis_id='$ID'");
        $numberOfRow = mysqli_num_rows($qry);
        if ($numberOfRow > 0) {
            while ($row1 = mysqli_fetch_array($qry)) {
    ?>

        <form id="update-Items" onsubmit="updateCornDisease()" enctype='multipart/form-data'>

            <div class="form-group">
                <input type="text" class="form-control" id="dis_id" value="<?= $row1['dis_id'] ?>" hidden>
            </div>

            <div class="form-group">
                <label for="dis_name">Corn Disease Name:</label>
                <input type="text" class="form-control" id="dis_name" value="<?= $row1['dis_name'] ?>">
            </div>

            <div class="form-group">
                <label for="dis_symptoms">Corn Disease Symptoms :</label>
                <input type="text" class="form-control" id="dis_symptoms" value="<?= $row1['dis_symptoms'] ?>">
            </div>

            <div class="form-group">
                <label for="dis_stage">Corn Disease Growth Stage:</label>
                <input type="text" class="form-control" id="dis_stage" value="<?= $row1['dis_stage'] ?>">
            </div>

            <div class="form-group">
                <label for="dis_alt_host">Corn Disease Alternative Host:</label>
                <input type="text" class="form-control" id="dis_alt_host" value="<?= $row1['dis_alt_host'] ?>">
            </div>

            <div class="form-group">
                <label for="dis_mgmt">Corn Disease Management:</label>
                <input type="text" class="form-control" id="dis_mgmt" value="<?= $row1['dis_mgmt'] ?>">
            </div>

            <div class="form-group">
                <img width='200px' height='150px' src='<?= str_replace('C:/xampp/htdocs', 'http://localhost', $row1["dis_photo"]) ?>'>
                <div>
                    <label for="file">Choose Image:</label>
                    <input type="text" id="existingImage" class="form-control" value="<?= $row1['dis_photo'] ?>" hidden>
                    <input type="file" id="new_Image" value="">
                </div>
            </div>

            <div class="form-group">
                <button type="submit" style="height:40px" class="btn btn-primary">Update Corn Disease Data</button>
            </div>
            
            <?php
                }
            }
            ?>
            
        </form>
</div>
