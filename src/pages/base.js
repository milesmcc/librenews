if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('service-worker.js').then(function(registration) {
      this.registration = registration;

      // Registration was successful
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
      if (isSubscribed()) {
        $("#notification-button").prop("disabled", true);
        $("#notification-button").text("You're Subscribed");
      }
    }, function(err) {
      // registration failed :(
      console.log('ServiceWorker registration failed: ', err);
    });
  });
} else {
  $("#notification-button").text("Incompatible Browser");
  $("#notification-button").prop("disabled", true);
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}


function askNotificationPermission() {
  return new Promise(function(resolve, reject) {
      const permissionResult = Notification.requestPermission(function(result) {
        resolve(result);
      });

      if (permissionResult) {
        permissionResult.then(resolve, reject);
      }
    })
    .then(function(permissionResult) {
      if (permissionResult !== 'granted') {
        throw new Error('We weren\'t granted permission.');
      } else {
        subscribeUserToPush();
      }
    });
}

function isSubscribed() {
  return registration.pushManager.getSubscription() != null;
}

function unsubscribeAllPushNotifications() {
  navigator.serviceWorker.ready.then(function(reg) {
    reg.pushManager.getSubscription().then(function(subscription) {
      subscription.unsubscribe().then(function(successful) {
        alert("You have been unsubscribed!")
        $("#notification-button").text("Resubscribe to Notifications");
        $("#notification-button").attr("onclick", "askNotificationPermission()");
      }).catch(function(e) {
        alert("Unable to unsubscribe...")
      })
    })
  });
}

function subscribeUserToPush() {
  return navigator.serviceWorker.register('service-worker.js')
    .then(function(registration) {
      const subscribeOptions = {
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(
          "{{applicationServerKey}}"
        )
      };
      return registration.pushManager.subscribe(subscribeOptions);
    })
    .then(function(pushSubscription) {
      console.log('Received PushSubscription: ', JSON.stringify(pushSubscription));
      sendSubscriptionToBackEnd(pushSubscription);
      $("#notification-button").prop("disabled", true);
      $("#notification-button").text("You're Subscribed");
      return pushSubscription;
    });
}

function sendSubscriptionToBackEnd(subscription) {
  return fetch('/push', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(subscription)
    })
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Bad status code from server.');
      }

      return response.json();
    })
    .then(function(responseData) {
      if (!(responseData.data && responseData.data.success)) {
        console.log(responseData.data)
        throw new Error('Bad response from server.');
      }
    });
}
