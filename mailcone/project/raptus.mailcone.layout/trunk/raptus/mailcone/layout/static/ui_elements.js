

ui_elements = {
  init: function(){
    ui_elements.accordion();
  },
  
  accordion: function(){
      $('.ui-accordion').each(function(){
          if($(this).hasClass('uldata')){
              var accordion = $(this);
              accordion.children().children().each(function(){
                  accordion.append('<h3>'+$(this).html()+'</h3>');
                  accordion.find('h3:last div:first').appendTo(accordion);
              });
              accordion.find('ul:first').remove();
              $(this).accordion();
          }
      })
  }
}
jQuery(document).ready(ui_elements.init);
