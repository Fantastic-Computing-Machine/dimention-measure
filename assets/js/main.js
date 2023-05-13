console.log("main.js loaded");

$(document).ready(function() {
    document.getElementById("dimentionCheck").checked = true;
    
    $("#estimateCheck").click(function() {
        document.getElementById("dimentionCheck").checked = false;
        document.getElementById("estimateCheck").checked = true;
    });

    $("#dimentionCheck").click(function() {
        document.getElementById("estimateCheck").checked = false;
        document.getElementById("dimentionCheck").checked = true;
    });

    $(document).on('click', '.result-item', function() {
        var projectUrl = $(this).data('url');
        var absoluteUrl = window.location.origin + projectUrl; // Append at the domain level

        window.location.href = absoluteUrl;
    });

    $('#searchForm').submit(function(e) {
      e.preventDefault();
      var formData = $(this).serialize();

    //   check if the formData contains the dimentionCheck the add type=dimentions
      if (document.getElementById("dimentionCheck").checked == true) {
        formData = formData + "&type=dimension";
      }
      else if (document.getElementById("estimateCheck").checked == true) {
        formData = formData + "&type=estimate";
      }

      // Send the AJAX request
    var startTime = new Date().getTime();
    $.ajax({
        type: 'POST',
        url: '/search',
        data: formData,
        success: function(response) {
          if (response.success) {
            var endTime = new Date().getTime();
            var duration = (endTime - startTime) / 1000; 
            if(response.results.length == 0){
                $('#searchResults').html('No results found.');
            }
            else{
            var resultsHtml = '<div class = "fw-light">About '+response.results.length +' results ('+duration+'seconds)</div><div class="list-group">';
            for (var i = 0; i < response.results.length; i++) {
              var result = response.results[i];
              var resultHtml = '<a href="'+result.url+'" class="list-group-item list-group-item-action"><span m-1>'+result.title+
              '<span class="badge bg-primary rounded-pill float-end">'+result.created_on+'</span></span></a>';
              resultsHtml += resultHtml;
            }
            resultsHtml += '</div>';
            $('#searchResults').html(resultsHtml);
            }

            // Display the search results on the page
          } else {
            // Display a message if no results found
            $('#searchResults').html('<p>No results found.</p>');
          }
        },
        error: function() {
          console.log('Error occurred');
        }
      });
    });
  });

function mtr_ft() {
    // Unit conversion meter to feet
    var len = parseFloat(document.getElementById("mt").value);
    if (isNaN(len)) { len = 0; }
    document.getElementById("ft").value = len * 3.28;
}

function ft_mtr() {
    // Unit conversion feet to meter
    var len = parseFloat(document.getElementById("ft").value);
    if (isNaN(len)) { len = 0; }
    document.getElementById("mt").value = len * 0.3048;
}

function sqmtr_sqft() {
    // Unit conversion sq. meter to sq. feet
    var area = parseFloat(document.getElementById("calc_sqmt").value);
    if (isNaN(area)) { area = 0; }
    document.getElementById("calc_sqft").value = area * 10.764;
}

function sqft_sqmtr() {
    // Unit conversion sq. feet to sq. meter
    var area = parseFloat(document.getElementById("calc_sqft").value);
    if (isNaN(area)) { area = 0; }
    document.getElementById("calc_sqmt").value = area * 0.092903;
}

$(document).ready(function () {
    $(".delete_button").hover(function () {
        $(this).children('img').attr('src', 'https://img.icons8.com/ios/50/000000/delete-forever--v2.gif');

    }, function () {
        $(this).children('img').attr("src", "https://img.icons8.com/ios/50/000000/delete-forever--v2.png");


    });
});

$(document).ready(function () {
    $(".setting").hover(function () {
        $(this).children('img').attr('src', 'https://img.icons8.com/ios/28/000000/settings--v2.gif');

    }, function () {
        $(this).children('img').attr("src", "https://img.icons8.com/ios/28/000000/settings--v2.png");


    });
});

// Dynamically change the year in the footer
document.getElementById("current_year").innerHTML = new Date().getFullYear();



$(document).ready(function () {
    $("#id_discount").on('input', function () {
        if ($(this).val() < 0 || $(this).val() > 100) {
            $('#DiscountError').prop('hidden', false);
            $('#discountChangeSubmit').prop('disabled', true);
        }
        else {
            $('#DiscountError').prop('hidden', true);
            $('#discountChangeSubmit').prop('disabled', false);
        }
    });
});

function enableNewitemPage() {
    console.log("enableNewitemPage2");
    document.getElementById('flexRadioDefault1').disabled = false;
    document.getElementById('id_length').disabled = false;
    document.getElementById('id_width').disabled = false;
    document.getElementById('flexRadioDefault2').disabled = false;
    document.getElementById('forQuantity').disabled = false;
    document.getElementById('id_discount').disabled = false;
    document.getElementById('id_rate').disabled = false;
    document.getElementById('id_unit').disabled = false;
    document.getElementById('id_room').disabled = false;
    document.getElementById('id_room_item').disabled = false;
    document.getElementById('id_room_item_description').disabled = false;
    document.getElementById('form_submit_button').disabled = false;
}

$(document).ready(function () {
    $("#edit_update_estimate").click(function () {
        var Q1 = $("#forQuantity").val();
        var Q2 = $("#id_length").val();
        var Q3 = $("#id_width").val();
        if (Q1 != undefined && Q1 != "") {
            $('#flexRadioDefault2').prop('checked', true);
            $('#flexRadioDefault1').prop('checked', false);
            $('#flexRadioDefault1').prop('disable', true);
            $('#id_length').prop('disabled', true);
            $('#id_width').prop('disabled', true);
            $('#sqm_box').prop('hidden', true);
            $('#sqft_box').prop('hidden', true);
            // this is comment

        }
        else {
            console.log("for area");
            $('#flexRadioDefault2').prop('disable', true);
            $('#flexRadioDefault1').prop('checked', true);
            $('#flexRadioDefault2').prop('checked', false);
            $('#forQuantity').prop('disabled', true);
        }
    });
});

$(document).ready(function () {
    $('.checkboxSelector').change(function () {
        if ($('.checkboxSelector:checked').length) {
            $('#delete_button').prop('disabled', false);
        } else {
            $('#delete_button').prop('disabled', true);
        }
    });
});



// document.onkeydown = function (e) {
//     if (event.keyCode == 123) {
//         return false;
//     }
//     if (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
//         return false;
//     }
//     if (e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
//         return false;
//     }
//     if (e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
//         return false;
//     }
// }
