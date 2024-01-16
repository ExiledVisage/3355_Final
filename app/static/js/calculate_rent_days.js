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

