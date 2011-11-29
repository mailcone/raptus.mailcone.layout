

ui_elements = {
  // dont change this order if you don't know what you do!
  init_functions: ['splitter',
                   'accordion',
                   'elastic',
                   'datatable',
                   'buttons',
                   'add',
                   'form_controls',
                   'datetime',
                   'jqtransform',
                   'tabs',
                   'ajax_content_submit'],
  
  
  init: function(context){
    ui_elements._form_controls_mapping();
    $.each(ui_elements.init_functions, function(index, func){
        ui_elements[func](context);
    });
  },
  
  
  accordion: function(context){
      var init = function(obj){
          var options = {};
          var data = obj.data('accordion-options');
          if (data)
            options = $.extend(options, data);
          obj.accordion(options);
      }
      ui_elements._context(context).find('.ui-accordion').each(function(){
          
          if($(this).hasClass('uldata')){
              var accordion = $(this);
              accordion.children().children().each(function(){
                  accordion.append('<h3>'+$(this).html()+'</h3>');
                  accordion.find('h3:last div:first').appendTo(accordion);
              });
              accordion.find('ul:first').remove();
              init($(this));
          }else {
              init($(this));
          }
      })
  },
  
  
  tabs: function(context){
      ui_elements._context(context).find('.ui-tabs').each(function(){
          var options = {};
          var data = $(this).data('tabs-options');
          if (data)
            options = $.extend(options, data);
          $(this).tabs();
      });
  },
  
  
  elastic: function(context){
      ui_elements._context(context).find('textarea').elastic();
  },
  
  
  datetime: function(context){
      ui_elements._context(context).find('input.date').attr('autocomplete', 'off').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: $.datepicker._defaults.dateFormat.replace('yy', 'y')
      });
      ui_elements._context(context).find('input.spinbox.hours').attr('autocomplete', 'off').spinbox({
        min: 0,
        max: 23,
        step: 1,
        bigStep: 5,
        mousewheel: false,
        keys: [/[0-9]/,9,13,8,46,33,34,37,38,39,40,96,97,98,99,100,101,102,103,104,105,109,188,190]
      });
      ui_elements._context(context).find('input.spinbox.minutes').attr('autocomplete', 'off').spinbox({
        min: 0,
        max: 59,
        step: 1,
        bigStep: 10,
        mousewheel: false,
        keys: [/[0-9]/,9,13,8,46,33,34,37,38,39,40,96,97,98,99,100,101,102,103,104,105,109,188,190]
      });
  },
  
  
  jqtransform: function(context){
      ui_elements._context(context).find('form').jqTransform();
      ui_elements._context(context).find('input[type="checkbox"]').jqTransCheckBox()
      ui_elements._context(context).find('input[type="radio"]').jqTransRadio();
  },
  
  
  datatable: function(context){
    ui_elements._context(context).find('.ui-datatable').each(function(){
         var table = $(this).dataTable( {
            sDom: 'T<"clear">frtiS',
            sScrollY: '100%',
            sScrollX: '100%',
            bDeferRender: true,
            bAutoWidth: true,
            sAjaxSource: $(this).data('ajaxurl'),
            bServerSide: true,
            bJQueryUI: true,
            fnDrawCallback: $.proxy(ui_elements._datatable_redraw, this),
            fnServerData: $.proxy(ui_elements._datatable_json, this),
            oTableTools: $(this).data('tabletools'),
        } );
        
       
        $(window).bind('resize', function () {
        table.fnAdjustColumnSizing();
    } );
    
        
        $(this).find('tbody').click(function(event) {
            var tr = $(event.target.parentNode);
            $(table.fnSettings().aoData).each(function (){
                $(this.nTr).removeClass('ui-state-active');
            });
            if (tr.data('ajaxcontent')){
                $(tr).addClass('ui-state-active');
                $('#ui-datatable-ajaxcontent').load(tr.data('ajaxcontent'),function(){
                    $('#ui-datatable-ajaxcontent').data('ajaxcontent', tr.data('ajaxcontent'));
                    ui_elements.init($('#ui-datatable-ajaxcontent'));
                });
            }
        });
    });
      
  },


  splitter: function(context){
    ui_elements._context(context).find('.ui-splitter').splitter({type: 'h',
      //outline: true,
      sizeTop: true,
      resizeToWidth: true,
     // cookie: "vsplitter",	
    });
  },
  
  
  buttons: function(context){
      ui_elements._context(context).find( '.ui-button' ).each(function(){
          var option = { icons: {primary:$(this).data('ui-icon')},
                         text: $(this).data('ui-text')?$(this).data('ui-text'):false};
          $(this).button(option);
          
      });
  },
  
  
  add: function(context){
    ui_elements._context(context).find('.ui-add').each(function(){
        $(this).click(function(){
            ui_elements._ajax_modal($(this).attr('href'), $(this));
            return false;
        });
        
    });
  },
  
  
  ajax_content_submit: function(context){
    ui_elements._context(context).find('.ui-ajax-content-submit').each(function(){
        $(this).click(function(){
            var content = $('#ui-datatable-ajaxcontent');
            var data = {};
            var tabindex = $('.ui-tabs:first').tabs('option','selected');
            content.find('.ui-datatable').each(function(){
                data = $.extend(data,$(this).data('inputdata')?$(this).data('inputdata'):{});
            });
            data = $.extend(data, ui_elements._data_crapper(content));
            content.load(content.data('ajaxcontent'), {metadata:JSON.stringify(data)}, function(){
                ui_elements.init(content);
                $('.ui-tabs:first').tabs('option','selected', tabindex);
            });
            return false;
        });
        
    });
  },
  
  
  _form_controls_mapping: function(){
    if (!ui_elements.form_controls_mapping)
     ui_elements.form_controls_mapping = {};
    ui_elements.form_controls_mapping['form.actions.submit']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.add']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.edit']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.delete']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.cancel']= ui_elements._form_controls_cancel;
    
  },


  form_controls: function(){
      var dialog = $('#ui-modal-content');
      var form = $('.actionsView').parents('form');
      form.submit(function(){
          return false;
      });
      var buttons = {};
      form.find('input[type="submit"]').each(function(){
          if ($(this).attr('id') in ui_elements.form_controls_mapping){
              var func = ui_elements.form_controls_mapping[$(this).attr('id')];
              buttons[$(this).val()] = $.proxy(func, this);
          }
      });
      dialog.dialog('option', 'buttons', buttons);
      dialog.find('.actionsView input').remove();

  },
  
  _context: function(context){
      if (context instanceof $)
        return context;
      return $('html');
      
  },
  
  
  _datatable_redraw: function(){
      $(this).find('tr .ui-datatable-ajaxlink').click(function(){
          ui_elements._ajax_modal($(this).attr('href'), $(this));
          return false;
      });
  },
  
  
  _datatable_json: function(sSource, aoData, fnCallback){
      var table = $(this)
      $.getJSON( sSource, aoData, function (json) {
          fnCallback(json);
          if (!json.metadata)
            return;
          var metadata = json.metadata;
          if (metadata.ajaxcontent) {
              table.find('tr').each(function(index){
                  ui_elements.init($(this));
                  $(this).data('ajaxcontent', metadata.ajaxcontent[index-1]);
              });
          }
          // input/checkbox stuff
          if (!table.data('inputdata'))
            table.data('inputdata', {});
          var data = table.data('inputdata');
          table.find('input').change(function(){
              data[$(this).attr('name')] = $(this).is(':checked');
          });
      });
  },
  
  
  _ajax_modal: function(url, element, postdata, callback){
      var dialogid = 'ui-modal-content';
      if (!$('#'+dialogid).length)
        $('body').append('<div id="'+dialogid+'"/>');
      var dialog = $('#'+dialogid);
      dialog.load(url, postdata, function(){
          if (callback)
            callback(dialog);
          ui_elements._init_dialog(dialog, element);
      });
    },
  
  
  _init_dialog: function(dialog, element){
      dialog.dialog({height: element?element.hasClass('ui-modal-minsize')?200:600:600,
                     width: 500,
                     modal: true});
      var title = dialog.find('h1:first');
      dialog.dialog( 'option', 'title', title.html() );
      title.remove();
      ui_elements.init(dialog);
  },
  
  _form_controls_submit: function(){
        var dialog = $('#ui-modal-content');
        var form = $('.actionsView').parents('form');
        var additional = '&'+$(this).attr('name')+'='+$(this).val();
        dialog.load(form.attr('action'),form.serialize() + additional, function(){
            if (dialog.find('.error').length)
               ui_elements._init_dialog(dialog);
            else
               window.location.reload(true);
        });
      },
      
      
  _form_controls_cancel: function(){
        var dialog = $('#ui-modal-content');
        dialog.dialog('close');
        return false;
      },
  
  
  _data_crapper: function(context){
      var di = {};
      context.find('input, textarea, select').val(function(index, value){
          if ($(this).is(':checkbox')){
              //special case for ckeckboxes, maybe we need some more..
              di[$(this).attr('name')] = $(this).is(':checked');
              return;
          }
          di[$(this).attr('name')] = value;
      });
      return di;
  },
  
}
jQuery(document).ready(ui_elements.init);