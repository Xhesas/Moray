

function delete_account(userid) {
    const title = document.createElement("h3");
    title.innerHTML = "Confirm deleting account"
    const p = document.createElement("p");
    p.innerHTML = "You are about to delete this users account, this change will be irreversible!";
    const a = document.createElement("a");
    a.href = "/delete_account/" + userid;
    a.classList.add("danger-button");
    a.innerHTML = "Delete Account";
    popup([title, p, a]);
}