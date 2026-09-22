$(document).ready(function() {
    var url = window.location.href;
    var region = url.substring(url.lastIndexOf('/')+1); 

    var items = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum.value);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: "/data_hotspots/" + region,
            filter: function (data) {
                return $.map(data, function (location) {

                    return {
                        value: location.locName
                        ,id: location.locID
                    };
                });
            }
        }
    });

    // initialize the bloodhound suggestion engine
    items.initialize();

    // instantiate the typeahead UI
    $('#prefetch-find .typeahead').typeahead(
        {
            hint: true,
            highlight: true,
            minLength: 1
        },
        {
            name: 'engine',
            displayKey: 'value',
            source: items.ttAdapter(),
            templates: {
                empty: [
                  '<a href="#" class="list-group-item list-group-item-danger">Unable to find any matching results.</a>'
                ].join('\n'),
                suggestion: function(data) {
                  return '<a href="/locations/' + region + '/' + data.value.replace(/'/g, "\'") + '/' + data.id + '" class="list-group-item list-group-item-action list-group-item-success">' + data.value + '</a>';
                }
            }
    });
});
