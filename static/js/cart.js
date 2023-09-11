// Obțineți elementele de input
var inputValoare1 = document.getElementById("valoare1");
var inputValoare2 = document.getElementById("valoare2");

// Adăugați evenimentul input pentru câmpurile de intrare
inputValoare1.addEventListener("input", afiseazaRezultat);
inputValoare2.addEventListener("input", afiseazaRezultat);

// Funcție pentru a calcula și afișa suma valorilor
function afiseazaRezultat() {
  var valoare1 = parseFloat(inputValoare1.value) || 0;
  var valoare2 = parseFloat(inputValoare2.value) || 0;
  var suma = valoare1 * valoare2;

  document.getElementById("rezultat").innerHTML = "Suma valorilor este: " + suma;
}
