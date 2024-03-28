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

        events.forEach((event, index) => {

            const latitude = event.latitude;
            const longitude = event.longitude;
            const magnitude = event.magnitude;
            const title = event.title;
            const url = event.url;
            const eventTime = event.eventTime;
            const depth = event.depth; 

            marker = L.marker([latitude, longitude]).addTo(map);
            marker.bindPopup("Title: " + title + "<br>Event time: " + eventTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");

            createCard("displayResults", event, index);
        })

    } catch (e){
        console.error("Error fetching earthquake data: ", e);
    }
});


/**
 * 
 * @param {string} elementId 
 * @param {event} eventObj 
 * @param {int} index 
 */
function createCard (elementId, eventObj, index) {
    const newCard = document.createElement("a");
    newCard.href = eventObj.url;
    newCard.target = "_blank";
    newCard.className = isEven(index) ? "list-group-item list-group-item-action active py-3 lh-sm" : "list-group-item list-group-item-action py-3 lh-sm";
    newCard.setAttribute("aria-current", "true");
    newCard.innerHTML = `<div class="d-flex w-100 align-items-center justify-content-between">
    <strong class="mb-1">${eventObj.title}</strong>
    <small>${eventObj.eventTime}</small>
  </div>
  <div class="mb-1 small">${eventObj.url}</div>`;

    const node = document.getElementById(elementId);
    node.appendChild(newCard);
}

/**
 * 
 * @param {int} n 
 * @returns {bool} boolean
 */
function isEven (n){
    return n % 2 == 0;
}