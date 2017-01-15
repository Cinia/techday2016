import React from 'react';
import ReactDOM from 'react-dom';
import _throttle from 'lodash/throttle';

import BotApi from './api/bot.js';
import Telemetry from './telemetry/index.jsx';
import config from './config.js';

import './styles/app.scss';
import LOGO from './images/cinia-logo.png';
import INNER from './images/inner.svg';


/** Control area default width in pixels. */
const CONTROL_SIZE = 400;
/** Drive commands will not be sent more often than this. */
const THROTTLE_MSEC = 200;

/**
 * A component that can be used to control the robot and see what it sees.
 */
export default class RobotView extends React.Component {
    static displayName = 'Robot.RobotView';

    constructor(props) {
        super(props);
        // let's not flood the robot API
        this._throttledDrive = _throttle(this.drive.bind(this), THROTTLE_MSEC);
    }

    drive(x, y) {
        return BotApi.drive(x, y);
    }

    grab() {
        return BotApi.grab();
    }

    release() {
        return BotApi.release();
    }

    /**
     * Update control indicator position inside the big circle.
     * @param {number} x - Horizontal position as [0..1]
     * @param {number} y - Vertical position as [0..1]
     */
    updateControlIndicator(x, y) {
        if (this.refControl) {
            this.refControl.style = `left: ${x * 100}%; top: ${y * 100}%`;
        }
    }

    /**
     * Stop repeating last control event.
     */
    clearPendingRepeat() {
        if (this.pendingRepeat) {
            window.clearTimeout(this.pendingRepeat);
            this.pendingRepeat = null;
        }
    }

    /**
     * Begin controlling the robot's movement direction.
     * @param {object} event - Touch end / mouse down event
     */
    controlBegin(event) {
        this.controlling = true;
        this.clearPendingRepeat();
        this.controlTouch(event);
    }

    /**
     * Stop controlling the robot's movement direction.
     * @param {object} event - Touch end / mouse up event
     */
    controlEnd() {
        this.controlling = false;
        this.clearPendingRepeat();
        this.updateControlIndicator(.5, .5);
    }

    /**
     * Handle touch, press, click or poke event in control area.
     * @note Doesn't actually call setState to avoid pointless re-render
     * @param {object} event - Touch event
     */
    controlTouch(event) {
        if (!this.controlling) {
            return;
        }
        this.clearPendingRepeat();

        let { offsetX, offsetY } = event.nativeEvent;

        let relX = offsetX / (CONTROL_SIZE / 2) - 1.0;
        let relY = -offsetY / (CONTROL_SIZE / 2) + 1.0;

        /*this.setState({
            lastX: relX,
            lastY: relY,
        });*/

        if (this.refControl) {
            this.updateControlIndicator(offsetX / CONTROL_SIZE, offsetY / CONTROL_SIZE);
        }

        this._throttledDrive(relX, relY);

        // HACK: keep repeating this control event even if no dragging happens
        event.persist();
        this.pendingRepeat = window.setTimeout(() => {
            this.controlTouch(event);
        }, THROTTLE_MSEC);
    }

    render() {
        // let { lastX, lastY } = this.state || {};
        return (<div>
            <div className="page-wrap">
                <img className="fullscreen-bg" src={config.streamUrl} />
                <div className="header-logo">
                    <img src={LOGO} />
                </div>
                <nav className="app-nav-wrap">
                    <ul className="app-nav">
                        <li><a role="button" onClick={this.grab.bind(this)}>
                            Grab
                        </a></li>
                        <li><a role="button" onClick={this.release.bind(this)}>
                            Release
                        </a></li>
                        <li><a role="button"></a></li>
                    </ul>
                </nav>
            </div>
            <div className="control-holder"
                onMouseDown={this.controlBegin.bind(this)}
                onMouseMove={this.controlTouch.bind(this)}
                onMouseUp={this.controlEnd.bind(this)}
                onMouseOut={this.controlEnd.bind(this)}
                draggable={false}
                >
                <div className="control" ref={(r) => { this.refControl = r; } }>
                    <img src={INNER} draggable={false} />
                </div>
            </div>
            <div className="telemetry-holder">
                <Telemetry src={config.telemetryUrl} />
            </div>
        </div>);
    }
}

ReactDOM.render((<RobotView />), document.getElementById('app'));
