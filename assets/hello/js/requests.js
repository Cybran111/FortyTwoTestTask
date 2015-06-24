/**
 * Created by cybran on 6/19/15.
 */
$( document ).ready(function() {

    var initialTitle = document.title;
    var updateInterval = 5000;
    var isActive;
    var clonedRequestRow = $(".request").last().clone();
    var last_id = $(clonedRequestRow).attr('id');
    var missedRequests = 0
    var newRow, newDom;

    window.onfocus = function () {
        isActive = true;
        document.title = initialTitle;
        missedRequests = 0;
    };

    window.onblur = function () {
        isActive = false;
    };

    function updateTable () {
        $.getJSON("list/", {"last_id": last_id}, function (data) {

            if (data.length != 0) {
                if (!isActive) {
                    missedRequests = missedRequests + data[data.length - 1].pk - last_id;
                    document.title = "(" + missedRequests + ") " + initialTitle;
                }
                last_id = data[data.length-1].pk;
            }
            $.each(data, function (key, value) {
                    newRow = clonedRequestRow.clone();
                    newDom = $(newRow).get(0);

                    $(newDom).find(".request-createdat").text(
                        moment.utc(value.fields.created_at).format('MMMM D, YYYY, hh:mm a')
                    );
                    $(newDom).find(".request-method").text(value.fields.method);
                    $(newDom).find(".request-path").text(value.fields.path);
                    $(newRow).attr('id', value.pk);

                    $(".table").append(newRow);
            });

        })
    }

    updateTable();
    setInterval(updateTable, updateInterval);

});