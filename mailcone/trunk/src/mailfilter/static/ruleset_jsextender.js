/*
 * XXX
 */
var blnClickRuleIcon = false;

/*
 * XXX
 */
function ajaxesFilterManager(ruleDetails, url){
	$(ruleDetails).find(".filterTypeManager:first").remove();
	$(ruleDetails).find(".filterLabel").prepend('<div class="editIcons"><a href="' + url + '" class="addFilterButton">add filter</a></div>');
};

/*
 * XXX
 */
function ajaxesActionManager(ruleDetails, url){
	$(ruleDetails).find(".actionTypeManager:first").remove();
	$(ruleDetails).find(".actionLabel").prepend('<div class="editIcons"><a href="' + url + '" class="addActionButton">add action</a></div>')
};

/*
 * XXX
 */
function hideTestmail(container) {
	var testMailwrapper = $(container).find('.testmailPart');
	$(testMailwrapper).prev('div:first').addClass('floatLeftTestmail');
	$(testMailwrapper).addClass('floatLeftTestmailLink');
	$(testMailwrapper).html('<a href="#" class="showTestmail">testmail</a>');
}

/*
 * start here not finished - just experimentel at the moment
 */
function sortableItems(container, itemWrapper, linkClass, sortableClass){
	var currentSortNr = '';
	var counter = 0;
	var direction = '';
	var sortContainer = '';
	
	if (sortableClass == null){
		sortContainer = $(container);
	}
	else{
		sortContainer = $(container).find(sortableClass);
	}
		
	
	$(sortContainer).sortable({    	
    	start: function(event, ui) {
			currentSortNr = $(ui.item).attr('name');
		},
		
		stop: function(event, ui) {
			$(sortContainer).find(itemWrapper).each(function(){
				$(this).attr('onmouseover', "style.cursor='wait'");
			});
			
			var numberMoves = 0;
			if (currentSortNr > $(ui.item).next(itemWrapper+':first').attr('name')){
				numberMoves = currentSortNr - $(ui.item).next(itemWrapper+':first').attr('name');
				direction = 'moveUp';
			};
			if (currentSortNr < $(ui.item).prev(itemWrapper+':first').attr('name')){
				numberMoves = $(ui.item).prev(itemWrapper+':first').attr('name') - currentSortNr;
				direction = 'moveDown';
			};
			for (i=0; i<numberMoves; i++){
				var y = 1;
				
				$.ajax({  
					type: "GET",  
					url: $(ui.item).find(linkClass+':first').attr('href') + '/' + direction,  
					success: function(data){
				       	if (direction == 'moveUp'){
				       		var prevItemSortNr = parseInt(currentSortNr) - y;
				       		var prevItem = $(sortContainer).find(itemWrapper + '[name=' + prevItemSortNr + ']:first');
				       		$(prevItem).attr('name', prevItemSortNr + 1);
				       		$(ui.item).attr('name', prevItemSortNr);
				       	}
				       	
				       	if (direction == 'moveDown'){
				       		var nextItemSortNr = parseInt(currentSortNr) + y;
				       		var nextItem = $(sortContainer).find(itemWrapper + '[name=' + nextItemSortNr + ']:first');
				       		$(nextItem).attr('name', nextItemSortNr - 1);
				       		$(ui.item).attr('name', nextItemSortNr);
				       	};
				       	y++;
			    	}
				});
			};
			
			$(sortContainer).find(itemWrapper).each(function(){
				$(this).attr('onmouseover', "style.cursor='pointer'");
			});
		}
	});
};

/*
 * XXX
 */
function hideSortLinks(container, item){
	$(container).find(item).each(function(){
		$(this).find('a[class=moveUp]').addClass('hidden');
		$(this).find('a[class=moveDown]').addClass('hidden');
	});
};

/*
 * XXX
 */
$(document).ready(function() {
	/*
	 * Make rules sortable, if id ruleContainer exists on load
	 */
	sortableItems('#ruleContainer', '.rule-wrapper', '.ruleLink');
	hideSortLinks('#ruleContainer', '.rule');
});

/*
 * XXX
 */
$('#RuleSetConfiglet').live('click', function(e){
	e.preventDefault();
	$('#tabs').find('a').each(function(){
		$(this).removeClass('activeTab');
	});
	$(this).addClass('activeTab');
	$('#tabResultContainer').load($(this).attr('href') + ' #tabContent',function(){	
		$('input[name=selectRulesetButton]').addClass('hidden');
	});
});

/*
 * XXX
 */
$('.finderRuleset').live('change', function(){
	$('#ruleSetContainer').load($(this).val() + ' #rulesetContent',function(){	
		$('input[name=selectRulesetButton]').addClass('hidden');
		sortableItems('#ruleContainer', '.rule-wrapper', '.ruleLink');
		hideSortLinks('#ruleContainer', '.rule');
	});
});

/*
 * XXX
 */
