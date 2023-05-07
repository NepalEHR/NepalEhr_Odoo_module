odoo.define('module.extension_name', function (require) {
    var FormView = require('web.FormView');
    FormView.include({
     load_record: function() {
      this._super.apply(this, arguments);
      if (this.model === 'sale.order') {
          if (this.datarecord && (this.datarecord.state != 'draft')) {
            console.log(this.datarecord.state)
            this.$buttons.find('.o_form_button_edit').css({'display':'none'});
          }
          else {
            this.$buttons.find('.o_form_button_edit').css({'display':''});
          }
       }

       if (this.model === 'purchase.order') {
        
        console.log("test",this.datarecord.state)
          if (this.datarecord && (this.datarecord.state != 'draft')) {
            console.log("test",this.datarecord.state)
            this.$buttons.find('.o_form_button_edit').css({'display':'none'});
          }
          else {
            this.$buttons.find('.o_form_button_edit').css({'display':''});
            console.log("Hello load test")
          }
       }
    }
    });
});