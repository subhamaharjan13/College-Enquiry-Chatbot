var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  setTimeout(function() {
    fakeMessage(msg);
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

var Fake = [
  'Hello I am KBC Bot \n  I am here to provide you details about Kathmandu BernHardt College.',
]

function fakeMessage(msg=Fake[0]) {
var result = '';
var token = $('#token').val()
if(msg!=Fake[0]){
   $.ajax({
        url: '/message/',
        data: {
          'msg': msg,
          'csrfmiddlewaretoken':token,
        },
        method:'post',
        dataType: 'json',
        success: function (data) {
          if (data.msg) {
            result=data.msg;
          }else{
          result='sorry can get answer';
          }
        }
      });
 }
  var input = $('.message-input').val();
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="https://www.kbc.edu.np/images/logo.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    if(result==''){
    $('<div class="message new"><figure class="avatar"><img src="https://www.kbc.edu.np/images/logo.png" /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    }else{
    $('<div class="message new"><figure class="avatar"><img src="https://www.kbc.edu.np/images/logo.png" /></figure>' + result + '</div>').appendTo($('.mCSB_container')).addClass('new');
    }
    setDate();
    updateScrollbar();
    i++;
  }, 1000 + (Math.random() * 20) * 100);

}