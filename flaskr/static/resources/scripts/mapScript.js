const map = createMap();
let popups;

document.addEventListener("DOMContentLoaded", async function(){

    const url = 'http://127.0.0.1:5000/eventAPI';
    const events = await makeRequest(url);
    popups = addDataPoints(events, map);
    createCard("displayResults", events);

});

function openPopup(key, latitude, longitude){
    popups[key].openPopup();
    map.setView([latitude, longitude], 5);
}

/**
 * 
 * @param {string} elementId 
 * @param {event} eventObj 
 * @param {int} index 
 */
function createCard (elementId, eventObj) {

    eventObj.forEach((event, index) => {
        const newCard = document.createElement("button");
        newCard.href = event.url;
        newCard.setAttribute("onclick", `openPopup(${index}, ${event.latitude}, ${event.longitude})`);
        newCard.target = "_blank";
        newCard.className = isEven(index) ? "list-group-item list-group-item-action active py-3 lh-sm" : "list-group-item list-group-item-action py-3 lh-sm";
        newCard.setAttribute("aria-current", "true");
        newCard.innerHTML = `<div class="d-flex w-100 align-items-center justify-content-between">
        <strong class="mb-1">${event.title}</strong>
        <small>${event.eventTime}</small>
    </div>
    <div class="mb-1 small">${event.url}</div>`;

        const node = document.getElementById(elementId);
        node.appendChild(newCard);
    })
    
}

/**
 * 
 * @param {int} n 
 * @returns {bool} boolean
 */
function isEven (n){
    return n % 2 == 0;
}

async function makeRequest (url, getParameters) {
 
    const response = await fetch(url);
    if (!response){
        throw new Error(`HTTP error: ${response.status}`)
    }
    const data = await response.json();
    return data.events;
}

function createMap (){
    const map = L.map('map', {worldCopyJump: true}).setView([0, 0], 3);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    return map;
}

function addDataPoints (events, mapObj){
    const popups = [];

    events.forEach((event, index) => {

        const latitude = event.latitude;
        const longitude = event.longitude;
        const magnitude = event.magnitude;
        const title = event.title;
        const url = event.url;
        const eventTime = event.eventTime;
        const depth = event.depth; 

        const marker = L.marker([latitude, longitude]).addTo(mapObj);
        const popup = marker.bindPopup("Title: " + title + "<br>Event time: " + eventTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");
        popups.push(popup);
    })
    return popups;
}