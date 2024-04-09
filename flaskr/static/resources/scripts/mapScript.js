const [map, layerControl] = createMap();
let popups;
let predictions;
let earthquakeLayer;
let userCircle;
const url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&';
const countUrl = 'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson&';
const predictionUrl = 'http://localhost:5000/testpredictiondata'
const geocodeURL = 'https://geocode.maps.co/search?q=';
const geocodeAPIKey = '6612fe31db408262351014htr8789af';

// Initial document load-in
document.addEventListener("DOMContentLoaded", async function(){

    const date = getDefaultDate();
    document.getElementById('minDate').value = date[0];
    document.getElementById('maxDate').value = date[1];
    const queryString = url + `starttime=${getDefaultDate()[0]}&endtime=${getDefaultDate()[1]}`
    const eventsResponse = await makeRequest(queryString);
    const events = eventsResponse.features;
    [popups, earthquakeLayer] = addDataPoints(events, map, layerControl);
    createCardEvents("displayResults", events);
    const predictionResponse = await makeRequest(predictionUrl);
    const prediction = predictionResponse;
    predictionCircles(prediction, map, layerControl);
});

// When user searches for new data
const submit = document.getElementById("search");
submit.addEventListener('click', async function(e,) {
    if (userCircle) userCircle.remove();
    const address = document.getElementById('location').value;
    let latitude = document.getElementById('lat').value;
    let longitude = document.getElementById('long').value;
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
    if (address){
        const addressString = convertAddress(address);
        const geocodeString = geocodeURL + addressString + '&api_key=' + geocodeAPIKey;
        const geocode = await makeRequest(geocodeString);
        latitude = geocode[0].lat;
        longitude = geocode[0].lon;
        queryString += `latitude=${latitude}&`;
        queryString += `longitude=${longitude}&`;
    }
    else if (latitude && longitude){
        queryString += `latitude=${latitude}&`;
        queryString += `longitude=${longitude}&`;
    }
    if (radius){
        queryString += `maxradiuskm=${radius}&`;
    }
    if (queryString.endsWith('&')){
        queryString = queryString.slice(0, -1);
    }

    if (radius && (address || (latitude && longitude))){
        userCircle = createSearchCircle(map, latitude, longitude, radius * 1000);
        userCircle.openPopup()
    }
    newQuery (queryString);
})


/** Populates the map with events from a new query.
 * 
 * @param {string} queryString 
 */
async function newQuery (queryString){

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
            earthquakeLayer.clearLayers();
            const eventsResponse = await makeRequest(urlQuery);
            const events = eventsResponse.features;
            [popups, earthquakeLayer] = editLayer(events, earthquakeLayer);
            createCardEvents("displayResults", events);
        }
    }
    catch (e){
        console.error(e);
    }
}


/** Creates prediction circles on the map given prediction object
 * 
 * @param {object} predictionObject JSON object with lat, long, rank, and description fields
 * @returns {array} Returns array of prediction objects (circles on map) 
 */
function predictionCircles(predictionObject, map, layerControl){
    let predictionArray = [];
    predictionObject.forEach(event =>{
        const circle = L.circle([event.latitude, event.longitude],{
            'color': 'red',
            'fillColor': '#f03',
            'fillOpacity': 0.5,
            'radius': 500000
        }).bindPopup(`Rank: ${event.rank}<br>Description: ${event.description}`);
        predictionArray.push(circle);
    })
    const prediction = L.layerGroup(predictionArray);
    layerControl.addOverlay(prediction, "Predictions");
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
 * Create the leaflet map object and layer-control object
 * 
 * @returns {array} Returns map object and layerc-ontrol object
 */
function createMap (){
    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19, 
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    const topographic = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: 'Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap (CC-BY-SA)'
    });
    const satellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
    });
    const map = L.map('map', {
        worldCopyJump: true,
        layers: [osm]
    }).setView([0, 0], 3);
    const baseMaps = {
        "OpenStreet": osm,
        "OpenTopoMap": topographic,
        "Google Satellite": satellite
    }
    const layerControl = L.control.layers(baseMaps).addTo(map);
    
    return [map, layerControl];
}

/**
 * Adds the data points to the leaflet map.
 * 
 * @param {array} events Json data array
 * @param {map} mapObj Leaflet map object 
 * @param {layerControl} layerControl The leaflet layer control object
 * @returns {array} Returns popup array and layer object
 */
function addDataPoints (events, mapObj, layerControl){
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

        const popup = L.marker([latitude, longitude]).bindPopup("Title: " + title + "<br>Event time: " + dateTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");
        popups.push(popup);
    })
    const earthquakes = L.layerGroup(popups).addTo(mapObj);
    layerControl.addOverlay(earthquakes, "Earthquakes");
    return [popups, earthquakes];
}

/** Edits the existing layer with new data points
 * 
 * @param {JSON} events Json object from API
 * @param {layer} earthquakeLayer Leaflet layer object
 * @returns {array} Returns popup array and leaflet layer
 */
function editLayer(events, earthquakeLayer){
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

        const popup = L.marker([latitude, longitude]).bindPopup("Title: " + title + "<br>Event time: " + dateTime + "<br>Magnitude: " + magnitude + "<br>Latitude: " + latitude + "<br>Longitude: " + longitude + "<br>Depth: " + depth + "<br>URL: <a href='" + url + "' target='_blank'>Event Link</a>");
        popups.push(popup);
    })
    const layerGroup = L.layerGroup(popups);
    earthquakeLayer.addLayer(layerGroup);
    // layerControl.addOverlay(earthquakes, "Earthquakes");
    return [popups, earthquakeLayer];
}

/** Gets todays date and tomorrows date. Used for empty queries.
 * 
 * @returns Date array of todays date and tomorrows date, used for default view on search load.
 */
function getDefaultDate(){
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String((today.getMonth() + 1)).padStart(2, '0');
    const year = today.getFullYear();

    const tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
    const tomorrowDay = String(tomorrow.getDate()).padStart(2, '0');
    const tomorrowMonth = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const tomorrowYear = tomorrow.getFullYear();

    return [`${year}-${month}-${day}`, `${tomorrowYear}-${tomorrowMonth}-${tomorrowDay}`]
}

/** Removes spaces and commas from string. Used for geocode
 * 
 * @param {String} address String address
 * @returns Address with + in between elements
 */
function convertAddress(address){
    const parts = address.split(/[ ,]+/);
    return parts.join('+');
}

/** Creates circle of a users search
 * 
 * @param {Leaflet Map} mapObj 
 * @param {float} lat 
 * @param {float} lon 
 * @param {float} radius 
 * @returns {circle}
 */
function createSearchCircle(mapObj, lat, lon, radius){
    const circle = L.circle([lat, lon], {
        color: 'green',
        fillColor: '#abd6b7',
        fillOpacity: 0.5,
        'radius': radius
    }).addTo(mapObj).bindPopup(`Search result:<br>Latitude: ${lat}<br>Longitude: ${lon}<br>Radius: ${radius / 1000}`);
    return circle;
}