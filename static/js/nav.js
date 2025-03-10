/**
 * Открыть/закрыть главное меню (бургер).
 * Просто переключаем display: block / none.
 */
function toggleMainNav() {
  let mainNav = document.getElementById("main-nav");
  if (mainNav.style.display === "block") {
    mainNav.style.display = "none";
  } else {
    mainNav.style.display = "block";
  }
}

/**
 * Открыть/закрыть меню "Ещё".
 * Переключаем класс "show" у #more-dropdown.
 */
function toggleMoreMenu() {
  let moreDropdown = document.getElementById("more-dropdown");
  moreDropdown.classList.toggle("show");
}

/**
 * Открыть/закрыть меню аватара.
 * Переключаем класс "show" у #userDropdown.
 */
function toggleDropdown() {
  let userDropdown = document.getElementById("userDropdown");
  userDropdown.classList.toggle("show");
}

/**
 * Функция для адаптивного скрытия пунктов локальной навигации,
 * которые не помещаются в одну строку. Они переносятся в "Ещё".
 */
function adjustNavItems() {
    let navContainer = document.querySelector(".sub-nav");
    if (!navContainer) return;

    let navItems = Array.from(document.querySelectorAll("#local-nav li:not(#more-menu)"));
    let moreMenu = document.getElementById("more-menu");
    let moreDropdown = document.getElementById("more-dropdown");
    if (!moreMenu || !moreDropdown) return;

    // Если справа есть фиксированный блок (аватар и т.п.), учтём его ширину:
    let userMenu = document.querySelector(".user-menu");
    let userWidth = userMenu ? userMenu.offsetWidth : 0;

    // 1) Сброс: показываем все пункты, прячем кнопку «Ещё», очищаем её список
    navItems.forEach(item => {
        item.style.display = "inline-block";
    });
    moreMenu.style.display = "none";
    moreDropdown.innerHTML = "";
    moreDropdown.classList.remove("show");

    // 2) Считаем, сколько места доступно без учёта «Ещё»
    let availableWidth = navContainer.offsetWidth - userWidth - 20; 
    let usedWidth = 0;
    let hiddenItems = [];

    // 3) Первый проход: скрываем пункты, которые не поместились
    navItems.forEach(item => {
        usedWidth += item.offsetWidth;
        if (usedWidth > availableWidth) {
            item.style.display = "none";
            let link = item.querySelector("a");
            if (link) {
                hiddenItems.push(
                    `<li onclick="window.location='${link.href}'">${link.innerText}</li>`
                );
            } else {
                hiddenItems.push(`<li>${item.innerText}</li>`);
            }
        }
    });

    // 4) Если вообще ничего не спрятали, «Ещё» не нужна — выходим
    if (hiddenItems.length === 0) {
        return;
    }

    // 5) Иначе показываем «Ещё» и вставляем в него скрытые пункты
    moreMenu.style.display = "inline-block";
    // Но учтём, что теперь «Ещё» занимает место => делаем второй проход

    let moreMenuWidth = moreMenu.offsetWidth;
    let newAvailableWidth = navContainer.offsetWidth - userWidth - 20 - moreMenuWidth;

    // Список, который скроем во второй фазе (уже при видимой кнопке «Ещё»)
    let secondPassHidden = [];
    usedWidth = 0;

    // 6) Второй проход: проверяем пункты, которые пока видны
    navItems.forEach(item => {
        if (item.style.display !== "none") {
            usedWidth += item.offsetWidth;
            if (usedWidth > newAvailableWidth) {
                item.style.display = "none";
                let link = item.querySelector("a");
                if (link) {
                    secondPassHidden.push(
                        `<li onclick="window.location='${link.href}'">${link.innerText}</li>`
                    );
                } else {
                    secondPassHidden.push(`<li>${item.innerText}</li>`);
                }
            }
        }
    });

    // 7) Объединяем оба списка спрятанных пунктов и вставляем их в меню «Ещё»
    hiddenItems = hiddenItems.concat(secondPassHidden);
    moreDropdown.innerHTML = hiddenItems.join("");
}

function tmp() {
    let moreDropdown = document.getElementById("more-dropdown");
    moreDropdown.innerHTML = "";
}

// Запускаем при загрузке и при изменении размера окна
window.addEventListener("load", adjustNavItems);
window.addEventListener("resize", tmp);
window.addEventListener("resize", adjustNavItems);
