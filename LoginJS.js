var username="Hello";
var password="World";



$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});

function CheckCredentials(){
    if(document.getElementById("Username")===username){
        if(document.getElementById("Password")===password){
            return true;
        }
    }
    return false;
}
