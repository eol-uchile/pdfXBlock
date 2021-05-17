/* Javascript for pdfXBlock. */
function pdfXBlockInitEdit(runtime, element) {

    $(element).find('.action-cancel').bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function() {
        var form_data = new FormData();
        form_data.append('display_name', $('#pdf_edit_display_name').val());
        form_data.append('pdf_file', $(element).find('#pdf_file').prop('files')[0]);
        
        runtime.notify('save', {state: 'start'});
        
        var handlerUrl = runtime.handlerUrl(element, 'save_pdf');
        $.ajax({
            url: handlerUrl,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: "POST",
            success: function(response) {
                if (response.errors.length > 0) {
                    response.errors.forEach(function(error) {
                        runtime.notify("error", {
                            "message": error,
                            "title": "PDF component save error"
                        });
                    });
                } else {
                    runtime.notify('save', {
                        state: 'end'
                    });
                }
            }
        });
    });
}