"use strict"

function calculateDiscountedPrice(price, discount){
    if(discount){
        return price - (price * (discount / 100)) 
    }else{
        return price
    }
}
console.log(`Задание 1 ~~~ ${calculateDiscountedPrice(500, 25)}`)

const result = function isEven(number){
    return number%2 == 0
}

console.log(`Задание 2 ~~~ ${result(2)}`)


const formatName = (lastName="", name = "")=>{
    
    if(name && lastName){
        return `${lastName}, ${name}`;
    }else if(lastName){
         return `Уважаемый(ая) ${lastName}`;
    }else{
        return "Anonim";
    }
}
console.log(`Задание 3 ~~~ ${formatName()}`);


const add = (a,b)=>a+b;
const subtract = (a,b) => a-b
const multiply = (a,b) => a*b

function mathOperation(a,b, fun){
    return fun(a,b)
}
console.log(`Задание 4 ~~~ ${mathOperation(2,3,multiply)}`)


function createGreating(text){
    return (name)=>`${text} ${name}`
}

const greeting = createGreating("Доброе утро")
console.log(`Задание 5 ~~~ ${greeting("Иван")}`)
