/*
 * ajax submit form data and create action with param (used by ControlPanelView)
 */
$("input[name='form.actions.addWriteLogAction']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	var match = $(form).find("select[name=form.match]").children('option:selected').val();
	var logfile = $(form).find("select[name=form.logfile]").children('option:selected').val();
	var loglevel = $(form).find("select[name=form.loglevel]").children('option:selected').val();
	var logmessage = $(form).find("input[name=form.logmessage]").val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.match=' + match +
					 '&form.logfile='+ logfile + 
					 '&form.loglevel=' + loglevel + 
					 '&form.logmessage=' + logmessage +
					 '&form.actions.addWriteLogAction=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var filterWrapper = $(form).parents('.newaction-wrapper:first');
	        var resultData = data;
			$(filterWrapper).html($(resultData).find('.actiontable:first'));
			$(filterWrapper).attr('name', $(resultData).find('.action-wrapper:first').attr('name'));
			hideSortLinks(filterWrapper, '.actiontable');
			$(filterWrapper).removeClass('newaction-wrapper').addClass('action-wrapper');
	    }
	});
});

/*
 * ajax submit form data and save action param (used by ControlPanelView)
 */
$("input[name='form.actions.editWriteLogAction']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	var match = $(form).find("select[name=form.match]").children('option:selected').val();
	var logfile = $(form).find("select[name=form.logfile]").children('option:selected').val();
	var loglevel = $(form).find("select[name=form.loglevel]").children('option:selected').val();
	var logmessage = $("input[name=form.logmessage]").val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.match=' + match +
					 '&form.logfile='+ logfile + 
	 				 '&form.loglevel=' + loglevel + 
	 				 '&form.logmessage=' + logmessage +
	 				 '&form.actions.editWriteLogAction=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var filterWrapper = $(form).parents('.action-wrapper:first');
	        var resultData = data;
			$(filterWrapper).html($(resultData).find('.actiontable:first'));
			hideSortLinks(filterWrapper, '.actiontable');
	    }
	});
});