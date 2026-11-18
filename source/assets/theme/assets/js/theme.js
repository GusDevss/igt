;(function ($) {

    "use strict";
    
    var pxl_scroll_top;
    var pxl_window_height;
    var pxl_window_width;
    var pxl_scroll_status = '';
    var pxl_last_scroll_top = 0;
    $(window).on('load', function () {        
        $(".pxl-loader").addClass("is-loaded");
        if ($('#pxl-loadding').hasClass('style-default')) {
            setTimeout(function() {
                $('#pxl-loadding.style-default').remove();
            }, 3000);
        } else {
            $(".pxl-loader").fadeOut("slow");
        }
        $('.pxl-gallery-scroll').parents('body').addClass('body-overflow').addClass('body-visible-sm');
        pxl_window_width = $(window).width();
        pxl_window_height = $(window).height();        
        hadkaur_header_sticky();
        hadkaur_header_mobile();
        hadkaur_scroll_to_top();
        hadkaur_footer_fixed();
        hadkaur_shop_quantity();
    });

    $(window).on('scroll', function () {
        pxl_scroll_top = $(window).scrollTop();
        pxl_window_height = $(window).height();
        pxl_window_width = $(window).width();
        if (pxl_scroll_top < pxl_last_scroll_top) {
            pxl_scroll_status = 'up';
        } else {
            pxl_scroll_status = 'down';
        }
        pxl_last_scroll_top = pxl_scroll_top;
        hadkaur_header_sticky();
        hadkaur_scroll_to_top();
        hadkaur_footer_fixed();
    });

    $(window).on('resize', function () {
        pxl_window_height = $(window).height();
        pxl_window_width = $(window).width();        
        hadkaur_header_mobile();
    });

    $(document).ready(function () {         
        calculate_bmi_bmr();
        hadkaur_svg_stroke();                
        var svgContainers = document.querySelectorAll('.pxl-service-grid .pxl-grid-item');

        svgContainers.forEach(function(gridItem) {
            var $svgElement1 = $(gridItem).find('.pxl-item--svg-stroke');
            var $textElement1 = $(gridItem).find('.pxl-item-text--svg-stroke');

            if ($textElement1.length > 0) {
                var bbox1 = $textElement1[0].getBBox();
                
                $svgElement1.attr('width', bbox1.width);
                $svgElement1.attr('height', bbox1.height);
            }
        });


        $('.pxl-logo-nav').parents('#pxl-header-elementor').addClass('pxl-header-rmboxshadow');

        /* Start Menu Mobile */
        $('.pxl-header-menu li.menu-item-has-children').append('<span class="pxl-menu-toggle"></span>');
        $('.pxl-menu-toggle').on('click', function () {
            if( $(this).hasClass('active')){
                $(this).closest('ul').find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();    
            }else{
                $(this).closest('ul').find('.pxl-menu-toggle.active').toggleClass('active');
                $(this).closest('ul').find('.sub-menu.active').toggleClass('active').slideToggle();
                $(this).toggleClass('active');
                $(this).parent().find('> .sub-menu').toggleClass('active');
                $(this).parent().find('> .sub-menu').slideToggle();
            }      
        });

        $("#pxl-nav-mobile").on('click', function () {
            $(this).toggleClass('active');
            $('body').toggleClass('body-overflow');
            $('.pxl-header-menu').toggleClass('active');
        });

        $('#pxl-main input[type="submit"]').before(function() {
            return $('<button class="pxl-wobble" data-text="'+ this.className +'" data-animation="pxl-xspin" value="Submit">' + this.className + '</button>');
        });

        setTimeout(() => {
            var wobbleElements = document.querySelectorAll('.pxl-wobble');
            wobbleElements.forEach(function(el){               
                el.addEventListener('mouseover', function(){

                    if(!el.classList.contains('animating') && !el.classList.contains('mouseover')){

                        el.classList.add('animating','mouseover');

                        var letters = el.innerText.split('');

                        setTimeout(function(){ el.classList.remove('animating'); }, (letters.length + 1) * 50);

                        var animationName = el.dataset.animation;
                        if(!animationName){ animationName = "pxl-jump"; }

                        el.innerText = '';

                        letters.forEach(function(letter){
                            if(letter == " "){
                                letter = "&nbsp;";
                            }
                            el.innerHTML += '<span class="letter">'+letter+'</span>';
                        });

                        var letterElements = el.querySelectorAll('.letter');
                        letterElements.forEach(function(letter, i){
                            setTimeout(function(){
                                letter.classList.add(animationName);
                            }, 50 * i);
                        });

                    }

                });

                el.addEventListener('mouseout', function(){
                    el.classList.remove('mouseover');
                });
            });
        }, 100);

        var post_view = $('.single .pxl---post .post-views');
        var post_meta = $('.single .pxl---post .pxl-item--meta');
        if(post_view) {
            post_meta.append(post_view);
        }

        $(".pxl-menu-close, .pxl-header-menu-backdrop, #pxl-header-mobile .pxl-menu-primary a.is-one-page").on('click', function () {
            $(this).parents('.pxl-header-main').find('.pxl-header-menu').removeClass('active');
            $('#pxl-nav-mobile').removeClass('active');
            $('body').toggleClass('body-overflow');
        });
        /* End Menu Mobile */

        $(".pxl-item--holder .pxl-item--meta .pxl--social").on('click', function () {
            // $(this).parents('.pxl-item--holder').removeClass('active');            
            $(this).parents('.pxl-item--holder').toggleClass('active');
        });

        /* Arrow Custom */
        $('.pxl-tabs').parents('.pxl-tab--title').addClass('pxl--hide-arrow');
        var section_tab = $('.pxl-navigation-tab').parents('.elementor-section').addClass('pxl--hide-arrow');
        setTimeout(function() {
            var target = section_tab.find('.pxl-tabs .pxl-tabs--title');
            var target_clone = target.clone();
            var target_tab = target.parents('.elementor-section.pxl--hide-arrow').find('.pxl-navigation-tab');
            target_tab.append(target_clone);
            target_tab.find('.pxl-tab--title').on('click', function () {    
                $(this).parents('.elementor-section.pxl--hide-arrow').find('.pxl-navigation-tab .pxl-tab--title').toggleClass('active');
                $(this).parents('.elementor-section.pxl--hide-arrow').find('.pxl-tabs .pxl-tab--title').toggleClass('active');
                $(this).parents('.elementor-section.pxl--hide-arrow').find('.pxl-tabs .pxl-tab--title.active').trigger('click');
            });
        }, 300);


        /* Widgets */
        var ClassElement = document.querySelector(".pxl-project-info1");
        if (ClassElement) {
            var boxElement = ClassElement.closest(".widget");
            if (boxElement) {
                boxElement.classList.add("widget-no-padding");
            }
        }
        var ClassElement1 = document.querySelector(".widget-btn");
        if (ClassElement1) {
            var boxElement1 = ClassElement1.closest(".widget");
            if (boxElement1) {
                boxElement1.classList.add("widget-all-no-padding");
            }
        }

        /* pxl-project */
        var classbtn = $('.pxl-project-info1 .pxl-project-inner .btn');
        var boxClassContainer = classbtn.closest(".pxl-project-info1");
        var classContactForm = boxClassContainer.find('.wpcf7');
        classContactForm.hide();

        classbtn.on('click', function() {
            var boxClass = classbtn.closest(".pxl-project-inner");
            boxClass.hide();
            classContactForm.show();
        });


    // Get the elements from the pxl-project-inner section
        var title_post = $('.single .portfolio .pxl-portfolio--title').text();
        var classPrice = $('.pxl-project-inner .pxl--item:nth-child(1) span').text();
        var classTime = $('.pxl-project-inner .pxl--item:nth-child(2) span').text();
        var intensity = $('.pxl-project-inner .pxl--item:nth-child(3) span').text();
        var seatsCapacity = $('.pxl-project-inner .pxl--item:nth-child(4) span').text();
        var seatsAvailable = $('.pxl-project-inner .pxl--item:nth-child(5) span').text();
        var breakTime = $('.pxl-project-inner .pxl--item:nth-child(6) span').text();

    // Get the elements in the contact-form-custom1 section where you want to display the information
        var titleField = $('.contact-form-custom1 .pxl-item--title');
        var classPriceField = $('.contact-form-custom1 .pxl--item:nth-child(3) span');
        var classTimeField = $('.contact-form-custom1 .pxl--item:nth-child(4) span');
        var intensityField = $('.contact-form-custom1 .pxl--item:nth-child(5) span');
        var seatsCapacityField = $('.contact-form-custom1 .pxl--item:nth-child(6) span');
        var seatsAvailableField = $('.contact-form-custom1 .pxl--item:nth-child(7) span');
        var breakTimeField = $('.contact-form-custom1 .pxl--item:nth-child(8) span');

    // Update the elements in the contact-form-custom1 section with the information from pxl-project-inner
        titleField.text(title_post);
        classPriceField.text(classPrice);
        classTimeField.text(classTime);
        intensityField.text(intensity);
        seatsCapacityField.text(seatsCapacity);
        seatsAvailableField.text(seatsAvailable);
        breakTimeField.text(breakTime);

        /* Elementor Header */
        $('.pxl-type-header-clip > .elementor-container').append('<div class="pxl-header-shape"><span></span></div>');

        /* Scroll To Top */
        $('.pxl-scroll-top').click(function () {
            $('html, body').animate({scrollTop: 0}, 800);
            return false;
        });

        /* Animate Time Delay */
        $('.pxl-grid-masonry').each(function () {
            var eltime = 40;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl-grid-item > .wow').each(function (index, obj) {
                $(this).css('animation-delay', eltime + 'ms');
                if (_elt === index) {
                    eltime = 40;
                    _elt = _elt + elt_inner;
                } else {
                    eltime = eltime + 40;
                }
            });
        });

        $('.pxl-item--text').each(function () {
            var pxl_time = 0;
            var pxl_item_inner = $(this).children().length;
            var _elt = pxl_item_inner - 1;
            $(this).find('> .pxl-text--slide > .wow').each(function (index, obj) {
                $(this).css('transition-delay', pxl_time + 'ms');
                if (_elt === index) {
                    pxl_time = 0;
                    _elt = _elt + pxl_item_inner;
                } else {
                    pxl_time = pxl_time + 80;
                }
            });
        });

        /* Lightbox Popup */
        $('.btn-video, .pxl-video-popup, .pxl--link-popup, .btn-video-text').magnificPopup({
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });

        $('.images-light-box').each(function () {
            $(this).magnificPopup({
                delegate: 'a.light-box',
                type: 'image',
                gallery: {
                    enabled: true
                },
                mainClass: 'mfp-fade',
            });
        });

        /* Comment Reply */
        $('.comment-reply a').append( '<i class="caseicon-angle-arrow-right"></i>' );

        /* Parallax */
        if($('#pxl-page-title-default').hasClass('pxl--parallax')) {
            $(this).stellar();
        }

        /* Animate Time */
        $('.btn-nina').each(function () {
            var eltime = 0.045;
            var elt_inner = $(this).children().length;
            var _elt = elt_inner - 1;
            $(this).find('> .pxl--btn-text > span').each(function (index, obj) {
                $(this).css('transition-delay', eltime + 's');
                eltime = eltime + 0.045;
            });
        });

        /* Search Popup */
        var $search_wrap_init = $("#pxl-search-popup");
        var search_field = $('#pxl-search-popup .search-field');
        var $body = $('body');

        $(".pxl-search-popup-button").on('click', function(e) {
            if (!$search_wrap_init.hasClass('active')) {
                $search_wrap_init.addClass('active');
                setTimeout(function() { search_field.get(0).focus(); }, 500);
            } else if (search_field.val() === '') {
                $search_wrap_init.removeClass('active');
                search_field.get(0).focus();
            }
            e.preventDefault();
            return false;
        });

        $("#pxl-search-popup .pxl-item--overlay, #pxl-search-popup .pxl-item--close").on('click', function (e) {
            $body.addClass('pxl-search-out-anim');
            setTimeout(function () {
                $body.removeClass('pxl-search-out-anim');
            }, 800);
            setTimeout(function () {
                $search_wrap_init.removeClass('active');
            }, 1200);
            e.preventDefault();
            return false;
        });

        /* Hidden Panel */
        $(".pxl-hidden-panel-button").on('click', function () {
            $('body').addClass('body-overflow');
            $('#pxl-hidden-panel-popup').addClass('active');
        });
        $("#pxl-hidden-panel-popup .pxl-item--overlay, #pxl-hidden-panel-popup .pxl-item--close").on('click', function () {
            $('body').removeClass('body-overflow');
            $('#pxl-hidden-panel-popup').removeClass('active');
        });

        /* Cart Sidebar Popup */
        $(".pxl-cart-sidebar-button").on('click', function () {
            $('body').addClass('body-overflow');
            $('#pxl-cart-sidebar').addClass('active');
        });
        $("#pxl-cart-sidebar .pxl-item--overlay, #pxl-cart-sidebar .pxl-item--close").on('click', function () {
            $('body').removeClass('body-overflow');
            $('#pxl-cart-sidebar').removeClass('active');
        });

        /* Popup */
        $(".pxl-popup-button").on('click', function () {
            $('body').addClass('body-overflow');
            $('#pxl-popup-elementor').addClass('active');
            $('#pxl-popup-elementor').removeClass('deactivation');
        });
        $("#pxl-popup-elementor .pxl-item--overlay, #pxl-popup-elementor .pxl-item--close, .pxl-menu-primary a.is-one-page").on('click', function () {
            $('body').removeClass('body-overflow');
            $('#pxl-popup-elementor').removeClass('active');
            $('#pxl-popup-elementor').addClass('deactivation');
        });

        /* Hover Active Item */
        $('.pxl--widget-hover').each(function () {
            $(this).hover(function () {
                $(this).parents('.elementor-row').find('.pxl--widget-hover').removeClass('pxl--item-active');
                $(this).parents('.elementor-container').find('.pxl--widget-hover').removeClass('pxl--item-active');
                $(this).addClass('pxl--item-active');
            });
        });

        /* Hover Button */
        $('.btn-plus-text').hover(function () {
            $(this).find('span').toggle(300);
        });

        /* Nav Logo */
        $(".pxl-nav-button").on('click', function () {
            $('.pxl-nav-button').toggleClass('active');
            $('.pxl-nav-button').parent().find('.pxl-nav-wrap').toggle(400);
        });

        /* Button Mask */
        $('.pxl-btn-effect4').append('<span class="pxl-btn-mask"></span>');

        /* Start Icon Bounce */
        var boxEls = $('.el-bounce, .pxl-image-effect1');
        $.each(boxEls, function(boxIndex, boxEl) {
            loopToggleClass(boxEl, 'bounce-active');
        });

        function loopToggleClass(el, toggleClass) {
            el = $(el);
            let counter = 0;
            if (el.hasClass(toggleClass)) {
                waitFor(function () {
                    counter++;
                    return counter == 2;
                }, function () {
                    counter = 0;
                    el.removeClass(toggleClass);
                    loopToggleClass(el, toggleClass);
                }, 'Deactivate', 1000);
            } else {
                waitFor(function () {
                    counter++;
                    return counter == 3;
                }, function () {
                    counter = 0;
                    el.addClass(toggleClass);
                    loopToggleClass(el, toggleClass);
                }, 'Activate', 1000);
            }
        }

        function waitFor(condition, callback, message, time) {
            if (message == null || message == '' || typeof message == 'undefined') {
                message = 'Timeout';
            }
            if (time == null || time == '' || typeof time == 'undefined') {
                time = 100;
            }
            var cond = condition();
            if (cond) {
                callback();
            } else {
                setTimeout(function() {
                    waitFor(condition, callback, message, time);
                }, time);
            }
        }
        /* End Icon Bounce */

        /* Image Effect */
        if($('.pxl-image-tilt').length){
            $('.pxl-image-tilt').parents('.elementor-top-section').addClass('pxl-image-tilt-active');
            $('.pxl-image-tilt').each(function () {
                var pxl_maxtilt = $(this).data('maxtilt'),
                pxl_speedtilt = $(this).data('speedtilt'),
                pxl_perspectivetilt = $(this).data('perspectivetilt');
                VanillaTilt.init(this, {
                    max: pxl_maxtilt,
                    speed: pxl_speedtilt,
                    perspective: pxl_perspectivetilt
                });
            });
        }

        /* Pricing Hover */
        $('.pxl-pricing1').each(function () {
            $(this).hover(function () {
                $(this).parents('.elementor-element').find('.pxl-pricing1').removeClass('is-popular');
                $(this).addClass('is-popular');
            });
        });

        /* Pricing Hover */
        $('.pxl-event-list .pxl-item--container:first').addClass('is-popular');
        $('.pxl-event-list .pxl-item--container').each(function () {
            $(this).hover(function () {
                $(this).parents('.elementor-element').find('.pxl-event-list .pxl-item--container').removeClass('is-popular');
                $(this).addClass('is-popular');
                $('.pxl-event-list .pxl-item--container .btn-event').hide();        
                if ($(this).hasClass('is-popular')) {
                    $(this).find('.btn-event').show();              
                }
            });
        });

        /* Select Theme Style */
        $('.wpcf7-select').each(function(){
            var $this = $(this), numberOfOptions = $(this).children('option').length;

            $this.addClass('pxl-select-hidden'); 
            $this.wrap('<div class="pxl-select"></div>');
            $this.after('<div class="pxl-select-higthlight"></div>');

            var $styledSelect = $this.next('div.pxl-select-higthlight');
            $styledSelect.text($this.children('option').eq(0).text());

            var $list = $('<ul />', {
                'class': 'pxl-select-options'
            }).insertAfter($styledSelect);

            for (var i = 0; i < numberOfOptions; i++) {
                $('<li />', {
                    text: $this.children('option').eq(i).text(),
                    rel: $this.children('option').eq(i).val()
                }).appendTo($list);
            }

            var $listItems = $list.children('li');

            $styledSelect.click(function(e) {
                e.stopPropagation();
                $('div.pxl-select-higthlight.active').not(this).each(function(){
                    $(this).removeClass('active').next('ul.pxl-select-options').addClass('pxl-select-lists-hide');
                });
                $(this).toggleClass('active');
            });

            $listItems.click(function(e) {
                e.stopPropagation();
                $styledSelect.text($(this).text()).removeClass('active');
                $this.val($(this).attr('rel'));
            });

            $(document).click(function() {
                $styledSelect.removeClass('active');
            });

        });

        /* Nice Select */
        $('.woocommerce-ordering .orderby, #pxl-sidebar-area select, .pxl-bmi-bmr select').each(function () {
            $(this).niceSelect();
        });

        /* Item Hover - Description */
        $( ".pxl-content-effect .pxl-item--inner" ).hover(
          function() {
            $( this ).find('.pxl-item--effect').slideToggle(250);
        }, function() {
            $( this ).find('.pxl-item--effect').slideToggle(250);
        }
        );

        /* Typewriter */
        if($('.pxl-title--typewriter').length) {
            function typewriterOut(elements, callback)
            {
                if (elements.length){
                    elements.eq(0).addClass('is-active');
                    elements.eq(0).delay( 3000 );
                    elements.eq(0).removeClass('is-active');
                    typewriterOut(elements.slice(1), callback);
                }
                else {
                    callback();
                }
            }

            function typewriterIn(elements, callback)
            {
                if (elements.length){
                    elements.eq(0).addClass('is-active');
                    elements.eq(0).delay( 3000 ).slideDown(3000, function(){
                        elements.eq(0).removeClass('is-active');
                        typewriterIn(elements.slice(1), callback);
                    });
                }
                else {
                    callback();
                }
            }

            function typewriterInfinite(){
                typewriterOut($('.pxl-title--typewriter .pxl-item--text'), function(){ 
                    typewriterIn($('.pxl-title--typewriter .pxl-item--text'), function(){
                        typewriterInfinite();
                    });
                });
            }
            $(function(){
                typewriterInfinite();
            });
        }
        /* End Typewriter */

            /* Get Mouse Move Direction */
        function getDirection(ev, obj) {
            var w = $(obj).width(),
            h = $(obj).height(),
            x = (ev.pageX - $(obj).offset().left - (w / 2)) * (w > h ? (h / w) : 1),
            y = (ev.pageY - $(obj).offset().top - (h / 2)) * (h > w ? (w / h) : 1),
            d = Math.round( Math.atan2(y, x) / 1.57079633 + 5 ) % 4;
            return d;
        }
        function addClass( ev, obj, state ) {
            var direction = getDirection( ev, obj ),
            class_suffix = null;
            $(obj).removeAttr('class');
            switch ( direction ) {
            case 0 : class_suffix = '--top';    break;
            case 1 : class_suffix = '--right';  break;
            case 2 : class_suffix = '--bottom'; break;
            case 3 : class_suffix = '--left';   break;
            }
            $(obj).addClass( state + class_suffix );
        }
        $.fn.ctDeriction = function () {
            this.each(function () {
                $(this).on('mouseenter',function(ev){
                    addClass( ev, this, 'pxl-in' );
                });
                $(this).on('mouseleave',function(ev){
                    addClass( ev, this, 'pxl-out' );
                });
            });
        }
        $('.pxl-effect--3d .pxl-effect--direction').ctDeriction();

        /* Section Particles */      
        setTimeout(function() {
            $(".pxl-row-particles").each(function() {
                particlesJS($(this).attr('id'), {
                  "particles": {
                    "number": {
                        "value": $(this).data('number'),
                    },
                    "color": {
                        "value": $(this).data('color')
                    },
                    "shape": {
                        "type": "circle",
                    },
                    "size": {
                        "value": $(this).data('size'),
                        "random": $(this).data('size-random'),
                    },
                    "line_linked": {
                        "enable": false,
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": $(this).data('move-direction'),
                        "random": true,
                        "out_mode": "out",
                    }
                },
                "retina_detect": true
            });
            });
        }, 400);

        /* Get checked input - Mailchimpp */
        $('.mc4wp-form input:checkbox').change(function(){
            if($(this).is(":checked")) {
                $('.mc4wp-form').addClass("pxl-input-checked");
            } else {
                $('.mc4wp-form').removeClass("pxl-input-checked");
            }
        });

        /* Alert */
        $(".pxl-alert .pxl-alert--close").on('click', function () {
            $(this).parent().fadeOut();
        });

    });

