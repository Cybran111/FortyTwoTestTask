/**
 * Created by cybran on 6/19/15.
 */
$( document ).ready(function() {

    var initialTitle = document.title;
    var updateInterval = 5000;
    var isActive;
    var clonedRequestRow = $(".request").clone().first();
    var last_id = 0;
    var missedRequests = 0;

    window.onfocus = function () {
        isActive = true;
    };

    window.onblur = function () {
        isActive = false;
    };

    function updateTable () {
        $.getJSON("list/", {"last_id": last_id}, function (data) {
            missedRequests = missedRequests + data[0].pk - last_id;

            if (isActive) {
                document.title = initialTitle;
                missedRequests = 0;
            } else {
                if (missedRequests != 0) {
                    document.title = "(" + missedRequests +") " + initialTitle;
                }
            }
            last_id = data[0].pk;
            $.each(data, function (key, value) {

                    $(".request").last().remove();

                    newRow = clonedRequestRow.clone();
                    newDom = $(newRow).get(0);

                    $(newDom).find(".request-createdat").text(value.fields.created_at);
                    $(newDom).find(".request-method").text(value.fields.method);
                    $(newDom).find(".request-path").text(value.fields.path);

                    $(newRow).insertAfter("#table-header");
                }
            );
        })
    }

    updateTable();
    setInterval(updateTable, updateInterval);

});