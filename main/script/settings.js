// image display
document.getElementById('image').addEventListener('change', e => {
    var img = document.getElementById('pfp');
    var reader = new FileReader();
    reader.onloadend = function() {
         img.src = reader.result;
    }
    reader.readAsDataURL(e.srcElement.files[0]);
});

// disable submit button when nothing was changed
const inputs = document.querySelectorAll("input, select");
for (const el of inputs){
    el.oldValue = el.value + el.checked;
}

// Declares function and call it directly
var setEnabled;
(setEnabled = function() {
    var e = true;
    for (const el of inputs) {
        if (el.oldValue !== (el.value + el.checked)) {
            e = false;
            break;
        }
    }
    document.getElementById('submit').disabled = e;
})();

document.oninput = setEnabled;
document.onchange = setEnabled;

async function submit_form() {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = '/settings';
    form.enctype = 'multipart/form-data';
    for (const el of inputs){
        if (el.oldValue !== (el.value + el.checked)) {
            form.appendChild(el);
        }
    }

    form.style = 'display: none';
    document.body.appendChild(form);
    form.submit();
}

function delete_profile() {
    const title = document.createElement("h3");
    title.innerHTML = "Confirm deleting profile"
    const p = document.createElement("p");
    p.innerHTML = "You are about to delete your profile, this change will be irreversible!";
    const a = document.createElement("a");
    a.href = "/delete_account";
    a.classList.add("danger-button");
    a.innerHTML = "Delete Profile";
    popup([title, p, a]);
}