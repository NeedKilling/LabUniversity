'use strict'


function rangeJs(start, end){
    let arr = [];
    for(start; start < end; start++){
        arr.push(start);     
    };
    return arr
};
console.log(`Задание 1. «Аналог range» \n\t${rangeJs(3,8)}`);


const numbers = [2,5,8,12,3];
function transform(arr){
    let squares = [];
    for(let i = 0; i < arr.length; i++){
        squares.push(arr[i]**2);
    }
    

    let counter = 0;
    let sum = 0;
    while(counter < arr.length){
        sum+=arr[counter]
        counter++;
        
    }

    console.log("\tarr =  "+squares);
    console.log("\tsum = "+sum);

    return

    
}
console.log(`Задание 2. «Трансформация массива» \n`)
transform(numbers)


console.log(`Задание 3. «Жизнь циклов»`)
function drawPyramid(height){
    let str = ""
    for(let i = 0; i < height; i++){
        str+="#"
        console.log(str)
        
    }
}
drawPyramid(6)



const students = [
    { name: "Макар", role: "teamlead", exp: 5 },
    { name: "Денис", role: "programmer", exp: 4 },
    { name: "Анна", role: "programmer", exp: 2 },
    { name: "Даша", role: "designer", exp: 1 }
];
function getExperienced(studentsList, minExp){
    let arr = [];


    for( let item of studentsList){
        if (item.exp >= minExp ){
            arr.push(item.name)
        }
    }
    return arr
}

console.log(`Задание 4. «Фильтрация» \n\t${getExperienced(students,3)}`)