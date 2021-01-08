document.addEventListener("DOMContentLoaded", () => {  
  const likeButtons = document.querySelectorAll(".like");

  likeButtons.forEach(button => {
    button.addEventListener("click", clickLike);
  });

  const editButtons = document.querySelectorAll("span[class='edit float-right']")
  if (editButtons.length) {
    editButtons.forEach(span => {
      const editIcon = span.querySelector(".fas.fa-edit")
      editIcon.addEventListener("click", clickEdit);
    })
  }
})

// like button
const clickLike = async (e) => {
  const postId = e.currentTarget.parentElement.id;
  const options = {
    method: "PUT",
    mode: "same-origin", // do not send CSRF token to another domain
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      postId: postId,
      action: "like"
    })
  }
  // fetch server
  const response = await fetch(`/posts/${postId}`, options);
  const result = await response.json();
  
  // update number of likes
  e.target.parentNode.querySelector(".likes").innerHTML = result.likes;
  // update style of heart
  if (!result.liked) {
    e.target.classList.remove("text-danger");
  } else {
    e.target.classList.add("text-danger");
  }
}

// edit button
const clickEdit = (e) => {
  
  const postArticle = e.target.parentNode.parentNode.parentNode;
  // grab the icon and create a clone
  const icon = e.target;
  const iconClone = icon.cloneNode();
  // remove the edit event listener of the icon
  icon.removeEventListener("click", clickEdit);
  // replace the edit icon with a save icon
  icon.setAttribute("title", "save");
  icon.classList.replace("fa-edit", "fa-save");
  icon.classList.add("mx-2", "text-success")
  // set the clone icon as a save icon and append it to the DOM
  iconClone.classList.replace("fa-edit", "fa-window-close");
  iconClone.classList.replace("text-primary", "text-danger");
  iconClone.setAttribute("title", "cancel");
  icon.parentNode.appendChild(iconClone);
  // grab current post content
  const pTag = postArticle.querySelector(".post-content");
  pTag.style.display = "none";
  // create textarea
  const textarea = document.createElement("textarea");
  textarea.classList.add("form-control", "bg-dark", "text-white", "mb-1");
  textarea.value = pTag.innerText.trim();
  pTag.parentNode.insertBefore(textarea, pTag);
  // set event listener to the cancel and save icon
  iconClone.addEventListener("click", exitEdit);
  icon.addEventListener("click", save);
}
// cancel button
const exitEdit = (e) => {
  // select post article
  const post = e.target.parentNode.parentNode.parentNode;
  // create an edit icon
  const editIcon = e.target.cloneNode();
  editIcon.classList.replace("fa-window-close", "fa-edit");
  editIcon.classList.replace("text-danger", "text-primary")
  editIcon.setAttribute("title", "edit");
  // add edit event listener
  editIcon.addEventListener("click", clickEdit);
  // put the edit icon alone where it belongs
  post.querySelector("span[class='edit float-right']").innerHTML = "";
  post.querySelector("span[class='edit float-right']").appendChild(editIcon);  
  // bring back the p tag where the textarea is
  const pTag = post.querySelector(".post-content");
  pTag.style.display = "block";
  // bye textarea
  const textarea = post.querySelector("textarea");
  textarea.parentNode.removeChild(textarea)
  // textarea.remove();
  delete textarea;
}
// save post
const save = async (e) => {
  const postArticle = e.target.parentNode.parentNode.parentNode;
  const pTag = postArticle.querySelector(".post-content")
  
  // grab text from textarea
  const newText = postArticle.querySelector("textarea").value.trim();
  // prepare options object to fetch
  const options = {
    method: "PUT",
    mode: "same-origin", // do not send CSRF token to another domain
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      postId: postArticle.id,
      action: "edit",
      newText
    })
  }
  if (newText) {
    const response = await fetch(`/posts/${postArticle.id}`, options);
    if (response.status == 204) {
      postArticle.querySelector(".fa-window-close").click();
      return;
    }
    const data = await response.json();
    // change post content
    pTag.innerText = data.post_content;
    // exit edit mode
    postArticle.querySelector(".fa-window-close").click();
  } else {
    postArticle.querySelector(".fa-window-close").click();
    return;    
  }
}
// Get csrf token
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}