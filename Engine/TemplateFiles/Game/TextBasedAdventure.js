const userInput = document.getElementById('user-input');
const gameOutput = document.getElementById('game-output');

let waspreviouscommandmove = false;
let currentLocation = "main menu";

let commandHistory = [];
let historyIndex = -1;

userInput.addEventListener('keydown', function(event)
{
    if (event.key === 'Enter')
    {
        // const command = userInput.value.trim();
        // if (command)
        // {
        //     if (waspreviouscommandmove === true)
        //     {
        //         const paragraphtoRemove = gameOutput.querySelectorAll("p.command-response");
        //         paragraphtoRemove[paragraphtoRemove.length - 1].remove();
        //         waspreviouscommandmove = false;
        //     }
        //     const response = "you entered: " + command;
        //     const paragraph = document.createElement("p");
        //     paragraph.className = "command-response";
        //     paragraph.textContent = response;
        //     gameOutput.appendChild(paragraph);
        //     userInput.value = "";
        //     waspreviouscommandmove = true;
        // }
        
        const command = userInput.value.trim();
        if (command)
        {
            const commandParagraph = document.createElement("p");
            commandParagraph.className = "user-command";
            commandParagraph.textContent = "> " + command;
            gameOutput.appendChild(commandParagraph);
            const response = decideNextAction(command);
            const paragraph = document.createElement("p");
            paragraph.className = "command-response";
            paragraph.textContent = response;
            gameOutput.appendChild(paragraph);
            userInput.value = "";
        }
    }
});


// Implement game data
// (location, items, inventory, objects, scenery (unmoveable objects), starting point, commands, descriptions, characters, choices)
const gameData = {
    "locations": {
        "main menu": {
            "image": "Images/Location Images/main_menu.png",
            "description": "You are at the main menu. Type 'start' to begin your adventure.",
            "items": [],
            "objects": [],
            "scenery": [],
            "characters": [],
            "choices": ["start"],
            "connected-locations": {}
        },
        "starting point": {
            "image": "Images/Location Images/starting_point.png",
            "description": "You are at the starting point of your adventure. There is a path leading north.",
            "items": ["map"],
            "objects": ["signpost"],
            "scenery": ["trees"],
            "characters": ["Narrator"],
            "choices": ["go north", "look around"],
            "connected-locations": {
                "north": "forest"
            }
        },
        "forest": {
            "image": "Images/Location Images/forest.jpg",
            "description": "You are in a dense forest. The trees tower above you, and you can hear the sounds of wildlife all around.",
            "items": [],
            "objects": [],
            "scenery": ["trees", "bushes"],
            "characters": [],
            "choices": ["go south", "look around"],
            "connected-locations": {
                "south": "starting point"
            }
        }
    },
    "items": {
        "map": {
            "commands": ["examine", "take"],
            "description": "A worn-out map showing the layout of the surrounding area."
        }
    },
    "objects": {
        "signpost": {
            "commands": ["examine"],
            "description": "A wooden signpost with directions to nearby locations."
        }
    },
    "characters": {
        "narrator": {
            "dialogue": ["Welcome to your adventure!"],
            "commands": ["talk to"],
            "description": "You feel the presence of the narrator."
        }
    },
    "inventory": {
        "items": []
    }
};

// Init game
initialiseGame();

function initialiseGame()
{
    if (getCurrentLocation() !== "main menu") return;
    moveToLocation("main menu");
}

function getCurrentLocation()
{
    return currentLocation;
}

function getLocationDescription(location)
{
    const locationData = gameData.locations[location];
    const descParagraph = document.createElement("p");
    descParagraph.className = "location-description";
    descParagraph.textContent = locationData.description;
    gameOutput.appendChild(descParagraph);

    checkLocationForItemsETC(location);
    if (locationData.items.length > 0)
    {
        // gameOutput.appendChild(document.createElement("p")).textContent = "You see the following items: " + locationData.items.join(", ");
        for (const item of locationData.items)
        {
            const itemData = gameData.items[item.toLowerCase()];
            const description = itemData.description.toLowerCase();
            const itemParagraph = document.createElement("p");
            itemParagraph.className = "location-description";
            itemParagraph.textContent = "You see " + description;
            gameOutput.appendChild(itemParagraph);
        }
    }
    if (locationData.objects.length > 0)
    {
        // gameOutput.appendChild(document.createElement("p")).textContent = "You notice the following objects: " + locationData.objects.join(", ");
        for (const object of locationData.objects)
        {
            const objectData = gameData.objects[object.toLowerCase()];
            const description = objectData.description.toLowerCase();
            const objectParagraph = document.createElement("p");
            objectParagraph.className = "location-description";
            objectParagraph.textContent = "You notice " + description;
            gameOutput.appendChild(objectParagraph);
        }
    }
    // if (locationData.scenery.length > 0)
    // {
    //     // gameOutput.appendChild(document.createElement("p")).textContent = "The scenery includes: " + locationData.scenery.join(", ");
    //     for (const sceneryItem of locationData.scenery)
    //     {
    //         gameOutput.appendChild(document.createElement("p")).textContent = "You see " + sceneryItem.toLowerCase() + " around you.";
    //     }
    // }
    if (locationData.characters.length > 0)
    {
        // gameOutput.appendChild(document.createElement("p")).textContent = "You see the following characters: " + locationData.characters.join(", ");
        for (const character of locationData.characters)
        {
            const characterData = gameData.characters[character.toLowerCase()];
            const characterParagraph = document.createElement("p");
            characterParagraph.className = "location-description";
            characterParagraph.textContent = characterData.description;
            gameOutput.appendChild(characterParagraph);
        }
    }
    // if (locationData.choices.length > 0)
    // {
    //     gameOutput.appendChild(document.createElement("p")).textContent = "Available choices: " + locationData.choices.join(", ");
    // }
    if (locationData.locations)
    {
        const exitsParagraph = document.createElement("p");
        exitsParagraph.className = "exits-description";
        exitsParagraph.textContent = "Exits: " + Object.keys(locationData.locations).join(", ");
        gameOutput.appendChild(exitsParagraph);
    }
}

