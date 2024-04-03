const map = createMap();
let popups;
const url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&';
const countUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&';


// Initial document load-in
document.addEventListener("DOMContentLoaded", async function(){

    const date = getDefaultDate();
    document.getElementById('minDate').value = date[0];
    document.getElementById('maxDate').value = date[1];
    const eventsResponse = await makeRequest(url);
    const events = eventsResponse.features;
    popups = addDataPoints(events, map);
    createCard("displayResults", events);
});

const submit = document.getElementById("search");
submit.addEventListener('click', function(e){
    const latitude = document.getElementById('lat').value;
    const longitude = document.getElementById('long').value;
    const radius = document.getElementById('radius').value;
    const minMagnitude = document.getElementById('minMag').value;
    const maxMagnitude = document.getElementById('maxMag').value;
    const starttime = document.getElementById('minDate').value;
    const endtime = document.getElementById('maxDate').value;

    let queryString = '';
    
    if (starttime){
        queryString += `starttime=${starttime}&`;
    }
    if (endtime){
        queryString += `endtime=${endtime}&`;
    }
    if (minMagnitude){
        queryString += `minmagnitude=${minMagnitude}&`;
    }
    if (maxMagnitude){
        queryString += `maxmagnitude=${maxMagnitude}&`
    }
    if (latitude){
        queryString += `latitude=${latitude}&`;
    }
    if (longitude){
        queryString += `longitude=${longitude}&`;
    }
    if (radius){
        queryString += `maxradiuskm=${radius}&`;
    }
    if (queryString.endsWith('&')){
        queryString = queryString.slice(0, -1);
    }
    // console.log(queryString);

    newQuery (queryString);
})

/**
 * Populates the map with events from a new query.
 */
async function newQuery (queryString){

    // TODO: get the form data from search input
    // get.data

    clearMarkers(popups);
    removeChildElements("displayResults");

    try{
        const countResponse = await makeRequest(countUrl, queryString);
        const count = countResponse.count;
        if (count > 1000){
            alert("Query results too large. Try a smaller query.")
            throw new Error('Requested query is too large. Try a smaller query.')
        }
        if (count == 0){
            alert("No results");
        }
        else{
            const eventsResponse = await makeRequest(url, queryString);
            const events = eventsResponse.features;
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
    const parent = document.getElementById(parentElement);
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
        newCard.setAttribute("onclick", `openPopup(${index}, ${event.geometry.coordinates[1]}, ${event.geometry.coordinates[0]})`);
        newCard.className = "list-group-item list-group-item-action py-3 lh-sm";
        newCard.setAttribute("aria-current", "true");
        // const formattedDate = timestampToDate(event.properties.time);
        const date = new Date(event.properties.time);
        formattedDate = date.toUTCString();
        newCard.innerHTML = `<div class="d-flex w-100 align-items-center justify-content-between">
        <strong class="mb-1">${event.properties.title}</strong>
        <small>${formattedDate}</small>
    </div>
    <div class="mb-1 small">${event.properties.url}</div>`;

        const node = document.getElementById(elementId);
        node.appendChild(newCard);
    })
}

/**Given a timestamp, converts to a string formatted yyyy-mm-dd hh:mm:ss
 * 
 * @param {int} timestamp 
 * @returns {String} 
 */
function timestampToDate(timestamp){
    const date = new Date(timestamp);
    return date.toUTCString();
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
async function makeRequest (url, queryString=false) {
    
    const getRequest = queryString ? url + queryString : url + 'starttime=' + getDefaultDate()[0] + "&endtime=" + getDefaultDate()[1];
    console.log(getRequest);
    const response = await fetch(getRequest);
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

        const latitude = event.geometry.coordinates[1];
        const longitude = event.geometry.coordinates[0];
        const magnitude = event.properties.mag;
        const title = event.properties.title;
        const url = event.properties.url;
        const unixTime = event.properties.time;
        const depth = event.geometry.coordinates[2]; 

        const dateTime = timestampToDate(unixTime);

        const marker = L.marker([latitude, longitude]).addTo(mapObj);
        const popup = marker.bindPopup("Title: " + title + "<br>Event time: " + dateTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");
        popups.push(popup);
    })
    return popups;
}

function getDefaultDate(){
    const date = new Date();
    const day = String(date.getDay()).padStart(2, '0');
    const month = String((date.getMonth() + 1)).padStart(2, '0');
    const year = date.getFullYear();
    const nextDay = String(date.getDay() + 1).padStart(2, '0');

    return [`${year}-${month}-${day}`, `${year}-${month}-${nextDay}`]
}