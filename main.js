const titulo = document.querySelector("h1");
const vista = document.querySelector("#vista")
const botonmodo = document.querySelector("#botonmodo");
const articulo = document.querySelectorAll(".articulo")

titulo.style.color = "lightblue";

const sizes = ["small", "medium", "large"];
let current = 1; // empieza en medium

vista.addEventListener("click", () => {
  articulo.forEach(articulo => {
    articulo.classList.remove(sizes[current]);
    articulo.classList.add(sizes[(current + 1) % sizes.length]);
  });

  current = (current + 1) % sizes.length;
});

botonmodo.addEventListener("click", function () {
  console.log("modo");
  document.body.classList.toggle("noche");
});