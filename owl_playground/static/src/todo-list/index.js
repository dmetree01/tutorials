/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { todoPropShape, Todo } from "./todo";
import { useAutofocus } from '../utils';

export class TodoList extends Component {
    static template = "owl_playground.todo-list";
    static components = { Todo };
    static props = { todos: {type: Array, element: todoPropShape} };
    
    todos = useState(this.props.todos)

    setup() {
        useAutofocus("todoInput");
    }

    toggleState(e) {
        const todo = this.todos.find(it => it.id == e.target.value)
        todo.done = !todo.done;
    }

    addTodo(e) {
        if (e.keyCode === 13 && e.target.value?.length) {
            this.todos.push({
                id: (Math.max(...(this.todos.map(it => it.id)), 0)+1),
                description: e.target.value,
                done: false,
            });
        }
    }

    removeTodo(e) {
        const index = this.todos.findIndex((it) => it.id == e.target.getAttribute('data-id'));
        if (index >= 0) {
            this.todos.splice(index, 1);
        }
    }
}
