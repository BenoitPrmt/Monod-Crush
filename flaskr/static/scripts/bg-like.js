function like(postId, btn) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "post/" + postId + "/like", true);
    xhr.setRequestHeader("crendentials", "include");

    xhr.onload = function() {
        if (xhr.status === 200) {

            btn.querySelectorAll("svg").forEach(function(svg) {
                svg.classList.toggle("is-hidden");
            });

            btn.querySelector(".nb-likes").innerHTML = JSON.parse(xhr.responseText).likes;

            if (JSON.parse(xhr.responseText).likes === 0) {
                btn.querySelector(".nb-likes").classList.add("is-hidden");
            } else {
                btn.querySelector(".nb-likes").classList.remove("is-hidden");
            }

        } else if (xhr.status === 401) {
            document.location.href = "/auth/login";
        }

    }
    xhr.send();
}

document.addEventListener('DOMContentLoaded', () => {

    const likeButtons = Array.prototype.slice.call(document.querySelectorAll('.like-button'), 0);

    if (likeButtons.length > 0) {

        likeButtons.forEach(btn => {
            btn.addEventListener('click', () => {

                const postId = btn.dataset.target;

                like(postId, btn);

            });
        });
    }

});