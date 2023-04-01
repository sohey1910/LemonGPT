// main.js
$(document).ready(function(){
	$('.submit-btn').on('click', function(){
		var question = $('.question-input').val();
		

		if (question.trim() == '') return;
		$('.chatlogs').append('<p class="user-question">提问：' + question + '</p>');
		$('.question-input').val('');
		
		$.ajax({
			url: '/chat',
			type: 'POST',
			data: {question: question},
			success: function(data){
				$('.chatlogs').append('<p class="bot-answer">' + data.answer + '</p>');
			}
		});
	});

	$('.submit-btn').on('click', function(){
		var source = new EventSource("/streaming");
		// sse 连接开启时回调函数
		source.onopen = function (event) {
			console.log('EventSource.readyState ' + source.readyState);
		}
		// 消息监听，event 是后端返回的数据,相当于python字典
		source.onmessage = function (event) {
			// update_data(event);
			console.log(event);
		}
		source.onerror = function (event) {
			source.close();
			console.log('EventSource.readyState ' + source.readyState);
		}
	});
});
