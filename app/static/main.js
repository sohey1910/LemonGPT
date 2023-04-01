// main.js
$(document).ready(function(){
	$('.submit-btn').on('click', function(){
		var question = $('.question-input').val();
		if (question.trim() == '') return;
		$('.chatlogs').append('<p class="user-question">' + question + '</p>');
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
});
