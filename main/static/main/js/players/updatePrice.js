// some formatting for the badges
const badgeFormat = {0: "Unequipped", 1: "Bronze", 2: "Silver", 3: "Gold", 4: "Hall of Fame"};
const badgeEmojis = {0: "🚫", 1: "🟫", 2: "🌫️", 3: "🟨", 4: "🟪"};

// cart variables
let badgeUpgrades = document.getElementsByClassName("badgeUpgrade");
let attributeUpgrades = document.getElementsByClassName("attributeUpgrade");
let tendencyUpgrades = document.getElementsByClassName("tendencyUpgrade");
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

// attribute price tiers
attributePriceRanges = {
    "60-70": [0, 70],
    "71-80": [71, 80],
    "81-86": [81, 86],
    "87-93": [87, 93],
    "94-96": [94, 96],
    "97-99": [97, 99],
}

// calculate price of attributes in the form
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
            let cost = 0;
            for (let i = (currentAttribute + 1); i < Number(futureAttribute) + 1; i++) {
                if (i >= 100) { break };
                for (const [tier, value] of Object.entries(attributePriceRanges)) {
                    if (i >= value[0] && i <= value[1]) {
                        console.log(`${i} was found inside ${tier} (${value[0]}/${value[1]})`);
                        if (primaryAttributes.includes(currentIndex.name)) {
                            cost += attributePrices[tier]["primary"];
                        } else if (secondaryAttributes.includes(currentIndex.name)) {
                            cost += attributePrices[tier]["secondary"];
                        } else {
                            cost += attributePrices[tier]["base"];
                        }
                    }
                }
            }
            cart[currentIndex.name] = [timesUpgraded, cost];
            price += cost;
        }
    }
    // return price
    return [price, cart];
}

// calculate price of badges in the form
const calculateBadgePrice = function() {
    let price = 0;
    let cart = {};
    for (let i = 0; i < badgeUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = badgeUpgrades[i];
        let futureLevel = currentIndex.options[currentIndex.selectedIndex].value;
        let currentLevel = badgeAttributes[currentIndex.name]
        let timesUpgraded = Number(futureLevel) - Number(currentLevel)
        // recalculate the price
        if (Number(futureLevel) > currentLevel) {
            let cost = 0;
            // for loop to calculate the price of the badge
            for (let i = (currentLevel + 1); i < Number(futureLevel) + 1; i++) {
                // break the loop at the max badge level
                if (i >= 5) { break };
                // loop through the badge prices
                for (const [tier, value] of Object.entries(badgePrices)) {
                    // if the badge level is equivalent to the index of the tier
                    if (i == tier) {
                        // check which traits the user has, and use the price for those traits
                        if (traitOneBadges.includes(currentIndex.name)) {
                            cost += value["trait_one"];
                        } else if (traitTwoBadges.includes(currentIndex.name)) {
                            cost += value["trait_two"];
                        } else {
                            cost += value["base"];
                        }
                    }
                }
            }
            cart[currentIndex.name] = [timesUpgraded, cost];
            price += cost;
        }
    }
    // return the price
    return [price, cart];
}

// calculate price of badges in the form
const calculateTendencyPrice = function() {
    console.log("Calculating price");
    let price = 0;
    let cart = {};
    for (let i = 0; i < tendencyUpgrades.length; i++) {
        // find the current index + level of badge
        let currentIndex = tendencyUpgrades[i];
        let futureLevel = currentIndex.value;
        let currentLevel = badgeAttributes[currentIndex.name]
        let timesUpgraded = Number(futureLevel) - Number(currentLevel)
        // recalculate the price
        if (Number(futureLevel) > currentLevel) {
            cost = timesUpgraded;
            price += cost;
            cart[currentIndex.name] = [timesUpgraded, cost];
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
    const tendencyInfo = calculateTendencyPrice();
    const tendencyPrice = tendencyInfo[0];
    const tendencyCart = tendencyInfo[1];
    // get the total price
    const totalPrice = attributePrice + badgePrice + tendencyPrice;
    // update price & cash labels
    priceLabel.innerText = totalPrice;
    cashLeft.innerText = cash - totalPrice;
    // add attributes & badges to cart list
    buyingAttributes = Object.keys(attributeCart);
    buyingBadges = Object.keys(badgeCart);
    buyingTendencies = Object.keys(tendencyCart);
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
    // add tendencies to cart list
    buyingTendencies.forEach(name => {
        const quantity = tendencyCart[name][0];
        const cost = tendencyCart[name][1];   
        let listItem = document.createElement("li");
        listItem.innerText = `($${cost}) ${name}`;
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