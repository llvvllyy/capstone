<div>
  <h2>Corn Pests</h2>
  <table class="table ">
    <thead>
      <tr>
        <th class="text-center">S.N.</th>
        <th class="text-center">Pest/Insect Image</th>
        <th class="text-center">Pest Name</th>
        <th class="text-center">Pest Life Cycle</th>
        <th class="text-center">Pest Damage</th>
        <th class="text-center">Pest Control</th>
        <th class="text-center" colspan="2">Action</th>
      </tr>
    </thead>
    <?php
      include_once '../../config/db_connect.php';
      $sql = "SELECT * from pest";
      $result = $conn-> query($sql);
      $count = 1;
      if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
          // Convert local file path to URL
          $imagePath = str_replace('C:/xampp/htdocs', 'http://localhost', $row["pest_photo"]);
      // if ($result-> num_rows > 0){
      //   while ($row=$result-> fetch_assoc()) {
    ?>
    <tr>
      <td><?=$count?></td>
      <!-- <td><img height='100px' src='http://localhost/DSS/admin/upload/17.png'></td> -->
      <td><img height='60px' src='<?= $imagePath ?>'></td>
      <td><?=$row["pest_name"]?></td>
      <td><?=$row["life_cycle"]?></td>      
      <td><?=$row["pest_damage"]?></td> 
      <td><?=$row["pest_control"]?></td>     
      <td><button class="btn btn-primary" style="height:20px font-size: 11px;" onclick="editPestForm('<?=$row['pest_id']?>')">Edit</button></td>
      <td><button class="btn btn-danger" style="height:20px font-size: 11px;" onclick="pestDelete('<?=$row['pest_id']?>')">Delete</button></td>
      </tr>
      <?php
            $count=$count+1;
          }
        }
      ?>
  </table>

  <!-- Trigger the modal with a button -->
  <button type="button" class="btn btn-secondary " style="height:40px" data-toggle="modal" data-target="#myModal">
    Add New Pest Data
  </button>

  <!-- Modal -->
  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">New Pest Data</h4>
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="modal-body">
          <form enctype='multipart/form-data' method="POST">
            
            <div class="form-group">
              <label for="pest_name">Pest Name:</label>
              <input type="text" class="form-control" id="pest_name" required>
            </div>

            <div class="form-group">
              <label for="life_cycle">Pest Life Cycle</label>
              <input type="text" class="form-control" id="life_cycle" required>
            </div>

            <div class="form-group">
              <label for="pest_damage">Pest Damage</label>
              <input type="text" class="form-control" id="pest_damage" required>
            </div>

            <div class="form-group">
              <label for="pest_control">Pest Control</label>
              <input type="text" class="form-control" id="pest_control" required>
            </div>


            <div class="form-group">
                <label for="file">Choose Image:</label>
                <input type="file" class="form-control-file" id="file">
            </div>

            <div class="form-group">
              <button type="submit" class="btn btn-secondary" id="upload" style="height:40px">Add New Data</button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<script>

$(document).ready(function() {
    $('form').submit(function(e) {
        e.preventDefault();
        addPest();
    });
});


</script>