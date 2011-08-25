$('.item').live('click', function(){
	window.location.href = $(this).find('a.itemLink:first').attr('href');
});

$('.item').live('click', function(e){
	e.preventDefault();
});