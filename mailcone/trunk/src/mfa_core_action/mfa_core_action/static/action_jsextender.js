$(".addActionButton").live('click', function(e){
	e.preventDefault();
	
	var actionContainer = $(this).parents('.details:first').find('.markerActionManagement:first');
	$(actionContainer).append('<div class="newaction-wrapper"><div class="newactiontype"></div><div class="newaction"></div></div>');
	var action = $(actionContainer).find('.newaction:last'); 
	$(actionContainer).find('.newactiontype:last').load($(this).attr('href') + ' .actionTypeManager', function(){
		$(actionContainer).find('.newactiontype:last').find('select[name=actionType]').addClass('addActionType');
		$(action).load($(actionContainer).find('.newactiontype:last').find('select[name=actionType]').find('option:first').val()  + ' form', function(){
			$(action).find('h1:first').remove();
		});
		$(actionContainer).find('.newactiontype:last').find('.markerButton').addClass('hidden');
	});
});

$('.addActionType').live('change', function(){
	var action = $(this).parents('.newaction-wrapper:first').find('.newaction:first');
	$(action).load($(this).children('option:selected').val() + ' form', function(){
		$(action).find('h1:first').remove();
	});
});

$(".editAction").live('click', function(e){
	e.preventDefault();
	var actionWrapper = $(this).parents(".action-wrapper:first");
	$(actionWrapper).load ($(this).attr('href') + ' form', function(){
		$(actionWrapper).find('h1:first').remove();
	});
});

$('.delAction').live('click', function(e){
	e.preventDefault();
	
	var actionWrapper = $(this).parents('.action-wrapper:first');
	$.ajax({  
		type: "GET",  
		url: $(this).attr('href'),
		success: function(){
			$(actionWrapper).remove();
		}
	});
});