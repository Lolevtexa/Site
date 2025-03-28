function toggleVisibility(id) {
    let element = document.getElementById(id);
    if (element) {
        element.classList.toggle("show");
    }
}

function toggleMainNav() {
    let mainNav = document.getElementById("main-nav");
    if (mainNav) mainNav.classList.toggle("show");
}

function toggleDropdown() {
    toggleVisibility("userDropdown");
}

document.addEventListener("click", function (event) {
    const menus = [
        { button: ".menu-toggle", menu: "#main-nav" },
        { button: ".avatar-container", menu: "#userDropdown" },
    ];

    menus.forEach(({ button, menu }) => {
        const buttonEl = document.querySelector(button);
        const menuEl = document.querySelector(menu);
        if (menuEl && !menuEl.contains(event.target) && !buttonEl.contains(event.target)) {
            menuEl.classList.remove("show");
        }
    });
});

function toggleMoreDropdown() {
    const moreButton = document.getElementById("more-button");
    const moreDropdown = document.getElementById("more-dropdown");
    if (moreDropdown.classList.contains("show")) {
        moreDropdown.classList.remove("show");
    } else {
        // Позиционирование меню относительно кнопки "Ещё"
        const rect = moreButton.getBoundingClientRect();
        // Вычисляем позицию: верх = нижняя граница кнопки,
        // левый отступ = правая граница кнопки минус ширина меню.
        // Если ширина меню известна (220px), можно использовать её напрямую.
        moreDropdown.style.top = rect.bottom + "px";
        moreDropdown.style.left = (rect.right - 220) + "px";
        moreDropdown.classList.add("show");
    }
}

function adjustLocalNav() {
    const nav = document.getElementById("local-nav");
    const moreButton = document.getElementById("more-button");
    const moreDropdown = document.getElementById("more-dropdown");

    // 1. Возвращаем все пункты из подменю обратно
    while (moreDropdown.firstChild) {
        nav.insertBefore(moreDropdown.firstChild, moreButton);
    }

    // Сначала спрячем «Ещё», чтобы при первом проходе не мешала
    moreButton.style.display = "none";

    const navWidth = nav.offsetWidth;

    // Все пункты (кроме «Ещё»)
    const navItems = Array.from(nav.querySelectorAll("li:not(#more-button)"));

    // 2. Идём слева направо и проверяем, влезает ли каждый пункт
    let usedWidth = 0;
    let lastFittingIndex = -1;

    // Можете заменить offsetWidth на getBoundingClientRect().width + margin
    navItems.forEach((item, idx) => {
        const w = item.offsetWidth;
        if (usedWidth + w <= navWidth) {
            usedWidth += w;
            lastFittingIndex = idx;
        }
    });

    // 3. Если lastFittingIndex < navItems.length - 1, значит не все пункты влезли
    if (lastFittingIndex < navItems.length - 1) {
        // Теперь показываем «Ещё», чтобы учесть её ширину
        moreButton.style.display = "inline-flex";
        const buttonWidth = moreButton.offsetWidth;

        // Пересчитываем заново, учитывая ширину кнопки
        usedWidth = 0;
        lastFittingIndex = -1;
        for (let i = 0; i < navItems.length; i++) {
            const w = navItems[i].offsetWidth;
            // Теперь сравниваем с (navWidth - buttonWidth)
            if (usedWidth + w <= (navWidth - buttonWidth - 10)) {
                usedWidth += w;
                lastFittingIndex = i;
            } else {
                break;
            }
        }

        // Всё, что не влезло (начиная со следующего индекса), уезжает в подменю
        for (let i = lastFittingIndex + 1; i < navItems.length; i++) {
            moreDropdown.appendChild(navItems[i]);
        }
    }
    else {
        // Все пункты поместились — «Ещё» не нужно
        moreButton.style.display = "none";
    }
}

// Запускаем функцию при загрузке страницы и при изменении размера окна
document.addEventListener("DOMContentLoaded", adjustLocalNav);
window.addEventListener("resize", adjustLocalNav);
window.addEventListener("resize", function () {
    const moreDropdown = document.getElementById("more-dropdown");
    if (moreDropdown.classList.contains("show")) {
        const moreButton = document.getElementById("more-button");
        const rect = moreButton.getBoundingClientRect();
        moreDropdown.style.top = rect.bottom + "px";
        moreDropdown.style.left = (rect.right - 220) + "px";
    }
});