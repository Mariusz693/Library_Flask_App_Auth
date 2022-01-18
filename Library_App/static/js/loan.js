const errorEl = document.getElementById('error-message');
const url = window.location.href;


function returnLoan(idLoan) {
    const obj = {
        loan: idLoan
    };
    fetch(url, {
        method: 'POST',
        body: JSON.stringify(obj),
    })
    .then(response => {
        if (response.status === 200){
            window.location = url;
        }
        else if (response.status === 404) {
            errorEl.firstElementChild.innerText = 'Błąd zapisu zwrotu, anuluj i spróbuj ponownie';
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


function deleteLoan(idLoan) {
    const obj = {
        loan: idLoan
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
            errorEl.firstElementChild.innerText = 'Błąd usuwania pozycji, anuluj i spróbuj ponownie';
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


document.addEventListener("DOMContentLoaded", function () {
    for (let i=0, buttonEl, buttonsEl = document.querySelectorAll('[data-toggle="modal"]'); buttonEl = buttonsEl[i]; i++){
        buttonEl.onclick = function (e) {
            e.preventDefault();
            errorEl.classList.add('d-none');
            const headerEl = document.querySelector('.modal-header');
            const bodyEl = document.querySelector('.modal-body');
            const footerEl = document.querySelector('.modal-footer');
            if (e.target.hasAttribute("data-today")) {
                headerEl.firstElementChild.innerText = 'Zapisz zwrot książki';
                bodyEl.children[3].classList.add('my-row');
                bodyEl.children[3].children[1].classList.add('my-bold-text');
                bodyEl.children[0].children[1].innerText = '"' + e.target.dataset.book + '"';
                bodyEl.children[1].children[1].innerText = e.target.dataset.user;
                bodyEl.children[2].children[1].innerText = e.target.dataset.loan_date;
                bodyEl.children[3].children[1].innerText = e.target.dataset.today;
                footerEl.firstElementChild.classList.add('btn-success');
                footerEl.firstElementChild.classList.remove('btn-danger');
                footerEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    returnLoan(e.target.dataset.id);
                }
            }
            else if (e.target.hasAttribute("data-return_date")){
                headerEl.firstElementChild.innerText = 'Usuń z historii wypożyczeń';
                bodyEl.children[3].classList.remove('my-row');
                bodyEl.children[3].children[1].classList.remove('my-bold-text');
                bodyEl.children[0].children[1].innerText = '"' + e.target.dataset.book + '"';
                bodyEl.children[1].children[1].innerText = e.target.dataset.user;
                bodyEl.children[2].children[1].innerText = e.target.dataset.loan_date;
                bodyEl.children[3].children[1].innerText = e.target.dataset.return_date;
                footerEl.firstElementChild.classList.remove('btn-success');
                footerEl.firstElementChild.classList.add('btn-danger');
                footerEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    deleteLoan(e.target.dataset.id);
                }
            };
        }
    }
});