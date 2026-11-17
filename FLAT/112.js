let arr = [10, 20, 30, 40, 50]

function getElement(a, index) {
    if (index < 0 ){
        return a[a.length + index] 
    }
    else {
        return a[index]
    }
}

console.log(getElement(arr, -1))
console.log(getElement(arr, -2))
console.log(getElement(arr, -3))