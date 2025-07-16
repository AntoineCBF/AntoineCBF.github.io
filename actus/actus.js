let liste= document.getElementById('liste');
let tableLi= liste.getElementsByTagName('li');
let tableP= liste.getElementsByTagName('p');

let delay=0;
for(let i=0; i<(tableLi.length); i++){
    tableLi[i].style.animation='slide 1s ease-out '+delay+'s 1 forwards';
    tableP[i].style.animation='slide 1s ease-out '+delay+'s 1 forwards';
    delay+=0.3;
}