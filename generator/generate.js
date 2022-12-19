import fs from "fs";

const seriesSize = 9999;

// create a table of rarities
// the weights al need to add up to 1
// the modifier changes the chance of rolling rarer items in the table
// Common, Uncommon, Rare, Epic, Legendary, Epic, Omni

const rarities = [
  { value: "Common", weight: 0.5, modifier: 1 },
  { value: "Uncommon", weight: 0.3, modifier: 1.5 },
  { value: "Rare", weight: 0.1, modifier: 2 },
  { value: "Epic", weight: 0.0125, modifier: 3 },
  { value: "Legendary", weight: 0.025, modifier: 4 },
];

// create a table of rarity modifiers, using nomenclature from the game
// the modifier changes the chance of rolling rarer items in the table
// Recruit, Initiate, Veteran, Elite, Champion, Hero, Legend
const rarityModifier = [
  { value: "Common", rarity: rarities[0], gearScore: [0, 0, 0, 0, 0, 0] },
  { value: "Uncommon", rarity: rarities[1], gearScore: [1, 1, 0, 0, 0, 0] },
  { value: "Rare", rarity: rarities[2], gearScore: [1, 0, 0, 1, 1, 0] },
  { value: "Epic", rarity: rarities[3], gearScore: [1, 1, 1, 1, 1, 1] },
  { value: "Legendary", rarity: rarities[4], gearScore: [1, 1, 1, 2, 1, 1] },
];

const BladeColor = [
  { value: "Blue", rarity: rarities[0], gearScore: [0, 1, 1, 0, 0, 0] },
  { value: "Green", rarity: rarities[0], gearScore: [0, 0, 0, 1, 1, 0] },
  { value: "Red", rarity: rarities[0], gearScore: [1, 0, 1, 0, 0, 0] },
  { value: "Yellow", rarity: rarities[0], gearScore: [0, 1, 0, 0, 1, 0] },
  { value: "Orange", rarity: rarities[1], gearScore: [0, 0, 1, 1, 1, 0] },
  { value: "Cyan", rarity: rarities[1], gearScore: [1, 1, 0, 0, 1, 0] },
  { value: "Purple", rarity: rarities[1], gearScore: [0, 1, 1, 1, 0, 0] },
  { value: "Pink", rarity: rarities[2], gearScore: [0, 0, 1, 1, 1, 1] },
  { value: "Silver", rarity: rarities[2], gearScore: [1, 1, 1, 1, 0, 0] },
  { value: "White", rarity: rarities[3], gearScore: [0, 3, 1, 1, 1, 1] },
  { value: "Black", rarity: rarities[3], gearScore: [3, 0, 1, 1, 1, 1] },
]

// gearScores are [attack, defense, vitality, spirit, dexterity, luck]
const EmitterType = [
  { value: "Inquisitor", rarity: rarities[0], gearScore: [0, 0, 0, 1, 0, 0] },
  { value: "Avenger", rarity: rarities[0], gearScore: [1, 0, 0, 0, 0, 0] },
  { value: "Defender", rarity: rarities[0], gearScore: [0, 1, 0, 0, 0, 0] },
  { value: "Paladin", rarity: rarities[0], gearScore: [0, 0, 1, 0, 0, 0] },
  { value: "Redeemer", rarity: rarities[0], gearScore: [0, 0, 0, 0, 0, 1] },
  { value: "Devastator", rarity: rarities[0], gearScore: [2, 0, 0, 0, 0, 0] },
  { value: "Zealot", rarity: rarities[0], gearScore: [1, 0, 0, 1, 0, 0] },
  { value: "Sentinel", rarity: rarities[0], gearScore: [0, 0, 1, 1, 0, 0] },
  { value: "Protector", rarity: rarities[1], gearScore: [0, 1, 1, 0, 0, 0] },
  { value: "Crusader", rarity: rarities[1], gearScore: [1, 0, 0, 1, 0, 0] },
  { value: "Templar", rarity: rarities[1], gearScore: [0, 0, 1, 0, 1, 0] },
  { value: "Seer", rarity: rarities[1], gearScore: [0, 0, 0, 0, 0, 2] },
  { value: "Silencer", rarity: rarities[1], gearScore: [0, 0, 0, 2, 0, 0] },
  { value: "Liberator", rarity: rarities[1], gearScore: [0, 0, 2, 0, 0, 0] },
  { value: "Guardian", rarity: rarities[1], gearScore: [0, 2, 1, 0, 0, 0] },
  { value: "Exemplar", rarity: rarities[2], gearScore: [0, 0, 0, 0, 2, 1] },
  { value: "Vindicator", rarity: rarities[2], gearScore: [0, 2, 0, 1, 0, 0] },
  { value: "Vigilante", rarity: rarities[2], gearScore: [2, 0, 0, 1, 0, 0] },
  { value: "Vanquisher", rarity: rarities[2], gearScore: [1, 1, 1, 0, 0, 0] },
  { value: "Conqueror", rarity: rarities[2], gearScore: [1, 0, 0, 1, 0, 1] },
  { value: "Steward", rarity: rarities[3], gearScore: [0, 2, 1, 1, 0, 0] },
  { value: "Warden", rarity: rarities[3], gearScore: [0, 1, 1, 0, 1, 1] }
];

