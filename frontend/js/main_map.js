 const proxyurl = 'http://95.217.8.18:8000/complex/get';
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
     //alert(JSON.stringify(data.data[0].events[0].probability))
     //alert(JSON.stringify(parseFloat(data.data[0].events[0].markers[0].geographic_location.latitude)))
     //alert(JSON.stringify(data.data[0].events[0].markers[0].geographic_location.longitude))

     //alert(data.data.length);
     for (let i = 0; i < data.data.length; i++) {
         const location = { lat:   parseFloat(JSON.stringify(data.data[i].geographic_location.latitude)), lng: parseFloat(JSON.stringify(data.data[i].geographic_location.longitude))};
         let contentString = "";
         if (data.data[i].events.length != 0) {
             contentString =
                 '<div id="content">' +
                 '<div id="siteNotice">' +
                 "</div>" +
                 '<h1 id="firstHeading" class="firstHeading">' + data.data[i].title.toString() + '</h1>' +
                 '<div id="bodyContent">' +
                 "<p>Тип КЗ: " + data.data[i].events[0].event_type.toString() +"</p>" +
                 "<p>Длительность КЗ: " + data.data[i].events[0].event_length + " мс.</p>" +
                 "<p>Время: " + data.data[i].events[0].event_start + "</p>" +
                 "<p>К-во ошибок: " + data.data[i].events[0].probability + "</p>" +
                 "</div>" +
                 "</div>";


                let ul = document.getElementById("myUL");
                let li = document.createElement("li");
                let a = document.createElement("a");
                a.appendChild(document.createTextNode( data.data[i].title.toString() + " - " + data.data[i].events[0].event_start))
                li.appendChild(a);
                ul.appendChild(li);

         } else {
             contentString = '<div id="content">' +
                 '<div id="siteNotice">' +
                 "</div>" +
                 '<div id="firstHeading" class="firstHeading">' +
                 data.data[i].title.toString() + '</div>' +
                 "</div>";
         }
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

