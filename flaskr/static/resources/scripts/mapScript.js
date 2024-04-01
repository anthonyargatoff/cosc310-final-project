document.addEventListener("DOMContentLoaded", async function(){

    const url = 'http://127.0.0.1:5000/eventAPI';

    try{
        const response = await fetch(url);
        if (!response){
            throw new Error(`HTTP error! ${response.status}`);
        }

        const data = await response.json();
        const events = data.events;
        const map = L.map('map', {worldCopyJump: true}).setView([0, 0], 3);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);

        events.forEach(event => {
            const latitude = event.latitude;
            const longitude = event.longitude;
            const magnitude = event.magnitude;
            const title = event.title;
            const url = event.url;
            const eventTime = event.eventTime;
            const depth = event.depth; 

            marker = L.marker([latitude, longitude]).addTo(map);
            marker.bindPopup("Title: " + title + "<br>Event time: " + eventTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");
        })

    } catch (e){
        console.error("Error fetching earthquake data: ", e);
    }
});