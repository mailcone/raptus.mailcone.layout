

ui_elements = {
  init_functions: ['splitter',
                   'accordion',
                   'elastic',
                   'datatable',
                   'buttons',
                   'add',
                   'form_controls'],
  
  
  init: function(context){
    $.each(ui_elements.init_functions, function(index, func){
        ui_elements[func](context);
    });
  },
  
  
  accordion: function(context){
      ui_elements._context(context).find('.ui-accordion').each(function(){
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
  },
  
  
  elastic: function(){
      $('textarea').elastic();
  },
  
  
  datatable: function(context){
    ui_elements._context(context).find('.ui-datatable').each(function(){
        $(this).dataTable( {
            bProcessing: true,
            sAjaxSource: $(this).data('ajaxurl')
        } );
        
    });
      
  },


  splitter: function(context){
    ui_elements._context(context).find('.ui-splitter').splitter({type: 'h', anchorToWindow:false,});
  },
  
  
  buttons: function(context){
      ui_elements._context(context).find( '.ui-button' ).button();
  },
  
  
  add: function(context){
    ui_elements._context(context).find('.ui-add').each(function(){
        $(this).click(function(){
            ui_elements._ajax_modal($(this).attr('href'));
            return false;
        });
        
    });
  },
  
  
  form_controls: function(){
      var form = $('#actionsView').parents('form');
      var dialog = $('#ui-modal-content');
      form.submit(function(){
          return false;
      });
      
      var submit = function(){
        var additional = '&'+$(this).attr('name')+'='+$(this).val();
        dialog.load(form.attr('action'),form.serialize() + additional, function(){
            if (dialog.find('.error').length)
               ui_elements._init_dialog(dialog);
            else
               window.location.reload(true);
        });
      }
      
      var close = function(){
        dialog.dialog('close');
        return false;
      }
      
      var buttons = {};
      form.find('input[type="submit"]').each(function(){
          switch($(this).attr('id')) {
            case 'form.actions.add':
                buttons[$(this).val()] = $.proxy(submit, this);
                break;
            case 'form.actions.edit':
                buttons[$(this).val()] = $.proxy(submit, this);
                break;
            case 'form.actions.cancel':
                buttons[$(this).val()] = $.proxy(close, this);
                break;
          }
      });
      dialog.dialog('option', 'buttons', buttons);
      dialog.find('#actionsView input').remove();

  },
  
  _context: function(context){
      if (context instanceof $)
        return context;
      return $('html');
      
  },
  
  _ajax_modal: function(url){
      var dialogid = 'ui-modal-content';
      if (!$('#'+dialogid).length)
        $('body').append('<div id="'+dialogid+'"/>');
      
      var dialog = $('#'+dialogid);
      dialog.dialog({height: 600,
                     width: 500,
                     modal: true});
      dialog.load(url, function(){
          ui_elements._init_dialog(dialog)
      });
    },
  
  
  _init_dialog: function(dialog){
      var title = dialog.find('h1:first');
      dialog.dialog( 'option', 'title', title.html() );
      title.remove();
      ui_elements.init(dialog);
  }
  
  
}
jQuery(document).ready(ui_elements.init);
