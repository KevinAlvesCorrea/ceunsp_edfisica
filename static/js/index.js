const form = document.getElementById('form');
const nome = document.getElementById('nome');
const senha = document.getElementById('senha');


form.addEventListener('submit', (e) => {
    e.preventDefault()

    checkInputs()
});

    function checkInputs() {
    const nomeValue = nome.value.trim()
    const senhaValue = senha.value.trim()

    if (nomeValue === ''){

        errorValidation(nome, 'Preencha esse campo')
    }else{
        successValidation(nome)

    }

    if (senhaValue === ''){
        errorValidation(senha, 'Preencha esse campo')

    }else{
        successValidation(senha)

    }

}
function errorValidation(input, message){
    const formControl = input.parentElement;
    const small = formControl.querySelector('small')
    small.innerText = message

    formControl.className = 'input-field error'
}

function successValidation(input){
    const formControl = input.parentElement;

    formControl.className = 'input-field success'
}
