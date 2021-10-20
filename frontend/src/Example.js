import React, {useRef} from 'react'
import { YMaps, Map } from 'react-yandex-maps'


export default function App() {
    const map = useRef(null);
    const mapState = {
        center: [55.739625, 37.5412],
        zoom: 12
    };

    const addRoute = (ymaps) => {
        const pointA = [55.749, 37.524];
        const pointB = "Москва, Красная площадь";

        const multiRoute = new ymaps.multiRouter.MultiRoute(
            {
                referencePoints: [pointA, pointB],
                params: {
                    routingMode: "pedestrian"
                }
            },
            {
                boundsAutoApply: true
            }
        );

        map.current.geoObjects.add(multiRoute);
    };

    return (
        <div className="App">
            <YMaps query={{ apikey: "7d6e1cff-fe79-475d-8018-09fbbae4aeea" }}>
                <Map
                    modules={["multiRouter.MultiRoute"]}
                    state={mapState}
                    width="100%" height="100%"
                    instanceRef={map}
                    onLoad={addRoute}
                ></Map>
            </YMaps>
        </div>
    );
}