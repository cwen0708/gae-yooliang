/*#############################################################
Name: mouse to CSS
Version: 0.1
#############################################################*/
$(function(){
             jQuery('.img_change').mouseover(function () {
                $(this).attr("src", $(this).attr("src").replace("_out", "_over"));
            }).mouseout(function () {
                $(this).attr("src", $(this).attr("src").replace("_over", "_out"));
            });
    });