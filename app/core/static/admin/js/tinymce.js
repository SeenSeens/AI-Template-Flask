'use strict';

class TinyMCEManager {
  constructor() {
    this.initTinyMCE();
  }


  initTinyMCE() {
    tinymce.init({
      selector: 'textarea',
      license_key: 'gpl|1qa5t0dn0b46dukvifb2b500e7ausw3qelzj0jie038xyejf',
      height: 500,
      content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
      plugins: [
        'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
        'anchor', 'searchreplace', 'visualblocks', 'fullscreen', 'file-manager',
        'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount',
      ],
      toolbar: 'undo redo | link image | code | blocks | bold italic backcolor | ' +
               'alignleft aligncenter alignright alignjustify | ' +
               'bullist numlist outdent indent | removeformat | help',
      images_file_types: 'jpg, svg, webp, png',
      file_picker_types: 'file image uploads',
      image_title: true,
      automatic_uploads: true,
    });
  }

}

// Khởi tạo class khi DOM đã sẵn sàng
document.addEventListener("DOMContentLoaded", () => {
  new TinyMCEManager();
});
