describe("Get an unordered list and its items", function() {
  var val;
  beforeAll(function() {
    val = "message";
  });

  it("returns <ul>", function() {
    var html = getUnorderedList().outerHTML;

    expect(html).toEqual(jasmine.stringMatching('ul'));
    expect(html).toEqual(jasmine.stringMatching('data-role="listview"'));
    expect(html).toEqual(jasmine.stringMatching('class="ui-listview'));
    expect(html).toEqual(jasmine.stringMatching('/ul'));
  });

  it("returns <li> with passed text as item", function() {
    var html = getListItem(val).outerHTML;

    expect(html).toEqual(jasmine.stringMatching('li'));
    expect(html).toEqual(jasmine.stringMatching('class="ui-li-static ui-body-inherit"'));
    expect(html).toEqual(jasmine.stringMatching(val));
    expect(html).toEqual(jasmine.stringMatching('/li'));
  });

  it("returns <li> with passed text as item styled to act as a header", function() {
    var html = getListItemDivider(val).outerHTML;

    expect(html).toEqual(jasmine.stringMatching('li'));
	  expect(html).toEqual(jasmine.stringMatching('data-role="list-divider"'));
	  expect(html).toEqual(jasmine.stringMatching('role="heading"'));
    expect(html).toEqual(jasmine.stringMatching('class="ui-li-divider ui-body-inherit"'));
    expect(html).toEqual(jasmine.stringMatching(val));
    expect(html).toEqual(jasmine.stringMatching('/li'));
  });

  it("returns <ul><li> with passed text as item's styled header message", function() {
    var html = formatResponseMessage(val).outerHTML;

    expect(html).toEqual(jasmine.stringMatching('ul'));
    expect(html).toEqual(jasmine.stringMatching('li'));
    expect(html).toEqual(jasmine.stringMatching(val));
    expect(html).toEqual(jasmine.stringMatching('/li'));
    expect(html).toEqual(jasmine.stringMatching('/ul'));
  });
});

describe("Get data html output", function() {
   it("returns correctly formatted checklist submission data", function() {
        var region = "Suffolk (US-MA-025)";
        var html = getChecklistSubmissions(region, "Search again").outputHtml;
        expect(html).not.toBe("");
   });

   it("returns correctly formatted notable sightings data", function() {
        var region = "Suffolk (US-MA-025)";
        var html = getNotableSightings(region, "Search again").outputHtml;
        expect(html).not.toBe("");
   });

   it("returns correctly formatted location data", function() {
        var locationId = "L248222";
        var html = getLocationSubmissions(locationId).outputHtml;
        expect(html).not.toBe("");
   });

   it("returns correctly formatted species data", function() {
        var region = "Massachusetts (US-MA)";
        var scientificName = "Passer domesticus";
        var html = getSpeciesSightings(region, scientificName);
        expect(html).not.toBe("");
   });
});

describe("Get error message from json", function() {
    var html = "";
    var region = "Massachusetts (US-MA)";
    var badregion = "Somesuch (XX-XX)";
    var badsciname = "Xxxxx xxxxxxx";
    var badlocid = "LXXXXXX";//"L248222";
  beforeAll(function() {
    console.log(html);
  });

    it("returns correctly formatted no checklists for bad region" + html, function() {
        html = getChecklistSubmissions(badregion);
        expect(html.indexOf('0 checklists') !== -1).toBe(true);
    });

    it("returns correctly formatted no notable sightings for a bad region" + html, function() {
        html = getNotableSightings(badregion, "message");
        expect(html.indexOf('0 notable species') !== -1).toBe(true);
    });

    it("returns no data message for bad location data" + html, function() {
        html = getLocationSubmissions(badlocid);
        expect(html.indexOf('No data found') !== -1).toBe(true);
    });

    it("returns correctly formatted no species data found message" + html, function() {
        html = getSpeciesSightings(region, badsciname);
        expect(html).not.toBe("");
    });
});
