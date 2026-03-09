
// popup function
function popup(elements, enable_close=true) {
    const modal = document.createElement("div");
    const modal_content = document.createElement("div");
    const span = document.createElement("span");

    modal.id = 'popup';

    span.innerHTML = "&times;";
    (enable_close) && modal_content.appendChild(span);
    for (el of elements) {
        modal_content.appendChild(el);
    }
    modal.appendChild(modal_content);

    modal.classList.add("modal");
    modal_content.classList.add("modal-content");
    span.classList.add("close-button");

    modal.style.display = "flex";

    document.body.appendChild(modal);

    (enable_close) && span.addEventListener("click", () => {
        document.body.removeChild(modal);
    });

    (enable_close) && window.addEventListener("click", (event) => {
        if (event.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

function yeet_popup() {
    document.body.removeChild(document.getElementById('popup'));
}