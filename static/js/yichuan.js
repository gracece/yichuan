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
          console.log("page"+url);
          $('#myCanvas').css("background-image",'url('+url+')')
          $('canvas').clearCanvas();
        }
    });

    updater.poll();
  },

  onError: function(e){
    console.log(e);
  }
};
