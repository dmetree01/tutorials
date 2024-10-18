/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Card } from './card';
import { Counter } from './counter';
import { TodoList } from './todo-list';

export class Playground extends Component {
    static template = "owl_playground.playground";
    static components = { Card, Counter, TodoList };
    todos = [
        { id: 3, description: "buy milk", done: false }, 
        { id: 4, description: "buy eggs", done: true }, 
        { id: 5, description: "buy avocado", done: true },
    ]
}
