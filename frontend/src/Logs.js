import React from 'react';
import './css/Logs.css';
import {Map, Placemark, YMaps} from "react-yandex-maps";

class Searchbox extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        this.props.onSearchChange(e.target.value);
    }

    render() {
        let searchRequestCurrent = this.props.search;
//        alert(searchRequestCurrent)
        return (<input type="text" value={searchRequestCurrent}  id="myInput" onChange={(e) => this.handleChange(e)} placeholder="Поиск данных о КЗ"/>);
    }
}

class Log extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);

    }

    handleChange(e) {
        this.props.onLogAdd(this.props.index, this.props.text);
    }

    render() {
        return (<li><a> {this.props.text} </a></li>);
    }
}

export default class Logs extends React.Component {
    constructor(props) {
        super(props);
        this.handleSearchRequest = this.handleSearchRequest.bind(this);
        this.state = {search: "",
                      logs: []
        }

    }

    handleSearchRequest(searchRequest) {
        this.setState({search: searchRequest});
    }

    handleLogsData(i, logsData) {
        const logs = this.state.logs.slice()
        logs[i] = logsData
        this.setState({search: this.state.search,
                            logs: logs
        });
    }

    render() {
        let parsed = JSON.parse(this.props.data)["events"]
        let lis = []
        for (let i = 0; i < parsed.length; i++) {
            let data = parsed[i].timestamp + ", тип КЗ - " + parsed[i].type + ", релейная защита - " +
                parsed[i].protection
            if (data.includes(this.state.search)) {
                lis.push(<Log index={i} text={data} onLogAdd={(e) => this.handleLogsData(e)}/>)
            }
        }
        return (
            <div className="panels">
                <div className="logs">
                    <div className="logs_header">
                        <div className="title">Логи</div>
                        <Searchbox search = {this.state.search} onSearchChange={(e) => this.handleSearchRequest(e)} />
                    </div>
                    <ul id="myUL">
                        {lis}
                    </ul>
                </div>
                <div className="menu">
                    <div className="title">Логи</div>
                    <div className="info"></div>
                    <div className="buttons">
                        <div className="back"></div>
                        <div className="next"></div>
                    </div>
                </div>
            </div>
        );
    }
}
