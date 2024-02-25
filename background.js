chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  $.ajax({
    url: "http://localhost:3000",
    method: "POST",
    data: request,
    timeout: 15000,
    success: data => {
      sendResponse({ success: true, phishing: data.result });
    },
    error: (XMLHttpRequest, textStatus, errorThrown) => {
      console.log(textStatus);
      console.log(errorThrown);
      sendResponse({ success: false });
    }
  });
});
