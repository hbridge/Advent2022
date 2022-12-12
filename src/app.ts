import { argv } from "process";

const glob = require('glob');
const days = [];

const mode = process.argv[2] || 'all';

glob.sync(__dirname + '/days/*.js').forEach(
    file => days.push(require(file))
);

if (mode == 'last') {
    days[days.length - 1].run();
}

for (let day of days) {
    day.run();
}

