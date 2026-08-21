const imageInput =
    document.getElementById("imageInput");

const preview =
    document.getElementById("preview");

const loading =
    document.getElementById("loading");

const error =
    document.getElementById("error");


imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    const reader =
        new FileReader();

    reader.onload = function (event) {

        preview.src =
            event.target.result;

        preview.style.display =
            "block";
    };

    reader.readAsDataURL(file);

});


async function analyzeImage() {

    const file =
        imageInput.files[0];

    error.textContent = "";

    if (!file) {

        error.textContent =
            "Please select a leaf image first.";

        return;
    }


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    loading.style.display =
        "block";


    try {

        const response =
            await fetch(
                "/api/predict",
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Prediction failed."
            );

        }


        sessionStorage.setItem(
            "plantResult",
            JSON.stringify(
                data.prediction
            )
        );


        window.location.href =
            "/result.html";


    } catch (err) {

        error.textContent =
            err.message;

    } finally {

        loading.style.display =
            "none";

    }

}