data = [
    ("create a function to add two numbers", "function add(a, b) { return a + b; }"),
    (
        "create a function to subtract two numbers",
        "function subtract(a, b) { return a - b; }",
    ),
    (
        "create a function to multiply two numbers",
        "function multiply(a, b) { return a * b; }",
    ),
    (
        "create a function to divide two numbers",
        "function divide(a, b) { return a / b; }",
    ),
    (
        "create a function to return the square of a number",
        "function square(a) { return a * a; }",
    ),
    (
        "create a function to return the cube of a number",
        "function cube(a) { return a * a * a; }",
    ),
    (
        "create a function to find the maximum of two numbers",
        "function max(a, b) { return a > b ? a : b; }",
    ),
    (
        "create a function to find the minimum of two numbers",
        "function min(a, b) { return a < b ? a : b; }",
    ),
    (
        "create a function to check if a number is even",
        "function isEven(num) { return num % 2 === 0; }",
    ),
    (
        "create a function to check if a number is odd",
        "function isOdd(num) { return num % 2 !== 0; }",
    ),
    (
        "create a function to calculate the factorial of a number",
        "function factorial(n) { if (n === 0) return 1; else return n * factorial(n - 1); }",
    ),
    (
        "create a function to check if a string is a palindrome",
        "function isPalindrome(str) { return str === str.split('').reverse().join(''); }",
    ),
    (
        "create a function to reverse a string",
        "function reverseString(str) { return str.split('').reverse().join(''); }",
    ),
    (
        "create a function to find the length of a string",
        "function stringLength(str) { return str.length; }",
    ),
    (
        "create a function to convert a string to uppercase",
        "function toUpperCase(str) { return str.toUpperCase(); }",
    ),
    (
        "create a function to convert a string to lowercase",
        "function toLowerCase(str) { return str.toLowerCase(); }",
    ),
    (
        "create a function to find the sum of an array of numbers",
        "function sumArray(arr) { return arr.reduce((a, b) => a + b, 0); }",
    ),
    (
        "create a function to find the product of an array of numbers",
        "function productArray(arr) { return arr.reduce((a, b) => a * b, 0); }",
    ),
    (
        "create a function to find the average of an array of numbers",
        "function averageArray(arr) { return arr.reduce((a, b) => a + b, 0) / arr.length; }",
    ),
    (
        "create a function to sort an array of numbers in ascending order",
        "function sortAscending(arr) { return arr.sort((a, b) => a - b); }",
    ),
    (
        "create a function to sort an array of numbers in descending order",
        "function sortDescending(arr) { return arr.sort((a, b) => b - a); }",
    ),
    (
        "create a function array",
        "function createArrayOfObjects() {let array = [];for (let i = 0; i < 10; i++) {array.push({});}return array;}",
    ),
    (
        "create a function to find the index of an element in an array",
        "function indexOf(arr, element) {return arr.indexOf(element);}",
    ),
    (
        "create a function to find the last index of an element in an array",
        "function lastIndexOf(arr, element) {return arr.lastIndexOf(element);}",
    ),
    (
        "create a function to capitalize words in a string",
        "function capitalizeWords(str) {return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');}",
    ),
    (
        "This function takes a string as input and returns a new string with the first letter of each",
        "const capitalizeWords = (str) => {return str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');};",
    ),
    (
        "create a function to find the first occurrence of a substring in a string",
        "function findSubstring(str, substring) {return str.indexOf(substring);}",
    ),
    (
        "create a function to find the last occurrence of a substring in a string",
        "function findLastSubstring(str, substring) {return str.lastIndexOf(substring);}",
    ),
    (
        "create a function to find the number of occurrences of a substring in a string",
        "function countSubstring(str, substring) {return str.split(substring).length - 1;}",
    ),
]
