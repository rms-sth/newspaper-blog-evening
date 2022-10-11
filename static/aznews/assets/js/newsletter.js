$(document).ready(function () {

  (function ($) {
    "use strict";


    jQuery.validator.addMethod('answercheck', function (value, element) {
      return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function () {
      $('#newsletterForm').validate({
        rules: {
          email: {
            required: true,
            email: true
          }
        },
        messages: {
          email: {
            required: "Email field is required"
          }
        },
        submitHandler: function (form) {
          $(form).ajaxSubmit({
            type: "POST",
            data: $(form).serialize(),
            url: "/newsletter/",
            success: function (response) {
              $("#newsletter_form_message").append(
                `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                  <strong>Contact form was submitted successfully. We will contact you soon.</strong>
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>  
                `
              );
              $(form).trigger("reset");
              setTimeout(function () {
                // closing bootstrap alert message after 5000 millisecond
                $('.alert').alert('close');
              }, 5000);
            },
            error: function (response) {
              $("#contact_form_message").append(
                `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                  <strong>Something went wrong. Please make sure all fields are valid.</strong>
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>  
                `
              );
              setTimeout(function () {
                // closing bootstrap alert message after 5000 millisecond
                $('.alert').alert('close');
              }, 5000);
            }
          })
        }
      })
    })

  })(jQuery)
})