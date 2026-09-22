$(document).ready(function() {
    var items = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum.value);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: "/data_subnationals",
            filter: function (data) {
                return $.map(data.response.regions, function (region) {
                    var subnational = region.subnational2_code || region.subnational1_code;

                    return {
                        value: region.name + " (" + subnational + ")"
                    };
                });
            }
        }
    });

    // initialize the bloodhound suggestion engine
    items.initialize();

    // set results page to show from url
    var page = "checklists";
    if (document.URL.includes('hotspots')) {
        page = "hotspots";
    } else if (document.URL.includes('notables')) {
        page = "notables";
    }

    var species = "";
    if (document.URL.includes('taxa')) {
        // extract species code for pass-through to region links.
        page = "species";
        var str = document.URL;
        species = "/" + str.slice(str.lastIndexOf("(")+1, str.lastIndexOf(")"));
    }

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
                  //return "<a href='/" + page + "/" + data.value + "" + species + "' class='list-group-item list-group-item-action list-group-item-secondary'>" + data.value + "</a>";
                  return '<a href="/' + page + '/' + data.value + '' + species + '" class="list-group-item list-group-item-action list-group-item-secondary">' + data.value + '</a>';
                }
            }
    });
});
