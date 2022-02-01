const myErrorEl = document.getElementById('error-message');
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
        else {
            myErrorEl.firstElementChild.innerText = 'Błąd usuwania kategorii, anuluj i spróbuj ponownie';
            myErrorEl.classList.remove('d-none');
        }
    })
    .catch(error => {
        window.location = url;
    });
};


function addCategory (formField) {
    if (formField.value === ''){
        myErrorEl.firstElementChild.innerText = 'Pole obowiązkowe';
        myErrorEl.classList.remove('d-none');
    }
    else {
        const obj = {
            name: formField.value
        };
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(obj),
        })
        .then(response => {
            if (response.status === 200){
                return response.json();
            }
            else {
                throw Error()
            };
        })
        .then(data => {
            if (data['status'] === 'add') {
                window.location = url;
            }
            else if (data['status'] === 'exist'){
                myErrorEl.firstElementChild.innerText = 'Kategoria już istnieje w bazie';
                myErrorEl.classList.remove('d-none');
            };
        })
        .catch(error => {
            window.location = url;
        });
    };
};


document.addEventListener("DOMContentLoaded", function () {
    for (let i=0, buttonEl, buttonsEl = document.querySelectorAll('[data-toggle="modal"]'); buttonEl = buttonsEl[i]; i++){
        buttonEl.onclick = function (e) {
            e.preventDefault();
            myErrorEl.classList.add('d-none');
            const myHeaderEl = document.querySelector('.modal-header');
            const myBodyEl = document.querySelector('.modal-body');
            const myFooterEl = document.querySelector('.modal-footer');
            if (e.target.hasAttribute("data-id")) {
                myHeaderEl.firstElementChild.innerText = 'Potwierdź usunięcie kategorii';
                myBodyEl.children[0].innerText = e.target.dataset.name;
                myBodyEl.children[0].classList.remove('d-none');
                myBodyEl.children[1].classList.add('d-none');
                myFooterEl.firstElementChild.classList.add('btn-danger');
                myFooterEl.firstElementChild.classList.remove('btn-success');
                myFooterEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    deleteCategtory(e.target.dataset.id);
                }
            }
            else {
                myHeaderEl.firstElementChild.innerText = 'Dodaj nowa kategorię';
                myBodyEl.children[0].classList.add('d-none');
                myBodyEl.children[1].classList.remove('d-none');
                myBodyEl.children[1].value = '';
                myFooterEl.firstElementChild.classList.add('btn-success');
                myFooterEl.firstElementChild.classList.remove('btn-danger');
                myFooterEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    addCategory(myBodyEl.children[1]);
                }
            };
        }
    }
});
