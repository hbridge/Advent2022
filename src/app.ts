import { argv } from "process";

const dayNum = process.argv[2] ? Number(process.argv[2]) : 0;
const fs = require('fs');

const days = {
    0: () => 0, 
    1: function (prompt: string) {
        const elfChunks = prompt.split('\n\n');

        let maxFound = 0;
        for (const chunk of elfChunks) {
            const numbers = chunk.split("\n").map(str => Number(str));
            const elfCalories = numbers.reduce((prev, cur) => prev + cur, 0);
            maxFound = Math.max(elfCalories, maxFound);
        }

        return maxFound;
    },
    2: function (prompt: string) {
        const elfChunks = prompt.split('\n\n');

        let topThreeAsc = [0, 0, 0];
        for (const chunk of elfChunks) {
            const numbers = chunk.split("\n").map(str => Number(str));
            const elfCalories = numbers.reduce((prev, cur) => prev + cur, 0);
            
            let insertIndex = -1;
            let i = 0;
            while(elfCalories > topThreeAsc[i]) {
                insertIndex = i;
                i++;
            }

            if (insertIndex >= 0) {
                //insert the new elf value after the one it's bigger than
                topThreeAsc.splice(insertIndex + 1, 0, elfCalories);
                topThreeAsc.splice(0, 1); // discard the lowest
            }
        }

        return topThreeAsc.reduce((prev, cur) => prev + cur);
    }
}

function run (dayNum = Object.keys(days).length - 1) {
    console.log('\n*** Running day %d***', dayNum);
    const example = fs.readFileSync(`${process.cwd()}/data/day${dayNum}example.txt`);
    const input = fs.readFileSync(`${process.cwd()}/data/day${dayNum}data.txt`);

    console.log("Example result: %s", JSON.stringify(days[dayNum](example.toString())));
    console.log("Input result: %s\n", JSON.stringify(days[dayNum](input.toString())));
}

if (dayNum > 0) {
    run(dayNum);
} else {
    run();
}