/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2ManyBinary } from "@web/views/fields/many2many_binary/many2many_binary";

export class MultiImageDragDrop extends Many2ManyBinary {
    setup() {
        super.setup();
        this.dragCounter = 0; // Track drag events
    }

    // Override template rendering if necessary
    get template() {
        return 'YourModule.MultiImageDragDrop';
    }

    // Bind drag-and-drop events after rendering
    onMounted() {
        super.onMounted();
        this.el.addEventListener('dragover', this._onDragOver.bind(this));
        this.el.addEventListener('drop', this._onDrop.bind(this));
        this.el.addEventListener('dragleave', this._onDragLeave.bind(this));
    }

    // Event handler when files are dragged over the widget
    _onDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        this.el.classList.add('o_drag_over');
    }

    // Event handler when files are dropped into the widget
    _onDrop(event) {
        event.preventDefault();
        event.stopPropagation();
        this.el.classList.remove('o_drag_over');

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this._handleFileUpload(files);
        }
    }

    // Event handler for drag leave
    _onDragLeave(event) {
        event.preventDefault();
        event.stopPropagation();
        this.dragCounter--;
        if (this.dragCounter === 0) {
            this.el.classList.remove('o_drag_over');
        }
    }

    // Handle the file upload
    _handleFileUpload(files) {
        const attachments = [];
        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = (event) => {
                const data = event.target.result.split(',')[1]; // Extract base64 data
                attachments.push({
                    name: file.name,
                    data: data,
                    mimetype: file.type,
                });
                this._addAttachment(attachments); // Add files to the widget
            };
            reader.readAsDataURL(file);
        });
    }

    // Add files to the Many2ManyBinary field
    async _addAttachment(attachments) {
        for (let attachment of attachments) {
            await this.model.saveRecord({
                data: attachment,
            });
        }
        // Re-render the widget after adding files
        this.render();
    }
}

// Register the new widget
registry.category("fields").add("many2many_binary_drag_drop", MultiImageDragDrop);