jQuery(document).ajaxComplete(function(event, xhr, settings){
    hadkaur_shop_quantity();
    hadkaur_svg_stroke();
});

jQuery( document ).on( 'updated_wc_div', function() {
    hadkaur_shop_quantity();
} );

function hadkaur_svg_stroke() {
    var $svgElement = $('.pxl-heading--inner .pxl-item--svg-stroke');
    var $textElement = $('.pxl-heading--inner .pxl-item-text--svg-stroke');    
    if($textElement.getBBox) {
        var bbox = $textElement[0].getBBox();
        $svgElement.attr('width', bbox.width);
        $svgElement.attr('height', bbox.height);        
    } 
}

    /* Header Sticky */
function hadkaur_header_sticky() {
    if($('#pxl-header-elementor').hasClass('is-sticky')) {
        if (pxl_scroll_top > 100) {
            $('.pxl-header-elementor-sticky.pxl-sticky-stb').addClass('pxl-header-fixed');
            $('#pxl-header-mobile').addClass('pxl-header-mobile-fixed');
        } else {
            $('.pxl-header-elementor-sticky.pxl-sticky-stb').removeClass('pxl-header-fixed');
            $('#pxl-header-mobile').removeClass('pxl-header-mobile-fixed');
        }

        if (pxl_scroll_status == 'up' && pxl_scroll_top > 100) {
            $('.pxl-header-elementor-sticky.pxl-sticky-stt').addClass('pxl-header-fixed');
        } else {
            $('.pxl-header-elementor-sticky.pxl-sticky-stt').removeClass('pxl-header-fixed');
        }
    }

    $('.pxl-header-elementor-sticky').parents('body').addClass('pxl-header-sticky');
}

    /* Header Mobile */
