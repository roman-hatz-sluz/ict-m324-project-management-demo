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
  saveToDatabase();
});

// (3) Interaktionen programmieren
// Validiert das Formular
const onChangeEmailField = () => {
  if (emailField.value === "") {
    submitButton.disabled = true;
  } else {
    submitButton.disabled = false;
  }
};

// Speichert die Daten in der Datenbank
const saveToDatabase = async () => {
  const data = {
    // Ändern Sie diese 3 Werte
    group: "teacher", // SQL Gruppenname
    pw: "02bd77f9", // SQL Passwort
    tableName: "user", // Name der Tabelle in der SQL Datenbank

    columns: {
      // "email": Name der Spalte in der SQL Tabelle, muss mit ihrem SQL Schema übereinstimmen
      // "emailField.value": Eingabe des Benutzers aus dem Formularfeld
      email: emailField.value,
    },
  };
  // Speichert die Daten in der Datenbank
  // Await wird benutzt, damit die Funktion asynchron ausgeführt wird. Es wird gewartet bis die Daten gespeichert sind
  await databaseClient.insertInto(data);
};
