require('jquery');
require('jquery-ui');
require('speakingurl');


$(function() {
    var data = $.ajax({"url": data_url, "async": false});
    var $tree = $('#sacrud-tree');
    $tree.tree({
        data: data.responseJSON,
        dragAndDrop: true,
        usecontextmenu: true,
        autoOpen: true,

        onCreateLi: function(node, $li) {
            dom_node = $li.find('.jqtree-title');
            if(!node.visible) {
                dom_node.addClass('jqtree-hidden');
            }
            if(node.redirect_code && node.redirect_code != '200'  ) {
                dom_node.after(
                  '<span class="jqtree-label jqtree-redirect ' + node.CSSredirect + '">'
                  + node.redirect_code + ' — ' + node.redirect + '</span>');
          }
      }
    });

  $tree.bind(
      'tree.click',
      function(event) {
          window.location = event.node.url_update;
      });

  $tree.bind(
      'tree.move',
      function(event) {
          event.preventDefault();
          var url = "/sacrud_pages/move/" + event.move_info.moved_node.id + "/" +
                    event.move_info.position + "/" +
                    event.move_info.target_node.id + "/";
          var status = $.ajax({"url": url, "async": false}).status;
          if (status==200) {
              event.move_info.do_move();
          }
      });

  // $tree.bind(
  //     'tree.contextmenu',
  //       function(event) {
  //           // The clicked node is 'event.node'
  //           var node = event.node;
  //           alert(node.name);
  //       }
  //   );


  $tree.jqTreeContextMenu($('#sacrud-tree-menu'), {
    "delete": function (node) {
        var url = node.url_delete;
        var status = $.ajax({'url': url, "async": false}).status;
        if (status==200) {
          $tree.tree('removeNode', node);
        }
    },
    "edit": function (node) {
      window.location = node.url_update;
    },
    "visible": function (node) {
        var url = node.url_visible;
        var visible = $.ajax({'url': url, "async": false}).responseJSON.visible;
        var element = $(node.element).find('.jqtree-title').first();
        if(visible){
            element.removeClass('jqtree-hidden');
        } else {
            element.addClass('jqtree-hidden');
        }
        element.parents('.jqtree-selected').removeClass('jqtree-selected');
    }
  });

  $("input[name='name'].form-control").on( "click", function() {
    console.log( $( this ).text() );
  });


});