function hadkaur_header_mobile() {
    var h_header_mobile = $('#pxl-header-elementor').outerHeight();
    if(pxl_window_width < 1199) {
        $('#pxl-header-elementor').css('min-height', h_header_mobile + 'px');
    }
}

    /* Scroll To Top */
function hadkaur_scroll_to_top() {
    if (pxl_scroll_top < pxl_window_height) {
        $('.pxl-scroll-top').addClass('pxl-off').removeClass('pxl-on');
    }
    if (pxl_scroll_top > pxl_window_height) {
        $('.pxl-scroll-top').addClass('pxl-on').removeClass('pxl-off');
    }
}

    /* Footer Fixed */
function hadkaur_footer_fixed() {
    setTimeout(function(){
        var h_footer = $('.pxl-footer-fixed #pxl-footer-elementor').outerHeight() - 1;
        $('.pxl-footer-fixed #pxl-main').css('margin-bottom', h_footer + 'px');
    }, 600);
}

function calculateNutrition(totalCalories, proteinPercentage, fatPercentage) {
    const proteinCalories = totalCalories * proteinPercentage;
    const fatCalories = totalCalories * fatPercentage;
    const carbohydrateCalories = totalCalories - proteinCalories - fatCalories;

    const proteinGrams = proteinCalories / 4; // 1g protein = 4 calo
    const fatGrams = fatCalories / 9; // 1g chất béo = 9 calo
    const carbohydrateGrams = carbohydrateCalories / 4; // 1g carbohydrate = 4 calo

    return {
        protein: proteinGrams.toFixed(2),
        fat: fatGrams.toFixed(2),
        carbohydrates: carbohydrateGrams.toFixed(2)
    };
}


