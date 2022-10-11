$(document).ready(function () {

  (function ($) {
    "use strict";


    jQuery.validator.addMethod('answercheck', function (value, element) {
      return this.optional(element) || /^\bcat\b$/.test(value)
    }, "type the correct answer -_-");

    // validate contactForm form
    $(function () {
      $('#contactForm').validate({
        rules: {
          name: {
            required: true,
            minlength: 2
          },
          subject: {
            required: true,
            minlength: 4
          },
          number: {
            required: true,
            minlength: 5
          },
          email: {
            required: true,
            email: true
          },
          message: {
            required: true,
            minlength: 20
          }
        },
        messages: {
          name: {
            required: "come on, you have a name, don't you?",
            minlength: "your name must consist of at least 2 characters"
          },
          subject: {
            required: "come on, you have a subject, don't you?",
            minlength: "your subject must consist of at least 4 characters"
          },
          number: {
            required: "come on, you have a number, don't you?",
            minlength: "your Number must consist of at least 5 characters"
          },
          email: {
            required: "no email, no message"
          },
          message: {
            required: "um...yea, you have to write something to send this form.",
            minlength: "thats all? really?"
          }
        },
        submitHandler: function (form) {
          $(form).ajaxSubmit({
            type: "POST",
            data: $(form).serialize(),
            url: "/contact/",
            success: function (response) {
              $("#contact_form_message").append(
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