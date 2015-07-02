/**
 * Created by cybran on 6/24/15.
 */

$(document).ready(function () {

    var Base64 = {

        _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",

        _utf8_encode: function (string) {
            string = string.replace(/\r\n/g, "\n");
            var utftext = "";

            for (var n = 0; n < string.length; n++) {

                var c = string.charCodeAt(n);

                if (c < 128) {
                    utftext += String.fromCharCode(c);
                }
                else if ((c > 127) && (c < 2048)) {
                    utftext += String.fromCharCode((c >> 6) | 192);
                    utftext += String.fromCharCode((c & 63) | 128);
                }
                else {
                    utftext += String.fromCharCode((c >> 12) | 224);
                    utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                    utftext += String.fromCharCode((c & 63) | 128);
                }

            }

            return utftext;
        }
    };

    function removeErrors() {
        $(".error").remove();
        $(".bg-danger").removeClass("bg-danger")
    }

    function showErrors(errors){
        parsed_errors = $.parseJSON(errors.responseText);

        $.each(parsed_errors, function(field, error) {

            var parent = $( "#id_"+field).parent();
            parent.addClass("bg-danger");
            parent.prepend("<p class='error'>" + error +"</p>");
        })


    }

    var bar = $('#progress-bar');
    var percent = $('#percent');
    var status = $('#form-status');
    var progressWrap = $("#progress-wrap");
    var editform = $('#editform');

    function startUpload() {
        var csrftoken = data["csrfmiddlewaretoken"];

        data["photo"] = typeof photo === 'undefined' ? "" : Base64._utf8_encode(fr.result) ;

        $.ajax({
            url: "",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",

            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                editform.find(':input:not(:disabled)').prop('disabled', true);
                progressWrap.removeClass("hidden");
                var percentVal = '0%';
                bar.width(percentVal);
                percent.html(percentVal);
            },

            uploadProgress: function (event, position, total, percentComplete) {
                var percentVal = percentComplete + '%';
                bar.width(percentVal);
                percent.html(percentVal);
            },

            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function (evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = evt.loaded / evt.total;
                        percentComplete = parseInt(percentComplete * 100);
                        var percentVal = percentComplete + '%';
                        bar.width(percentVal);
                        percent.html(percentVal);
                    }
                }, false);

                return xhr;
            },
            complete: function () {
                var percentVal = '100%';
                bar.width(percentVal);
                percent.html(percentVal);
                editform.find(':input:disabled').prop('disabled', false);
                status.removeClass("hidden");
            },

            success: function () {
                removeErrors();
                status.text("Changes have been saved");
            },

            error: function(errors) {
                removeErrors();
                status.text("Error! Changes haven't been saved");
                showErrors(errors);
            }

        });
    }

    $('#id_birth_date').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true
    });

    $(editform).submit(function (event) {
        event.preventDefault();
        data = {};
        $.each(editform.find(':input[name]:not([name=photo])'), function (number, el) {
            data[$(el).attr("name")] = $(el).val();
        });
        photo = editform.find(':input[name=photo]')[0].files[0];
        if (photo) {
            fr = new FileReader();
            fr.onload = startUpload;
            fr.readAsDataURL(photo);
        } else {
            startUpload(true)
        }
    });

});