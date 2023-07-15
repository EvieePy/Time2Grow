const event = new EventSource('http://localhost:8000/event');


event.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const plants = data["plants"];

    console.log(plants);

    let plantSection = document.querySelector('.plantSection');
    plantSection.innerHTML = ``;


    for (let plant of plants) {
        let username = plant["username"];
        let growthNum = Math.min(plant["growth"], 4);
        let flareNum = Math.min((plant["growth"] - growthNum) - 1, 4);

        let plantImg = '';
        let flareImg = '';
        let epicImg = '';
        let waterImg = '';
        let rainImg = '';

        if (plant["wilted"]) {
            plantImg = '../images/plants/wilted.png';
            waterImg = `<img class="plantWater" src='../images/water.png'>`;
        }

        else if (plant["dead"]) {
            plantImg = '../images/tomb.png';
        }

        else {
            plantImg = `../images/plants/${growthNum}.png`;
        }

        if (flareNum >= 0) {
            flareImg = `<img class="plantFlare" src='../images/shields/${flareNum}.png'>`
        }

        if (plant["maxed"]) {
            epicImg = `<img class="plantEpic" src='../images/epic.gif'>`
        }

        if (plant["watering"]) {
            rainImg = `<img class="plantRain" src='../images/rain.gif'>`
        }

        if (username.length > 9) {
            username = `${plant["username"].slice(0, 9)}...`
        }

        let inner = `
            <div class="plantContainer">
                <img class="plantImg" src=${plantImg}>
                <img class="plantBanner" src="images/banner.png">
                <span class="username">${username}</span>
                ${flareImg}
                ${epicImg}
                ${waterImg}
                ${rainImg}
            </div>
        `
        plantSection.insertAdjacentHTML('beforeend', inner);
    }

};