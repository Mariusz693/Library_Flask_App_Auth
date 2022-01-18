const errorEl = document.getElementById('error-message');
const url = window.location.href;


function deleteCategtory(idCategory) {
    const obj = {
        category: idCategory
    };
    fetch(url, {
        method: 'DELETE',
        body: JSON.stringify(obj),
    })
    .then(response => {
        if (response.status === 200){
            window.location = url;
        }
        else if (response.status === 404) {
            errorEl.firstElementChild.innerText = 'Błąd usuwania kategorii, anuluj i spróbuj ponownie';
            errorEl.classList.remove('d-none');
        }
        else {
            throw Error();
        };
    })
    .catch(error => {
        window.location = url;
    });
};


function addCategory () {
    document.querySelector('form').addEventListener('submit', function(e){
        e.preventDefault();
        const formField = e.target.elements;
        if (formField[0].value === ''){
            errorEl.firstElementChild.innerText = 'Pole obowiązkowe';
            errorEl.classList.remove('d-none');
        }
        else {
            let url = window.location.href;    
            const obj = {
                name: formField[0].value
            };
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(obj),
            })
            .then(response => {
                if (response.status === 200){
                    window.location = url;
                }
                else if (response.status === 409) {
                    errorEl.firstElementChild.innerText = 'Kategoria już istnieje w bazie';
                    errorEl.classList.remove('d-none');
                }
                else {
                    throw Error();
                };
            })
            .catch(error => {
                window.location = url;
            });
        };
    });
};


document.addEventListener("DOMContentLoaded", function () {
    for (let i=0, buttonEl, buttonsEl = document.querySelectorAll('[data-toggle="modal"]'); buttonEl = buttonsEl[i]; i++){
        buttonEl.onclick = function (e) {
            e.preventDefault();
            errorEl.classList.add('d-none');
            const headerEl = document.querySelector('.modal-header');
            const bodyEl = document.querySelector('.modal-body');
            const footerEl = document.querySelector('.modal-footer');
            if (e.target.hasAttribute("data-id")) {
                headerEl.firstElementChild.innerText = 'Potwierdź usunięcie kategorii';
                bodyEl.children[0].innerText = e.target.dataset.name;
                bodyEl.children[0].classList.remove('d-none');
                bodyEl.children[1].classList.add('d-none');
                footerEl.firstElementChild.innerText = 'Usun';
                footerEl.firstElementChild.classList.add('btn-danger');
                footerEl.firstElementChild.classList.remove('btn-success');
                footerEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    deleteCategtory(e.target.dataset.id);
                }
            }
            else {
                headerEl.firstElementChild.innerText = 'Dodaj nowa kategorię';
                bodyEl.children[0].classList.add('d-none');
                bodyEl.children[1].classList.remove('d-none');
                footerEl.firstElementChild.innerText = 'Dodaj';
                footerEl.firstElementChild.classList.add('btn-success');
                footerEl.firstElementChild.classList.remove('btn-danger');
                addCategory();
            };
        }
    }
});
