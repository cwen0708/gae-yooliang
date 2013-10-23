CKEDITOR.plugins.add( 'gpimage',
{
    init: function( editor )
    {
        //Plugin logic goes here.
        editor.addCommand( 'insertGooglePickerImage',
        {
            exec : function( editor )
            {
                gp_last_editor = editor;
                google_picker_before_editor_select();
            }
        });
        editor.ui.addButton( 'GooglePickerImage',
        {
            label: '插入圖片',
            command: 'insertGooglePickerImage',
            icon: this.path + 'gpimg_16.gif'
        });
    }
});
