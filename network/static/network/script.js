const editbuttons = document.querySelectorAll('#edit');
const likebuttons = document.querySelectorAll('#like');

editbuttons.forEach(button => {
    button.classList.add('btn', 'btn-primary')
    button.addEventListener('click', () => {
        // Retrieve post body, store content, and remove body
        // console.log(button.parentNode);
        let bod = button.parentNode.querySelector('#body');
        let post = bod.parentNode;
        let content = bod.innerHTML;
        const post_id = post.dataset.postId;
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
              const cookies = document.cookie.split(";");
              for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
                }
              }
            }
            return cookieValue;
          }

        button.remove();
        let form = document.createElement('form');
        bod.replaceWith(form);
        let input = document.createElement('textarea');
        let save = document.createElement('button');
        input.value = content;
        save.textContent = 'Save';
        save.classList.add('btn', 'btn-primary');
        form.appendChild(input);
        form.appendChild(save);

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            fetch("/edit", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({payload: input.value, post_id: post_id}),
              })
              .then(response => response.json())
              .then(data => {
                console.log(data);
                if (data.status == "success") {
                    form.replaceWith(bod);
                    post.appendChild(button);
                    bod.innerHTML = input.value;
                }
              });
        })
    })
})

likebuttons.forEach(lb => {

  // change like/unlike

  let likecount = lb.parentNode.querySelector('#likes');

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  lb.addEventListener('click', () => {
    const postId = lb.dataset.postId;
    console.log(postId);
    fetch(`/like/${postId}`, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.status == "liked") {
        lb.classList.replace('btn-success', 'btn-danger');
        lb.innerHTML = 'Unlike';
        likecount.innerHTML = 'Likes: ' + data.likes;
      } else if (data.status == "unliked") {
        lb.classList.replace('btn-danger', 'btn-success');
        lb.innerHTML = 'Like';
        likecount.innerHTML = 'Likes: ' + data.likes;
      }
    });
  });
});