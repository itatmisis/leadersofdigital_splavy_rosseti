 const proxyurl = 'https://cors-anywhere.herokuapp.com/' + 'http://95.217.164.134/complex/get';
 google.maps.event.addDomListener(window, 'load', initMap);
 let map, infoWindow;



 //alert(proxyurl)
 fetch(proxyurl).then((response) => {
     return response.json();
 }).then((data) => {
//     alert(JSON.stringify(data.data[0].geographic_location.longitude));




     function addMarker(coordinates, content) {

         const infowindow = new google.maps.InfoWindow({
             content: content,
         });

         const marker = new google.maps.Marker({
             position: coordinates,
             map
         });
         infowindow.open(map, marker);
         marker.addListener("click", () => {
             infowindow.open(map, marker);
         });
     }
     alert(JSON.stringify(data.data))
//     alert(JSON.stringify(parseFloat(data.data[0].events[0].markers[0].geographic_location.latitude)))
//     alert(JSON.stringify(data.data[0].events[0].markers[0].geographic_location.longitude))
     alert(data.data.length);
     for (let i = 0; i < data.data.length; i++) {
         const location = { lat:   parseFloat(JSON.stringify(data.data[i].events[0].markers[0].geographic_location.latitude)), lng: parseFloat(JSON.stringify(data.data[i].events[0].markers[0].geographic_location.longitude))};

         const contentString =
             '<div id="content">' +
             '<div id="siteNotice">' +
             "</div>" +
             '<h1 id="firstHeading" class="firstHeading">ВКБ-1123</h1>' +
             '<div id="bodyContent">' +
             "<p>Тип КЗ:" +  + "</p>" +
             "<p>Длительность КЗ: 43 мс</p>" +
             "<p>Время: 12:54:13:1032 - 12:54:13:1075</p>" +
             "<p>Вероятность срабатывания защиты: 0.71</p>" +
             "</div>" +
             "</div>";
         addMarker(location, contentString);
 }

 });

 function initMap() {
     map = new google.maps.Map(document.getElementById("map"), {
         center: { lat: -34.397, lng: 150.644 },
         zoom: 6,
     });
     infoWindow = new google.maps.InfoWindow();
 }

