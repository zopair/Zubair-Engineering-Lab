(() => {
  const root = document.documentElement;
  const views = Array.from(document.querySelectorAll("[data-language]"));
  const languageButtons = Array.from(document.querySelectorAll("[data-set-language]"));

  function setLanguage(language) {
    const selected = language === "ar" ? "ar" : "en";
    root.lang = selected;
    root.dir = selected === "ar" ? "rtl" : "ltr";

    views.forEach((view) => {
      view.hidden = view.dataset.language !== selected;
    });

    languageButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.setLanguage === selected));
    });
  }

  languageButtons.forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.setLanguage));
  });

  document.querySelectorAll(".demo-form").forEach((form) => {
    const fieldset = form.querySelector("fieldset");
    if (fieldset) fieldset.disabled = false;

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const message = form.querySelector("[data-form-message]");
      if (message) message.textContent = "Demo only: validation passed. No data was sent or stored.";
      form.reset();
    });
  });

  setLanguage(root.lang);
})();
