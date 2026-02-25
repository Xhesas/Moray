
// popup function
function popup(elements) {
    const modal = document.createElement("div");
    const modal_content = document.createElement("div");
    const span = document.createElement("span");

    span.innerHTML = "&times;";
    modal_content.appendChild(span);
    for (el of elements) {
        modal_content.appendChild(el);
    }
    modal.appendChild(modal_content);

    modal.classList.add("modal");
    modal_content.classList.add("modal-content");
    span.classList.add("close-button");

    modal.style.display = "flex";

    document.body.appendChild(modal);

    span.addEventListener("click", () => {
    document.body.removeChild(modal);
    });

    window.addEventListener("click", (event) => {
        if (event.target === modal) {
    document.body.removeChild(modal);
        }
    });
}