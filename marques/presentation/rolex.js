// Création d'un tableau pour les boutons
let buttons = [];
// Création d'un tableau pour les volets
let volets = [];

// Remplissage des tableaux avec les boutons et les volets correspondants
for (let i = 0; i <= 12; i++) {
  buttons.push(document.getElementById('more' + i));
  volets.push(document.getElementById('hidden' + i));
}

// Fonction générique pour afficher ou masquer un volet
function toggleVolet(index) {
  let volet = volets[index];
  if (volet.style.display !== 'block') {
    volet.style.display = 'block';
    window.setTimeout(function() {
      volet.style.opacity = 1;
      volet.style.transform = 'scale(1)';
    }, 0);
  } else {
    volet.style.transform = 'scale(0)';
    window.setTimeout(function() {
      volet.style.display = 'none';
    }, 700);
  }
}

// Fonction pour gérer le clic sur un bouton
function handleClick(index) {
  buttons[index].addEventListener('click', function() {
    toggleVolet(index);
  });
}

// Appel de la fonction handleClick pour chaque bouton et volet
for (var i = 0; i <= 12; i++) {
  handleClick(i);
}