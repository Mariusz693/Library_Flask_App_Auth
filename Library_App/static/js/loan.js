const myErrorEl = document.getElementById('error-message');
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
        else {
            myErrorEl.firstElementChild.innerText = 'Błąd zapisu zwrotu, anuluj i spróbuj ponownie';
            myErrorEl.classList.remove('d-none');
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
        else {
            myErrorEl.firstElementChild.innerText = 'Błąd usuwania pozycji, anuluj i spróbuj ponownie';
            myErrorEl.classList.remove('d-none');
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
            myErrorEl.classList.add('d-none');
            const myHeaderEl = document.querySelector('.modal-header');
            const myBodyEl = document.querySelector('.modal-body');
            const myFooterEl = document.querySelector('.modal-footer');
            if (e.target.hasAttribute("data-today")) {
                myHeaderEl.firstElementChild.innerText = 'Zapisz zwrot książki';
                myBodyEl.children[3].children[1].classList.add('my-bold-text');
                myBodyEl.children[0].children[1].innerText = '"' + e.target.dataset.book + '"';
                myBodyEl.children[1].children[1].innerText = e.target.dataset.user;
                myBodyEl.children[2].children[1].innerText = e.target.dataset.loan_date;
                myBodyEl.children[3].children[1].innerText = e.target.dataset.today;
                myFooterEl.firstElementChild.classList.add('btn-success');
                myFooterEl.firstElementChild.classList.remove('btn-danger');
                myFooterEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    returnLoan(e.target.dataset.id);
                }
            }
            else if (e.target.hasAttribute("data-return_date")){
                myHeaderEl.firstElementChild.innerText = 'Usuń z historii wypożyczeń';
                myBodyEl.children[3].children[1].classList.remove('my-bold-text');
                myBodyEl.children[0].children[1].innerText = '"' + e.target.dataset.book + '"';
                myBodyEl.children[1].children[1].innerText = e.target.dataset.user;
                myBodyEl.children[2].children[1].innerText = e.target.dataset.loan_date;
                myBodyEl.children[3].children[1].innerText = e.target.dataset.return_date;
                myFooterEl.firstElementChild.classList.remove('btn-success');
                myFooterEl.firstElementChild.classList.add('btn-danger');
                myFooterEl.firstElementChild.onclick = function (event){
                    event.preventDefault();
                    deleteLoan(e.target.dataset.id);
                }
            };
        }
    }
});