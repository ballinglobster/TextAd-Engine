const userInput = document.getElementById('user-input');
const gameOutput = document.getElementById('game-output');

let waspreviouscommandmove = false;
let currentLocation = "starting point";

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
            const response = decideNextAction(command);
            const paragraph = document.createElement("p");
            paragraph.className = "command-response";
            paragraph.textContent = response;
            gameOutput.appendChild(paragraph);
            userInput.value = "";
        }
    }
});

// Initial game message
const initialMessage = "Welcome to the Text-Based Adventure Game! Type your commands below to begin your journey.";
const initialParagraph = document.createElement("p");
initialParagraph.textContent = initialMessage;
gameOutput.appendChild(initialParagraph);

// Implement game data
// (location, items, inventory, objects, scenery (unmoveable objects), starting point, commands, descriptions, characters, choices)
const gameData = 
{
    locations: 
    {
        "starting point": 
        {
            description: "You are at the starting point of your adventure. There is a path leading north.",
            items: ["map"],
            objects: ["signpost"],
            scenery: ["trees"],
            characters: ["Narrator"],
            choices: ["go north", "look around"],
            locations:
            {
                "north": "forest"
            }
        },
        "forest":
        {
            description: "You are in a dense forest. The trees tower above you, and you can hear the sounds of wildlife all around.",
            items: [],
            objects: [],
            scenery: ["trees", "bushes"],
            characters: [],
            choices: ["go south", "look around"]
        }
    },
    items:
    {
        "map":
        {
            commands: ["examine", "take"],
            description: "A worn-out map showing the layout of the surrounding area."
        }
    },
    objects:
    {
        "signpost":
        {
            commands: ["examine"],
            description: "A wooden signpost with directions to nearby locations."
        }
    },
    characters:
    {
        "narrator":
        {
            dialogue: ["Welcome to your adventure!"],
            commands: ["talk to"],
            description: "You feel the presence of the narrator."
        }
    },
    inventory: 
    {
        items: 
        [
            
        ]
    }
}

function getCurrentLocation()
{
    return currentLocation;
}

function getLocationDescription(location)
{
    const locationData = gameData.locations[location];
    checkLocationForItemsETC(location);
    if (locationData.items.length > 0)
    {
        // gameOutput.appendChild(document.createElement("p")).textContent = "You see the following items: " + locationData.items.join(", ");
        for (const item of locationData.items)
        {
            const itemData = gameData.items[item.toLowerCase()];
            const description = itemData.description.toLowerCase();
            gameOutput.appendChild(document.createElement("p")).textContent = "You see " + description;
        }
    }
    if (locationData.objects.length > 0)
    {
        // gameOutput.appendChild(document.createElement("p")).textContent = "You notice the following objects: " + locationData.objects.join(", ");
        for (const object of locationData.objects)
        {
            const objectData = gameData.objects[object.toLowerCase()];
            const description = objectData.description.toLowerCase();
            gameOutput.appendChild(document.createElement("p")).textContent = "You notice " + description;
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
            gameOutput.appendChild(document.createElement("p")).textContent = characterData.description;
        }
    }
    // if (locationData.choices.length > 0)
    // {
    //     gameOutput.appendChild(document.createElement("p")).textContent = "Available choices: " + locationData.choices.join(", ");
    // }
    if (locationData.locations)
    {
        gameOutput.appendChild(document.createElement("p")).textContent = "Exits: " + Object.keys(locationData.locations).join(", ");
    }
    return locationData.description;
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
    
}

function moveToLocation(location)
{
    // update player's current location
    currentLocation = location;
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