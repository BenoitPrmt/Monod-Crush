function follow(userID, btn) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "user/" + userID + "/follow", true);
    xhr.setRequestHeader("crendentials", "include");

    xhr.onload = function() {
        if (xhr.status === 200) {

            btn.querySelectorAll("svg").forEach(function(svg) {
                svg.classList.toggle("is-hidden");
            });

            btn.querySelector(".nb-follows").innerHTML = JSON.parse(xhr.responseText).followers;

            if (JSON.parse(xhr.responseText).followers === 0) {
                btn.querySelector(".nb-follows").classList.add("is-hidden");
            } else {
                btn.querySelector(".nb-follows").classList.remove("is-hidden");
            }

        } else if (xhr.status === 401) {
            document.location.href = "/auth/login";
        }

    }
    xhr.send();
}

document.addEventListener('DOMContentLoaded', () => {

    const followButtons = Array.prototype.slice.call(document.querySelectorAll('.follow-button'), 0);

    if (followButtons.length > 0) {

        followButtons.forEach(btn => {
            btn.addEventListener('click', () => {

                const userID = btn.dataset.target;

                follow(userID, btn);

            });
        });
    }

});