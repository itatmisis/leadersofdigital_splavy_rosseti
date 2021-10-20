import React from 'react';
import { YMaps, Map, Placemark, Polyline, ZoomControl } from "react-yandex-maps";
import './css/Map.css';

const mapState = {
    center: [54.306031, 48.155887],
    zoom: 15
};

export default class Custom_Map extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            towerLayoutTemplate: null,
            substationLayoutTemplate: null,
            brigadeLayoutTemplate: null
        };
    }

    render() {
        let placemarks = []
        let [nodes, edges, brigades] = [JSON.parse(this.props.graph)["nodes"],
                                        JSON.parse(this.props.graph)["edges"],
                                        JSON.parse(this.props.brigades)["brigades"]]
        for (let i = 0; i < nodes.length; i++) {
            switch (nodes[i].type) {
                case "tower":
                    placemarks.push(<Placemark
                        geometry={nodes[i].location}
                        options={{
                            iconLayout: this.state.towerLayoutTemplate,
                            balloonPanelMaxMapArea: Infinity
                        }}
                    />)
                    break;
                case "substation":
                    placemarks.push(<Placemark
                        geometry={nodes[i].location}
                        options={{
                            iconLayout: this.state.substationLayoutTemplate,
                            balloonPanelMaxMapArea: Infinity
                        }}
                    />)
                    break;
            }
        }

        let brigades_placemarks = []
        for (let i = 0; i < brigades.length; i++) {
            brigades_placemarks.push(<Placemark
                geometry={brigades[i].location}
                options={{
                    iconLayout: this.state.brigadeLayoutTemplate,
                    balloonPanelMaxMapArea: Infinity
                }}
            />)
        }

        let polylines = []
        for (let i = 0; i < edges.length; i++) {
            let [from, to] = [nodes[edges[i]["from"]].location, nodes[edges[i]["to"]].location]
            polylines.push(<Polyline
                    geometry={[from, to]}
                    options={{
                        balloonCloseButton: false,
                        strokeColor: '#000',
                        strokeWidth: 2,
                        strokeOpacity: 0.5,
                    }}
                />)
        }

        return (
            <div>
                <YMaps id = "map" query={{ lang: "ru_RU", load: "package.full" }}>
                    <Map defaultState={mapState}
                         width="100%" height="100%"
                         modules={[
                             "templateLayoutFactory",
                             "option.presetStorage",
                             "option.Manager",
                             "control.ZoomControl",
                             "control.FullscreenControl"
                         ]}
                         instanceRef={(ref) => (this.map = ref)}
                         onLoad={(ymaps) => {
                             this.setState({
                                 towerLayoutTemplate: ymaps.templateLayoutFactory.createClass('<div class="tower"></div>'),
                                 substationLayoutTemplate: ymaps.templateLayoutFactory.createClass('<div class="substation"></div>'),
                                 brigadeLayoutTemplate: ymaps.templateLayoutFactory.createClass('<div class="brigade"></div>')
                             })}
                         }>

                        {placemarks}
                        {brigades_placemarks}
                        {polylines}

                    </Map>
                </YMaps>
            </div>
        );
    }
}
