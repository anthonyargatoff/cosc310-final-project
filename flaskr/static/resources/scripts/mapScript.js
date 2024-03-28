const url = 'http://127.0.0.1:5000/send_data';
let data = Array();

async function push_data(item) {
    await new Promise(resolve => {
        data.push(item);
        setTimeout(resolve, 10);
    });
}

fetch(url).then(response => response.json()).then(async json => {
    //console.log(JSON.stringify(json));
    for (key in json){
        console.log(key);
        await push_data(json[key]);
    }
});
// console.log('This is from mapScript');



// console.log(Object.values(data));
// console.log(data[0][0]);


const map = L.map('map').setView([49.88, -119.49], 13);



L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);

var marker = L.marker([49.88, -119.49]).addTo(map);


// function fromMapScript() {
    
// }



// fromMapScript();
