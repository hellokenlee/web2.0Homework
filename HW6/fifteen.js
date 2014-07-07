 step=0;
 
 jQuery.fn.exchange=function () {
	// 设置 exchange 换位函数
	var tempX=$(this).css("left");
	var tempY=$(this).css("top");
	$(this).animate({
		left:emptyX,
		top:emptyY,
	})
	emptyX=tempX;
	emptyY=tempY;
	step++;
	$("#step").text("step:"+step.toString());
}

jQuery.fn.exchangeInit=function () {
	// 设置 exchange 换位函数
	var tempX=$(this).css("left");
	var tempY=$(this).css("top");
	$(this).css("left",emptyX);
	$(this).css("top",emptyY);
	emptyX=tempX;
	emptyY=tempY;	
}

$(document).ready(function(){
  var allPieces=$("#puzzlearea").find("div");
  allPieces.addClass("puzzlepiece");
  allPieces.css("background-repeat","no-repeat");
  var j=0;
  var i=0;
  emptyX="300px";
  emptyY="300px";
  step=0;
  for(var pos=0;pos<15;pos++){
		var left=i.toString()+"px";
		var top=j.toString()+"px";
		allPieces.eq(pos).css("left",left);//调整位置
		allPieces.eq(pos).css("top",top);
		allPieces.eq(pos).css("background-position","-"+left+" -"+top);//调整背景位置,CSS用的坐标系也太鸡巴了吧！
		i=i+100;
		if(pos==3||pos==7||pos==11){
			j=j+100;
			i=0;
		}
	}

	$("#shufflebutton").click(function(){//洗牌
		step=0;

		for(var i=0;i<100;i++){
			var rd=Math.floor(4*Math.random());//0上1下2左3右
			var eX=parseInt(emptyX);
			var eY=parseInt(emptyY);
			if(rd==0){
				for(var j=0;j<15;j++){
					if(allPieces.eq(j).css("left")==emptyX&&allPieces.eq(j).css("top")==(eY-100).toString()+"px"){
						allPieces.eq(j).exchangeInit();
					}
				}
			}
			if(rd==1){
				for(var j=0;j<15;j++){
					if(allPieces.eq(j).css("left")==emptyX&&allPieces.eq(j).css('top')==(eY+100).toString()+"px"){
						allPieces.eq(j).exchangeInit();
					}
				}
			}
			if(rd==2){
				for(var j=0;j<15;j++){
					if(allPieces.eq(j).css("top")==emptyY&&allPieces.eq(j).css('left')==(eX-100).toString()+"px"){
						allPieces.eq(j).exchangeInit();
					}
				}
			}
			if(rd==3){
				for(var j=0;j<15;j++){
					if(allPieces.eq(j).css("top")==emptyY&&allPieces.eq(j).css('left')==(eX+100).toString()+"px"){
						allPieces.eq(j).exchangeInit();
					}
				}
			}
		}
		
	})
	allPieces.click(function(){
		var classes=$(this).attr("class");
		if(classes.indexOf("movablepiece")>=0){
			$(this).exchange();
		}
	})
	allPieces.mouseover(function(){//检测movable
		var x=parseInt($(this).css("left"));
		var y=parseInt($(this).css("top"));
		var eX=parseInt(emptyX);
		var eY=parseInt(emptyY);
		//alert(eX+","+eY);
		if(x-100==eX&&y==eY){
			$(this).addClass("movablepiece");
		}
		if(x+100==eX&&y==eY){
			$(this).addClass("movablepiece");
		}
		if(y-100==eY&&x==eX){
			$(this).addClass("movablepiece");
		}
		if(y+100==eY&&x==eX){
			$(this).addClass("movablepiece");
		}
	})
	allPieces.mouseleave(function(){
		$(this).removeClass("movablepiece");
	})
});
