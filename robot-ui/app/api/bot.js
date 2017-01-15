import _template from 'lodash/template';
import config from '../config';


export class Endpoint {
    constructor(pathTemplate) {
        this._template = _template(pathTemplate);
    }

    xhr(path, method, data) {
        return new Promise((resolve, reject) => {
            let req = new XMLHttpRequest();
            req.addEventListener('load', (e) => {
                // resolve(JSON.parse(req.responseText));
                resolve(req.responseText);
            });
            req.addEventListener('error', () => {
                reject(req.responseText);
                // let parsed = JSON.parse(req.responseText);
                // reject(parsed);
            });
            req.addEventListener('abort', (e) => {
                reject(req.responseText);
                // let parsed = JSON.parse(req.responseText);
                // reject(parsed);
            });
            req.open(method, config.apiUrl + path);
            if(data) {
                req.data = JSON.stringify(data);
            }
            req.send();
        });
    }

    /**
     * Make a GET request.
     * @param {object} pathParams - Params for endpoint's path template
     * @param {object} [data] - Data to pass, if any
     * @returns {Promise} - Async result
     */
    get(pathParams, data) {
        return this.xhr(this._template(pathParams), 'GET', data);
    }
}

/**
 * API for controlling the robot.
 */
export class BotApi {
    constructor() {
        // TODO: do we need to care about proper param encoding?
        this.epDrive = new Endpoint('/drive?x=${x}&y=${y}');
        this.epGrab = new Endpoint('/grab');
        this.epRelease = new Endpoint('/release');
    }

    /**
     * Make the robot drive in a direction.
     * @param {number} x - right/left input, should be within [-1, 1]
     * @param {number} y - forward/back input, should be within [-1, 1]
     * @returns {Promise} - request status
     */
    drive(x, y) {
        return this.epDrive.get({ x, y });
    }

    /**
     * Make the robot grab something.
     * @returns {Promise} - request status
     */
    grab() {
        return this.epGrab.get();
    }

    /**
     * Make the robot open its claws.
     * @returns {Promise} - request status
     */
    release() {
        return this.epRelease.get();
    }
}

export default new BotApi();
