<div >
  <h2>Corn Diseases</h2>
  <table class="table ">
    <thead>
      <tr>
        <th class="text-center">S.N.</th>
        <th class="text-center">Corn Disease Image</th>
        <th class="text-center">Corn Disease Name</th>
        <th class="text-center">Corn Disease Symptoms</th>
        <th class="text-center">Corn Disease Growth Stage</th>
        <th class="text-center">Corn Disease Alternative Host</th>
        <th class="text-center">Corn Disease Management</th>
        <th class="text-center" colspan="2">Action</th>
      </tr>
    </thead>

      <?php
        include_once '../../config/db_connect.php';
        $sql = "SELECT * from disease";
        $result = $conn-> query($sql);
        $count = 1;
        if ($result->num_rows > 0) {
          while ($row = $result->fetch_assoc()) {
            $imagePath = str_replace('C:/xampp/htdocs', 'http://localhost', $row["dis_photo"]);
      ?>

    <tr>
      <td><?=$count?></td>
      <td><img height='60px' src='<?= $imagePath ?>'></td>
      <td><?=$row["dis_name"]?></td>
      <td><?=$row["dis_symptoms"]?></td>      
      <td><?=$row["dis_stage"]?></td> 
      <td><?=$row["dis_alt_host"]?></td>  
      <td><?=$row["dis_mgmt"]?></td>       
      <td><button class="btn btn-primary" style="height:20px font-size: 11px;" onclick="editDiseaseForm('<?=$row['dis_id']?>')">Edit</button></td>
      <td><button class="btn btn-danger" style="height:20px font-size: 11px;" onclick="diseaseDelete('<?=$row['dis_id']?>')">Delete</button></td>
      </tr>
      <?php
            $count=$count+1;
          }
        }
      ?>
  </table>

  <!-- Trigger the modal with a button -->
  <button type="button" class="btn btn-secondary " style="height:40px" data-toggle="modal" data-target="#myModal">
    Add New Corn Disease Data
  </button>

  <!-- Modal -->
  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog">
    
      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title">New Corn Disease Data</h4>
          <button type="button" class="close" data-dismiss="modal">&times;</button>
        </div>
        <div class="modal-body">
          <form enctype='multipart/form-data' method="POST">
            
            <div class="form-group">
              <label for="dis_name">Corn Disease Name:</label>
              <input type="text" class="form-control" id="dis_name" required>
            </div>

            <div class="form-group">
              <label for="dis_symptoms">Corn Disease Symptoms</label>
              <input type="text" class="form-control" id="dis_symptoms" required>
            </div>

            <div class="form-group">
              <label for="dis_stage">Corn Disease Growth Stage</label>
              <input type="text" class="form-control" id="dis_stage" required>
            </div>

            <div class="form-group">
              <label for="dis_alt_host">Corn Disease Alternative Host</label>
              <input type="text" class="form-control" id="dis_alt_host" required>
            </div>

            <div class="form-group">
              <label for="dis_mgmt">Corn Disease Management</label>
              <input type="text" class="form-control" id="dis_mgmt" required>
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
        addCornDisease();
    });
});


</script>