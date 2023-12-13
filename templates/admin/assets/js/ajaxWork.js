function showUser() {
    $.ajax({
        url: "./controller/show_user.html",
        method: "post",
        data: { record: 1 },
        success: function (data) {
            $('.allContent-section').html(data);
        }
    });
}

//show pest data 
function showPestData() {

    $.ajax({
        url: "./controller/showPestData.php",
        method: "post",
        data: { record: 1 },
        success: function (data) {
            console.log('AJAX success callback:', data);
            // Close the modal and remove modal-open class
            $('#myModal').modal('hide');
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
            $('.allContent-section').html(data);
        }
    });
}

function showDiseaseData() {

    $.ajax({
        url: "./controller/showDiseaseData.php",
        method: "post",
        data: { record: 1 },
        success: function (data) {
            console.log('AJAX success callback:', data);
            // Close the modal and remove modal-open class
            $('#myModal').modal('hide');
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
            $('.allContent-section').html(data);
        }
    });
}

//edit form for Pest
function editPestForm(id) {
    $.ajax({
        url: "./controller/editPestForm.php",
        method: "post",
        data: { record: id },
        success: function (data) {
            $('.allContent-section').html(data);
        }
    });
}

function editDiseaseForm(id) {
    $.ajax({
        url: "./controller/editDiseaseForm.php",
        method: "post",
        data: { record: id },
        success: function (data) {
            $('.allContent-section').html(data);
        }
    });
}

//delete pest data
function pestDelete(id) {
    $.ajax({
        url: "./controller/deletePest.php",
        method: "post",
        data: { record: id },
        success: function (data) {
            alert('Pest Data Successfully deleted');
            $('form').trigger('reset');
            showPestData();
        }
    });
}

function diseaseDelete(id) {
    $.ajax({
        url: "./controller/deleteCornDisease.php",
        method: "post",
        data: { record: id },
        success: function (data) {
            alert('Corn Disease Data Successfully deleted');
            $('form').trigger('reset');
            showDiseaseData();
        }
    });
}

//update Pest data
function updatePest() {
    var pest_id = $('#pest_id').val();
    var pest_name = $('#pest_name').val();
    var life_cycle = $('#life_cycle').val();
    var pest_damage = $('#pest_damage').val();
    var pest_control = $('#pest_control').val();
    var existingImage = $('#existingImage').val();
    var new_Image = $('#new_Image')[0].files[0];

    var fd = new FormData();
    fd.append('pest_id', pest_id);
    fd.append('pest_name', pest_name);
    fd.append('life_cycle', life_cycle);
    fd.append('pest_damage', pest_damage);
    fd.append('pest_control', pest_control);
    fd.append('existingImage', existingImage);

    if (new_Image) {
        fd.append('new_Image', new_Image);
    }

    $.ajax({
        url: './controller/updatePest.php',
        method: 'post',
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('Pest Data Update Success.');
            $('form').trigger('reset');
            showPestData();
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}

function updateCornDisease() {
    var dis_id = $('#dis_id').val();
    var dis_name = $('#dis_name').val();
    var dis_symptoms = $('#dis_symptoms').val();
    var dis_stage = $('#dis_stage').val();
    var dis_alt_host = $('#dis_alt_host').val();
    var dis_mgmt = $('#dis_mgmt').val();
    var existingImage = $('#existingImage').val();
    var new_Image = $('#new_Image')[0].files[0];

    var fd = new FormData();
    fd.append('dis_id', dis_id);
    fd.append('dis_name', dis_name);
    fd.append('dis_symptoms', dis_symptoms);
    fd.append('dis_stage', dis_stage);
    fd.append('dis_alt_host', dis_alt_host);
    fd.append('dis_mgmt', dis_mgmt);
    fd.append('existingImage', existingImage);

    if (new_Image) {
        fd.append('new_Image', new_Image);
    }

    $.ajax({
        url: './controller/updateCornDisease.php',
        method: 'post',
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('Corn Disease Data Update Success.');
            $('form').trigger('reset');
            showDiseaseData();
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}

//add Pest data
function addPest() {

    var pest_name = $('#pest_name').val();
    var life_cycle = $('#life_cycle').val();
    var pest_damage = $('#pest_damage').val();
    var pest_control = $('#pest_control').val();
    var upload = $('#upload').val();
    var file = $('#file')[0].files[0];

    var fd = new FormData();
    fd.append('pest_name', pest_name);
    fd.append('life_cycle', life_cycle);
    fd.append('pest_damage', pest_damage);
    fd.append('pest_control', pest_control);
    fd.append('file', file);
    fd.append('upload', upload);

    $.ajax({
        url: "./controller/addPest.php",
        method: "post",
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('New Pest Data Added successfully.');
            $('form').trigger('reset');
            showPestData();
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}

function addCornDisease() {

    var dis_name = $('#dis_name').val();
    var dis_symptoms = $('#dis_symptoms').val();
    var dis_stage = $('#dis_stage').val();
    var dis_alt_host = $('#dis_alt_host').val();
    var dis_mgmt = $('#dis_mgmt').val();
    var upload = $('#upload').val();
    var file = $('#file')[0].files[0];

    var fd = new FormData();
    fd.append('dis_name', dis_name);
    fd.append('dis_symptoms', dis_symptoms);
    fd.append('dis_stage', dis_stage);
    fd.append('dis_alt_host', dis_alt_host);
    fd.append('dis_mgmt', dis_mgmt);
    fd.append('file', file);
    fd.append('upload', upload);

    $.ajax({
        url: "./controller/addCornDisease.php",
        method: "post",
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
            alert('New Corn Disease Data Added successfully.');
            $('form').trigger('reset');
            showDiseaseData();
        },
        error: function (xhr, status, error) {
            console.error(xhr.responseText);
        }
    });
}