$('.rule').live('click', function(){
	if (blnClickRuleIcon == false){
		var url = $(this).find('a.ruleLink:first').attr('href');
		var itemWrapper = $(this).parents(".rule-wrapper:first");
		if ($(itemWrapper).find(".details:first").length == 0) { 
			$(itemWrapper).append('<div class="details"></div>');
			var ruleDetails = $(itemWrapper).find(".details:first");
			$(ruleDetails).load(url + ' .details', function(){
				ajaxesFilterManager (ruleDetails, url);
				ajaxesActionManager (ruleDetails, url);
				sortableItems(ruleDetails, '.filter-wrapper', '.filterLink', '.markerFilterManagement');
				hideSortLinks(ruleDetails, '.filtertable');
				sortableItems(ruleDetails, '.action-wrapper', '.actionLink', '.markerActionManagement');
				hideSortLinks(ruleDetails, '.actiontable');
				hideTestmail(ruleDetails);
			});
		}
		else {
			$(itemWrapper).find(".details:first").remove();
		}
	}
	else {
		blnClickRuleIcon = false;
	}
});

/*
 * Disable reload for item link
 */
$('.ruleLink').live('click', function(e){
	e.preventDefault();
});

/*
 * ajax get form for new ruleset (used by ControlPanelView)
 */
$('.addRuleSet').live('click', function(e){
	e.preventDefault();
	$('#ruleSetContainer').load ($(this).attr('href') + ' form');
});

/*
 * ajax submit form data and create rule set with param (used by ControlPanelView)
 */
$('#addRuleSetButton').live('click', function(e){
	e.preventDefault();

	var form = $(this).parents('form:first');
	
	var name = $(form).find("input[name=name]:first").val();
	var description = $(form).find("textarea[name=description]:first").val();
	var dataString = 'name='+ name + '&description=' + description;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var response = data;
	        var rulesetConfigletLink = $('#RuleSetConfiglet').attr('href');
	        $('#columnRulesetSelector').load(rulesetConfigletLink + ' #columnRulesetSelector',function(){	
				$('input[name=selectRulesetButton]').addClass('hidden');
				sortableItems('#ruleContainer', '.rule-wrapper', '.ruleLink');
				hideSortLinks('#ruleContainer', '.rule');
				$('#columnRulesetSelector').find('option:last').attr('selected', 'selected');
			});
	        $('#ruleSetContainer').html($(response).find('#rulesetContent').html());
	    }
	});
});

/*
 * ajax get form for edit ruleset (used by ControlPanelView)
 */
$('.editRuleset').live('click', function(e){
	e.preventDefault();
	$('#rulesetContent').find('.part:first').load($(this).attr('href') + ' form');
});

/*
 * ajax submit form data and save rule param (used by ControlPanelView)
 */
$('#editRuleSetButton').live('click', function(e){
	e.preventDefault();
	
	var form = $(this).parents('form:first');
	
	var name = $(form).find("input[name=name]:first").val();
	var description = $(form).find("textarea[name=description]:first").val();
	var dataString = 'name='+ name + '&description=' + description;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
			$('#RuleSetConfiglet').click();
	    }
	});
});

/*
 * XXX
 */
$('.delRuleset').live('click', function(e){
	e.preventDefault();
	
	$.ajax({  
		type: "GET",  
		url: $(this).attr('href'),
		success: function(){
			$('#RuleSetConfiglet').click();
		}
	});
})

/*
 * ajax get form for new rule (used by ControlPanelView)
 */
$(".addRule").live('click', function(e){
	e.preventDefault();
	$('#ruleContainer').append('<div class="rule-wrapper"><div class="item">NEW RULE</div><div class="details"></div></div>');
	$('#ruleContainer').find('.rule-wrapper:last').find('.details').load($(this).attr('href') + ' form', function(){
		var newRule = $('#ruleContainer').find('.rule-wrapper:last');
		$(newRule).find('h1:first').remove();
		// disable mail period and mail period unit as long as mail expect is not active
		$(newRule).find('input[name=form.expect_period]:first').attr('DISABLED', 'True');
		$(newRule).find('select[name=form.expect_period_unit]:first').attr('DISABLED', 'True');
		// XXX - edit same code, make funciton
		$(newRule).find('label[for=form.testmail]:first').parents('tr:first').remove(); // remove textarea for testmail
	});
});

/*
 * ajax submit form data and create rule with param (used by ControlPanelView)
 */
