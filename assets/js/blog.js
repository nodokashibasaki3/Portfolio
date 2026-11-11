// Gives each blog callout (a quote tagged {: .callout}) an icon column on the left:
// its leading emoji, or the site icon of its first link. Posts stay plain Markdown, and
// without this script callouts still read fine, just without the icon column.
(function () {
  "use strict";

  var FAVICON_URL = "https://www.google.com/s2/favicons?sz=64&domain=";
  // An emoji at the very start, including variation selectors, skin tones, and ZWJ sequences.
  var LEADING_EMOJI =
    /^\s*(\p{Extended_Pictographic}(?:️|[\u{1F3FB}-\u{1F3FF}]|‍\p{Extended_Pictographic})*️?)\s*/u;

  /**
   * Removes the emoji that starts the callout's first paragraph and returns it.
   * @param {HTMLElement} callout
   * @returns {Text | null}
   */
  function takeLeadingEmoji(callout) {
    var first = callout.firstElementChild;
    var node = first && first.tagName === "P" ? first.firstChild : null;
    if (!node || node.nodeType !== Node.TEXT_NODE) return null;
    var match = node.textContent.match(LEADING_EMOJI);
    if (!match) return null;
    node.textContent = node.textContent.slice(match[0].length);
    return document.createTextNode(match[1]);
  }

  /**
   * @param {HTMLElement} callout
   * @returns {HTMLImageElement | null} the site icon of the callout's first external link
   */
  function firstLinkIcon(callout) {
    var link = callout.querySelector('a[href^="http"]');
    if (!link) return null;
    var img = document.createElement("img");
    img.src = FAVICON_URL + new URL(link.href).hostname;
    img.alt = "";
    img.loading = "lazy";
    return img;
  }

  /**
   * Wraps the callout's content and puts its icon in a column to the left.
   * @param {HTMLElement} callout
   */
  function addIcon(callout) {
    var icon = takeLeadingEmoji(callout) || firstLinkIcon(callout);
    if (!icon) return;
    var iconBox = document.createElement("span");
    iconBox.className = "callout-icon";
    iconBox.setAttribute("aria-hidden", "true");
    iconBox.appendChild(icon);
    var content = document.createElement("div");
    content.className = "callout-content";
    while (callout.firstChild) content.appendChild(callout.firstChild);
    callout.appendChild(iconBox);
    callout.appendChild(content);
    callout.classList.add("has-icon");
  }

  document.querySelectorAll(".post blockquote.callout:not(.callout-link)").forEach(addIcon);
})();
