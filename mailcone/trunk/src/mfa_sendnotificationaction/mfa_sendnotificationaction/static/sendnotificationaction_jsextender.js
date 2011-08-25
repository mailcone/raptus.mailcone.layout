/*
 * ajax submit form data and create action with param (used by ControlPanelView)
 */
$("input[name='form.actions.addSendNotificationAction']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	var match = $(form).find("select[name=form.match]").children('option:selected').val();
	var to = $(form).find("input[name=form.to]").val();
	var subject = $(form).find("input[name=form.subject]").val();
	var body = $(form).find("textarea[name=form.body]").val();
	var orgMail = ''; 
	if ($(form).find("input[name=form.orgMail]").attr('checked')){
		orgMail = $(form).find("input[name=form.orgMail]").val();
	};
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.match=' + match +
					 '&form.to='+ to + 
					 '&form.subject=' + subject + 
					 '&form.body=' + body + 
					 '&form.orgMail=' + orgMail +
					 '&form.actions.addSendNotificationAction=' + buttonId;
	
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
$("input[name='form.actions.editSendNotificationAction']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	var match = $(form).find("select[name=form.match]").children('option:selected').val();
	var to = $(form).find("input[name=form.to]").val();
	var subject = $(form).find("input[name=form.subject]").val();
	var body = $(form).find("textarea[name=form.body]").val();
	var orgMail = ''; 
	if ($(form).find("input[name=form.orgMail]").attr('checked')){
		orgMail = $(form).find("input[name=form.orgMail]").val();
	};
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.match=' + match +
					 '&form.to='+ to + 
					 '&form.subject=' + subject + 
					 '&form.body=' + body + 
					 '&form.orgMail=' + orgMail +
					 '&form.actions.editSendNotificationAction=' + buttonId;
	
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