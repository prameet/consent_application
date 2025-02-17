<!-- JavaScript to show/hide input field -->
    if (document.getElementById('otherOption')) {
        document.getElementById('otherOption').addEventListener('checked', toggleOtherInput)
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
                location.reload();
            });
        }, 5000);
    }

    function toggleOtherInput() {
        let checkBox = document.getElementById("otherOption");
        let textInput = document.getElementById("otherInput");
        if (textInput.classList.contains('d-none')) {
            textInput.classList.remove('d-none');

        } else {
            textInput.classList.add('d-none');
        }
    }



    function validateCheckboxes() {
        let checkboxes = document.querySelectorAll('input[name="services[]"]');
        let errorMessage = document.getElementById('checkboxError');

        let checked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (!checked) {
            errorMessage.classList.remove('d-none'); // Show error message
            return false; // Prevent form submission
        }

        errorMessage.classList.add('d-none'); // Hide error message if valid
        return true; // Allow form submission
    }
    function generateServiceCode() {
        let application = document.getElementById("application").value;
        if (application) {
            let timestamp = Date.now().toString().slice(-6); // Get last 6 digits of timestamp
            let serviceCode = application.toUpperCase().substring(0, 6) + "-" + timestamp;
            document.getElementById("service_code").value = serviceCode;
        } else {
            document.getElementById("service_code").value = ""; // Reset if no selection
        }
    }
    $(document).ready(function() {
        function getCSRFToken() {
            return $('input[name="csrfmiddlewaretoken"]').val();
        }
        $('#consent-form').submit(function(e) {
            e.preventDefault();
            // Validate checkboxes before submission
            if (!validateCheckboxes()) {
                return; // Stop form submission if validation fails
            }
            var formData = new FormData(this);
            $.ajax({
//                url: "{% url 'consent_form:create_consent_form' %}",
                url: "/consent_form/create/",
                type: "POST",
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    "X-CSRFToken": getCSRFToken() ,// Include CSRF token
                },
                success: function(response) {
                    if (response.status === "success") {

                        $('#new_consent_form_request_modal').modal('hide');  // Hide modal

                        // Show success alert
                        showAlert("Consent Form submitted successfully!", "success");

                        // Remove the deleted row from table (if applicable)
                        $("#row-" + consentFormId).fadeOut();

                        // Optional: Reload the page after 1 seconds
                        setTimeout(function () {
                            location.reload();
                        }, 1000);

                    } else {
                         showAlert("Error submitting consent form. Please try again.", "danger");
                    }
                },
                error: function(xhr, status, error) {
                    $('#message').html("<p style='color: red;'>An error occurred: " + error + "</p>");
                }
            });

        });
    });