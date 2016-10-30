/**
 * Created by koyexes on 8/4/2016.
 */

$('#loginModalJs').modal('show');// automatically showing the modal login error when a login error occurs

$('#loginModalJs').on('hidden.bs.modal', function(e){
    $('.loginAlert').each(function () {
       $(this).alert('close');
    });
    $('#loginModalJs').attr('id', 'loginModal');
    $('#loginForm').trigger('reset');
});

$('#loginModal').on('show.bs.modal', function (e) {
     $("#loginForm").trigger('reset');
});

// works with the homepage icons, changing their color gradient as mouse hovers over their labels
$('.iconLabel').hover(
    function(e){ $(e.target).parent().siblings('img').css({" -ms-filter" :"grayscale(0%)", "filter" : "grayscale(0%)", "-webkit-filter" : "grayscale(0%)"});},
    function(e){ $(e.target).parent().siblings('img').css({" -ms-filter" :"grayscale(100%)", "filter" : "grayscale(100%)", "-webkit-filter" : "grayscale(100%)"});}
);

/******** WORKPAGE SECTION *******/
// resetting all modal form inputs when form modal closes
$('.modalForm').each(function () {
    $(this).on('hidden.bs.modal', function (e) {
        $($(this).find('form')[0]).trigger('reset');
    });
});

// shows alert modal for messages to be displayed to users
$('#alert-modal').modal('show');

// changes the id attribute of the alert modal after closing it
$('#alert').on('hidden.bs.modal', function(e){
    $('#alert').attr('id', 'dont-alert-modal');
});

// closes alert-modal after alert closes
$('#form-feedback-alert').on('closed.bs.alert', function () {
    $('#alert-modal').modal('hide');
});

/**** homepage section ****/
// confirming whether the new password and the confirm password textfield values are the same
$('#new-password, #confirm-password').focusout( function () {
    var password_form = $('#passwordForm');
    var newPassword = $('#new-password').val();
    var confirmPassword = $('#confirm-password').val();
    var span = $(password_form).find('span.form-control-feedback');
    var parentDiv = $(password_form).find('div.has-feedback');
    if ((newPassword && confirmPassword) && (newPassword === confirmPassword)) {
        $(span).each( function () {
            $(this).removeClass('glyphicon glyphicon-remove ').addClass('glyphicon glyphicon-ok ');
        });
        $(parentDiv).each( function () {
            $(this).removeClass('has-error ').addClass('has-success ');
        });

    } else if ((newPassword && confirmPassword) && (newPassword !== confirmPassword)) {
        $(span).each( function () {
            $(this).removeClass('glyphicon glyphicon-ok ').addClass('glyphicon glyphicon-remove ');
        });
        $(parentDiv).each( function () {
            $(this).removeClass('has-success ').addClass('has-error ');
        });

    } else {
        $(span).each( function () {
            $(this).removeClass('glyphicon glyphicon-ok glyphicon glyphicon-remove ');
        });
        $(parentDiv).each( function () {
           $(this).removeClass('has-success has-error');
        });
    }
});


$('#passwordForm').on('submit', function (e) {
    var newPassword = $('#new-password').val();
    var confirmPassword = $('#confirm-password').val();
    if (newPassword === confirmPassword) {
        $(this).submit();
    }else{
        e.preventDefault();
        alert("the confirm password doesnt match with the new password ");
    }
});


