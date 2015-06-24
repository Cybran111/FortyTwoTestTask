/**
 * Created by cybran on 6/24/15.
 */

$(document).ready(function () {

    var bar = $('#progress-bar');
    var percent = $('#percent');
    var status = $('#form-status');
    var progressWrap = $("#progress-wrap");
    var editform = $('#editform');

        $('#id_birth_date').datepicker({
             format: "yyyy-mm-dd",
             autoclose: true,
        });

    editform.ajaxForm({
        beforeSend: function () {
            editform.find(':input:not(:disabled)').prop('disabled',true);
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
        success: function () {
            var percentVal = '100%';
            bar.width(percentVal);
            percent.html(percentVal);
            status.removeClass("hidden");
            editform.find(':input:disabled').prop('disabled',false);
        }
    });
});