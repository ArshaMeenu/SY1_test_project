// var input_fields = document.querySelectorAll('.input');
// var login_btn  = document.querySelector('#login_btn');

const form = document.querySelector("form");
userField = form.querySelector(".username"),
userInput = userField.querySelector("input"),
passwordField = form.querySelector(".password"),
passwordInput = passwordField.querySelector("input");

form.onsubmit =(e)=>{
  
  e.preventDefault();
  console.log("Start");
  console.log(userInput.value);
  (userInput.value == "") ? userField.classList.add("shake", "error") : checkUsername();

  (passwordInput.value == "") ? passwordField.classList.add("shake","error"):checkPassword();

  setTimeout(()=>{
    userField.classList.remove("shake");
    passwordField.classList.remove("shake");
  },500);
//  onkeyup event occurs when the user releases a key (on the keyboard).
  userInput.onkeyup = ()=>{
      checkUsername();
    }
  passwordInput.onkeyup=()=>{
    checkPassword();
  }

  function checkUsername(){ //checkUsername function
    let pattern = /^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$/; //pattern for validate username
    if(!userInput.value.match(pattern)){ //if pattern not matched then add error and remove valid class
      userField.classList.add("error");
      userField.classList.remove("valid");
      let errorTxt = userField.querySelector(".error-txt");
      //if username value is not empty then show please enter valid username else show username can't be blank
      (userInput.value != "") ? errorTxt.innerText = "Enter a valid username with atleast 3 letters." : errorTxt.innerText = "username can't be blank";
    }else{ //if pattern matched then remove error and add valid class
      userField.classList.remove("error");
      userField.classList.add("valid");
    }
  }

  function checkPassword(){
    let pattern = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/; //pattern for validate username
    if(!passwordInput.value.match(pattern)){
      passwordField.classList.add("error");
      passwordField.classList.remove("valid");
      let errorText = passwordField.querySelector('.error-txt');
      (passwordInput.value != "")? errorText.innerText ="Minimum eight characters, at least one lower case,at least one upper case , one digit and one special character." :errorText.innerText = "Password can't be blank."
    }
    else{
      passwordField.classList.remove("error");
      passwordField.classList.add("valid");
    }
  }

  if(!userField.classList.contains("error") && !passwordField.classList.contains("error")){


    var posting = $.post( url, { s: term } );
    data = {
          'username':userInput.value,
          'password':passwordInput.value}
    }
    posting.done(function( data ) {
      alert(data);
    });
  //   const url = "{% url 'login' %}";
  //   data = {
  //     'username':userInput.value,
  //     'password':passwordInput.value}
  //   success = "login"
  //   dataType = "json"
  //   console.log("end");

  //   $.ajax({
  //     type: 'POST',
  //     url: url,  
  //     data: data,
  //     success: success  ,
  //     dataType: dataType
      
  // });

  }


}
