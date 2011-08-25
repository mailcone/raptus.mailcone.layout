/*
 * XXX
 */
$('#AppConfiglet').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#tabResultContainer').load($(this).attr('href') + ' #tabContent',function(){	
		// Add class slidecontainer to first ul find
		$('#settingTabs').find('ul:first').addClass('slidecontainer');
		// Add class tab to slides 
		$('#settingTabs').find('a').each(function(){
			$(this).addClass('tab');
		});
		$('#settingTabs').append('<div id="settingTabResultContainer"></div>');
		$('#settingTabs').find('a:first').click();
	});
});

/*
 * XXX
 */
$('#AppSettings').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#settingTabResultContainer').load($(this).attr('href') + ' form');
});

/*
 * XXX
 */
$('#DatabaseSettings').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#settingTabResultContainer').load($(this).attr('href') + ' #tabContent');
});

// XXX - should be moved to mfa_core_action
/*
 * XXX
 */
$('#ActionSettings').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	// XXX - will be not a form later
	$('#settingTabResultContainer').load($(this).attr('href') + ' #tabContent');
});

// XXX - should be moved to mfa_core_filter
/*
 * XXX
 */
$('#FilterSettings').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	// XXX - will be not a form later
	$('#settingTabResultContainer').load($(this).attr('href') + ' #tabContent');
});

/*
 * XXX
 */
$('#SmtpSettings').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#settingTabResultContainer').load($(this).attr('href') + ' form');
});

/*
 * XXX
 */
$("input[name='form.actions.saveSmtpSettings']").live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	
	var host = $("input[name=form.host]").val();
	var email = $("input[name=form.email]").val();
	var authrequired = ''; 
	if ($(form).find("input[name=form.authrequeried]").attr('checked')){
		authrequired = $(form).find("input[name=form.authrequeried]").val();
	};
	var user = $("input[name=form.user]").val();
	var passwd = $("input[name=form.passwd]").val();
	var buttonId = $(form).find("input[type=submit]").val();

	var dataString = 'form.host='+ host +
					 '&form.email=' + email +
					 '&form.authrequeried='+ authrequired +
					 '&form.user='+ user +
					 '&form.passwd='+ passwd +
					 '&form.actions.saveSmtpSettings=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
			$('#settingTabResultContainer').prepend('<div class="messageBox">SETTINGS SAVED!</div>');
		}
	});
});