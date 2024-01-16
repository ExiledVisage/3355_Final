if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition((position) => {
    const userLocation = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    };

    console.log(userLocation.lat)
    console.log(userLocation.lng)

    fetch('/get_offices') // Fetch data from Flask route
      .then(response => response.json())
      .then(data => {
        const offices = data.offices; // Extract office data from response
        console.log(offices); // Check fetched office data in the console
        offices.forEach(office => { 
          console.log('Office: ', office)
          console.log('Office_id:', office[0])});

        // Use the fetched office data to mark offices within 30km radius
        displayMap(userLocation,offices);
      })
      .catch(error => {
        console.error('Error fetching office data:', error);
      });
  }, (error) => {
    console.error('Error getting user location:', error);
  });
} else {
  console.error('Geolocation is not supported by this browser');
}

  // Example code to display map and markers
function displayMap(userLocation,offices) 
{
  const map = new google.maps.Map(document.getElementById('map'), {
    center: userLocation,
    zoom: 12 // Adjust zoom level as needed
    });

    const userMarker = new google.maps.Marker({
      position: userLocation,
      map: map,
      title: 'Your Location'
    });

    offices.forEach(office => {
      const officeLocation = {
        lat: parseFloat(office[7]),
        lng: parseFloat(office[8])
      };
      
      console.log(officeLocation.lat)
      console.log(officeLocation.lng)

      const distanceInKm = calculateHaversineDistance(
        userLocation.lat,
        userLocation.lng,
        officeLocation.lat,
        officeLocation.lng
      );

      console.log(distanceInKm)    
      // Create a marker for each office
      // If office is within 30km radius, display marker on the map
    if (distanceInKm <= 30) {
      const marker = new google.maps.Marker({
        position: officeLocation,
        map: map,
        title: office[2] // Assuming 'office_title' is the title of the office
      });

      // Add click event listener to the marker to display information
      marker.addListener('click', () => {
        // Show information about the office (e.g., in an info window)
        // Populate info window with details from the office
        const infoWindow = new google.maps.InfoWindow({
          content: `<div>${office[2]}</div><div>${office[3]}</div>`
        });
        infoWindow.open(map, marker);
      });
    }
    }); 

}

function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth radius in kilometers
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c; // Distance in kilometers
  return distance;
}

function calculateRentDays() {
  // Retrieve pickup and return dates
  var pickupDate = document.getElementById('pickupDate').value;
  var returnDate = document.getElementById('returnDate').value;

  // Convert dates to JavaScript Date objects
  var pickupDateObj = new Date(pickupDate);
  var returnDateObj = new Date(returnDate);

  // Check if pickup date is after return date
  if (pickupDateObj > returnDateObj) {
      // Display error message
      var errorContainer = document.getElementById('errorContainer');
      errorContainer.innerHTML = 'Error: Pickup date cannot be after return date.';
      return false; // Prevent the form from submitting
  }

  // Calculate the difference in days
  var timeDifference = returnDateObj.getTime() - pickupDateObj.getTime();
  var daysDifference = Math.ceil(timeDifference / (1000 * 3600 * 24));

  // Display the result in a div
  var resultContainer = document.getElementById('resultContainer');
  resultContainer.innerHTML = 'Rent for ' + daysDifference + ' days.';


  return true; // Allow the form to submit
}