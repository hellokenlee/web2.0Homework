//by KenLee@2013 in Web2.0 courses sysu.
s='7 pt';
m='12 pt';
l='24pt';
i=0;//当前到达哪一桢
var isRunning=0;
var time = 200; 
var interval; //调度器对象。
action='Blank';
all='';//储存开始前字符串
ANIMATIONS["Custom"]="Now Loading... \\\n"+"=====\n"+"Now Loading... |\n"+"=====\n"+"Now Loading... /\n"+"=====\n"+"Now Loading... -\n"
$(document).ready(function(){
	$('#small').click(function(){
		$('#displayarea').css("fontSize","7pt");
	})
	$('#medium').click(function(){
		$('#displayarea').css("fontSize","12pt");
	})
	$('#large').click(function(){
		$('#displayarea').css("fontSize","24pt");
	})
	$('#animation').change(function(){//以上是大小调节
		action=$('#animation').val();
		$('#displayarea').val(ANIMATIONS[action]);
		isRunning=0;
		i=0;
	});
	$('#start').click(function(){
		if(isRunning==0){
			all=$('#displayarea').val();
			q=all.split("=====\n");
			//alert(q);
			interval = setInterval("autoPlay()",time);
			isRunning=1;
			$('#stop').attr("disabled",false);
			$('#start').attr("disabled",true);
			$('#animation').attr("disabled",true);
		}
	})
	$('#stop').click(function(){//停止
		if(isRunning==1){
			clearInterval(interval);
			$('#displayarea').val(all);
			isRunning=0;
			i=0;
			$('#stop').attr("disabled",true);
			$('#start').attr("disabled",false);
			$('#animation').attr("disabled",false);
		}
	})
	$('#speed').click(function(){//调节速度
		//alert($('#speed').attr("checked"));
		if($('#speed').attr("checked")=="checked"){
			//alert("check!");
			time=50;
			if(isRunning==1){
				clearInterval(interval);
				interval = setInterval("autoPlay()",time);
			}
		}
		else{
			//alert("nocheck!");
			time=200;
			if(isRunning==1){
				clearInterval(interval);
				interval = setInterval("autoPlay()",time);
			}
		}
	})
});
function autoPlay(){//连续播放动画
	$('#displayarea').val(q[i]);
	i++;
	if(i>=q.length)
		i=i%q.length;
}
