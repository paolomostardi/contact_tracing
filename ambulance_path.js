function getRoadBetweenCoordinates(startCoords, endCoords) {
    var directionsService = new google.maps.DirectionsService();
    
    var request = {
        origin: startCoords,
        destination: endCoords,
        travelMode: 'DRIVING'
    };
    
    directionsService.route(request, function(response, status) {
        if (status === 'OK') {
            var route = response.routes[0];
            var leg = route.legs[0];
            var roadName = leg.steps[0].name;
            console.log("Road Name:", roadName);
        }
    });
}



