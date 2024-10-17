/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export const todoPropShape = {type: Object, shape: {id: Number, description: String, done: Boolean }};

export class Todo extends Component {
    static template = "owl_playground.todo";
    static props = { todo: todoPropShape };

    constructor(parent) {
        super(parent);
        console.log(parent)
    }
}
