const createTable = async () => {
  const users = await databaseClient.executeSqlQuery("SELECT * FROM user");
  console.log(users[1]);
  createListHTML(users[1]);
};
const createListHTML = (data) => {
  const container = document.getElementById("formContainer");

  const title = document.createElement("h4");
  title.textContent = "Database Content";
  title.style.marginTop = "49px";
  container.appendChild(title);

  const list = document.createElement("ul");

  data.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = `ID: ${item.ID}, Email: ${item.email}, Created At: ${item.created_at}`;
    list.appendChild(listItem);
  });

  container.appendChild(list);
};

createTable();
