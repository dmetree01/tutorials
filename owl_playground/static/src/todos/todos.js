/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { todoPropShape } from "../todo/todo";
import { Todo } from "../todo/todo";

export class Todos extends Component {
    static template = "owl_playground.todos";
    static components = { Todo };
    static props = { todos: {type: Array, element: todoPropShape} };

    // constructor(parent) {
    //     super(parent);
    //     console.log(parent)
    // }
}
