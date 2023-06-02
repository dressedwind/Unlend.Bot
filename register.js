let submitButton = document.getElementById("submit");
let nameInput = document.getElementById("name");
let passwordInput = document.getElementById("password");

submitButton.addEventListener("click", function(event) {
    event.preventDefault(); // Предотвращаем отправку формы

    let name = nameInput.value;
    let password = passwordInput.value;

    if (name.trim() === "" || password.trim() === "") {
        alert("Пожалуйста, заполните все поля.");
        return;
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "register.php", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            alert(xhr.responseText);
        }
    };

    let data = "name=" + encodeURIComponent(name) + "&password=" + encodeURIComponent(password);
    xhr.send(data);
});
