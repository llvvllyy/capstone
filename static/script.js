function showUser() {
    $.ajax({
        url: "/show_user",
        method: "post",
        data: { record: 1 },
        success: function (data) {
            $('.allContent-section').html(data);
        },
        error: function (xhr, status, error) {
            console.error('Error fetching user data:', xhr.responseText);
        }
    });
}

function deleteUser(button) {

    var userId = button.dataset.id || button.getAttribute('data-id');

    if (userId && confirm('Are you sure you want to delete this user?')) {
        $.ajax({
            url: '/delete_user/' + userId,
            method: 'POST',
            success: function (data) {
                alert(data.message);
                // Optionally, you can update the user list after deletion
                $('.allContent-section').html(data);
                showUser()
            },
            error: function (xhr, status, error) {
                alert('Error deleting user');
                console.error(xhr.responseText);
            }
        });
    }
}

// function showPest() {
//     $.ajax({
//         url: "/show_pest",
//         method: "post",
//         data: { record: 1 },
//         success: function (data) {
//             $('.allContent-section').html(data);
//         },
//         error: function (xhr, status, error) {
//             console.error('Error fetching user data:', xhr.responseText);
//         }
//     });
// }

function showPest() {
    $.ajax({
        url: "/show_pest",
        method: "post",
        data: { record: 1 },
        success: function (data) {
            // Check the received data
            console.log(data);

            // Update the content only if the data is not empty
            if (data.trim() !== '') {
                $('.allContent-section').html(data);
            } else {
                console.error('Received empty data from the server.');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error fetching pest data:', xhr.responseText);
        }
    });
}


function deletePest(button) {

    var pestId = button.dataset.id || button.getAttribute('data-id');

    if (pestId && confirm('Are you sure you want to delete this pest data?')) {
        $.ajax({
            url: '/delete_pest/' + pestId,
            method: 'POST',
            success: function (data) {
                alert(data.message);
                // Optionally, you can update the user list after deletion
                $('.allContent-section').html(data);
                showPest()
            },
            error: function (xhr, status, error) {
                alert('Error deleting user');
                console.error(xhr.responseText);
            }
        });
    }
}

function updatePest(element) {
    // Check if element is a button or an event
    var pestId;
    if (element instanceof HTMLElement) {
        pestId = $(element).data("id");
    } else {
        pestId = $(element.target).data("id");
    }

    // Ensure pestId is not null or undefined
    if (!pestId) {
        console.error("Error: Pest ID not found.");
        return;
    }

    // Fetch the pest details using an API endpoint
    $.getJSON(`/get_pest_details/${pestId}`)
        .done(function (data) {
            console.log("Pest details:", data);

            // Populate the form fields with the fetched data
            var modal = $("#updateModal");
            modal.find('input[name="pest_name"]').val(data.pest_name);
            modal.find('textarea[name="pest_damage"]').val(data.pest_damage);
            modal.find('textarea[name="pest_cycle"]').val(data.pest_cycle);
            modal.find('textarea[name="pest_control"]').val(data.pest_control);

            // Show the modal
            modal.modal("show");
        })
        .fail(function (error) {
            console.error("Error fetching pest details:", error);
        });
}
