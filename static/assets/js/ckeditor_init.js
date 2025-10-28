document.addEventListener("DOMContentLoaded", function() {
    ClassicEditor
        .create(document.querySelector('#id_content'), {
            language: 'fa',
            toolbar: [
                'heading', '|',
                'bold', 'italic', 'underline', 'strikethrough', 'highlight', '|',
                'link', 'blockQuote', 'code', 'codeBlock', '|',
                'bulletedList', 'numberedList', 'todoList', '|',
                'outdent', 'indent', '|',
                'alignment', '|',
                'insertTable', 'imageUpload', 'mediaEmbed', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
                'removeFormat', 'sourceEditing'
            ],
            alignment: {
                options: [ 'left', 'right', 'center', 'justify' ]
            },
            table: {
                contentToolbar: [
                    'tableColumn', 'tableRow', 'mergeTableCells',
                    'tableProperties', 'tableCellProperties'
                ],
                tableProperties: {
                    borderColors: [
                        { color: 'hsl(4, 90%, 58%)', label: 'Red' },
                        { color: 'hsl(340, 82%, 52%)', label: 'Pink' },
                        { color: 'hsl(291, 64%, 42%)', label: 'Purple' },
                        { color: 'hsl(262, 52%, 47%)', label: 'Deep Purple' },
                        { color: 'hsl(231, 48%, 48%)', label: 'Indigo' },
                        { color: 'hsl(207, 90%, 54%)', label: 'Blue' }
                    ],
                    backgroundColors: [
                        { color: 'hsl(4, 90%, 58%)', label: 'Red' },
                        { color: 'hsl(340, 82%, 52%)', label: 'Pink' },
                        { color: 'hsl(291, 64%, 42%)', label: 'Purple' },
                        { color: 'hsl(262, 52%, 47%)', label: 'Deep Purple' },
                        { color: 'hsl(231, 48%, 48%)', label: 'Indigo' },
                        { color: 'hsl(207, 90%, 54%)', label: 'Blue' }
                    ]
                },
                tableCellProperties: {
                    borderColors: [
                        { color: 'hsl(4, 90%, 58%)', label: 'Red' },
                        { color: 'hsl(340, 82%, 52%)', label: 'Pink' },
                        { color: 'hsl(291, 64%, 42%)', label: 'Purple' },
                        { color: 'hsl(262, 52%, 47%)', label: 'Deep Purple' },
                        { color: 'hsl(231, 48%, 48%)', label: 'Indigo' },
                        { color: 'hsl(207, 90%, 54%)', label: 'Blue' }
                    ],
                    backgroundColors: [
                        { color: 'hsl(4, 90%, 58%)', label: 'Red' },
                        { color: 'hsl(340, 82%, 52%)', label: 'Pink' },
                        { color: 'hsl(291, 64%, 42%)', label: 'Purple' },
                        { color: 'hsl(262, 52%, 47%)', label: 'Deep Purple' },
                        { color: 'hsl(231, 48%, 48%)', label: 'Indigo' },
                        { color: 'hsl(207, 90%, 54%)', label: 'Blue' }
                    ]
                }
            }
        })
        .then(editor => {
            editor.editing.view.change(writer => {
                writer.setAttribute('dir', 'rtl', editor.editing.view.document.getRoot());
            });
        })
        .catch(error => {
            console.error(error);
        });
});
