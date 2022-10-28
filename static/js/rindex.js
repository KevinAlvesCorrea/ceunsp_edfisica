const form = document.getElementById('form')
const nome = document.getElementById('nome')
const email = document.getElementById('email')
const senha = document.getElementById('senha')
const senha2 = document.getElementById('senha2')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    checkInputs()
})

    function checkInputs() {
    const nomeValue = nome.value.trim()
    const emailValue = email.value.trim()
    const senhaValue = senha.value.trim()
    const senha2Value = senha2.value.trim()

    if (nomeValue === ''){

        errorValidation(nome, 'Preencha esse campo')

    }else{
        successValidation(nome)

    }
    
    if (emailValue === ''){

        errorValidation(email, 'Preencha esse campo')
    }else{
        successValidation(email)

    }
    
    if (senhaValue === ''){

        errorValidation(senha, 'Preencha esse campo')
    }else if(senhaValue.length <8 ){   
        errorValidation(senha, 'Senha deve ter no minimo 8 caracteres')

    }else{
        successValidation(senha)

    }

    if (senha2Value === ''){
        errorValidation(senha2, 'Preencha esse campo')

    }else if (senha2Value !== senhaValue ){
        errorValidation(senha2, 'As senhas devem ser iguais.')

    }else{

        successValidation(senha2)

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


//function toggleButton() {
//    const aceitar = document.querySelector('#aceitar').value;

//    if (aceitar){
//        document.querySelector('#register').disabled = false;
//        return
//    }
//    document.querySelector('#register').disabled = true;
    
//}



var checa = document.getElementsByName("checkbox");
var numElementos = checa.length;
var bt = document.getElementById("register");
for(var x=0; x<numElementos; x++){
   checa[x].onclick = function(){
      // "input[name='toggle']:checked" conta os checkbox checados
      var cont = document.querySelectorAll("input[name='checkbox']:checked").length;
      // ternário que verifica se há algum checado.
      // se não há, retorna 0 (false), logo desabilita o botão
      bt.disabled = cont ? false : true;
   }
}