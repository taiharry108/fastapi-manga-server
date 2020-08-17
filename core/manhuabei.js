var CryptoJS = require("crypto-js");
function wordToByteArray(wordArray) {
    var byteArray = [], word, i, j;
    for (i = 0; i < wordArray.length; ++i) {
        word = wordArray[i];
        for (j = 3; j >= 0; --j) {
            console.log(word);
            byteArray.push((word >> 8 * j) & 0xFF);
        }
    }
    console.log(byteArray);
    return byteArray;
}

function byteArrayToString(byteArray) {
    var str = "", i;
    for (i = 0; i < byteArray.length; ++i) {
        str += escape(String.fromCharCode(byteArray[i]));
    }
    return str;
}
console.log(byteArrayToString(wordToByteArray([1094861636, 1162228039, 859059251, 842097250]))
);