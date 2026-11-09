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

  /* No form backend yet: the action is a mailto: link. Instead of the
     browser's raw text/plain post, open the visitor's mail program with the
     enquiry written out as a readable message.                            */
  if (form && form.getAttribute("action").indexOf("mailto:") === 0) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var trap = form.querySelector('[name="_gotcha"]');
      if (trap && trap.value) {
        return;
      }
      var lines = [];
      var seen = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.name.charAt(0) === "_" || el.name === "consent" || seen[el.name]) {
          return;
        }
        var label, value;
        if (el.type === "checkbox") {
          seen[el.name] = true;
          var picked = form.querySelectorAll('[name="' + el.name + '"]:checked');
          value = Array.prototype.map.call(picked, function (c) { return c.value; }).join(", ");
          var set = el.closest("fieldset");
          label = set && set.querySelector("legend") ? set.querySelector("legend").textContent : el.name;
        } else {
          value = el.value;
          var l = el.id ? form.querySelector('label[for="' + el.id + '"]') : null;
          label = l ? l.textContent : el.name;
        }
        if (value && value.trim()) {
          label = label.trim();
          lines.push(label + (/[?:]$/.test(label) ? " " : ": ") + value.trim());
        }
      });
      window.location.href = form.getAttribute("action") +
        "&body=" + encodeURIComponent(lines.join("\n"));
    });
  } else if (form && window.fetch && form.getAttribute("action").indexOf("http") === 0) {
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
