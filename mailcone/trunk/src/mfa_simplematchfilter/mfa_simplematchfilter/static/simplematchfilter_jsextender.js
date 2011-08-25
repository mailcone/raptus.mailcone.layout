/*
 * ajax submit form data and create filter with param (used by ControlPanelView)
 */
$("input[name='form.actions.addSimpleMatchFilter']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	
	var source = $(form).find("select[name='form.source']").children('option:selected').val();
	var operator = $(form).find("select[name='form.operator']").children('option:selected').val();
	var condition = $(form).find("input[name='form.condition']").val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.source='+ source + 
	 				 '&form.operator=' + operator + 
	 				 '&form.condition=' + condition + 
	 				 '&form.actions.addSimpleMatchFilter=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),
		data: dataString,
		success: function(data){
			var filterWrapper = $(form).parents('.newfilter-wrapper:first');
			var resultData = data;
			$(filterWrapper).html($(resultData).find('.filtertable:first'));
			$(filterWrapper).attr('name', $(resultData).find('.filter-wrapper:first').attr('name'));
			hideSortLinks(filterWrapper, '.filtertable');
			$(filterWrapper).removeClass('newfilter-wrapper').addClass('filter-wrapper');
	    }
	});
});

/*
 * ajax submit form data and save filter param (used by ControlPanelView)
 */
$("input[name='form.actions.editSimpleMatchFilter']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	var source = $(form).find("select[name='form.source']").children('option:selected').val();
	var operator = $(form).find("select[name='form.operator']").children('option:selected').val();
	var condition = $(form).find("input[name='form.condition']").val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.source='+ source + 
					 '&form.operator=' + operator + 
					 '&form.condition=' + condition + 
					 '&form.actions.editSimpleMatchFilter=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var filterWrapper = $(form).parents('.filter-wrapper:first');
	        var resultData = data;
			$(filterWrapper).html($(resultData).find('.filtertable:first'));
			hideSortLinks(filterWrapper, '.filtertable');
	    }
	});
});