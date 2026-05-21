"use strict"
console.log("Задание 1. Создание объектов и работа со свойствами\n")
const Book =  {
    title: 'title',
    author: 'author',
    year: 2026,
    pages: 1,

    getInfo(){
        console.log(this.title,this.author,this.year,this.pages)
    }
}
Book.getInfo()

const features = ["perevod","pages"]
Book[features[0]] = "молодец"
delete Book.pages

console.log("perevod" in Book)
console.log(Book.hasOwnProperty("pages"))


console.log("\nЗадание 2. Функция-конструктор и ключевое слово new\n")

function Student(name,group,grades){
    this.name = name
    this.group = group
    this.grades = grades
}

Student.prototype.getAverage = function(){
    if(this.grades){
        return this.grades.reduce((acum,item) => acum + item,0) / this.grades.length
    }else{
        return 0
    }
}
Student.prototype.isPassed = function(){
    return this.getAverage() >= 60
}

const Student1 = new Student("ivan","1", [90,75,60,80])
const Student2 = new Student("livan","2", [50,45,80])
const Student3 = new Student("karam","3", [30,60])

console.log(Student1)
console.log(Student2)
console.log(Student3)
console.log(`${Student1.name}: средний балл = ${Student1.getAverage().toFixed(2)} сдал ${Student1.isPassed()}`);
console.log(`${Student2.name}: средний балл = ${Student2.getAverage().toFixed(2)} сдал ${Student2.isPassed()}`);
console.log(`${Student3.name}: средний балл = ${Student3.getAverage().toFixed(2)} сдал ${Student3.isPassed()}`);

console.log(Student1.hasOwnProperty("getAverage"))
console.log(Student1.hasOwnProperty("isPassed"))
console.log("isPassed" in Student1)
console.log(Student2.hasOwnProperty("getAverage"))
console.log(Student2.hasOwnProperty("isPassed"))
console.log("isPassed" in Student2)


console.log("\nЗадание 3. Цепочка прототипов и наследование\n")

function Animal(name,sound){
    this.name = name;
    this.sound = sound;
}
Animal.prototype.speak = function(){
    return this.sound
}

function Dog(name) {
    Animal.call(this, name, "Гав");
}

Dog.prototype = Object.create(Animal.prototype);
// Dog.prototype.constructor = Dog;
Dog.prototype.speak = function(){
    return `${this.name} лает ${this.sound}`
}

const cat = new Animal("barsik","mya")
const dog = new Dog("ужас","dsd")
console.log(cat.speak())
console.log(dog.speak())

console.log(cat instanceof Animal,cat instanceof Dog)
console.log(dog instanceof Animal,dog instanceof Dog)
console.log(Object.getPrototypeOf(dog) === Dog.prototype)
console.log(Object.getPrototypeOf(Dog.prototype) === Animal.prototype)