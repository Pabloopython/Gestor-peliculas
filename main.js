const titulo = document.querySelector("h1");
const vista = document.querySelector("mododevista")
const botonmodo = document.querySelector("#botonmodo");

titulo.style.color = "darkwhite";

const sizes = ["small", "medium", "large"];
let current = 1; // empieza en medium
/* 
button.addEventListener("click", () => {

  articulos.classList.remove(sizes[current]);

  current = (current + 1) % sizes.length;

  articulos.classList.add(sizes[current]);

});
 */
botonmodo.addEventListener("click", function () {
  console.log("modo");
  document.body.classList.toggle("noche");
});