const SwitchType = EmitterType

const HandleType = EmitterType

const ColorScheme = [
  { value: "BlackSilver", rarity: rarities[0], gearScore: [0, 0, 0, 0, 0, 0] },
  { value: "SilverBronze", rarity: rarities[0], gearScore: [0, 0, 0, 0, 0, 0] },
  { value: "BlackGold", rarity: rarities[1], gearScore: [0, 0, 0, 0, 0, 1] },
  { value: "WhiteSilver", rarity: rarities[1], gearScore: [0, 0, 0, 0, 1, 0] },
  { value: "RedSilver", rarity: rarities[1], gearScore: [1, 0, 0, 0, 0, 0] },
  { value: "YellowBlack", rarity: rarities[2], gearScore: [1, 0, 0, 0, 1, 0] },
  { value: "PinkWhite", rarity: rarities[2], gearScore: [0, 1, 0, 0, 1, 1] },
  { value: "Gold", rarity: rarities[3], gearScore: [0, 0, 1, 1, 1, 1] }
];

const getTableOutput = (randomNumber, table, min = 0) => {
  let totalVal;
  totalVal = table.reduce((a, b) => a + b.rarity.weight, 0);

  const adjustedVal = totalVal - min;
  const roll = randomNumber * adjustedVal + min;

  for (let i = 0; i < table.length; i++) {
    if (i === 0) table[i]["min"] = 0;
    else
      table[i]["min"] = table
        .slice(0, i)
        .reduce((a, b) => a + b.rarity.weight, 0);
    if (i === table.length - 1) table[i]["max"] = totalVal + 1000;
    else
      table[i]["max"] = table
        .slice(0, i + 1)
        .reduce((a, b) => a + b.rarity.weight, 0);
  }

  const output = table.find((x) => roll >= x["min"] && roll <= x.max);

  return output;
};

let alreadyCreated = [];

/**
 * Return random int from 0 -> max
 *  @param {number} max - max
 *  @return {number} randomized number in range
 */
function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

/** 
*  Return initial randomized array with rules,
*  
*  - Composed of array representing [attack, defense, vitality, spirit, dexterity, luck]
*  - Each stat starts at 2, except luck
*  - Randomly assign 9 free points to attributes except luck 
*  - The sum of attributes must equal 21  
*  @return {Array} initialStats
*/

function generateInitialStats() {
  let pointsToSpend = 9;
  let maxAttributeScore = 7;
  let initialStatsSum = 21;
  // initialize stats to 2, except luck
  let initialStats = [2, 2, 2, 2, 2, 2, 0];
  while (pointsToSpend) {
    // select stat that isn't luck
    let index = getRandomInt(initialStats.length - 1)
    // if stat is at max retry increment
    if (initialStats[index] === maxAttributeScore) {
      continue;
    } else {
      initialStats[index]++;
      pointsToSpend--;
    }
  }
  // initial stats must equal 21
  console.assert(initialStats.reduce((a, b) => a + b, 0) === initialStatsSum, "Initial stats sum failed with values " + initialStats);
  return initialStats;
}

