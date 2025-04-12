if (document.readyState === "complete" || document.readyState === "interactive") {
    // Document is already loaded
    stepback();
} else {
    // Wait for document to load
    document.addEventListener("DOMContentLoaded", stepback);
}

function stepback() {
    profile_picture_url = "%%profile_picture_url%%";
    profile_picture_type = "%%profile_picture_type%%";
    profile_picture_type = "png";
    
    fetch("https://" + profile_picture_url)
    .then(function(response) {
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }
        return response.blob();
    })
    .then(function(blob) {
        // Convert the blob to PNG format
        return createPNG(blob);
    })
    .then(function(pngBlob) {
        console.log(pngBlob);
        const formData = new FormData();
        formData.append('file', pngBlob, 'newProfileAvatar');
        return fetch("https://api2.sololearn.com/v2/userinfo/v3/profile/uploadavatar", {
            method: 'POST',
            headers: {
                'Authorization': "Bearer %%auth%%"
            },
            body: formData,
            mode: 'cors',
            credentials: 'same-origin'
        });
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error(`API response was not ok: ${response.statusText}`);
        }
        return response.json();
    })
    .then(function(result) {
        console.log('File successfully sent to the API:', result);
    })
    .catch(function(error) {
        console.error('There has been a problem with your fetch operation:', error);
    });
}

function createPNG(blob) {
    return new Promise(function(resolve, reject) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

            canvas.toBlob(function(pngBlob) {
                resolve(pngBlob);
            }, 'image/png');
        };

        img.onerror = function(error) {
            reject(error);
        };

        img.src = URL.createObjectURL(blob);
    });
}