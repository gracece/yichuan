var updater = {
  poll: function(){
    $.ajax({url: "/draw?t="+timestamp+"&f="+file_id,
           type: "GET",
           dataType: "json",
           success: updater.onSuccess,
           error: updater.onError});
  },
  onSuccess: function(data, dataStatus){

    $.each(data,function(i,ONE){
      timestamp = ONE.timestamp;
      type = ONE.type;
      if(type=='draw') {
        item = ONE.line;
        console.log(item);
        $('canvas').drawLine({
          strokeStyle: 'blue',
          strokeWidth: 5,
          rounded: true,
          x1: item.x1, y1: item.y1,
          x2: item.x2, y2: item.y2,
        });
      }
      else if(type='jump')
        {
          page = ONE.page;
          $('#page').html(page);
          url = "/static/upload/"+file_id+"/p-"+page+".png";
          $('#loading').css("display",'block')
          $.get(url, function(result){
            $('#loading').css("display",'none')
            $('#myCanvas').css("background-image",'url('+url+')')
            $('canvas').clearCanvas();
          });
          console.log("page"+url);
        }
    });

    updater.poll();
  },

  onError: function(e){
    console.log(e);
  }
};

function launchFullScreen(element) {  
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.msRequestFullscreen) {
    element.msRequestFullscreen();
  } else if (element.mozRequestFullScreen) {
    element.mozRequestFullScreen();
  } else if (element.webkitRequestFullscreen) {
    element.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
  }
}
