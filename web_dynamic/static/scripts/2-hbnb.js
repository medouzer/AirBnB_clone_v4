$(document).ready(function () {
  const list = $('input[type="checkbox"]');
  const selectedAminties = {};
  list.change(function () {
    const data_id = $(this).attr('data-id');
    const data_name = $(this).attr('data-name');
    if ($(this).is(':checked')) {
      selectedAminties[data_id] = data_name;
    } else {
      delete selectedAminties[data_id];
    }
    const amenity_list = [];
    for (const amemity in selectedAminties) {
      amenity_list.push(selectedAminties[amemity]);
    }
    $('.amenities h4').text(amenity_list.join(', '));
  });
  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/status/',
    method: 'GET',
    dataType: 'json',
    success: function (response) {
      if (response.status === 'OK') {
        $('div#api_status').addClass('available');
      } else {
        $('div#api_status').removeClass('available');
      }
    },
  });
});
