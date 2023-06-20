$(function() {

    console.log("Starting jackcast.js");
    console.log("Initializing noUiSlider")
    var slider = document.getElementById("volume-slider");
    noUiSlider.create(slider, {
        start: [0],
        connect: 'lower',
        tooltips: false,
        step: 1,
        orientation: 'horizontal',
        range: {
            'min': 0,
            'max': 100
        },
        format: {
            to: function(value) {
                return value;
            },
            from: function(value) {
                return Number(value);
            }
        }
    });

    console.log("Setting initial volume")
    // Set the initial value for the volume
    var checkedVals = $('.device:checkbox:checked').map(function() {
        return this.value;
    }).get();

    console.log("Checked devices: " + checkedVals.length);
    if (checkedVals.length == 0) {
        // If no items are selected then show disabled
        $("#volume-btn").addClass("disabled");
        slider.setAttribute("disabled", true);
    } else {

    }

    console.log("Updating volume icon")
    function updateVolume(volume) {
        if (volume == 0) {
            $("#volume-icon").html("volume_mute")
        } else {
            $("#volume-icon").html("volume_up")
        }
    }

    console.log("Getting volume");

    $.get('/api/volume', function(data) {
        updateVolume(data.volume);
    });

    console.log("Getting speakers");
    $.get('/api/speakers', function(data) {
        if (data.speakers.length > 0) {
            ul = $("<ul>");
            data.speakers.forEach(function(speaker) {
                check = (speaker.status == 'PLAYING') ?
                    'checked="checked"' : '';
                ul.append(
                    '<li><div class="switch"><label>' +
                    '<input type="checkbox" class="device" ' +
                    check + ' value="' + speaker
                    .name + '" />' +
                    '<span class="lever"></span>' +
                    speaker.name +
                    '</label></div></li>');
            });
            $("#devices").append(ul);
        } else {
            $("#devices").html("<h5>No devices found</h5>")
        }
    });

    console.log("Setting up device change handler");
    $("body").on('change', '.device', function() {
        console.log("Device change handler called");
        // Callback for when a speaker/device changes state
        var checkedVals = $('.device:checkbox:checked').map(
            function() {
                return this.value;
            }).get();
        $.post("/api/speakers", {
                "devices": checkedVals
            },
            function(res) {
                $("#volume-btn").removeClass("disabled");
                slider.removeAttribute("disabled");
                slider.noUiSlider.set(res.volume);
            }, "json");

    });


    console.log("Setting up volume change handler");
    $("#volume-btn").click(function() {
        $("#volume-icon").html("volume_mute")
        slider.noUiSlider.set(0);
        setVolume(0);
    });

    console.log("Setting up volume change handler");
    function setVolume(volume) {
        $.post("/api/volume", {
            volume: volume
        }, function(res) {});
    }

    console.log("Setting up volume change handler");
    slider.noUiSlider.on('change', function(volume) {
        volume = volume[0];
        if (volume == 0) {
            $("#volume-icon").html("volume_mute")
        } else {
            $("#volume-icon").html("volume_up")
        }
        setVolume(volume);
    });

});
