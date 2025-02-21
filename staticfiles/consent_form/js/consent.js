if (document.getElementById("otherOption")) {
    document
      .getElementById("otherOption")
      .addEventListener("checked", toggleOtherInput);
  }
  function showAlert(message, type = "success") {
    var alertHTML = `
              <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                  ${message}
                  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
              </div>
          `;
  
    $("#alert-container").append(alertHTML);
  
    // Auto-dismiss alert after 5 seconds
    setTimeout(function () {
      $(".alert").fadeOut("slow", function () {
        $(this).remove();
        // location.reload();
      });
    }, 5000);
  }
  
  function toggleOtherInput() {
    let checkBox = document.getElementById("otherOption");
    let textInput = document.getElementById("otherInput");
    if (textInput.classList.contains("d-none")) {
      textInput.classList.remove("d-none");
    } else {
      textInput.classList.add("d-none");
    }
  }
  
  // function validateCheckboxes() {
  //   let checkboxes = document.querySelectorAll('input[name="services[]"]');
  //   let errorMessage = document.getElementById("checkboxError");
  
  //   let checked = Array.from(checkboxes).some((checkbox) => checkbox.checked);
  
  //   if (!checked) {
  //     errorMessage.classList.remove("d-none"); // Show error message
  //     return false; // Prevent form submission
  //   }
  
  //   errorMessage.classList.add("d-none"); // Hide error message if valid
  //   return true; // Allow form submission
  // }
  function generateServiceCode() {
    let application = document.getElementById("application").value;
    if (application) {
      let timestamp = Date.now().toString().slice(-6); // Get last 6 digits of timestamp
      let serviceCode =
        application.toUpperCase().substring(0, 6) + "-" + timestamp;
      document.getElementById("service_code").value = serviceCode;
    } else {
      document.getElementById("service_code").value = ""; // Reset if no selection
    }
  }
  
  function getCSRFToken() {
    return $('input[name="csrfmiddlewaretoken"]').val();
  }
  $(document).on("click", ".delete-btn", function () {
    var consentFormId = $(this).data("id"); // Get the ID from the clicked button
    console.log("Consent Form ID:", consentFormId); // Debugging
  
    if (consentFormId) {
        $("#consentFormId").val(consentFormId); // Set the hidden input value
    } else {
        console.log("Error: No consentFormId found!");
    }
  });
  
  
  $(document).ready(function () {
    
    $("#consent-form").submit(function (e) {
      e.preventDefault();
      
      // Validate checkboxes before submission
      if (!validateCheckboxes()) {
        return; // Stop form submission if validation fails
      }
      var formData = new FormData(this);
      var dynamicURL = createConsentFormUrl;  
      $.ajax({
        url: dynamicURL,
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        headers: {
          "X-CSRFToken": getCSRFToken(), // Include CSRF token
        },
        success: function (response) {
          if (response.status === "success") {
            $("#new_consent_form_request_modal").modal("hide"); // Hide modal
            $("#new_consent_form_request_modal").on("hidden.bs.modal", function () {
              $("body").removeClass("modal-open").css("overflow", "auto"); 
              $(".modal-backdrop").remove();
            });
            
            $("#consent-form")[0].reset();
            $(".is-invalid").removeClass("is-invalid"); // Remove validation styles
            $(".invalid-feedback").remove(); // Remove old error messages
            showAlert("Consent Form submitted successfully!", "success");
            //$(".dashboard_services_box").load(window.location.href + " .dashboard_services_box");
            $(".dashboard_services_box").load(location.href + " .dashboard_services_box > *", function () {
              console.log("Div reloaded successfully!");
            });
          } else {
            showAlert(
              "Error submitting consent form. Please try again.",
              "danger"
            );
          }
        },
        error: function (xhr, status, error) {
          if (xhr.status === 400) {
            let errors = xhr.responseJSON.errors;
  
            $(".is-invalid").removeClass("is-invalid"); // Remove old validation
            $(".invalid-feedback").remove(); // Remove old error messages
  
            // Loop through errors and display them
            $.each(errors, function (field, message) {
                let input = $(`[name="${field}"]`);
  
                if (input.length > 0) {
                    input.addClass("is-invalid"); // Add Bootstrap validation class
  
                    // Append error message
                    if (input.next(".invalid-feedback").length === 0) {
                        input.after(`<div class="invalid-feedback">${message}</div>`);
                    }
                }
            });
  
            // Scroll to the first error field
            // $('html, body').animate({
            //     scrollTop: $(".is-invalid").first().offset().top - 100
            // }, 500);
          } else {
            showAlert("An unexpected error occurred. Please try again.", "danger");
          }
        },
      });
    });
  });
  
  
  
  
  
  
  