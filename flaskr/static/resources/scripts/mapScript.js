const map = createMap();
let popups;
const url = 'http://localhost:5000/eventAPI';
const countUrl = 'http://localhost:5000/eventAPIcount';

// Initial document load-in
document.addEventListener("DOMContentLoaded", async function(){

    const eventsResponse = await makeRequest(url);
    const events = eventsResponse.events;
    popups = addDataPoints(events, map);
    createCard("displayResults", events);
});


/**
 * Populates the map with events from a new query.
 */
async function newQuery (){

    // TODO: get the form data from search input
    // get.data...

    clearMarkers(popups);
    removeChildElements("displayResults");

    try{
        const countResponse = await makeRequest("http://localhost:5000/eventAPIcount?latitude=45&longitude=45&radius=4000"); //TODO remove test data
        const count = countResponse.count;
        if (count > 1000){
            alert("Query results too large. Try a smaller query.")
            throw new Error('Requested query is too large. Try a smaller query.')
        }
        else{
            const eventsResponse = await makeRequest("http://localhost:5000/eventAPI?latitude=45&longitude=45&radius=4000"); // TODO add query string to url
            const events = eventsResponse.events;
            popups = addDataPoints(events, map);
            createCard("displayResults", events);
        }
    }
    catch (e){
        console.error(e);
    }
}

/** Removes all children element from their parent container.
 * 
 * @param {string} parentElement 
 */
function removeChildElements (parentElement){
    const parent = document.getElementById("displayResults");
    while (parent.firstChild){
        parent.removeChild(parent.firstChild)
    }
}

/**
 * Removes all markers from the map.
 * 
 * @param {array} popups 
 */
function clearMarkers(popups){
    popups.forEach(popup => {
        popup.remove();
    })
}

/**
 * Open the popup when user clicks on card
 * 
 * @param {int} key 
 * @param {float} latitude 
 * @param {float} longitude 
 */
function openPopup(key, latitude, longitude){
    popups[key].openPopup();
    map.setView([latitude, longitude], 5);
}

/**
 * Creates the card elements
 * 
 * @param {string} elementId Parent div id
 * @param {array} eventObj Json event data
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
 * Is even or not.
 * 
 * @param {int} n 
 * @returns {bool} Returns boolean
 */
function isEven (n){
    return n % 2 == 0;
}

/**
 * Makes request to API, returns JSON
 * 
 * @param {string} url 
 * @param {string} getParameters 
 * @returns {array} Returns json array
 */
async function makeRequest (url) {
    const response = await fetch(url);
    if (!response){
        throw new Error(`HTTP error: ${response.status}`)
    }
    const data = await response.json();
    return data;
}

/**
 * Create the leaflet map object
 * 
 * @returns {L} Returns map object
 */
function createMap (){
    const map = L.map('map', {worldCopyJump: true}).setView([0, 0], 3);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
    return map;
}

/**
 * Adds the data points to the leaflet map.
 * 
 * @param {array} events Json data array
 * @param {map} mapObj Leaflet map object 
 * @returns 
 */
function addDataPoints (events, mapObj){
    const popups = [];
    events.forEach((event) => {

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
