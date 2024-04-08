const map = createMap();
let popups;
let predictions;
const url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&';
const countUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&';
const predictionUrl = 'http://localhost:5000/testpredictiondata'


// Initial document load-in
document.addEventListener("DOMContentLoaded", async function(){

    const date = getDefaultDate();
    document.getElementById('minDate').value = date[0];
    document.getElementById('maxDate').value = date[1];
    const queryString = url + `starttime=${getDefaultDate()[0]}&endtime=${getDefaultDate()[1]}`
    const eventsResponse = await makeRequest(queryString);
    const events = eventsResponse.features;
    popups = addDataPoints(events, map);
    createCardEvents("displayResults", events);
});

// When user searches for new data
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

// User views predictions data
const prediction = document.getElementById("test");
prediction.addEventListener('click', function(e){
    e.preventDefault();
    predictionQuery(predictionUrl);
})

/** Populates the map with events from a new query.
 * 
 * @param {string} queryString 
 */
async function newQuery (queryString){

    clearMarkers(popups);
    clearMarkers(predictions);
    removeChildElements("displayResults");
    let urlQuery;
    let countQuery;
    if (!queryString){
        const date = getDefaultDate();
        urlQuery = url + `starttime=${date[0]}&endtime=${date[1]}`;
        countQuery = countUrl + `starttime=${date[0]}&endtime=${date[1]}`;
    }
    else{
        urlQuery = url + queryString;
        countQuery = countUrl + queryString;
    }

    try{
        const countResponse = await makeRequest(countQuery);
        const count = countResponse.count;
        if (count > 1000){
            alert("Query results too large. Try a smaller query.")
        }
        else if (count == 0){
            alert("No results");
        }
        else{
            const eventsResponse = await makeRequest(urlQuery);
            const events = eventsResponse.features;
            popups = addDataPoints(events, map);
            createCardEvents("displayResults", events);
        }
    }
    catch (e){
        console.error(e);
    }
}

/** Displays the prediction data from the endpoint
 * 
 * @param {string} url 
 */
async function predictionQuery(url){
    clearMarkers(predictions);
    clearMarkers(popups);
    removeChildElements("displayResults");

    const predictionResponse = await makeRequest(url);
    const predictionEvents = predictionResponse;
    predictions = predictionCircles(predictionEvents, map);
    createCardPredictions("displayResults", predictionEvents);
}

/** Creates prediction circles on the map given prediction object
 * 
 * @param {object} predictionObject JSON object with lat, long, rank, and description fields
 * @returns {array} Returns array of prediction objects (circles on map) 
 */
function predictionCircles(predictionObject, map){
    let predictionArray = [];
    predictionObject.forEach(event =>{
        const circle = L.circle([event.latitude, event.longitude],{
            'color': 'red',
            'fillColor': '#f03',
            'fillOpacity': 0.5,
            'radius': 100000
        }).addTo(map);
        predictionArray.push(circle);
        circle.bindPopup(`Rank: ${event.rank}<br>Description: ${event.description}`);

    })
    return predictionArray
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
 * Removes all markers from the map if the array exists.
 * 
 * @param {array} 
 */
function clearMarkers(array){
    if (array){
        array.forEach(item => {
            item.remove();
        })
    }
}

/**
 * Open the popup when user clicks on card. Sets and removes the active class for styling.
 * 
 * @param {int} key 
 * @param {float} latitude 
 * @param {float} longitude 
 */
function openPopup(key, latitude, longitude){
    const children = document.getElementById("displayResults").children;
    for (let i = 0; i < children.length; i++){
        if(children[i].classList.contains("active")){
            children[i].classList.remove("active");
        }
    }
    popups[key].openPopup();
    map.setView([latitude, longitude], 5);
    document.getElementById(key).classList.add('active');
}

/**
 * Creates the card elements for events
 * 
 * @param {string} elementId Parent div id
 * @param {array} eventObj Json event data
 */
function createCardEvents (elementId, eventObj) {

    eventObj.forEach((event, index) => {
        const newCard = document.createElement("button");
        newCard.setAttribute("onclick", `openPopup(${index}, ${event.geometry.coordinates[1]}, ${event.geometry.coordinates[0]})`);
        newCard.id = index;
        newCard.className = "list-group-item list-group-item-action py-3 lh-sm";
        newCard.setAttribute("aria-current", "true");
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

/** Creates cards for the prediction data
 * 
 * @param {string} elementId Parent element in DOM
 * @param {object} eventObj Json object from endpoint
 */
function createCardPredictions (elementId,  eventObj){
    eventObj.forEach((event, index) => {
        const newCard = document.createElement("button");
        newCard.setAttribute("onclick", `openPopup(${index}, ${event.latitude}, ${event.longitude})`);
        newCard.id = index;
        newCard.className = "list-group-item list-group-item-action py-3 lh-sm";
        newCard.setAttribute("aria-current", "true");
        newCard.innerHTML = `<div class="d-flex w-100 align-items-center justify-content-between">
        <strong class="mb-1">${event.rank}</strong>
        <small></small>
        </div>
        <div class="mb-1 small">${event.description}</div>`;

        const node = document.getElementById(elementId);
        node.appendChild(newCard);
    })
}

/**Given a timestamp, converts to a UTC formatted string
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

/**
 * 
 * @returns Date array of todays date and tomorrows date, used for default view on search load.
 */
function getDefaultDate(){
    const date = new Date();
    const day = String(date.getDay()).padStart(2, '0');
    const month = String((date.getMonth() + 1)).padStart(2, '0');
    const year = date.getFullYear();
    const nextDay = String(date.getDay() + 1).padStart(2, '0');

    return [`${year}-${month}-${day}`, `${year}-${month}-${nextDay}`]
}