
function addNewAuthor (newAuthor) {
    const mySelect = document.querySelector('select');
    const myOption = mySelect.firstElementChild.cloneNode();
    myOption.value = newAuthor['id'];
    myOption.innerText = newAuthor['name'];
    myOption.selected = 'selected';
    mySelect.appendChild(myOption);
    document.querySelector('.alert').parentElement.classList.remove('my-display-none');
    document.querySelector('.alert').firstElementChild.innerText = newAuthor['name'];
    document.querySelector('[data-dismiss="modal"]').click();
};


function addErrors (errors) {
    const myUlElement = document.createElement('ul');
    const myliElement = document.createElement('li');
    myliElement.classList.add('my-error');
    const myModalInput = document.querySelectorAll('.my-modal-input');
    for (let i=0; i<myModalInput.length; i++){
        if (myModalInput[i].children.length > 2){
            myModalInput[i].removeChild(myModalInput[i].lastElementChild);
        }
    }
    if (errors['name']) {
        myModalInput[0].appendChild(myUlElement.cloneNode());
        for (let i=0; i<errors['name'].length; i++){
            myModalInput[0].lastElementChild.appendChild(myliElement.cloneNode());
            myModalInput[0].lastElementChild.lastElementChild.innerText = errors['name'][i];
        }
    }
    if (errors['date_of_birth']) {
        myModalInput[1].appendChild(myUlElement.cloneNode());
        for (let i=0; i<errors['date_of_birth'].length; i++){
            myModalInput[1].lastElementChild.appendChild(myliElement.cloneNode());
            myModalInput[1].lastElementChild.lastElementChild.innerText = errors['date_of_birth'][i];
        }
    }
    if (errors['date_of_death']) {
        myModalInput[2].appendChild(myUlElement.cloneNode());
        for (let i=0; i<errors['date_of_death'].length; i++){
            myModalInput[2].lastElementChild.appendChild(myliElement.cloneNode());
            myModalInput[2].lastElementChild.lastElementChild.innerText = errors['date_of_death'][i];
        }
    }
};


document.addEventListener("DOMContentLoaded", function () {
    
    document.querySelector('[data-toggle="modal"]').addEventListener('click', function(e){
        const myModalInput = document.querySelectorAll('.my-modal-input');
        for (let i=0; i<myModalInput.length; i++){
            if (myModalInput[i].children.length > 2){
                myModalInput[i].removeChild(myModalInput[i].lastElementChild);
            }
            myModalInput[i].children[1].value = '';
        }
    })

    document.querySelector('.my-form').addEventListener('submit', function(e){
        e.preventDefault();
        const url = window.location.href;
        const formField = e.target.elements    
        const obj = {
            name: formField[0].value,
            date_of_birth: formField[1].value,
            date_of_death: formField[2].value,
        };
        fetch(url, {
            method: 'PUT',
            body: JSON.stringify(obj),
        })
        .then(response => {
            if (response.status === 200){
                return response.json();
            }
            else {
                throw Error();
            };
        })
        .then(data => {
            if (data['status'] === 'add') {
                addNewAuthor(data['new_author']);
            }
            else if (data['status'] === 'error'){
                addErrors(data['errors']);
            };
        })
        .catch(error => {
            window.location = url;
        });
    });
});


