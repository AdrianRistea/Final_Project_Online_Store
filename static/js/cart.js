// cart.js

function inmultire(a, b) {
    return a * b;
}

document.addEventListener('DOMContentLoaded', function () {
    const decreaseButtons = document.querySelectorAll('.btn-decrease');
    const increaseButtons = document.querySelectorAll('.btn-increase');
    const quantityElements = document.querySelectorAll('.quantity');

    decreaseButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const quantityElement = document.querySelector(`.quantity[data-product-id="${productId}"]`);
            const currentQuantity = parseInt(quantityElement.textContent);
            if (currentQuantity > 1) {
                const newQuantity = currentQuantity - 1;
                quantityElement.textContent = newQuantity;

                // Calculează și actualizează rezultatul înmulțirii
                const productPrice = parseFloat(this.getAttribute('data-product-price'));
                const newResult = inmultire(newQuantity, productPrice);
                const resultElement = document.getElementById(`rezultat_${productId}`);
                if (resultElement) {
                    resultElement.innerHTML = newResult + " lei";
                }
            }
        });
    });

    increaseButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.getAttribute('data-product-id');
            const quantityElement = document.querySelector(`.quantity[data-product-id="${productId}"]`);
            const currentQuantity = parseInt(quantityElement.textContent);
            const newQuantity = currentQuantity + 1;
            quantityElement.textContent = newQuantity;

            // Calculează și actualizează rezultatul înmulțirii
            const productPrice = parseFloat(this.getAttribute('data-product-price'));
            const newResult = inmultire(newQuantity, productPrice);
            const resultElement = document.getElementById(`rezultat_${productId}`);
            if (resultElement) {
                resultElement.innerHTML = newResult + " lei";
            }
        });
    });
});
