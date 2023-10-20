const event = new EventSource('/event');


event.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const plants = data["plants"];
    const extra = data["extra"];

    // console.log(plants);

    let plantSection = document.querySelector('.plantSection');
    plantSection.innerHTML = ``;


    for (let plant of plants) {
        let username = plant["username"];
        let plantType = plant["plant_type"];
        let growthNum = Math.min(plant["growth"], 4);
        let flareNum = Math.min((plant["growth"] - growthNum) - 1, 4);

        let plantImg = '';
        let flareImg = '';
        let epicImg = '';
        let waterImg = '';
        let rainImg = '';
        let glassesImg = '';
        let speechImg = '';
        let medalImg = '';

        if (plant["wilted"]) {
            plantImg = `../images/plants/${plantType}/wilted.png`
            waterImg = `<img class="plantWater" src='../images/water.png'>`
        }

        else if (plant["dead"]) {
            plantImg = '../images/tomb.png'
        }

        else {
            plantImg = `../images/plants/${plantType}/${growthNum}.png`
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

        if (plant["blood_rain"]) {
            rainImg = `<img class="plantRain" src='../images/blood.gif'>`
        }

        if (plant["glasses"]) {
            glassesImg = `<img class="plantGlasses" src="../images/glasses.png">`
        }

        if (extra && extra["event"] === "attacked" && extra["reversed"] && extra["attacker"] === plant["username"]) {
            speechImg = `<img class="plantSpeech" src="../images/speech/win.png">`
        }

        else if (plant["speech"]) {
            speechImg = `<img class="plantSpeech" src="../images/speech/${plant["speech"]}.png">`
        }

        if (plant["top"] <= 3) {
            medalImg = `<img class="plantMedal" src="../images/medals/${plant["top"]}.png">`
        }

        if (username.length > 9) {
            username = `${plant["username"].slice(0, 9)}...`
        }

        let inner = `
            <div class="plantContainer">
                <img class="plantImg" src=${plantImg}>
                <img class="plantBanner" src="images/banner.png">
                ${medalImg}
                <span class="username">${username}</span>
                ${flareImg}
                ${epicImg}
                ${waterImg}
                ${rainImg}
                ${glassesImg}
                ${speechImg}
            </div>
        `;

        plantSection.insertAdjacentHTML('beforeend', inner);
    }

};