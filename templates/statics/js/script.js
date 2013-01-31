var tabeebi = {
    init: function() {
        this.slider();
    },

    slider: function() {
        var slider = $('.slider_wrapper');
        if(slider.length > 0) {
            var children = slider.find('section'),
                len      = children.length,
                current  = 1,
                buttons  = '';

            children.each(function() {
                var that   = $(this),
                    string = '',
                    i      = 0;

                string += '<div class="js_buttons">';
                string += '<button class="active"></button>';
                i++;
                for(; i < len; i++) {
                    string += '<button></button>';
                }
                string += '</div>';
                that.append(string);
            });

            buttons = slider.find('.js_buttons');

            slider.append('<button class="prev"></button><button class="next"></button>');

            slider.find('button.prev, button.next, .js_buttons button').click(function(e) {
                var btn = $(this);

                if(btn.hasClass('prev')) {
                    if(current === 1) {
                        current = len;
                    } else {
                        current--;
                    }
                } else if(btn.hasClass('next')) {
                    if(current === len) {
                        current = 1;
                    } else {
                        current++;
                    }
                } else {
                    current = btn.index() + 1;
                }

                buttons.each(function() {
                    var wrp = $(this);

                    wrp.find('.active').removeClass('active');
                    $(wrp.find('button')[current - 1]).addClass('active');
                });
                console.log(current);
                var zindex = parseInt(slider.find( 'section:visible .phones' ).css( "z-index" ), 2 );
                console.log(zindex);
                var new_section = $(slider.find('section')[current - 1]);
                new_section.find('.phones').css('z-index', zindex + 1);
                slider.find('section:visible .phones').css('z-index', zindex - 1);    
                slider.find('section:visible').fadeOut(function(){
                    new_section.fadeIn();
                });

                e.preventDefault();
            });
        }
    }
};

$(function() {

    tabeebi.init();

});