// main.js

function  randomChar(l)  {
	var  x="0123456789qwertyuioplkjhgfdsazxcvbnm";
	var  tmp="";
	var timestamp = new Date().getTime();
	for(var  i=0;i<  l;i++)  {
		tmp  +=  x.charAt(Math.ceil(Math.random()*100000000)%x.length);
	}
	return  timestamp+tmp;
};

$(document).ready(function(){
	$('.submit-btn').on('click', function(){
		var question = $('.question-input').val();
		var id=randomChar(6);

		if (question.trim() == '') return;
		$('.chatlogs').append('<p class="user-question">提问：' + question + '</p>');
		$('.question-input').val('');
		
		$.ajax({
			url: '/chat',
			type: 'POST',
			data: {question: question,id:id},
			success: function(data){
				var source = new EventSource("/streaming?id="+id);
				// sse 连接开启时回调函数
				source.onopen = function (event) {
					console.log('EventSource.readyState ' + source.readyState);
				}
				// 消息监听，event 是后端返回的数据,相当于python字典
				source.onmessage = function (event) {
					// update_data(event);
					console.log(event.data);
				}
				source.onerror = function (event) {
					source.close();
					console.log('EventSource.readyState ' + source.readyState);
				}
				// $('.chatlogs').append('<p class="bot-answer">' + data.answer + '</p>');
			}
		});
	});

	$.ajax({
		url: '/get_token',
		type: 'GET',
		success: function(data){
				console.log(data);
			}
	});


});
