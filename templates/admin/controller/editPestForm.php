<div class="container p-5">

    <h4>Edit Pest Data</h4>
    <?php
    include_once "../../config/db_connect.php";
    $ID = $_POST['record'];
    $qry = mysqli_query($conn, "SELECT * FROM pest WHERE pest_id='$ID'");
    $numberOfRow = mysqli_num_rows($qry);
    if ($numberOfRow > 0) {
        while ($row1 = mysqli_fetch_array($qry)) {
            // $catID=$row1["category_id"];
            ?>
            <form id="update-Items" onsubmit="updatePest()" enctype='multipart/form-data'>

                <div class="form-group">
                    <input type="text" class="form-control" id="pest_id" value="<?= $row1['pest_id'] ?>" hidden>
                </div>

                <div class="form-group">
                    <label for="pest_name">Pest Name:</label>
                    <input type="text" class="form-control" id="pest_name" value="<?= $row1['pest_name'] ?>">
                </div>

                <div class="form-group">
                    <label for="life_cycle">Pest Life Cycle:</label>
                    <input type="text" class="form-control" id="life_cycle" value="<?= $row1['life_cycle'] ?>">
                </div>

                <div class="form-group">
                    <label for="pest_damage">Pest Damage:</label>
                    <input type="text" class="form-control" id="pest_damage" value="<?= $row1['pest_damage'] ?>">
                </div>

                <div class="form-group">
                    <label for="pest_control">Pest Control:</label>
                    <input type="text" class="form-control" id="pest_control" value="<?= $row1['pest_control'] ?>">
                </div>

                <div class="form-group">
                    <img width='200px' height='150px' src='<?= str_replace('C:/xampp/htdocs', 'http://localhost', $row1["pest_photo"]) ?>'>
                    <div>
                        <label for="file">Choose Image:</label>
                        <input type="text" id="existingImage" class="form-control" value="<?= $row1['pest_photo'] ?>" hidden>
                        <input type="file" id="new_Image" value="">
                    </div>
                </div>

                <div class="form-group">
                    <button type="submit" style="height:40px" class="btn btn-primary">Update Pest Data</button>
                </div>
                <?php
            }
        }
        ?>
    </form>

</div>