function calculate_bmi_bmr() {
    $('.bmi-bmr-calc').click(function (event) {
        event.stopPropagation();
        const height = parseFloat($('.height').val());
        const weight = parseFloat($('.weight').val());
        const age = parseInt($('.age').val());
        const gender = $('.gender').val();
        const activity = parseFloat($('.activity').val());
        const goal = $('.goal').val();

        const bmi = weight / ((height / 100) ** 2);
        let bmr = (gender === 'm') ? (88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)) : (447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age));
        const tdee = bmr * activity;

        let totalCalories;
        if (goal === 'lose') {
            totalCalories = tdee - 500;
        } else if (goal === 'gain') {
            totalCalories = tdee + 500;
        }

        const proteinPercentage = 0.15;
        const fatPercentage = 0.25;

    // Tính lượng protein, chất béo và carbohydrate dựa trên tỷ lệ và lượng calo đã tính
        const nutrition = calculateNutrition(totalCalories, proteinPercentage, fatPercentage);

        if (isNaN(height) || isNaN(weight) || isNaN(age) || gender === '' || isNaN(activity) || goal === '') {      
          return;
      }

      $('.r-bmi').text(bmi.toFixed(2));
      $('.r-bmr').text(bmr.toFixed(2));
      $('.r-tdee').text(tdee.toFixed(2));
      $('.r-total').text(totalCalories.toFixed(2));
      $('.r-protein').text(nutrition.protein);
      $('.r-fat').text(nutrition.fat);
      $('.r-carbs').text(nutrition.carbohydrates);
      $('.result-wrap').css('display', 'block');
      event.preventDefault();
  });
}

    /* WooComerce Quantity */
