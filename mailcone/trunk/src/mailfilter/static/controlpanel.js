/*
 * Function set different classes, 
 * listed configlets appears as tabs afterwards
 */
$(function(){
	// Add class slidecontainer to first ul find
	$('#tabs').find('ul:first').addClass('slidecontainer')
	// Add class tab to slides 
	$('#tabs').find('a').each(function(){
		$(this).addClass('tab');
	});
	$('#tabs').append('<div id="tabResultContainer"></div>');
	$('#tabs').find('a:first').click();
});