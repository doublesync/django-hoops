// some formatting for the badges
const badgeFormat = {0: "Unequipped", 1: "Bronze", 2: "Silver", 3: "Gold", 4: "Hall of Fame"};
const badgeEmojis = {0: "🚫", 1: "🟫", 2: "🌫️", 3: "🟨", 4: "🟪"};

// cart variables
let badgeUpgrades = document.getElementsByClassName("badgeUpgrade");
let attributeUpgrades = document.getElementsByClassName("attributeUpgrade");
let cartList = document.getElementById("cartList");
let confirmationPriceLabel = document.getElementById("confirmationPrice");

// show current badge level
window.onload = function() {
    for (let i = 0; i < badgeUpgrades.length; i++) {
        let currentIndex = badgeUpgrades[i];
        let badgeName = currentIndex.name;
        let badgeValue = badgeAttributes[badgeName];
        currentIndex.selectedIndex = 0;
        currentIndex.options[currentIndex.selectedIndex].text = `${badgeEmojis[badgeValue]}`;
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
    let cart = {};
    for (let i = 0; i < attributeUpgrades.length; i++) {
        // find the current index + level of attribute
        let currentIndex = attributeUpgrades[i];
        let futureAttribute = currentIndex.value;
        let currentAttribute = badgeAttributes[currentIndex.name];
        let timesUpgraded = Number(futureAttribute) - Number(currentAttribute)
        // recalculate the price
        if (futureAttribute > currentAttribute) {
            cost = timesUpgraded * attributePrices["Default"];
            cart[currentIndex.name] = [timesUpgraded, cost];
            price += cost;
        }
    }
    // return price
    return [price, cart];
}

// calculate price of badges in form
const calculateBadgePrice = function() {
    let price = 0;
    let cart = {};
    for (let i = 0; i < badgeUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = badgeUpgrades[i];
        let futureLevel = currentIndex.options[currentIndex.selectedIndex];
        let currentLevel = badgeAttributes[currentIndex.name]
        // recalculate the price
        if (futureLevel.value in badgePrices) {
            if (futureLevel.value > currentLevel) {
                cost = badgePrices[futureLevel.value];
                cart[currentIndex.name] = [futureLevel.value, cost];
                price += cost;
            }
        }
    }
    // return the price
    return [price, cart];
}

// update price on changes of attributes + badges
const updatePrice = function() {
    // calculate prices & fetch cart/s
    const attributeInfo = calculateAttributePrice();
    const attributePrice = attributeInfo[0];
    const attributeCart = attributeInfo[1];
    const badgeInfo = calculateBadgePrice();
    const badgePrice = badgeInfo[0];
    const badgeCart = badgeInfo[1];
    // get the total price
    const totalPrice = attributePrice + badgePrice;
    // update price & cash labels
    priceLabel.innerText = totalPrice;
    cashLeft.innerText = cash - totalPrice;
    // add attributes & badges to cart list
    buyingAttributes = Object.keys(attributeCart);
    buyingBadges = Object.keys(badgeCart);
    // add attributes to cart list
    cartList.innerText = ""; // first, reset the cart list
    buyingAttributes.forEach(name => {
        const quantity = attributeCart[name][0];
        const cost = attributeCart[name][1];   
        let listItem = document.createElement("li");
        listItem.innerText = `($${cost}) ${name}`;
        listItem.className = "list-group-item";
        cartList.appendChild(listItem); 
    });
    // add badges to cart list
    buyingBadges.forEach(name => {
        const value = badgeCart[name][0];
        const cost = badgeCart[name][1];
        let listItem = document.createElement("li");
        listItem.innerText = `($${cost}) ${badgeEmojis[value]} ${name}`;
        listItem.className = "list-group-item";
        cartList.appendChild(listItem);
    });
    // update confirmation modal price label
    confirmationPriceLabel.innerText = `$${totalPrice}`;
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