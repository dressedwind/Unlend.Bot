let name = document.querySelector('#name');
let password = document.querySelector('#password');
let submit = document.querySelector('#submit');

let users = {}; // Создаем пустой объект для хранения пользователей

function User(name, password) {
    this.name = name;
    this.password = password;
}

function createId(users) {
    return Object.keys(users).length;
}

submit.addEventListener('click', () => {
    const nameUser = name.value;
    const passwordUser = password.value;

    const user = new User(nameUser, passwordUser);

    const userId = 'User' + createId(users);
    users[userId] = user;

    console.log(user); // Выводим созданного пользователя в консоль

    alert(`${nameUser}, вы успешно зарегестрированы`);
});
