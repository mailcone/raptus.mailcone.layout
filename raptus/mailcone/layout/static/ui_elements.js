

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
                   'codemirror',
                   'proposewidget',
                   'tabs',
                   'ajax_content_submit',
                   'mail_chart'],
  
  
  init: function(context){
    ui_elements._form_controls_mapping();
    $.each(ui_elements.init_functions, function(index, func){
        ui_elements[func](context);
    });
  },
  
  
  mail_chart: function(context){

    var jsonurl = './indexajaxsource';
    var email_element_id = 'mail_chart';
    
    if (!$('#' + email_element_id).length)
        return;

    var ajaxDataRenderer = function(url, plot, options) {
        var ret = null;
        $.ajax({
            // have to use synchronous here, else the function
            // will return before the data is fetched
            async : false,
            url : url,
            dataType : "json",
            success : function(data) {
                ret = data;
                console.warn(data);
            }
        });
        return ret;
    }; 

    $.jqplot.config.enablePlugins = true;
    var plot2 = $.jqplot(email_element_id, jsonurl,{
        dataRenderer: ajaxDataRenderer,
        dataRendererOptions: {
          unusedOptionalUrl: jsonurl
        },
        axes:{
            xaxis:{
                renderer:$.jqplot.DateAxisRenderer, 
                rendererOptions:{
                    tickRenderer:$.jqplot.CanvasAxisTickRenderer
                },
                tickOptions:{
                    formatString:'%b %#d, %H:%M  ',
                    tickInterval:'10 days',
                    angle:-60
                }
            },
            yaxis:{
                rendererOptions:{
                    tickRenderer:$.jqplot.CanvasAxisTickRenderer},
                    tickOptions:{
                        tickOptions:{formatString:'%d'},
                    }
            }
        },
        series:[{ lineWidth:4, markerOptions:{ style:'square' } }],
      });
  },
  
  
  accordion: function(context){
      var init = function(obj){
          var options = {navigation:true,
                         navigationFilter:function(index, context){
                             return $(context).parent().hasClass('active');
                         }};
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
                  var div = accordion.find('h3:last div:first');
                  div.addClass(div.find('li.active').length?'active':'');
                  div.appendTo(accordion);
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
      ui_elements._context(context).find('select').parent().jqTransform();
      ui_elements._context(context).find('input[type="checkbox"]').jqTransCheckBox()
      ui_elements._context(context).find('input[type="radio"]').jqTransRadio();
      var index_fix = function(){
          $('.jqTransformSelectWrapper').css('z-index', 10);
          $(this).css('z-index', 11);
      };
      $('.jqTransformSelectWrapper').mouseover(index_fix);
  },
  
  
  datatable: function(context){
    ui_elements._context(context).find('.ui-datatable').each(function(){
        // !!! remove id to fix destroy datatable
        // http://www.datatables.net/forums/discussion/7423/fndestroy-not-working/p1
        $(this).attr('id', '');
        var table = $(this).dataTable( {
          sDom: 'frtiS',
          sScrollY: '100%',
          bDeferRender: true,
          bAutoWidth: true,
          sAjaxSource: $(this).data('ajaxurl'),
          bServerSide: true,
          bJQueryUI: true,
          fnDrawCallback: $.proxy(ui_elements._datatable_redraw, this),
          fnServerData: $.proxy(ui_elements._datatable_json, this),
          oTableTools: $(this).data('tabletools'),
          oScroller: {
            loadingIndicator: true,
            rowHeight: 22
            }
       } );
       // save datatable instance to html tag
       //$(this).addClass('ui-datatable-inst')
       //$(this).data('datatable_inst',table);
       
        // resize table
        var scroller = table.parents('.dataTables_scroll').resize(function(){table.fnAdjustColumnSizing()});
        var sparent = scroller.parents('.dataTables_wrapper');
        function set_size(){
            scroller.height(sparent.height() - 87);
        }
        set_size();
        sparent.resize(set_size);
        $(this).find('tbody').mouseover(function(){
            var tr = $(event.target.parentNode);
            if (tr.data('ajaxcontent'))
                tr.css('cursor', 'pointer');
        });
        
        $(this).find('tbody').click(function(event) {
            var tr = $(event.target.parentNode);
            if (!tr.is('tr'))
                tr = tr.parents('tr');
            $(tr.parent().find('tr')).each(function (){
                $(this).removeClass('ui-state-active');
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
    /*
    for better user experience we're going to store the position of the splitter and will restore it
    
    $("#MySplitter").splitter("resize", 200);
    $.cookie("example", "foo");
    */
    
    var splitters = ui_elements._context(context).find('.ui-splitter').splitter({
        type: 'h',
        resizeToWidth: true
        //anchorToWindow: true
        // cookie: "vsplitter",	
      }
    );
   
   
   splitters.each(function(){
      // Account for margin or border on the splitter container and enforce min height
      
      var dimSum=function dimSum(jq, dims) {
            // Opera returns -1 for missing min/max width, turn into 0
            var sum = 0;
            for(var x = 0; x < jq.length; x++)
                for (var i=1; i < arguments.length; i++ )
                    sum += Math.max(parseInt($(jq[x]).css(arguments[i])) || 0, 0);
            return sum;
        };
      
      /* modified version of anchorToWindow - sadly it's not possible to solve it with pure css*/
      var adjust = dimSum($(this), "borderTopWidth", "borderBottomWidth", "marginBottom", 'marginTop');
      var hmin = Math.max(dimSum($(this).children(), "minHeight"), 20);
      
      var obj = $(this);
      
      $(window).bind("resize", function(){
        obj.css('height', 0);
        var top = 0;//obj.offset().top;//-obj.parent().offset().top;
        var wh = obj.parent().height();//[0].offsetHeight;
        //window.status = wh + ' / ' + top + ' / ' + adjust + ' / ' + hmin + ' / '+ (wh-top-adjust);
        obj.css("height", Math.max(wh-top-adjust, hmin)+"px");
        if ( !$.browser.msie ) obj.triggerHandler("resize");
      }).trigger("resize");
    });
    
    /* we can not use the intern cookie function of the splitter because we're overwriting the position by our (needed) resizing function -_- */
    $(window).unload(function(){
       var top = splitters.find('.hsplitbar').css('top');
       if(top != undefined && top != 'auto')
          $.cookie('verticalsplitter', parseInt(top, 10));
    });
    
    splitters.trigger('resize', [$.cookie('verticalsplitter')]);
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
            data = $.extend(data, ui_elements._data_collector(content));
            content.load(content.data('ajaxcontent'), {metadata:JSON.stringify(data)}, function(){
                ui_elements.init(content);
                $('.ui-tabs:first').tabs('option','selected', tabindex);
            });
            return false;
        });
        
    });
  },
  
  
  codemirror: function(context){
      ui_elements._context(context).find('.ui-codemirror').each(function(){
          var area = $(this);
          var parent = area.parent();
          var mode = $(this).data('mode');
          area.replaceWith('<textarea id="'+area.attr('id')+
                            '" class="'+area.attr('class')+
                            '" name="'+area.attr('name')+
                            '">'+area.text()+'</textarea>');
          area = parent.find('.ui-codemirror');
          console.log(area);
          var editor = CodeMirror.fromTextArea(area[0],{
            mode: mode,
            lineNumbers: true,
            onChange: function() {
                area.val(editor.getValue());
            },
            onCursorActivity: function() {
                editor.setLineClass(hlLine, null);
                hlLine = editor.setLineClass(editor.getCursor().line, "activeline");
                }
            });
            var hlLine = editor.setLineClass(0, "activeline");
      });
  },
  
  
  proposewidget: function(context){
      ui_elements._context(context).find('.propose-widget').each(function(){
          var textarea = $(this).find('textarea');
          var options = $(this).find('option');
          options.each(function(){
              $(this).click(function(){
                  var text = textarea.val();
                  var end = textarea.caret().start;
                  var input = '${'+$(this).val()+'}';
                  options.removeAttr('selected');
                  textarea.val(text.slice(0, end)+ input + text.slice(end, text.length));
              });
          });
          
      });
  },
  
  
  _form_controls_mapping: function(){
    if (ui_elements.form_controls_mapping)
        return;
    ui_elements.form_controls_mapping = {};
    ui_elements.form_controls_mapping['form.actions.submit']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.add']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.edit']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.delete']= ui_elements._form_controls_submit;
    ui_elements.form_controls_mapping['form.actions.cancel']= ui_elements._form_controls_cancel;
    
    ui_elements.datatable_controls_mapping = {};
    ui_elements.datatable_controls_mapping['ui-datatable-ajaxlink']= ui_elements._datatable_control_ajaxlink;
  },


  form_controls: function(context){
      var form = ui_elements._context(context).find('.actionsView');
      var dialog = form.parents('#ui-modal-content');
      if (!form.length)
            return;
      form = form.parents('form');
      var buttons = {};
      form.find('input[type="submit"]').each(function(){
          if ($(this).attr('id') in ui_elements.form_controls_mapping){
              var func = ui_elements.form_controls_mapping[$(this).attr('id')];
              buttons[$(this).val()] = $.proxy(func, this);
          }
      });
      
      if (dialog.length) {
          form.submit(function(){
              return false;
          });
          dialog.dialog('option', 'buttons', buttons);
          dialog.find('.actionsView input').remove();
      }

  },
  
  _context: function(context){
      if (context instanceof $)
        return context;
      return $('html');
      
  },
  
  
  _datatable_redraw: function(){
      var context = this;
      $.each(ui_elements.datatable_controls_mapping, function(key, func){
          $(context).find('tr .' + key).each(function(){
              $.proxy(func, this)();
          });
      });
  },
  
  
  _datatable_control_ajaxlink: function(){
      $(this).click(function(){
          ui_elements._ajax_modal($(this).attr('href'), $(this));
          return false;
      });
  },
  
  
  _datatable_json: function(sSource, aoData, fnCallback){
      var table = $(this);
      var loader = $('div.DTS div.DTS_Loading');
      loader.show();
      $.getJSON( sSource, aoData, function (json) {
          fnCallback(json);
          loader.hide();
          if (!json.metadata)
            return;
          var metadata = json.metadata;
          table.find('tr').each(function(index){
            if ('css_class' in metadata)
              $(this).addClass(metadata.css_class[index-1]?metadata.css_class[index-1]:'');
            if (metadata.ajaxcontent)
              $(this).data('ajaxcontent', metadata.ajaxcontent[index-1]);
            ui_elements.init($(this));
          });
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
      $('#'+dialogid).remove()
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
  
  
  _data_collector: function(context){
      var di = {};
      context.find('input, textarea, select').val(function(index, value){
          if ($(this).is(':checkbox')){
              //special case for ckeckboxes, maybe we need some more..
              di[$(this).attr('name')] = $(this).is(':checked');
              return;
          }
          di[$(this).attr('name')] = value;
          return value;
      });
      return di;
  },
  
}

jQuery(document).ready(ui_elements.init);
