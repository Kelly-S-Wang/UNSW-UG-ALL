var options = {
  valueNames: ['name', 'category']
};

var hackerList = new List('hacker-list', options);

$('#filter-sweden').click(function() {
  hackerList.filter(function(item) {
    if (item.values().category == "Sweden") {
      return true;
    } else {
      return false;
    }
  });
  return false;
});

$('#filter-denmark').click(function() {
  hackerList.filter(function(item) {
    if (item.values().category == "Denmark") {
      return true;
    } else {
      return false;
    }
  });
  return false;
});

$('#filter-none').click(function() {
  hackerList.filter();
  return false;
});

$('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {

  var options = {
    valueNames: ['name']
  };

  var hackerList = new List('hacker-list-2', options);

})