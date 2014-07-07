a=0;
s=0;
$(document).ready(function(){
	$('div.boundary').mouseover(function(){//lose
		if(a!=1&&s==1){
			$('div.boundary').addClass('youlose');
			$('#status').text("You Lose!!Click the S block to Restart");
			a=1;
			s=0;
		}
	});
	$('#end').mouseover(function(){//win
		if(a==0 && s==1){
			$('#status').text('You Win!!Move your mouse over the S to Playagain.');
			a=0;
			s=0;
		}
	});
	$('#start').mouseover(function(){//start
		s=1;
		if(a!=1){
			$('#status').text("Now Don't Touch The Wall...");
		}
	});
	$('#start').click(function(){//restart
		$('div.boundary').removeClass('youlose');
		$('#status').text("Now Don't Touch The Wall...");
		a=0;
		s=1;
	});
	$('#maze').mouseleave(function(){
		if(a!=1&&s==1){
			$('div.boundary').addClass('youlose');
			$('#status').text("You Lose!!Click the S block to Restart");
			a=1;
			s=0;
		}
	});
});

