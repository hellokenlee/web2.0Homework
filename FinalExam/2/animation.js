time=50;
dir="right";
counter=0;
$(document).ready(function(){
	$("#stop").attr("disabled", true);
	counter=0;
});
function start(){
	$("#start").attr("disabled", true);
	$("#stop").attr("disabled", false);
	interval = setInterval("autoPlay()",time,dir);
}
function stop(){
	clearInterval(interval);
	$("#start").attr("disabled", false);
	$("#stop").attr("disabled", true);
}
function autoPlay(){//连续播放动画
	if(dir=="right"){
		$("#a").prepend("<span id='e'>&nbsp</span>")
		counter+=1;
		if(counter >= 80){
			dir="left";
		}
	}
	if(dir=="left"){
		$("#e").remove();
		counter-=1;
		if(counter <= 0){
			dir="right";
		}
	}
}
