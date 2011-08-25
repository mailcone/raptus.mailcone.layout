var blnClickIcon = false;

$('#CustomerConfiglet').live('click', function(e){
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

$('.item').live('click', function(){
	var itemWrapper = $(this).parents(".item-wrapper:first");
	if ($(itemWrapper).find(".details:first").hasClass('hidden')) { 
		$(itemWrapper).find(".details:first").removeClass('hidden');
	}
	else {
		if (blnClickIcon == false){
			$(itemWrapper).find(".details:first").addClass('hidden');
		}
		else{
			blnClickIcon = false;
		}
	}
});

$('#addCustomerLink').live('click', function(e){
	e.preventDefault();
	$('#customerContainer').append('<div class="item-wrapper"><div class="item">NEW CUSTOMER</div><div class="details"></div></div>');
	var container = $('#customerContainer').find(".item-wrapper:last").find(".details:first");
	$(container).load($(this).attr('href') + ' form', function() {
		$(container).find('h1:first').remove();
	});
});

$('#addCustomerButton').live('click', function(e){
	e.preventDefault();
	
	var itemWrapper = $(this).parents('.item-wrapper:first');
	var form = $(itemWrapper).find('form:first');
	
	var name = $("input[name=name]").val();
	var address = $("textarea[name=address]").val();
	var dataString = 'name='+ name + '&address=' + address;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var response = data;
			$(itemWrapper).html($(response).find('.item-wrapper:first'));
	    }
	});
});

$(".editIcon").live('click', function(e){
	e.preventDefault();
	
	// disable toggle for details
	blnClickIcon = true;
	
	var itemDetails = $(this).parents('.item-wrapper:first').find('.details:first');
	$(itemDetails).load($(this).attr('href') + ' form');
});

$('#editCustomerButton').live('click', function(e) {
	e.preventDefault();
	
	var itemWrapper = $(this).parents('.item-wrapper:first');
	var form = $(itemWrapper).find('form:first');
	
	var name = $("input[name=name]").val();
	var address = $("textarea[name=address]").val();
	var dataString = 'name='+ name + '&address=' + address;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var response = data;
			$(itemWrapper).html($(response).find('.item-wrapper:first').html());
	    }
	});
});

$('.delCustomer').live('click', function(e){
	e.preventDefault();
	
	// disable toggle for details
	blnClickIcon = true;
	
	$.ajax({  
		type: "GET",  
		url: $(this).attr('href'),
		success: function(){
			$('#CustomerConfiglet').click();
		}
	});
});