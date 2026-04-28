// Buscamos los elementos del título, botón de vista, botón de modo y artículo
const titulo = document.querySelector("h1");
const vista = document.querySelector("#vista")
const botonmodo = document.querySelector("#botonmodo");
const articulo = document.querySelectorAll(".articulo")

// Establecemos el color del título a negro
titulo.style.color = "black";

// Establecemos tres tamaños para los artículos: pequeño, mediano y grande
const sizes = ["small", "medium", "large"];
let current = 1; // empieza en medium

// Cuando se pulsa "cambiar vista", se elimina la clase que ya está activa y se le suma 1 (cambia a la siguiente clase o tamaño)
vista.addEventListener("click", () => {
    articulo.forEach(articulo => {
        articulo.classList.remove(sizes[current]);
        articulo.classList.add(sizes[(current + 1) % sizes.length]);
    });

    current = (current + 1) % sizes.length;
});

// Cuando se pulsa el botón modo de vista, se carga un mensaje en la consola y se activa o desactiva la clase noche
botonmodo.addEventListener("click", function () {
    console.log("modo");
    document.body.classList.toggle("noche");
});

// Establecemos los elementos del modal, el botón de "cerrar" modal, y el contenido del modal
const modal = document.getElementById("modal");
const cerrar = document.getElementById("cerrar");
const modalBody = document.getElementById("modal-body");

const articulos = document.querySelectorAll("article");

// Para que el modal tenga el contenido del artículo
articulos.forEach(article => {
    article.addEventListener("click", () => {

        // Copiamos todo el contenido del artículo
        modalBody.innerHTML = article.innerHTML;

        // Mostramos el modal
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
        
        // Si la categoría de la película no coincide con el filtro, esta se oculta
        peliculas.forEach(pelicula => {
            if (filtro === "todos" || pelicula.dataset.categoria === filtro) {
                pelicula.classList.remove("oculto"); // Si coincide, se mantiene en la lista
            } else {
                pelicula.classList.add("oculto"); 
            }
        });
    });
});

// Abrir modal
articulos.forEach(article => {
    article.addEventListener("click", () => {
        modalBody.innerHTML = `<article class="articulo">${article.innerHTML}</article>`; // Copiar contenido del artículo al modal

        modal.classList.add("show");
    });
});