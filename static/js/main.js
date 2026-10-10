/* Service Hub — основной скрипт */

document.addEventListener('DOMContentLoaded', () => {
    // Sticky header: тень при скролле
    const header = document.getElementById('siteHeader');
    if (header) {
        const onScroll = () => {
            if (window.scrollY > 20) header.classList.add('scrolled');
            else header.classList.remove('scrolled');
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // Анимации при скролле
    const reveals = document.querySelectorAll('.section, .category-card, .advantage-card, .review-card, .hero-card, .service-card, .master-card, .post-card');
    reveals.forEach(el => el.classList.add('reveal'));

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });

    reveals.forEach(el => observer.observe(el));

    // Плавный скролл к якорям
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // Автозакрытие алертов
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 6000);
    });
});