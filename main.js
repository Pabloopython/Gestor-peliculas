const titulo = document.querySelector("h1");
const vista = document.querySelector("mododevista")

titulo.style.color = "red";

const sizes = ["small", "medium", "large"];
let current = 1; // empieza en medium

button.addEventListener("click", () => {

  articulos.classList.remove(sizes[current]);

  current = (current + 1) % sizes.length;

  articulos.classList.add(sizes[current]);

});