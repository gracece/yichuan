function getLine(id){
        file_id = id;
        $.getJSON("/draw?t="+timestamp+"&f="+file_id,function(data){

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
        });
        setTimeout("getLine("+file_id+")",500);
      }

