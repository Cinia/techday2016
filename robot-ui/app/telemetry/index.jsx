import React from 'react';
import io from 'socket.io-client';


export default class Telemetry extends React.Component {
    static displayName = 'Robot.Telemetry';

    static propTypes = {
        src: React.PropTypes.string.isRequired
    }

    state = {
        temperature: 0
    }

    componentWillMount() {
        let socket = io(this.props.src);
        socket.on('robot/senses/temperature',
            this.handleMessage.bind(this, 'temperature'));
        socket.on('robot/senses/humidity/humidity',
            this.handleMessage.bind(this, 'humidity'));
        socket.on('robot/senses/pressure/pressure',
            this.handleMessage.bind(this, 'pressure'));
        socket.on('robot/senses/compass',
            this.handleMessage.bind(this, 'compass'));
        this.socket = socket;
    }

    handleMessage(name, val) {
        // TODO: collect stats for graphing
        this.setState({
            [name]: val
        });
    }

    componentWillUnmount() {
        if (this.socket) {
            this.socket.disconnect();
        }
    }

    render() {
        let { temperature, humidity, pressure, compass } = this.state;
        return (<div className="telemetry">
            <div className="row">
                <div className="col-sm-6">Temperature</div>
                <div className="col-sm-6">{temperature}</div>
            </div>
            <div className="row">
                <div className="col-sm-6">Humidity</div>
                <div className="col-sm-6">{humidity}</div>
            </div>
            <div className="row">
                <div className="col-sm-6">Pressure</div>
                <div className="col-sm-6">{pressure}</div>
            </div>
            <div className="row">
                <div className="col-sm-6">Compass</div>
                <div className="col-sm-6">{compass}</div>
            </div>
        </div>);
    }
}