$("input[name='form.actions.addRule']").live('click', function(e){
	e.preventDefault();
	
	var ruleWrapper = $(this).parents('.rule-wrapper:first');
	var form = $(ruleWrapper).find('form:first');
	
	var name = $("input[name=form.name]").val();
	var description = $("textarea[name=form.description]").val();
	var severity = $(form).find("select[name=form.severity]").children('option:selected').val();
	var matching = $(form).find("select[name=form.matching]").children('option:selected').val();
	var expect_mail = ''; 
	if ($(form).find("input[name=form.expect_mail]").attr('checked')){
		expect_mail = $(form).find("input[name=form.expect_mail]").val();
	};
	var expect_period = $("input[name=form.expect_period]").val();
	var expect_period_unit = $(form).find("select[name=form.expect_period_unit]").children('option:selected').val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.name='+ name + 
					 '&form.description=' + description +
					 '&form.severity=' + severity +
					 '&form.matching=' + matching +
					 '&form.expect_mail=' + expect_mail +
					 '&form.expect_period=' + expect_period +
					 '&form.expect_period_unit=' + expect_period_unit +
					 '&form.testmail=' + // testmail is not display if js is active, has own js
					 '&form.actions.addRule=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
	        var response = data;
			$(ruleWrapper).html($(response).find('.rule-wrapper:first').html());
			
			var ruleDetails = $(ruleWrapper).find(".details:first");
			var url = $(ruleWrapper).find('.ruleLink:first').attr('href');
			ajaxesFilterManager (ruleDetails, url);
			ajaxesActionManager (ruleDetails, url);
			hideSortLinks('#ruleContainer', '.rule');
			sortableItems(ruleDetails, '.filter-wrapper', '.filterLink', '.markerFilterManagement');
			sortableItems(ruleDetails, '.action-wrapper', '.actionLink', '.markerActionManagement');
			hideTestmail(ruleWrapper);
	    }
	});
});

/*
 * ajax get form for edit rule (used by ControlPanelView)
 */
$(".editRule").live('click', function(e){
	e.preventDefault();
	blnClickRuleIcon = true;
	
	var itemWrapper = $(this).parents(".rule-wrapper:first");
	var details = $(itemWrapper).find(".details:first");
	if ($(details).length == 0){
		$(itemWrapper).append('<div class="details"></div>');
		details = $(itemWrapper).find(".details:first");
	};
	$(details).load($(this).attr('href') + ' form', function(){
		$(itemWrapper).find('h1:first').remove();
		// disable mail period and period unit if expect mail is not active
		var expectMail = $(itemWrapper).find('input[name=form.expect_mail]:first');
		if (!$(expectMail).attr('checked')){
			$(itemWrapper).find('input[name=form.expect_period]:first').attr('DISABLED', 'True');
			$(itemWrapper).find('select[name=form.expect_period_unit]:first').attr('DISABLED', 'True');
		};
		$(itemWrapper).find('label[for=form.testmail]:first').parents('tr:first').remove(); // remove textarea for testmail
	});
});

/*
 * ajax submit form data and save rule param (used by ControlPanelView)
 */
$("input[name='form.actions.editRule']").live('click', function(e){
	e.preventDefault();
	
	var ruleWrapper = $(this).parents(".rule-wrapper:first");
	var form = $(this).parents('form:first');
	
	var name = $(form).find("input[name=form.name]:first").val();
	var description = $(form).find("textarea[name=form.description]:first").val();
	var severity = $(form).find("select[name=form.severity]").children('option:selected').val();
	var matching = $(form).find("select[name=form.matching]").children('option:selected').val();
	var expect_mail = ''; 
	if ($(form).find("input[name=form.expect_mail]").attr('checked')){
		expect_mail = $(form).find("input[name=form.expect_mail]").val();
	};
	var expect_period = $("input[name=form.expect_period]").val();
	var expect_period_unit = $(form).find("select[name=form.expect_period_unit]").children('option:selected').val();
	var buttonId = $(form).find("input[type=submit]").val();
	var dataString = 'form.name='+ name + 
					 '&form.description=' + description +
					 '&form.severity=' + severity +
					 '&form.matching=' + matching +
					 '&form.expect_mail=' + expect_mail +
					 '&form.expect_period=' + expect_period +
					 '&form.expect_period_unit=' + expect_period_unit +
					 '&form.testmail=' + // testmail is not display if js is active, has own js
					 '&form.actions.editRule=' + buttonId;
	
	$.ajax({  
		type: "POST",  
		url: $(form).attr('action'),  
		data: dataString,
		success: function(data){
			var resultData = data;
			$(ruleWrapper).html($(resultData).find('.rule-wrapper:first').html());
			hideSortLinks('#ruleContainer', '.rule');
			hideSortLinks(ruleWrapper, '.filter-wrapper');
			hideSortLinks(ruleWrapper, '.action-wrapper');
			hideTestmail(ruleWrapper);
		}
	});
});

/*
 * XXX
 */
$(".delRule").live('click', function(e){
	e.preventDefault();
	blnClickRuleIcon = true;
	
	var ruleWrapper = $(this).parents('.rule-wrapper:first');
	$.ajax({  
		type: "GET",  
		url: $(this).attr('href'),
		success: function(){
			$(ruleWrapper).remove();
		}
	});
});

/*
 * XXX - de-/activate mail period, period unit if change
 */
$("input[name='form.expect_mail']").live('click', function(){
	var formWrapper = $(this).parents('.details:first');
	if ($(formWrapper).find('input[name=form.expect_period]:first').attr('DISABLED')) {
		$(formWrapper).find('input[name=form.expect_period]:first').removeAttr('DISABLED');
		$(formWrapper).find('select[name=form.expect_period_unit]:first').removeAttr('DISABLED');
	}
	else {
		$(formWrapper).find('input[name=form.expect_period]:first').attr('DISABLED', 'True');
		$(formWrapper).find('select[name=form.expect_period_unit]:first').attr('DISABLED', 'True');
	};
});