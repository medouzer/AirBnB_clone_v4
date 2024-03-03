$(document).ready(function () {
  const list = $('.amenities > .popover > li > input[type="checkbox"]');
  const selectedAminties = {};
  const selectedState = {};
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
  const list1 = $('.locations > .popover > li > input[type="checkbox"]');
  list1.change(function () {
    const data_id = $(this).attr('data-id');
    const data_name = $(this).attr('data-name');
    if ($(this).is(':checked')) {
      selectedState[data_id] = data_name;
    } else {
      delete selectedState[data_id];
    }
    const state_list = [];
    for (const state in selectedState) {
      state_list.push(selectedState[state]);
    }
    $('.locations h4').text(state_list.join(', '));
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
  $('button').click(function () {
    const selectedAmenityIds = Object.keys(selectedAminties);
    $.ajax({
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ amenities: selectedAmenityIds }),
      success: function (response) {
        for (const place of response) {
          const placeName = place.name;
          const priceByNight = place.price_by_night;
          const maxGuest = place.max_guest;
          const numRooms = place.number_rooms;
          const numBathrooms = place.number_bathrooms;
          const placeDesc = place.description;

          const content = `<article>
                <div class="title_box">
                    <h2>${placeName}</h2>
                    <div class="price_by_night">$${priceByNight}</div>
                </div>
                <div class="information">
                    <div class="max_guest">${maxGuest} Guest${
            maxGuest !== 1 ? 's' : ''
          }</div>
                    <div class="number_rooms">${numRooms} Bedroom${
            numRooms !== 1 ? 's' : ''
          }</div>
                    <div class="number_bathrooms">${numBathrooms} Bathroom${
            numBathrooms !== 1 ? 's' : ''
          }</div>
                </div>
                <div class="description">
                            ${placeDesc}
                </div>
                </article>`;
          $('section.places').append(content);
        }
      },
    });
  });
});