function generateStats() {
  // Rarity modifier
  let rarity = getTableOutput(Math.random(), rarityModifier);
  console.log('rarity: ', rarity.value, ' | ', rarity.gearScore, ' | ', rarity.rarity.value, ' | ', rarity.rarity.weight, ' | ', rarity.rarity.modifier, ' |')
  const fixedRarityModifier = rarities.find(
    (x) => x.value === rarity.value
  ).modifier - 1; // subtract one to normalize and account for base 1

  const bladeColor = getTableOutput(Math.random(), BladeColor, fixedRarityModifier);

  const emitterType = getTableOutput(Math.random(), EmitterType, fixedRarityModifier);

  const switchType = getTableOutput(Math.random(), SwitchType, fixedRarityModifier);

  const handleType = getTableOutput(Math.random(), HandleType, fixedRarityModifier);

  const colorScheme = getTableOutput(Math.random(), ColorScheme, fixedRarityModifier);

    let name = [switchType.value];

    if (emitterType.value !== bladeColor.value) {
      name.push(emitterType.value);
    }
    
    // if name doesn't include handleType.value, add it
    if (!name.includes(handleType.value)) {
      name.push(handleType.value);
    }

    const formattedName = name.join(" ");

    let hash = `${bladeColor.value} "${formattedName}" (${rarity.value})`;

  //[attack, defense, vitality, spirit, dexterity, luck]
  let baseStats = generateInitialStats();

  // Collect equipment values
  var gearScores = [
    bladeColor?.gearScore ?? 0,
    emitterType?.gearScore ?? 0,
    switchType.gearScore,
    handleType?.gearScore ?? 0,
    colorScheme?.gearScore ?? 0,
  ];

  gearScores.push(baseStats);

  // Vertical sum array
  var sum = (r, a) => 
    r.map((b, i) => { 
      return (a[i] + b);
  });
  var gearStats = gearScores.reduce(sum);

  const cryptosaber = {
    description: "",
    external_url: "",
    image: "",
    name: hash,
    attributes: [
      {
        trait_type: "bladeColor",
        value: bladeColor.value,
      },
      {
        trait_type: "emitterType",
        value: emitterType.value,
      },
      {
        trait_type: "switchType",
        value: switchType.value,
      },
      {
        trait_type: "handleType",
        value: handleType.value,
      },
      {
        trait_type: "colorScheme",
        value: colorScheme.value,
      },
      {
        trait_type: "attack",
        value: gearStats[0]
      },
      {
        trait_type: "defense",
        value: gearStats[1]
      },
      {
        trait_type: "vitality",
        value: gearStats[2]
      },
      {
        trait_type: "spirit",
        value: gearStats[3]
      },
      {
        trait_type: "dexterity",
        value: gearStats[4]
      },
      {
        trait_type: "luck",
        value: gearStats[6]
      },
    ],
    rarity: rarity.value
  };

  alreadyCreated.push(cryptosaber);

  return cryptosaber;
}

const series = [];
// How many cryptosabers to generate in the series?

for (let i = 0; i < seriesSize; i++) {
  const cryptosaber = generateStats();

  if (!cryptosaber.duplicate) series.push(cryptosaber);
}

console.log("cryptosaber", series)

const seriesFiltered = [];
series.forEach((cryptosaber) => {
  const newSaber = { ...cryptosaber };
  delete newSaber["duplicate"];
  delete newSaber["hash"];
  delete newSaber["rarity"];
  seriesFiltered.push(newSaber);
});

console.log(
  "Made a series with",
  seriesSize,
  "attempted. Generated",
  seriesFiltered.length,
  "cryptosabers"
);
if (seriesFiltered.length < seriesSize) {
  console.log(
    "Try adding more unique options to generators to increase likelihood of successful generation"
  );
}

const data = JSON.stringify(seriesFiltered);

fs.writeFileSync("data.json", data);
