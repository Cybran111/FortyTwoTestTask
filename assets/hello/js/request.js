/**
 * Created by cybran on 6/19/15.
 */
$( document ).ready(function() {

    var initialTitle = document.title;
    var updateInterval = 5000;
    var isActive;
    var clonedRequestRow = $(".request").last().clone();
    var last_count = $(".request").length;
    var missedRequests = 0;
    var newRow, newDom;
    var position_table = {
        1: $(".request[priority='1']").first(),
        2: $(".request[priority='2']").first(),
        3: $(".request[priority='3']").first(),
        4: $(".request[priority='4']").first(),
        5: $(".request[priority='5']").first()
    };
    console.log(position_table);

    window.onfocus = function () {
        isActive = true;
        document.title = initialTitle;
        missedRequests = 0;
    };

    window.onblur = function () {
        isActive = false;
    };

    function updateTable () {
        $.getJSON("list/", {"last_count": last_count}, function (data) {

            last_count = last_count+data.length;
            if (data.length != 0 && !isActive) {
                    missedRequests = missedRequests + data.length;
                    document.title = "(" + missedRequests + ") " + initialTitle;
            }
            $.each(data.reverse(), function (key, value) {
                    newRow = clonedRequestRow.clone();
                    newDom = $(newRow).get(0);
                    var priority = value.fields.priority;
                    $(newDom).find(".request-createdat").text(
                        moment.utc(value.fields.created_at).format('MMMM D, YYYY, hh:mm a')
                    );
                    $(newDom).find(".request-id").text(value.pk);
                    $(newDom).find(".request-method").text(value.fields.method);
                    $(newDom).find(".request-path").text(value.fields.path);
                $(newDom).find(".request-priority").text(priority);
                    $(newRow).attr('id', value.pk);
                    $(newRow).attr('priority', priority);

                    newRow.insertBefore(position_table[priority]);
                    position_table[priority] = newRow;
            });

        })
    }

    updateTable();
    setInterval(updateTable, updateInterval);

});