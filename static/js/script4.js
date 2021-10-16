const form = document.querySelector("form");
userField = form.querySelector(".username"),
userInput = userField.querySelector("input"),
passwordField = form.querySelector(".password"),
passwordInput = passwordField.querySelector("input");

form.onsubmit = (e)=>{
  e.preventDefault(); //preventing from form submitting
  //if username and password is blank then add shake class in it else call specified function
  (userInput.value == "") ? userField.classList.add("shake", "error") : checkUsername();
  (passwordInput.value == "") ? passwordField.classList.add("shake", "error") : checkPass();

  setTimeout(()=>{ //remove shake class after 500ms
    userField.classList.remove("shake");
    passwordField.classList.remove("shake");
  }, 500);

  userInput.onkeyup = ()=>{checkUsername();} //calling checkUsername function on username input keyup
  passwordInput.onkeyup = ()=>{checkPass();} //calling checkPassword function on pass input keyup

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
  function checkPass(){ //checkPass function
    let pattern = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/; //pattern for validate username

    if(!passwordInput.value.match(pattern)){ //if pass is empty then add error and remove valid class
      passwordField.classList.add("error");
      passwordField.classList.remove("valid");
      let errorTxt = passwordField.querySelector(".error-txt");
      //if username value is not empty then show please enter valid username else show username can't be blank
      (passwordInput.value != "") ? errorTxt.innerText = "Minimum eight characters, at least one lower case,at least one upper case , one digit and one special character. " : errorTxt.innerText = "";


    }else{ //if pass is empty then remove error and add valid class
      passwordField.classList.remove("error");
      passwordField.classList.add("valid");
    }
  }

  

  //if userField and passwordField doesn't contains error class that mean user filled details properly
  if(!userField.classList.contains("error") && !passwordField.classList.contains("error")){
    // window.location.href = form.getAttribute("action"); //redirecting user to the specified url which is inside action attribute of form tag
 
      //     var token = '{{csrf_token}}'
      //     var username =userInput.value
      //     console.log(username);
      //     var password =passwordInput.value
      //     console.log(password);
      //     const endpoint = "{% url 'login' %}";
      //     console.log(endpoint)
          
      //     fetch("{% url 'login' %}", {
      //         method: 'post',
      //         headers: {
      //             'Accept': 'application/json',
      //             'Content-Type': 'application/json',"X-CSRFToken":token
      //         },
      //         body: JSON.stringify({
      //             "username":username,
      //             "password":password,                
      //                         })
              
      //         }).then(function(res){ return res.json(); })
      //         .then(function(data){ 
                  
     
  
      //             if(data.success==true){
      //               const toast = swal.mixin({
      //             toast: true,
      //             position: 'top-end',
      //             showConfirmButton: false,
      //             timer: 6000,
      //             padding: '2em'
      //         });
                      
      //               toast({
      //             type: 'success',
      //             title: "Panel approved successfully.",
      //             padding: '2em',
      //         }).then(() => {
      //         location.reload();
      //         });
             
      //     }
      //     else{
      //         toast({
      //             "title":"Oops!",
      //             type: 'error',
      //             "text":data.message,
                 
      //             padding: '2em'
      //           }
          
      //           )}
      // }); 
   
        // console.log("abv0");
        // return true;
        var username =userInput.value
        $.ajax({
          url: "{% url 'login' %}",
          type: 'POST',
          data: {
              name: username
          },
          
          success: function (response) {
            console.log(data);
          },
          error: function (response) {
          }
      });

  }

      // else {
      //   alert ("Login was unsuccessful, please check your username and password");
      //   return false;
      // }
     



}