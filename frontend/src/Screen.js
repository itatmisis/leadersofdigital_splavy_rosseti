import React from 'react';
import './css/Screen.css';
import Custom_Map from './Map.js'
import Logs from "./Logs";

export default class Forma extends React.Component {
    constructor(props) {
        super(props);

        this.state ={ data: {}, graph: {}, brigades: {}, isFetching: true, error: null };
    }

 /*   componentDidMount() {
        fetch('http://localhost:3001')
            .then(response => response.json())
            .then(result => this.setState({data: result, isFetching: false })).catch(error => {
            console.log(error);
            this.setState({data: "no data", isFetching: false, error: error})
        });
    }
*/
    render() {
        this.state.data = JSON.stringify({events: [{timestamp: "12:05", type: "3", protection: "True", location: [57, 23]},
                                                            {timestamp: "13:23", type: "1", protection: "True", location: [56, 22]}]})

        this.state.graph = JSON.stringify({nodes: [{id: 0, type: "substation", location: [54.306031, 48.155887]},
                                                         {id: 1, type: "tower", location: [54.296831, 48.154087]},
                                                         {id: 2, type: "tower", location: [54.290331, 48.150987]},
                                                         {id: 3, type: "tower", location: [54.286631, 48.136687]},
                                                         {id: 4, type: "substation", location: [54.278831, 48.133087]},
                                                         {id: 5, type: "tower", location: [54.278931, 48.127987]}],
                                                edges: [{from: 0, to: 1}, {from: 1, to: 2}, {from: 2, to: 3}, {from: 3, to: 4}, {from: 4, to: 5}]})
        this.state.brigades = JSON.stringify({brigades: [{id: 0, location: [54.289916, 48.201294]}, {id: 1, location: [54.306628, 48.139332]}]})

//        const { data, isFetching, error } = this.state;

//        if (isFetching) return <div>...Loading</div>;

//        if (error) this.state.data = 0

        return (
            <div class = "screen_body">
                <Logs data = {this.state.data} />
                <Custom_Map data = {this.state.data} graph = {this.state.graph} brigades = {this.state.brigades} />
            </div>
        );
    }

}
