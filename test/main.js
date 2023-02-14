// query the DOM
let priceLabel = document.getElementById("price");
let cashLabel = document.getElementById("cash");
let statusLabel = document.getElementById("status");

// initialize variables
const cash = 167;
const badgePrices = {
    "N/A": 0,
    "Bronze": 10,
    "Silver": 25,
    "Gold": 50,
    "Hall of Fame": 75,
} 

// set cash label
cashLabel.innerText = cash;

// on change of badges
const badgeChange = function() {
    let price = 0;
    let badgeUpgrades = document.getElementsByClassName("badgeUpgrade");
    for (let i = 0; i < badgeUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = badgeUpgrades[i];
        let currentLevel = currentIndex.options[currentIndex.selectedIndex].text;
        // recalculate the price
        if (currentLevel in badgePrices) {
            price += badgePrices[currentLevel];
            priceLabel.innerText = price;
            cashLabel.innerText = `${cash} ➡️ $${cash - price}`;
            // check if user has enough cash
            if (cash >= price) {
                statusLabel.style.color = "green";
                statusLabel.innerText = "You can afford this upgrade!"
            } else {
                statusLabel.style.color = "red";
                statusLabel.innerText = "You cannot afford this upgrade!"
            }
        } else {
            console.log("Error: " + currentLevel + " not found in badgePrices");
        }
    }
}