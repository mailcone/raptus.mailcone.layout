/*
 * This js script provide popup to load rule set (templates) 
 * for a specific customer. Used by customer_viewlet.pt
 */

//SETTING UP OUR POPUP
//0 means disabled; 1 means enabled;
var popupStatus = 0;

//loading popup with jQuery magic!
function loadPopupLoadProfile(){
	//loads popup only if it is disabled
	if(popupStatus==0){
		$("#backgroundPopupLoadProfile").css({
			"opacity": "0.7"
		});
		$("#backgroundPopupLoadProfile").fadeIn("fast");
		$("#popupLoadProfil").fadeIn("fast");
		popupStatus = 1;
	}
}

//disabling popup with jQuery magic!
function disablePopupLoadProfile(){
	//disables popup only if it is enabled
	if(popupStatus==1){
		$("#backgroundPopupLoadProfile").fadeOut("fast");
		$("#popupLoadProfil").fadeOut("fast");
		popupStatus = 0;
	}
}

//centering popup
function centerPopupLoadProfile(){
	//request data for centering
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	var popupHeight = $("#popupLoadProfil").height();
	var popupWidth = $("#popupLoadProfil").width();
	//centering
	$("#popupLoadProfil").css({
		"position": "absolute",
		"top": windowHeight/2-popupHeight/2,
		"left": windowWidth/2-popupWidth/2
	});
	//only need force for IE6
	
	$("#backgroundPopupLoadProfile").css({
		"height": windowHeight
	});
	
}


//CONTROLLING EVENTS IN jQuery
$(document).ready(function(){
	
	//LOADING POPUP
	//Click the button event!
	$(".loadProfilButton").live('click', function(e){
		e.preventDefault();
		
		$("#popupLoadProfil").load($(this).attr('href') + ' form', function(data) {
			var resultData = data;
			var method = $(resultData).find('form:first').attr('method');
			var enctype = $(resultData).find('form:first').attr('enctype');
			var action = $(resultData).find('form:first').attr('action');
			var finderContainer = '<div id="finderContainer"></div>';
			var form = '<form action="' + action + '" enctype="' + enctype + '" method="' + method + '"></form>'; 
			
			$("#popupLoadProfil").html('');
			$("#popupLoadProfil").append(form);
			$("#popupLoadProfil").find('form:first').append(finderContainer);
			
			var finderContainer = $("#popupLoadProfil").find('#finderContainer');		
			$(finderContainer).append('<div id="finderWidth"></div>');
			var finderWidth = $(finderContainer).find('#finderWidth:first');
			$(finderWidth).append($(resultData).find('#rulesetContainer:first').addClass('popupFinderColumn'));
			$("#popupLoadProfil").find('form:first').append($(resultData).find('.finderButtons:first'));
			$("#popupLoadProfil").find('.ruleset').each(function (){
				$(this).removeClass('item');
				$(this).addClass('finderItem');
				$(this).parents('.ruleset-wrapper:first').find('.rules:first').remove();
			});
			
			//centering with css
			centerPopupLoadProfile();
			//load popup
			loadPopupLoadProfile();
		});
		
	});
				
	//CLOSING POPUP
	//Click the x event!
	$("#popupLoadProfilClose").click(function(){
		disablePopupLoadProfile();
	});
	//Click out event!
	$("#backgroundPopupLoadProfile").click(function(){
		disablePopupLoadProfile();
	});
	//Press Escape event!
	$(document).keypress(function(e){
		if(e.keyCode==27 && popupStatus==1){
			disablePopupLoadProfile();
		}
	});

});

$('#loadRuleSetsButton').live ('click', function(e){
	e.preventDefault();
	
	disablePopupLoadProfile();
});


/*
 * XXX - At the moment only rule if click on a ruleset, not relly generic
 */
var blnRulesetCheckbox = false; //flag set if ruleset checkbox is clicked
var blnRulesetChecked = false; //save state of selected ruleset checkbox

function toggleRules(rulesetContainer, rulesetChecked){
	$(rulesetContainer).find('.ruleCheckbox').each(function(){
		$(this).attr('checked', rulesetChecked);
	});
};

$('.finderItem').live('click', function(){
	var currentColumn = $(this).parents('.popupFinderColumn:first'); 
	var url = $(currentColumn).parents('form').attr('action');
	
	// remove active class
	$('#finderContainer').find('.ruleset').each(function(){
		$(this).removeClass('finderItemSelected');
	});
	// add selected class to clicked item
	$(this).addClass('finderItemSelected');
	
	// hidden already loaded
	$('#finderContainer').find('.ruleContainer').each(function(){
		$(this).addClass('hidden');
	});
	
	var rulesetId = $(this).parents('.ruleset-wrapper:first').attr('id');
	// check ruleset is already loaded, if it is, it will display it 
	if ($('#finderContainer').find('div[name$=' + rulesetId + ']').length == 1){
		var rules = $('#finderContainer').find('div[name$=' + rulesetId + ']');
		$(rules).removeClass('hidden');
		if (blnRulesetCheckbox == true){
			toggleRules(rules, blnRulesetChecked);
			blnRulesetCheckbox = false;
		};
	};
	
	// if selcted ruleset not loaded yet, load now
	if ($('#finderContainer').find('div[name$=' + rulesetId + ']').length == 0){
		$(currentColumn).after('<div class="popupFinderColumn ruleContainer"></div>');
		var newColumn = $(currentColumn).next('.popupFinderColumn').attr('name', rulesetId);
		$(newColumn).load(url + ' #' + rulesetId, function(data){
			var resultData = data;
			var rules = $(resultData).find('#'+rulesetId).find('.rules:first');
			$(rules).removeClass('details');
			$(newColumn).html($(rules));
			if (blnRulesetCheckbox == true){
				toggleRules(rules, blnRulesetChecked);
				blnRulesetCheckbox = false;
			};
		});
	};
});

/*
 * just set flag blnRulesetCheckbox afterwards run 
 * function $('.finderItem').live('click')
 */
$('.rulesetCheckbox').live('click', function(){
	blnRulesetCheckbox = true;
	blnRulesetChecked = $(this).attr('checked');
});

$('#loadRuleSetsButton').live('click', function(e){
	e.preventDefault();
	
	var dataString = '';
	var blnFirst = false;
	var form = $('#loadRuleSetsButton').parents('form:first'); 
	
	$(form).find("input").each(function() {
		if ($(this).attr('checked')){
			if (blnFirst == false){
				dataString = dataString + $(this).attr('name') + '=' + $(this).attr('value');
				blnFirst = true;
			}
			else{
				dataString = dataString + '&' + $(this).attr('name') + '=' + $(this).attr('value');
			};
		};
	});
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
			location.reload(); 
		}
	});
});