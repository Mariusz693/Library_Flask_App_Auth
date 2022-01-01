let author_select = document.getElementById('author');
let author_button = document.getElementById('my-button-author')
let author_add = document.getElementById('author_add');
for (let i=0; i<author_add.childElementCount; i++){
    console.log(author_add.children[i]);
    if (author_add.children[i].childElementCount > 2){
        author_add.classList.remove('my-display-none');
        author_add.children[0].children[1].setAttribute('required', '');
        author_add.children[1].children[1].setAttribute('required', '');
        break;    
    }
};
author_button.onclick = function () {
    author_select.value = '__None'
    author_add.classList.remove('my-display-none');
    author_add.children[0].children[1].setAttribute('required', '');
    author_add.children[1].children[1].setAttribute('required', '');
};
author_select.onchange = function () {
    if (author_select.value !== '__None') {
        author_add.classList.add('my-display-none');
        author_add.children[0].children[1].required = false;
        author_add.children[1].children[1].required = false;
        author_add.children[0].children[1].value = "";
        author_add.children[1].children[1].value = "";
        author_add.children[2].children[1].value = "";
        if(author_add.children[0].childElementCount > 2){
            author_add.children[0].removeChild(author_add.children[0].children[2]);
        };
        if(author_add.children[1].childElementCount > 2){
            author_add.children[1].removeChild(author_add.children[1].children[2]);
        };
        if(author_add.children[2].childElementCount > 2){
            author_add.children[2].removeChild(author_add.children[2].children[2]);
        }
    };
};