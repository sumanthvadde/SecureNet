console.log("here");
// TODO: Only links that doesnot start with # and check for relative links
$("a[href]").on("click", function(e) {
  e.preventDefault();
  // TODO: Handle ctrl+click and new tab event
  var evt = e.ctrlKey;
  var link = this.href;
  if (link.charAt(0) != "#" && navigator.onLine) {
    chrome.runtime.sendMessage({ url: link }, res => {
      if (res && res.success) {
        if (res.phishing) {
          if (confirm("This link is suspicious, Do you want to continue?"))
            window.location.href = link;
        } else window.location.href = link;
      } else {
        let option = confirm(
          "We cannot verify the integrity of the webpage. Continue?"
        );
        if (option) window.location.href = link;
      }
    });
  } else window.location.href = link;
});
