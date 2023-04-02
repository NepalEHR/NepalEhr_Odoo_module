odoo.define('bahmni_insurance_odoo.stock_quant_tree_view_button', function (require){
    "use strict";
    var Model = require('web.Model') 
    var core = require('web.core');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;
    var custom_model = new Model('stock.quant') 
    ListView.include({       
    
           
    
            render_buttons: function($node) {
                var self = this;
                this._super($node);
                    this.$buttons.find('.o_list_button_bulk_archieve').click(this.proxy('action_bulk_archieve'));
                   
        },
           
            action_bulk_archieve: function () {  
                new Model("stock.quant").call("action_bulk_archieve",[this.get_selected_ids()]).then(function(result){
                     window.location.reload() 
                    console.log(result);//show result in console
                    });
            }  
    
    });
    
    });