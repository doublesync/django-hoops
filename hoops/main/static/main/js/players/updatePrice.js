// show current badge level
window.onload = function() {
    let badgeFormat = {0: "Unequipped", 1: "Bronze", 2: "Silver", 3: "Gold", 4: "HOF"};
    for (let i = 0; i < badgeUpgrades.length; i++) {
        let currentIndex = badgeUpgrades[i];
        let badgeName = currentIndex.name;
        let badgeValue = formattedPlayer[badgeName];
        currentIndex.selectedIndex = 0;
        currentIndex.options[currentIndex.selectedIndex].text = `${badgeFormat[badgeValue]}`;
    }
}

// query the DOM
let priceLabel = document.getElementById("price");
let cashLabel = document.getElementById("cash");
let statusLabel = document.getElementById("status");
let cashLeft = document.getElementById("cashLeft");

const submitButton = document.getElementById("submitButton");

let badgeUpgrades = document.getElementsByClassName("badgeUpgrade");

// initialize variables
const cash = 167;

// set cash label
cashLabel.innerText = cash;

// update price on change of badges
const badgeChange = function() {
    let price = 0;
    for (let i = 0; i < badgeUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = badgeUpgrades[i];
        let currentLevel = currentIndex.options[currentIndex.selectedIndex].text;
        // recalculate the price
        if (currentLevel in badgePrices) {
            price += badgePrices[currentLevel];
            // check if user has enough cash
            if (cash >= price) {
                statusLabel.style.color = "green";
                submitButton.classList.remove("btn-danger");
                submitButton.classList.add("btn-success");
                submitButton.disabled = false;
                statusLabel.innerText = "You can afford this upgrade!"
            } else {
                statusLabel.style.color = "red";
                submitButton.classList.remove("btn-success");
                submitButton.classList.add("btn-danger");
                submitButton.disabled = true;
                statusLabel.innerText = "You cannot afford this upgrade!"
            }
        }
        // set the price & cash labels
        priceLabel.innerText = price;
        cashLeft.innerText = cash - price;
    }
}

const attributechange = function() {

}