function hadkaur_shop_quantity() {
    "use strict";
    $('#pxl-wapper .quantity').append('<span class="quantity-icon quantity-down pxl-icon--minus"></span><span class="quantity-icon quantity-up pxl-icon--plus"></span>');
    $('.quantity-up').on('click', function () {
        $(this).parents('.quantity').find('input[type="number"]').get(0).stepUp();
        $(this).parents('.woocommerce-cart-form').find('.actions .button').removeAttr('disabled');
    });
    $('.quantity-down').on('click', function () {
        $(this).parents('.quantity').find('input[type="number"]').get(0).stepDown();
        $(this).parents('.woocommerce-cart-form').find('.actions .button').removeAttr('disabled');
    });
    $('.quantity-icon').on('click', function () {
        var quantity_number = $(this).parents('.quantity').find('input[type="number"]').val();
        var add_to_cart_button = $(this).parents( ".product, .woocommerce-product-inner" ).find(".add_to_cart_button");
        add_to_cart_button.attr('data-quantity', quantity_number);
        add_to_cart_button.attr("href", "?add-to-cart=" + add_to_cart_button.attr("data-product_id") + "&quantity=" + quantity_number);
    });
    $('.woocommerce-cart-form .actions .button').removeAttr('disabled');
}
})(jQuery);
