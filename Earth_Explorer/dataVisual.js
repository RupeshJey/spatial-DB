// Earth_Explorer
// Created on April 19, 2020
// 
// This file is responsible for handling, parsing, 
// and visualizing all the data, as well as setting
// up all UI components defined in index.html


// Open IIFE
var dataVisual = (function() {

    // Use Javascript strict mode
    'use strict';

    // This is the access token for this project
    mapboxgl.accessToken = 'pk.eyJ1IjoicnVwZXNoamV5IiwiYSI6ImNrNXU2a2c3cTA2Z28za241Y3o4bnZzdGYifQ.LUPkB1SoOmQqD3-CsPWihw'

    // Create the map, with some default settigns
    var map = new mapboxgl.Map({
        container: 'map', // container id
        minzoom: 0.5,
        style: 'mapbox://styles/rupeshjey/ck8b0ilx918y61jnoim1x8hes', // stylesheet location
        bounds: [[-127, 24.9493], [-65, 49.5904, ]]  // USA center
    });

    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl,
        countries: 'us',
        collapsed: true
    })

    map.addControl(
        geocoder,
        'bottom-left'
    );

    map.addControl(new mapboxgl.NavigationControl({showCompass: false,
        showZoom: true}), 'bottom-left');

    // Return the dataVisual 'class'
    return dataVisual;

// Close IIFE
})();
