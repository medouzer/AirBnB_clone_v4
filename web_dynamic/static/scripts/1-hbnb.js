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
});
