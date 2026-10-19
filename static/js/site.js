/* 7pro8.com — progressive enhancement only. Everything works without it. */
(function () {
  "use strict";

  /* --- mobile navigation ------------------------------------------------ */
  var toggle = document.querySelector(".navtoggle");
  var nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* --- electrochromic glass demonstration -------------------------------
     The product's signature behaviour, shown rather than described. The
     switch is user-triggered; nothing animates on its own.                */
  var glass = document.querySelector("[data-glass]");
  if (glass) {
    var button = glass.querySelector("[data-glass-toggle]");
    var label = glass.querySelector("[data-glass-label]");
    if (button && label) {
      button.addEventListener("click", function () {
        var opaque = glass.classList.toggle("is-opaque");
        button.setAttribute("aria-pressed", opaque ? "true" : "false");
        label.textContent = opaque
          ? label.getAttribute("data-on")
          : label.getAttribute("data-off");
      });
    }
  }

  /* --- enquiry form ------------------------------------------------------
     Posts to the endpoint configured in content/site.json. If JavaScript or
     the endpoint is unavailable the form still submits normally and the
     mailto fallback below it stays visible.                               */
  var form = document.querySelector("[data-form]");
  if (form && window.fetch && form.getAttribute("action").indexOf("http") === 0) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
      }
      fetch(form.getAttribute("action"), {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      })
        .then(function (response) {
          if (!response.ok) {
            throw new Error("bad status");
          }
          var done = document.createElement("p");
          done.className = "lead";
          done.textContent = form.getAttribute("data-sent") || "Thank you. We will reply within two working days.";
          form.classList.add("is-sent");
          form.insertBefore(done, form.firstChild);
        })
        .catch(function () {
          if (button) {
            button.disabled = false;
          }
          form.removeAttribute("data-form");
          form.submit();
        });
    });
  }
})();
