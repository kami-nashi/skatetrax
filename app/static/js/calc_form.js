$(document).ready(function() {
  var delay = 2000;
  $(‘.btn-default’).click(function(e){
    e.preventDefault();
    var name = $(‘#name’).val();
    if(name == ”){
       $(‘.message_box’).html(
       ‘<span style=”color:red;”>Enter Your Name!</span>’
       );
       $(‘#name’).focus();
       return false;
      }
     var email = $(‘#email’).val();
     if(email == ”){
       $(‘.message_box’).html(
       ‘<span style=”color:red;”>Enter Email Address!</span>’
       );
       $(‘#email’).focus();
       return false;
      }
    if( $(“#email”).val()!=” ){
      if( !isValidEmailAddress( $(“#email”).val() ) ){
        $(‘.message_box’).html(
        ‘<span style=”color:red;”>Provided email address is incorrect!</span>’
        );
        $(‘#email’).focus();
        return false;
      }
     }
     var message = $(‘#message’).val();
     if(message == ”){
       $(‘.message_box’).html(
       ‘<span style=”color:red;”>Enter Your Message Here!</span>’
       );
       $(‘#message’).focus();
       return false;
      }
  $.ajax
  ({
  type: “POST”,
  url: “ajax.php”,                                              //submit action page here
  data: “name=”+name+“&email=”+email+“&message=”+message,
  beforeSend: function() {
  $(‘.message_box’).html(
  ‘<img src=”Loader.gif” width=”25″ height=”25″/>’
  );
  },
  success: function(data)
  {
  setTimeout(function() {
  $(‘.message_box’).html(data);
  }, delay);
  }
  });
  });
});
