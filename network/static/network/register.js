document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("register");
  form.addEventListener("submit", validateData);
});

const validateData = (e) => {
  e.preventDefault();
  const currentAlert = document.getElementById("alert");
  if (currentAlert) {
    currentAlert.remove();
  }
  
  const username = document.getElementById("username");
  const email = document.getElementById("email");
  const password = document.getElementById("password");
  const confirmation = document.getElementById("confirmation");

  if (username.value.length < 6) {
    const alertMessage = alertText(
      "Username must be at least 6 characters long"
    );
    username.insertAdjacentElement("afterend", alertMessage);
    return;
  }
  else if (!email.value.includes("@") || !email.value.includes(".")) {
    const alertMessage = alertText(
      "Must enter a valid email"
    );
    email.insertAdjacentElement("afterend", alertMessage);
    return;
  }
  else if (password.value.length < 6) {
    const alertMessage = alertText(
      "Password must be at least 6 characters long"
    );
    password.insertAdjacentElement("afterend", alertMessage);
    return;
  }
  else if (confirmation.value !== password.value) {
    const alertMessage = alertText(
      "Password and confirmation must match"
    );
    confirmation.insertAdjacentElement("afterend", alertMessage);
    return;
  }
  else {
    username.value = username.value.toLowerCase();
    const form = document.getElementById("register");
    form.submit();
  }
};

const alertText = (text) => {
  const alertSection = document.createElement("div");
  alertSection.setAttribute("class", "text-danger");
  alertSection.setAttribute("id", "alert");
  const alertText = document.createTextNode(text);
  alertSection.appendChild(alertText);
  return alertSection;
}
