document.addEventListener("DOMContentLoaded", () => {
  const followButton = document.getElementById("follow");
  if(followButton) {
    followButton.addEventListener("click", clickFollow);
  }
})

const clickFollow = async (e) => {

  const button = e.currentTarget;
  const user = e.currentTarget.dataset.user;
    
  const options = {
    method: "PUT",
    mode: "same-origin",
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      user: user,
      action: "follow",
    })
  }

  const response = await fetch(`/users/${user}`, options);
  const data = await response.json();
  if (data.following) {
    button.classList.replace("btn-primary", "btn-danger")
    button.textContent = " Unfollow "
    document.getElementById("followers").textContent = `Followers: ${data.followers_count}`
  } else {
    button.classList.replace("btn-danger", "btn-primary")
    button.textContent = " Follow "
    document.getElementById("followers").textContent = `Followers: ${data.followers_count}`
  }  
}