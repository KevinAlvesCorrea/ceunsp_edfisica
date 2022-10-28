const form = document.getElementById('form');
const nome = document.getElementById('name');
const data = document.getElementById('born');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password_confirmation = document.getElementById('password_confirmation');

    form.addEventListener('submit', e =>
    {
    e.preventDefault();


    if (checkInputs())
    {
        e.target.submit();
    }

    });

    function checkInputs()
    {
        let status = true;

        let nomeValue = nome.value.trim();
        let emailValue = email.value.trim();
        let passwordValue = password.value.trim();
        let password_confirmationValue = password_confirmation.value.trim();
        let dataValue = data.value.trim();

        if (nomeValue === "")
        {
            errorValidation(nome,"Nome Completo é obrigatório");
            status = false;
        }
        else
        {
            successValidation(nome);
        }
        if (dataValue === "")
        {
            errorValidation(data,"Data de nascimento é obrigatório");
            status = false;
        }
        else
        {
            successValidation(data);
        }
        if (emailValue === '')
        {
            errorValidation(email, 'O Email é obrigatório.');
            status= false;
        }
        else if(!isEmail(emailValue))
        {
            errorValidation(email, "Email não é válido");
            status = false;
        }
        else
        {
            successValidation(email)
        }
        if (passwordValue === '')
        {
            errorValidation(password, 'Por favor, informe sua senha.');
            status = false;
        }
        else if(passwordValue.length <8 )
        {
             errorValidation(password, 'Senha deve ter no minimo 8 caracteres.')
             status = false
        }

        else
        {
            successValidation(password);
        }
        if (password_confirmationValue === '')
        {
            errorValidation(password_confirmation, "Confirmação de senha não pode estar vazia !");
            status = false;
        }
        else if(password_confirmationValue !== passwordValue)
        {
            errorValidation(password_confirmation, "Senhas não conferem !");
            status = false;
        }
        else
        {
            successValidation(password_confirmation);
        }
        const formControls = form.querySelectorAll('.input-field')
                const formIsValid = [...formControls].every(formControl =>
                {
                    return (formControl.className === "input-field success")



                })

            if (formIsValid)
            {
                console.log('O formulario é válido')

            }

            return status;


    }



    function errorValidation(input, message)
    {
        const formControl = input.parentElement;
        const small = formControl.querySelector("small");
        //adiciona a mensagem de erro
        small.innerText = message;
        //adiciona a classe de erro
        formControl.className = "input-field error";
    }

    function successValidation(input)
    {
        const formControl = input.parentElement;
    
        formControl.className = "input-field success";

    }

     var checa = document.getElementsByName("checkbox");
        var numElementos = checa.length;
        var bt = document.getElementById("register");
        for(var x=0; x<numElementos; x++){
           checa[x].onclick = function(){

              var cont = document.querySelectorAll("input[name='checkbox']:checked").length;

              bt.disabled = cont ? false : true;
           }
           }
    function isEmail(email)
    {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
    }