function checkAvailableChoices(location)
{
    return gameData.locations[location].choices;
}


function getItemDescription(item)
{
    return gameData.items[item].description;
}

function getObjectDescription(object)
{
    return gameData.objects[object].description;
}

function getCharacterDialogue(character)
{
    return gameData.characters[character].dialogue;
}

function decideNextAction(command)
{
    // check command against gameData and return appropriate response
    const lowerCommand = command.toLowerCase();
    if (lowerCommand === "look around")
    {
        // describe current location
        return getLocationDescription(getCurrentLocation());
    }
    else if (lowerCommand === "go north" || lowerCommand === "go south" || lowerCommand === "go east" || lowerCommand === "go west")
    {
        // check if movement is possible
        const choices = checkAvailableChoices(getCurrentLocation());
        const currentLocation = getCurrentLocation();
        if (choices.includes(command))
        {
            // move to new location
            const direction = command.split(" ")[1];
            const newLocation = gameData.locations[currentLocation].locations[direction];
            return moveToLocation(newLocation);
        }
        else
        {
            return "You can't go that way.";
        }
    }
    else if (lowerCommand.startsWith("talk to "))
    {
        const character = command.substring(8).trim();
        return talkToCharacter(character);
    }
    else if (lowerCommand.startsWith("examine "))
    {
        // const object = command.substring(8).trim();
        // const item = command.substring(8).trim();
        // return getItemDescription(item);
        const target = command.substring(8).trim();
        if (gameData.items[target])
        {
            return getItemDescription(target);
        }
        else if (gameData.objects[target])
        {
            return getObjectDescription(target);
        }
    }
    else if (lowerCommand === "start" && getCurrentLocation() === "main menu")
    {
        return moveToLocation("starting point");
    }
    else
    {
        return "You can't do that.";
    }
    
}

function moveToLocation(location)
{
    // update player's current location
    currentLocation = location;
    removeCommandResponseParagraphs();
    addImageForLocation(location);
    return getLocationDescription(location);
}

function talkToCharacter(character)
{
    return getCharacterDialogue(character);
}

function checkLocationForItemsETC(location)
{
    const locationData = gameData.locations[location];
    return {
        items: locationData.items,
        objects: locationData.objects,
        scenery: locationData.scenery,
        characters: locationData.characters
    };
}

function removeCommandResponseParagraphs()
{
    // Remove responses
    const paragraphsToRemove = gameOutput.querySelectorAll("p.command-response");
    paragraphsToRemove.forEach(paragraph => paragraph.remove());

    // remove user commands
    const userCommandParagraphs = gameOutput.querySelectorAll("p.user-command");
    userCommandParagraphs.forEach(paragraph => paragraph.remove());

    // remove location description paragraphs
    const locationDescriptionParagraphs = gameOutput.querySelectorAll("p.location-description");
    locationDescriptionParagraphs.forEach(paragraph => paragraph.remove());

    // remove exits description paragraphs
    const exitsDescriptionParagraphs = gameOutput.querySelectorAll("p.exits-description");
    exitsDescriptionParagraphs.forEach(paragraph => paragraph.remove());
}

function addImageForLocation(location)
{
    const locationData = gameData.locations[location];

    // remove previous location images
    const previousImages = gameOutput.querySelectorAll("img");
    previousImages.forEach(image => image.remove());

    if (!locationData.image) return;
    // make sure to add the new image at the top of page
    const locationImage = document.createElement("img");
    locationImage.src = locationData.image;
    locationImage.alt = location + " image";
    gameOutput.insertBefore(locationImage, gameOutput.firstChild);
    
}