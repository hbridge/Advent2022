const fs = require('fs');

const DAY_NUM = 1;

function run () {
    console.log('\n*** Running day %d***', DAY_NUM);
    const example = fs.readFileSync(`${process.cwd()}/data/day${DAY_NUM}example.txt`);
    const input = fs.readFileSync(`${process.cwd()}/data/day${DAY_NUM}data.txt`);

    console.log("Example result: %d", solve(example.toString()));
    console.log("Input result: %d\n", solve(input.toString()));
}

function solve(prompt: string): number {
    let maxFound = 0;

    const elfChunks = prompt.split('\n\n');
    for (const chunk of elfChunks) {
        const numbers = chunk.split("\n").map(str => Number(str));
        const elfCalories = numbers.reduce((prev, cur) => prev + cur, 0);
        maxFound = Math.max(elfCalories, maxFound);
    }

    return maxFound;
}


module.exports.run = run;