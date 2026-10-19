/* Service Hub — lightbox с делегированием событий */

(function () {
    'use strict';

    function initLightbox() {
        var lightboxEl = document.getElementById('lightbox');
        if (!lightboxEl) {
            console.warn('[lightbox] #lightbox не найден в HTML');
            return;
        }

        var lbImg = lightboxEl.querySelector('.lightbox-img');
        var btnClose = lightboxEl.querySelector('.lightbox-close');
        var btnPrev = lightboxEl.querySelector('.lightbox-prev');
        var btnNext = lightboxEl.querySelector('.lightbox-next');

        if (!lbImg || !btnClose || !btnPrev || !btnNext) {
            console.warn('[lightbox] Не найдены внутренние элементы лайтбокса');
            return;
        }

        var currentIndex = 0;

        function getItems() {
            return Array.prototype.slice.call(
                document.querySelectorAll('[data-lightbox="service-gallery"]')
            );
        }

        function open(index) {
            var items = getItems();
            if (!items.length) return;
            currentIndex = index;
            lbImg.src = items[index].href;
            lightboxEl.classList.add('active');
            lightboxEl.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        }

        function close() {
            lightboxEl.classList.remove('active');
            lightboxEl.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        }

        function prev() {
            var items = getItems();
            currentIndex = (currentIndex - 1 + items.length) % items.length;
            lbImg.src = items[currentIndex].href;
        }

        function next() {
            var items = getItems();
            currentIndex = (currentIndex + 1) % items.length;
            lbImg.src = items[currentIndex].href;
        }

        // Делегирование клика по всему документу
        document.addEventListener('click', function (e) {
            var target = e.target.closest('[data-lightbox="service-gallery"]');
            if (!target) return;

            e.preventDefault();
            var items = getItems();
            var idx = items.indexOf(target);
            if (idx >= 0) open(idx);
        });

        btnClose.addEventListener('click', close);
        btnPrev.addEventListener('click', function (e) { e.stopPropagation(); prev(); });
        btnNext.addEventListener('click', function (e) { e.stopPropagation(); next(); });

        lightboxEl.addEventListener('click', function (e) {
            if (e.target === lightboxEl) close();
        });

        document.addEventListener('keydown', function (e) {
            if (!lightboxEl.classList.contains('active')) return;
            if (e.key === 'Escape') close();
            if (e.key === 'ArrowLeft') prev();
            if (e.key === 'ArrowRight') next();
        });

        console.log('[lightbox] инициализирован, элементов в галерее:', getItems().length);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLightbox);
    } else {
        initLightbox();
    }
})();