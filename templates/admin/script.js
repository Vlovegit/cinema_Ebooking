const modal = document.getElementById("add-modal");

const btn = document.getElementsByClassName("add-btn")[0];

const span = document.getElementsByClassName("close")[0];

btn.onclick = function () {
    modal.style.display = "block";
}

span.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

// EDIT
const editModal = document.getElementById("editPromotionModal");
const editBtns = document.getElementsByClassName("edit-btn");
const editSpan = editModal.querySelector(".close");

for (let i = 0; i < editBtns.length; i++) {
    editBtns[i].addEventListener('click', function () {
        console.log("meow")
        editModal.style.display = "block";

        var row = this.parentNode.parentNode;
        var name = row.querySelector(".promotion-name").textContent;
        var key = row.querySelector(".promotion-key").textContent;
        var value = row.querySelector(".promotion-value").textContent;
        var status = row.querySelector(".promotion-status").textContent;

        editModal.querySelector("#promotionName").value = name;
        editModal.querySelector("#promotionKey").value = key;
        editModal.querySelector("#promotionValue").value = value;
        editModal.querySelector("#promotionStatus").value = status;

        editModal.style.display = "none";
    })

}

editSpan.onclick = function() {
    editModal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == editModal) {
        editModal.style.display = "none";
    }
}

