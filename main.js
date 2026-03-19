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

const modal = document.getElementById("modal");
const cerrar = document.getElementById("cerrar");
const modalBody = document.getElementById("modal-body");

const articulos = document.querySelectorAll("article");

articulos.forEach(article => {
    article.addEventListener("click", () => {

        // Copiamos TODO el contenido del artículo
        modalBody.innerHTML = article.innerHTML;

        // Mostramos el modal
        modal.style.display = "block";
    });
});

// Cerrar modal
cerrar.addEventListener("click", () => {
    modal.style.display = "none";
});

// Cerrar haciendo click fuera
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});