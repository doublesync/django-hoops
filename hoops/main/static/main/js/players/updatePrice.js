let badgeUpgrades = document.getElementsByClassName("badgeUpgrade");
let attributeUpgrades = document.getElementsByClassName("attributeUpgrade");

// show current badge level
window.onload = function() {
    let badgeFormat = {0: "Unequipped", 1: "Bronze", 2: "Silver", 3: "Gold", 4: "Hall of Fame"};
    for (let i = 0; i < badgeUpgrades.length; i++) {
        let currentIndex = badgeUpgrades[i];
        let badgeName = currentIndex.name;
        let badgeValue = formattedPlayer[badgeName];
        currentIndex.selectedIndex = 0;
        currentIndex.options[currentIndex.selectedIndex].text = `${badgeFormat[badgeValue]}`;
        for (let i = 1; i <= 4; i++) {
            if (badgeValue > i || badgeValue == i) {
                currentIndex.options[i].disabled = true;
            }
        }
    }
}

// query the DOM
let priceLabel = document.getElementById("price");
let cashLabel = document.getElementById("cash");
let statusLabel = document.getElementById("status");
let cashLeft = document.getElementById("cashLeft");

const submitButton = document.getElementById("submitButton");

// set cash label
cashLabel.innerText = cash;
cashLeft.innerText = cash;

// calculate price of attributes in form
const calculateAttributePrice = function() {
    let price = 0;
    for (let i = 0; i < attributeUpgrades.length; i++) {
        // find the current index + level of attribute
        let currentIndex = attributeUpgrades[i];
        let futureAttribute = currentIndex.value;
        let currentAttribute = formattedPlayer[currentIndex.name];
        let timesUpgraded = Number(futureAttribute) - Number(currentAttribute)
        // recalculate the price
        price += timesUpgraded * attributePrices["Default"];
    }
    // return price
    return price;
}

// calculate price of badges in form
const calculateBadgePrice = function() {
    let price = 0;
    for (let i = 0; i < badgeUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = badgeUpgrades[i];
        let currentLevel = currentIndex.options[currentIndex.selectedIndex];
        // recalculate the price
        if (currentLevel.value in badgePrices) {
            price += badgePrices[currentLevel.value];
            console.log(currentLevel.Value);
        }
    }
    // return the price
    return price;
}

// update price on changes of attributes + badges
const updatePrice = function() {
    // calculate prices
    const attributePrice = calculateAttributePrice();
    const badgePrice = calculateBadgePrice();
    console.log(attributePrice, badgePrice);
    // get the total price
    const totalPrice = attributePrice + badgePrice;
    // update price & cash labels
    priceLabel.innerText = totalPrice;
    cashLeft.innerText = cash - totalPrice;
    // update status
    if (cash >= totalPrice) {
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