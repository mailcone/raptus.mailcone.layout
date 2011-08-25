function searchTarget (self, parentContainer, targetContainer)
{
	return $(self).parents(parentContainer).find (targetContainer);
};

function addSnippet (url, targetContainer, delCurrentContent) {
	$.ajax({
		  url: url,
		  success: function(data) {
		    addHTMLSnippet(targetContainer, data, delCurrentContent);
		  }
	});
	
};
	
function addHTMLSnippet (targetContainer, snippet, delCurrentContent)
{
	if (delCurrentContent == true){
		$(targetContainer).html("");
	}
	//add Item
	$(targetContainer).append (snippet);
};

$("#addRuleset").live ('click', function () 
{
	var tC = searchTarget($(this), ".jsRootMarker", ".newItemMarker");
	addSnippet ('http://localhost:8080/test/newRuleset', tC, true);
});

$(".addRule").live ('click', function () 
{
	addSnippet ('http://localhost:8080/test/newRule', "#RuleManagement", false);
});

/*
 * XXX: Missing, not yet implemented
 * $(".editRule").live ('click', function ()
 * ...
 */

$(".delRule").live ('click', function () 
{
	var wrapper = $(this).parents('.item-wrapper:first');	
	wrapper.remove();
});

$(".addFilter").live ('click', function () 
{
	var tC = $(this).parents(".markerFilterManagement:first");
	addSnippet ('http://localhost:8080/test/newFilter', tC, false);
});

/*
 * XXX: Missing, not yet implemented
 * $(".editFilter").live ('click', function ()
 * ...
 */

$(".delFilter").live ('click', function () 
{
	var wrapper = $(this).parents('.filterTable:first');	
	wrapper.remove();
});


/*
 * XXX: not done yet must be change also in app.py, at the moment coded with old approach
 */
$(".markerButton").live ('click', function ()
{
	var infoBox = $(this).parents(".jsRootMarker").find (".newItemMarker");
	
	/*
	 * XXX: not done yet must be change also in app.py, at the moment coded with old approach
	 */
	if ($(this).attr('id') == "addCustomer")
	{
		//url must be generic
		$.get('http://localhost:8080/test/customer_edit_form', function(data) {
			$(infoBox).append (data);
		});
	};
});