const map = L.map('map').setView([-12.043492364009019, -77.04357480145998], 15);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
L.control.scale().addTo(map);

let startMarker, endMarker;
const greenIcon = L.divIcon({
    html: '<i class="fas fa-map-marker-alt text-success h2"></i>',
    iconSize: [36, 36],
    className: ''
});

const redIcon = L.divIcon({
    html: '<i class="fas fa-map-marker-alt text-danger h2"></i>',
    iconSize: [36, 36],
    className: ''
});

function onMapClick(e) {
    const latlng = e.latlng;
    if (!startMarker) {
        startMarker = L.marker(latlng, { icon: greenIcon, draggable: true }).addTo(map);
        updateAddress(startMarker, latlng, 'map-input-start');
        startMarker.on('dragend', function(event) {
            updateAddress(event.target, event.target.getLatLng(), 'map-input-start');
        });
    } else if (!endMarker) {
        endMarker = L.marker(latlng, { icon: redIcon, draggable: true }).addTo(map);
        updateAddress(endMarker, latlng, 'map-input-end');
        endMarker.on('dragend', function(event) {
            updateAddress(event.target, event.target.getLatLng(), 'map-input-end');
        });
    }
}
function updateAddress(marker, latlng, inputId) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latlng.lat}&lon=${latlng.lng}`;
    fetch(url).then(response => response.json())
    .then(data => {
        const address = data.address;
        const street = address.road || address.pedestrian || address.cycleway || address.path || "Desconocida";
        marker.setLatLng(latlng).bindPopup(`Calle: ${street}`).openPopup();
        document.getElementById(inputId).value = street;
        calculateRoute();
    })
    .catch(error => console.error('Error:', error));
}
function calculateRoute() {
    const vehicleType = document.getElementById('vehicle-type').value;
    if (!startMarker || !endMarker || !vehicleType) {
        return;
    }
    const startLatLng = startMarker.getLatLng();
    const endLatLng = endMarker.getLatLng();

    const directionsService = new google.maps.DirectionsService();
    const request = {
        origin: { lat: startLatLng.lat, lng: startLatLng.lng },
        destination: { lat: endLatLng.lat, lng: endLatLng.lng },
        travelMode: vehicleType.toUpperCase()
    };

    directionsService.route(request, function(response, status) {
        if (status == 'OK') {
            const route = response.routes[0];
            const legs = route.legs[0];
            const duration = legs.duration.text;
            const distance = legs.distance.text;
            document.getElementById('estimated-duration').innerText = duration;
            document.getElementById('estimated-distance').innerText = distance;
        } else {
            console.error('Error en la obtención de la ruta:', status);
        }
    });
}
map.on('click', onMapClick);
document.getElementById('vehicle-type').addEventListener('change', function() {calculateRoute();});