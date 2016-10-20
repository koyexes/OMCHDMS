/**
 * Created by koyexes on 8/4/2016.
 */

$('#loginModalJs').modal('show');// automatically showing the modal login error when a login error occurs

$('#loginModalJs').on('hidden.bs.modal', function(e){
    $('#loginErrorAlert').alert('close');
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
// providing the success icon if the new password textfield isn't empty
/*$('#new-password').keyup( function () {
    var span = $(this).next('span');
    var parentDiv = $(this).parent('div.form-group');
    var newPassword = $(this).val();
    if ( newPassword !== "") {
        $(span).addClass('glyphicon glyphicon-ok');
        $(parentDiv).addClass('has-success');
    } else {
        $(span).removeClass('glyphicon glyphicon-ok');
        $(parentDiv).removeClass('has-success');
    }
});*/

$('#new-password').focusout( function () {
    var newPassword = $(this).val();
    var confirmPassword = $('#confirm-password').val();
    var span = $('#passwordForm span.form-control-feedback');
    var parentDiv = $('#passwordForm div.has-feedback');
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

    var newPassword = $($(this).find('input')[2]).val();
    var confirmPassword = $($(this).find('input')[3]).val();
    if (newPassword === confirmPassword) {
        $(this).submit();
    }else{
        e.preventDefault();
        alert("the confirm password doesnt match with the new password ");
    }
});


