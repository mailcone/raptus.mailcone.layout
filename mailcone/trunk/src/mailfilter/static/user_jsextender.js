// XXX - move to mfa_core_auth

$('#UserConfiglet').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#tabResultContainer').load($(this).attr('href') + ' #tabContent',function(){	
		$(document.body).find('.item').each(function(){
			var itemWrapper = $(this).parents(".item-wrapper:first");
			$(itemWrapper).find(".details:first").addClass('hidden');
		});
	});
});

$(".addUser").live('click', function(e){
	e.preventDefault();
	$('#userContainer').append('<div class="item-wrapper"><div class="item">NEW USER</div><div class="details"></div></div>');
	var newUserWrapper = $('#userContainer').find('.item-wrapper:last');
	var newUserDetails = $(newUserWrapper).find('.details:first');
	$(newUserDetails).load($(this).attr('href') + ' form', function(){
		$(newUserDetails).find('h1:first').remove();
		$(newUserDetails).find('input[type=submit]:first').addClass('addUserButton');
	});
});

$(".addUserButton").live('click', function(e){
	e.preventDefault();
	
	var itemWrapper = $(this).parents('.item-wrapper:first');
	var form = $(itemWrapper).find('form:first');
	
	var login = $("input[name='form.login']").val();
	var password = $("input[name='form.password']").val();
	var confirm_password = $("input[name='form.confirm_password']").val();
	var real_name = $("input[name='form.real_name']").val();
	var role = $(form).find("select[name='form.role']").children('option:selected').val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.login='+ login + 
					 '&form.password=' + password + 
					 '&form.confirm_password=' + confirm_password + 
					 '&form.real_name=' + real_name + 
					 '&form.role=' + role + 
					 '&form.actions.add=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
			var resultData = data;
			$(itemWrapper).html($(resultData).find('#' + login + ':first').html());
	    }
	});
});