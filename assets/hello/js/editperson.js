/**
 * Created by cybran on 6/24/15.
 */

$(document).ready(function () {

    var bar = $('#progress-bar');
    var percent = $('#percent');
    var status = $('#form-status');
    var progressWrap = $("#progress-wrap");
    var editform = $('#editform');
    var submit_button = editform.find(":input[type='submit']");
    console.log(submit_button);


    function startUpload() {
        var csrftoken = data["csrfmiddlewaretoken"];
        delete data["csrfmiddlewaretoken"];
        data["photo"] = btoa(fr.result);

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
            },

            success: function () {
                status.removeClass("hidden");
            }

        });
    }

    $('#id_birth_date').datepicker({
        format: "yyyy-mm-dd",
        autoclose: true
    });


    var data = {};
    $.each(editform.find(':input[name]:not([name=photo])'), function (number, el) {
        data[$(el).attr("name")] = $(el).val();
    });

    $(editform).submit(function (event) {
        event.preventDefault();


        file = editform.find(':input[name=photo]')[0].files[0];
        fr = new FileReader();
        fr.onload = startUpload;
        fr.readAsDataURL(file);
            //
        });
});