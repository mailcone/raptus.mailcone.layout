$(".item").live ('click', function () 
{	
	var wrapper = $(this).parents('.item-wrapper:first');
	var details = wrapper.find('.details:first');
	if (details.hasClass('hidden')) 
	{
		details.removeClass('hidden').addClass('visible');
	}
	else 
	{
		details.removeClass('visible').addClass('hidden');
	}
});

/*
 * XXX: does not work well must be designed better
 * XXX: OLD STUFF MUST BE DONE IN A DIFFRENT WAY

$(".markerButton").live ('click', function () {
	$(".item").bind ('live', ('click', function () 
	{	
		var wrapper = $(this).parents('.item-wrapper:first');
		var details = wrapper.find('.details:first');
		if (details.hasClass('hidden')) 
		{
			details.removeClass('hidden').addClass('visible');
		}
		else 
		{
			details.removeClass('visible').addClass('hidden');
		}
	}));
});
*/