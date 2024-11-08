/* @odoo-module */

import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.HelloWorldPopup = publicWidget.Widget.extend({
    selector: '#wrapwrap',

    init() {
        this.dialog = this.bindService("dialog");
    },
    start() {

      const toggleInfoButton = document.getElementById("toggle-info-button");
      const ownerInfo = document.getElementById("owner-info");
  
      if (toggleInfoButton) {
          toggleInfoButton.addEventListener("click", function () {
          //    $("#owner-info").slideToggle("slow");
  
              
              // Toggle class 'invisible' trên ownerInfo
              ownerInfo.classList.toggle("invisible_1")
              
              // Thay đổi nội dung của nút dựa trên trạng thái hiển thị
              if (ownerInfo.classList.contains("invisible_1")) {
                  toggleInfoButton.textContent = "Ẩn thông tin chủ nhà ";
                  
              } else {
                  toggleInfoButton.textContent = "Hiển thị thông tin chủ nhà";
                  
              }
          });
      }

        return this._super.apply(this, arguments);
    },
});


