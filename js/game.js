// (1) Variablen initialisieren
const formContainer = document.getElementById("formContainer");
const gameContainer = document.getElementById("game-container");
const submitButton = document.getElementById("submit");
submitButton.disabled = true;
const emailField = document.getElementById("email");

// (2) Interaktionen festlegen
emailField.addEventListener("keyup", () => {
  onChangeEmailField();
});
submitButton.addEventListener("click", async (event) => {
  event.preventDefault();
  onClickSubmit();
});

// (3) Interaktionen Code
const onChangeEmailField = () => {
  if (emailField.value === "") {
    submitButton.disabled = true;
  } else {
    submitButton.disabled = false;
  }
};
const onClickSubmit = async () => {
  // Speichert die Daten in der Datenbank
  await databaseClient.insertInto("user", {
    email: emailField.value,
  });

  // Nach dem Speichern verschwindet das Formular, das Game erscheint
  formContainer.classList.add("hidden");
  gameContainer.classList.remove("hidden");
};
