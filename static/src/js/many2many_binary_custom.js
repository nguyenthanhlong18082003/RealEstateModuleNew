/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Many2ManyBinaryField, many2ManyBinaryField } from "@web/views/fields/many2many_binary/many2many_binary_field";


export class Many2ManyBinaryFieldCustom extends Many2ManyBinaryField {
    setup() {
       super.setup();
    }
    isImage(file) {
        const imageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp'];
        return imageTypes.includes(file.mimetype);
    }

}
Many2ManyBinaryFieldCustom.template = "web.Many2ManyBinaryFieldCustom";

export const many2ManyBinaryFieldCustom = {
    ...many2ManyBinaryField,
    component: Many2ManyBinaryFieldCustom,
};
registry.category("fields").add("many2many_binary_custom", many2ManyBinaryFieldCustom);