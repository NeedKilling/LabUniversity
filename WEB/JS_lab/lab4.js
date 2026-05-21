"use strict"

function calculatePrice(price, tax){
    return price + (price*tax);
}
const cart = []
function addToCart(name){
    cart.push(name)
    console.log(`arr ${cart}`)
    return cart
}

console.log(calculatePrice(10, 0.2))
addToCart("name")


function factorial(n){
    
    if(n == 0){
        return 1
    }
    if(n < 0){
        return null
    }
    return n * factorial(n-1)
}
console.log(`Задание 2 ~~~ ${factorial(3)}`)


function squaresNumber(arr){
    return arr.filter((item)=>item > 10).map((item)=>item**2)
}
console.log(`Задание 3 ~~~ ${squaresNumber([5,12,8,130,44,3])}`)


function allPrice(arr){
    return arr.reduce((acum,item)=>acum + item.price * item.quantity,0)
}
console.log(`Задание 4 ~~~ ${allPrice([
    { product: "Ноутбук", price: 50000, quantity: 1 },
    { product: "Мышь", price: 1500, quantity: 2 },
    { product: "Клавиатура", price: 3000, quantity: 1 }
])}`)


function multiply(a){
  const inner = (b) => multiply(a * b);
  inner[Symbol.toPrimitive] = () => a;
  return inner;
};

console.log(`Задание 5 ~~~ ${multiply(2)(3)} ${multiply(2)(3)(4)}`);    // 6
