var symps = [];
var sbox = document.getElementById("sbox");

$(document).ready(function(){
    $("input").typeahead({
        source: symp_list,
        minLength: 2
    });

    if (!localStorage.getItem("key")) {
        introJs().start();
        localStorage.setItem("key", "keyValue");
    }
});

function appendNewSymp(name) {
    console.log(name);
    symps.push(name.replace("-", " "));
    $("#positive").append(' ' + ' <span class="badge badge-secondary">' + name + '</span> ' + ' ');
    $('#' + name).remove();
}

function deleteSymp(name) {
    $('#' + name).remove();
}

function appendSymp() {
    var a = $("#symptom").val();
    symps.push(a);
    $("#tags").append('<span> </span><span class="badge badge-secondary">' + a + '</span>');
    $("#symptom").val("");
}

$("#symp_upload").click(function() {
    $.ajax({
        url: '/disease', // Custom backend endpoint
        type: 'post',
        data: JSON.stringify({
            'symptoms': symps
        }),
        dataType: 'JSON',
        contentType: "application/json",
        success: function(response) {
            console.log(response);
            symps = [];
            SymFunc(response);
            console.log("DONE!");
        },
    });
});

function sendSymp() {
    $.ajax({
        url: '/find', // Custom backend endpoint
        type: 'post',
        data: JSON.stringify({
            'symptoms': symps
        }),
        dataType: 'text',
        contentType: "application/json",
        success: function(response) {
            console.log(response);
            symps = [];
            showDis(response);
            console.log("DONE!");
        },
    });
};

$("#but_upload").click(function() {
    var fd = new FormData();
    var files = $('#file')[0].files[0];

    if (files == undefined) {
        alert("Please insert an image");
    } else {
        fd.append('file', files);
        $("#details").append('<div class="spinner-border" style="width: 3rem; height: 3rem;" role="status"> <span class="sr-only">Loading...</span></div>');
        
        // Use Tesseract.js for OCR (prescription scanning)
        Tesseract.recognize(
            files, // The image file
            'eng', // Language
            {
                logger: (m) => console.log(m) // Optional: Log OCR progress
            }
        ).then(({ data: { text } }) => {
            console.log("OCR Result:", text);
            $("#details").empty(); // Clear the loading spinner
            RecieveFunc(text); // Display the result (processed text)
        });
    }
});

function SymFunc(data) {
    $("#cards").empty();
    $("#details").empty();
    $("#slogan").empty();
    sbox.classList.toggle("m-fadeOut");
    if (data.length === 0) {
        $("#cards").append('<div class="card text-center shadow rounded w-75 center"><div class="card-body"><h5 class="card-title">No results found!</h5></div></div>');
    } else {
        $("#details").append('<h3 class="text-white" style="text-align: center; text-shadow: 0 0 20px #000000;"><b>Please answer the following questions.</b></h3><br/><br/><a role="button" aria-pressed="true" href="." class="btn btn-outline-light btn-small">BACK</a>');
        data.forEach(function(name) {
            var name = name.replace(/\s/g, '-');
            $("#cards").append('<div class="card w-75 center text-center shadow p-3 mb-5 bg-white rounded boxy" id="' + name + '"> <div class="card-body"> <p class="card-title">Do you have/feel ?</p> <h4 class="card-text" style="text-align: center; text-shadow: 0 0 2px #000000;"><b>' + name + '</b></h4> <div class="row"> <div class="col-md-2"></div> <a class="btn btn-outline-success col-md-3 " onclick=appendNewSymp("' + name + '");><b> YES </b></a> <div class="col-md-2"></div> <a class="btn btn-outline-danger col-md-3" onclick=deleteSymp("' + name + '");><b> NO </b></a> <div class="col-md-2"></div> </div> </div> </div>');
        })
        $("#cards").append('<div class="card w-75 center text-center shadow p-3 mb-5 bg-white rounded boxy" id="' + name + '"><div class="card-body"><p class="card-title">Your symptoms</p><h5 class="card-text" id="positive"></h5></div><button type="button" onclick=sendSymp(); class="btn btn-warning btn-lg">SEARCH</button></div>');
    };
};

function showDis(data) {
    $("#cards").empty();
    $("#details").empty();
    $("#details").append('<h1 class="boxy text-white" style="text-align: center; text-shadow: 0 0 20px #000000;"><b>It is most probably ' + data + ' .</b></h1><br/><br/><a role="button" aria-pressed="true" href="." class="btn btn-outline-light btn-lg">BACK</a>');
}

function RecieveFunc(data) {
    $("#cards").empty();
    $("#details").empty();
    $("#slogan").empty();
    sbox.classList.toggle("m-fadeOut");
    if (data.length === 0) {
        $("#cards").append('<div class="card text-center shadow rounded w-75 center"><div class="card-body"><h5 class="card-title">No results found!</h5></div></div><br/><br/><a role="button" aria-pressed="true" href="." class="btn btn-outline-light btn-lg">BACK</a>');
    } else {
        $("#details").append('<h3 class="text-white" style="text-align: center; text-shadow: 0 0 20px #000000;"><b>Here is your schedule </b></h3><br/><br/><a role="button" aria-pressed="true" href="." class="btn btn-outline-light btn-small">BACK</a>');
        var count = Object.keys(data).length;
        console.log(count);

        var i = 1;
        $("#cards").append('<div class="card w-75 center text-center shadow p-3 mb-5 bg-white rounded boxy"> <div class="card-body"> <h5 class="card-title">Medicine</h5> <p class="card-text">Take Aspirin for 7 days.</p> <a class="btn btn-outline-success">Done</a> </div> </div>');
        $("#cards").append('<div class="card w-75 center text-center shadow p-3 mb-5 bg-white rounded boxy"> <div class="card-body"> <h5 class="card-title">Medicine</h5> <p class="card-text">Take Advil for 3 days.</p> <a class="btn btn-outline-success">Done</a> </div> </div>');
    }
};
