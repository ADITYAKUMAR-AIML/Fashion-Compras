// Make sure the DOM is loaded
document.addEventListener("DOMContentLoaded", function() { //After the doc fully loaded
    //After loading then js.
    const button = document.getElementById("view-more-btn");
    const hidden_items = document.querySelectorAll(".hidden-product"); // all items

    button.addEventListener("click", function() {
        hidden_items.forEach(item => {
            item.style.display = "block"; // show each hidden product
        });

        // Optional: hide the button after clicking
        button.textContent = "Show Less";
    });
});
