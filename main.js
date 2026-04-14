const titulo = document.querySelector("h1");
const vista = document.querySelector("#vista")
const botonmodo = document.querySelector("#botonmodo");
const articulo = document.querySelectorAll(".articulo")

titulo.style.color = "black";

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

const modal = document.getElementById("modal");
const cerrar = document.getElementById("cerrar");
const modalBody = document.getElementById("modal-body");

const articulos = document.querySelectorAll("article");

articulos.forEach(article => {
    article.addEventListener("click", () => {

        // Copiamos todo el contenido del artículo
        modalBody.innerHTML = article.innerHTML;

        // Lo ejectuta para hacer aparecer la ventana emergente
        modal.style.display = "block";
    });
});

// Abrir modal
articulos.forEach(article => {
    article.addEventListener("click", () => {
        modalBody.innerHTML = `<article class="articulo">${article.innerHTML}</article>`;

        modal.classList.add("show");
    });
})

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

// FILTROS DINÁMICOS
const botonesFiltro = document.querySelectorAll("#filtros button");
const peliculas = document.querySelectorAll(".articulo");

botonesFiltro.forEach(boton => {
    boton.addEventListener("click", () => {

        // Botón activo
        botonesFiltro.forEach(b => b.classList.remove("activo"));
        boton.classList.add("activo");

        const filtro = boton.dataset.filtro;

        peliculas.forEach(pelicula => {
            if (filtro === "todos" || pelicula.dataset.categoria === filtro) {
                pelicula.classList.remove("oculto");
            } else {
             pelicula.classList.add("oculto");
            }
        });
    });
});

