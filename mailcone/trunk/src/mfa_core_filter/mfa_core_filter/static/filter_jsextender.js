$(".addFilterButton").live('click', function(e){
	e.preventDefault();
	
	var filterContainer = $(this).parents('.details:first').find('.markerFilterManagement:first');
	$(filterContainer).append('<div class="newfilter-wrapper"><div class="newfiltertype"></div><div class="newfilter"></div></div>');
	var filter = $(filterContainer).find('.newfilter:last'); 
	$(filterContainer).find('.newfiltertype:last').load($(this).attr('href') + ' .filterTypeManager', function(){
		$(filterContainer).find('.newfiltertype:last').find('select[name=filterType]').addClass('addFilterType');
		$(filter).load($(filterContainer).find('.newfiltertype:last').find('select[name=filterType]').find('option:first').val() + ' form', function(){
			$(filter).find('h1:first').remove();
		});
		$(filterContainer).find('.newfiltertype:last').find('.markerButton').addClass('hidden');
	});
});

$('.addFilterType').live('change', function(){
	var filter = $(this).parents('.newfilter-wrapper:first').find('.newfilter:first');
	$(filter).load($(this).children('option:selected').val() + ' form', function(){
		$(filter).find('h1:first').remove();
	});
});

$(".editFilter").live('click', function(e){
	e.preventDefault();
	var filterWrapper = $(this).parents(".filter-wrapper:first");
	$(filterWrapper).load ($(this).attr('href') + ' form', function(){
		$(filterWrapper).find('h1:first').remove();
	});
});

$('.delFilter').live('click', function(e){
	e.preventDefault();
	
	var actionWrapper = $(this).parents('.filter-wrapper:first');
	$.ajax({  
		type: "GET",  
		url: $(this).attr('href'),
		success: function(){
			$(actionWrapper).remove();
		}
	});
});